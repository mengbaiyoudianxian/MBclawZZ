package admin

import (
	"bytes"
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"

	"github.com/Wei-Shaw/sub2api/internal/pkg/response"
	"github.com/Wei-Shaw/sub2api/internal/server/middleware"
	"github.com/Wei-Shaw/sub2api/internal/service"
	"github.com/gin-gonic/gin"
)

const maxAgentIterations = 10

type AgentHandler struct {
	adminService service.AdminService
	store        *agentStore
	tools        []agentToolDef
}

func NewAgentHandler(adminService service.AdminService, db *sql.DB) *AgentHandler {
	return &AgentHandler{
		adminService: adminService,
		store:        newAgentStore(db),
		tools:        buildAgentTools(),
	}
}

type agentChatRequest struct {
	Message        string `json:"message" binding:"required"`
	ConversationID *int64 `json:"conversation_id"`
	Model          string `json:"model"`
	APIKey         string `json:"api_key"`
	BaseURL        string `json:"base_url"`
}

type agentChatResponse struct {
	ConversationID int64  `json:"conversation_id"`
	Reply          string `json:"reply"`
}

func (h *AgentHandler) Chat(c *gin.Context) {
	var req agentChatRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		response.BadRequest(c, "Invalid request: "+err.Error())
		return
	}

	authSub, _ := middleware.GetAuthSubjectFromContext(c); userID := authSub.UserID
	model := req.Model
	if model == "" {
		model = "gpt-4o"
	}
	baseURL := req.BaseURL
	if baseURL == "" {
		baseURL = "https://api.openai.com/v1"
	}
	apiKey := req.APIKey
	if apiKey == "" {
		response.BadRequest(c, "api_key is required")
		return
	}

	ctx := c.Request.Context()

	// Load or create conversation
	conv, err := h.loadOrCreateConv(ctx, userID, model, req)
	if err != nil {
		response.ErrorFrom(c, err)
		return
	}

	// Parse existing messages
	messages, err := parseMessages(conv.Messages)
	if err != nil {
		response.ErrorFrom(c, err)
		return
	}

	// Append user message
	messages = append(messages, agentMessage{Role: "user", Content: req.Message})

	// Run agent loop
	reply, err := h.runAgentLoop(ctx, model, apiKey, baseURL, messages)
	if err != nil {
		response.ErrorFrom(c, err)
		return
	}

	// Append assistant reply
	messages = append(messages, agentMessage{Role: "assistant", Content: reply})

	// Persist
	if err := h.store.updateMessages(ctx, conv.ID, messages); err != nil {
		response.ErrorFrom(c, err)
		return
	}

	// Auto-title on first message
	if conv.Title == "" {
		title := truncate(req.Message, 80)
		_ = h.store.updateTitle(ctx, conv.ID, title)
	}

	response.Success(c, agentChatResponse{
		ConversationID: conv.ID,
		Reply:          reply,
	})
}

func (h *AgentHandler) ListConversations(c *gin.Context) {
	authSub, _ := middleware.GetAuthSubjectFromContext(c); userID := authSub.UserID
	convs, err := h.store.listConversations(c.Request.Context(), userID)
	if err != nil {
		response.ErrorFrom(c, err)
		return
	}
	if convs == nil {
		convs = []agentConversation{}
	}
	response.Success(c, convs)
}

func (h *AgentHandler) GetConversation(c *gin.Context) {
	authSub, _ := middleware.GetAuthSubjectFromContext(c); userID := authSub.UserID
	id := parseInt64Param(c, "id")
	conv, err := h.store.getConversation(c.Request.Context(), id, userID)
	if err != nil {
		response.ErrorFrom(c, err)
		return
	}
	response.Success(c, conv)
}

func (h *AgentHandler) DeleteConversation(c *gin.Context) {
	authSub, _ := middleware.GetAuthSubjectFromContext(c); userID := authSub.UserID
	id := parseInt64Param(c, "id")
	if err := h.store.deleteConversation(c.Request.Context(), id, userID); err != nil {
		response.ErrorFrom(c, err)
		return
	}
	response.Success(c, nil)
}

func (h *AgentHandler) loadOrCreateConv(ctx context.Context, userID int64, model string, req agentChatRequest) (*agentConversation, error) {
	if req.ConversationID != nil && *req.ConversationID > 0 {
		return h.store.getConversation(ctx, *req.ConversationID, userID)
	}
	return h.store.createConversation(ctx, userID, model, truncate(req.Message, 80))
}

func (h *AgentHandler) runAgentLoop(ctx context.Context, model, apiKey, baseURL string, messages []agentMessage) (string, error) {
	client := &http.Client{Timeout: 120 * time.Second}

	for i := 0; i < maxAgentIterations; i++ {
		body := map[string]any{
			"model":    model,
			"messages": messages,
			"tools":    h.tools,
		}

		respText, err := h.callLLM(ctx, client, apiKey, baseURL, body)
		if err != nil {
			return "", err
		}

		var llmResp struct {
			Choices []struct {
				Message struct {
					Role      string           `json:"role"`
					Content   string           `json:"content"`
					ToolCalls []agentToolCall  `json:"tool_calls"`
				} `json:"message"`
				FinishReason string `json:"finish_reason"`
			} `json:"choices"`
		}

		if err := json.Unmarshal([]byte(respText), &llmResp); err != nil {
			return "", fmt.Errorf("parse LLM response: %w", err)
		}

		if len(llmResp.Choices) == 0 {
			return "", fmt.Errorf("LLM returned empty choices")
		}

		choice := llmResp.Choices[0]

		// If stop or plain text, return
		if choice.FinishReason == "stop" || (choice.Message.Content != "" && len(choice.Message.ToolCalls) == 0) {
			return choice.Message.Content, nil
		}

		// Execute tool calls
		if len(choice.Message.ToolCalls) > 0 {
			// Add assistant message with tool calls
			messages = append(messages, agentMessage{
				Role:      "assistant",
				Content:   choice.Message.Content,
				ToolCalls: choice.Message.ToolCalls,
			})

			for _, tc := range choice.Message.ToolCalls {
				var args map[string]any
				if err := json.Unmarshal([]byte(tc.Function.Arguments), &args); err != nil {
					args = map[string]any{}
				}

				result, execErr := executeAgentTool(ctx, h.adminService, tc.Function.Name, args)
				if execErr != nil {
					result = fmt.Sprintf(`{"error": "%s"}`, execErr.Error())
				}

				messages = append(messages, agentMessage{
					Role:       "tool",
					ToolCallID: tc.ID,
					Content:    result,
				})
			}
			continue
		}

		// Fallback: return content
		return choice.Message.Content, nil
	}

	return "已达到最大工具调用次数限制，请简化你的问题。", nil
}

func (h *AgentHandler) callLLM(ctx context.Context, client *http.Client, apiKey, baseURL string, body map[string]any) (string, error) {
	data, err := json.Marshal(body)
	if err != nil {
		return "", err
	}

	url := baseURL + "/chat/completions"
	req, err := http.NewRequestWithContext(ctx, "POST", url, bytes.NewReader(data))
	if err != nil {
		return "", err
	}
	req.Header.Set("Content-Type", "application/json")
	if apiKey != "" {
		req.Header.Set("Authorization", "Bearer "+apiKey)
	}

	resp, err := client.Do(req)
	if err != nil {
		return "", fmt.Errorf("LLM request failed: %w", err)
	}
	defer resp.Body.Close()

	respBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	if resp.StatusCode != 200 {
		return "", fmt.Errorf("LLM returned status %d: %s", resp.StatusCode, truncate(string(respBytes), 500))
	}

	return string(respBytes), nil
}

func parseMessages(raw json.RawMessage) ([]agentMessage, error) {
	if len(raw) == 0 {
		return nil, nil
	}
	var msgs []agentMessage
	if err := json.Unmarshal(raw, &msgs); err != nil {
		return nil, err
	}
	return msgs, nil
}

func parseInt64Param(c *gin.Context, name string) int64 {
	var v int64
	if s, ok := c.Params.Get(name); ok {
		fmt.Sscanf(s, "%d", &v)
	}
	return v
}

func truncate(s string, maxLen int) string {
	runes := []rune(s)
	if len(runes) <= maxLen {
		return s
	}
	return string(runes[:maxLen]) + "..."
}

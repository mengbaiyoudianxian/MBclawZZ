package admin

import (
	"context"
	"strings"
	"time"

	"github.com/Wei-Shaw/sub2api/internal/handler/dto"
	"github.com/Wei-Shaw/sub2api/internal/pkg/response"
	"github.com/Wei-Shaw/sub2api/internal/service"
	"github.com/gin-gonic/gin"
)

const (
	mbclawSourceKey        = "mbclaw_source"
	mbclawOwnerUserIDKey   = "mbclaw_owner_user_id"
	mbclawTokenPoolKindKey = "mbclaw_token_pool_kind"
)

type MBclawHandler struct {
	adminService service.AdminService
}

func NewMBclawHandler(adminService service.AdminService) *MBclawHandler {
	return &MBclawHandler{adminService: adminService}
}

type mbclawUpstreamTokenRequest struct {
	Name                    string         `json:"name" binding:"required"`
	Platform                string         `json:"platform" binding:"required"`
	APIKey                  string         `json:"api_key" binding:"required"`
	BaseURL                 string         `json:"base_url"`
	Model                   string         `json:"model"`
	Models                  []string       `json:"models"`
	Provider                string         `json:"provider"`
	GroupIDs                []int64        `json:"group_ids"`
	OwnerUserID             *int64         `json:"owner_user_id"`
	Source                  string         `json:"source"`
	TokenPoolKind           string         `json:"token_pool_kind"`
	Concurrency             int            `json:"concurrency"`
	RateMultiplier          *float64       `json:"rate_multiplier"`
	LoadFactor              *int           `json:"load_factor"`
	Priority                int            `json:"priority"`
	Extra                   map[string]any `json:"extra"`
	ConfirmMixedChannelRisk *bool          `json:"confirm_mixed_channel_risk"`
}

type mbclawTokenPoolModuleRequest struct {
	Name           string         `json:"name" binding:"required"`
	BaseURL        string         `json:"base_url" binding:"required"`
	Provider       string         `json:"provider"`
	APIKey         string         `json:"api_key"`
	Models         []string       `json:"models"`
	GroupIDs       []int64        `json:"group_ids"`
	OwnerUserID    *int64         `json:"owner_user_id"`
	Source         string         `json:"source"`
	Kind           string         `json:"kind"`
	Concurrency    int            `json:"concurrency"`
	LoadFactor     *int           `json:"load_factor"`
	Priority       int            `json:"priority"`
	Extra          map[string]any `json:"extra"`
	Schedulable    *bool          `json:"schedulable"`
	RateMultiplier *float64       `json:"rate_multiplier"`
}

type mbclawFoundationStatus struct {
	Entrypoints         []string                     `json:"entrypoints"`
	ControlEntrypoints  []string                     `json:"control_entrypoints"`
	ControlCapabilities []string                     `json:"control_capabilities"`
	TokenSources        []mbclawTokenSourceStatus    `json:"token_sources"`
	Limits              mbclawFoundationLimitsStatus `json:"limits"`
	Panels              mbclawFoundationPanelStatus  `json:"panels"`
	UpdatedAt           string                       `json:"updated_at"`
}

type mbclawTokenSourceStatus struct {
	Kind        string `json:"kind"`
	Status      string `json:"status"`
	Description string `json:"description"`
}

type mbclawFoundationLimitsStatus struct {
	UserConcurrency       string `json:"user_concurrency"`
	UserRateMultiplier    string `json:"user_rate_multiplier"`
	APIKeyRateLimit       string `json:"api_key_rate_limit"`
	ModelRateMultiplier   string `json:"model_rate_multiplier"`
	AccountConcurrency    string `json:"account_concurrency"`
	AccountRateMultiplier string `json:"account_rate_multiplier"`
}

type mbclawFoundationPanelStatus struct {
	MBclawTokenPanel  string `json:"mbclaw_token_panel"`
	Sub2APIAdminPanel string `json:"sub2api_admin_panel"`
}

func (h *MBclawHandler) Status(c *gin.Context) {
	response.Success(c, mbclawFoundationStatus{
		Entrypoints: []string{
			"POST /v1/chat/completions",
			"POST /v1/embeddings",
			"GET /v1/health",
		},
		ControlEntrypoints: []string{
			"GET /api/v1/admin/mbclaw/status",
			"POST /api/v1/admin/mbclaw/upstream-tokens",
			"POST /api/v1/admin/mbclaw/token-pool-modules",
		},
		ControlCapabilities: []string{
			"admin API key or admin JWT controls this namespace",
			"created upstream tokens become sub2api accounts",
			"created token-pool modules are stored as upstream accounts with mbclaw metadata",
			"status reports stable sub2api foundation capabilities back to Mother",
		},
		TokenSources: []mbclawTokenSourceStatus{
			{Kind: "mbclaw-user-upload", Status: "ready", Description: "MBclaw users can upload OpenAI-compatible upstream keys through the reserved admin endpoint."},
			{Kind: "miclaw-proxy", Status: "reserved", Description: "External free proxy/token pools can be registered as OpenAI-compatible upstream modules."},
			{Kind: "commercial-relay", Status: "ready", Description: "Commercial relay keys map to normal sub2api upstream API key accounts."},
		},
		Limits: mbclawFoundationLimitsStatus{
			UserConcurrency:       "existing admin users.concurrency",
			UserRateMultiplier:    "existing group user rate-multipliers",
			APIKeyRateLimit:       "existing API key quota and rate_limit windows",
			ModelRateMultiplier:   "existing channel model_pricing and model_mapping",
			AccountConcurrency:    "existing accounts.concurrency, default normalized to 1 when omitted",
			AccountRateMultiplier: "existing accounts.rate_multiplier, default 1",
		},
		Panels: mbclawFoundationPanelStatus{
			MBclawTokenPanel:  "reserved: manage MBclaw keys, key purchase, miclaw/free proxy registration through MBclaw-facing endpoints",
			Sub2APIAdminPanel: "existing: accounts, groups, channels, API keys, usage, ops",
		},
		UpdatedAt: time.Now().UTC().Format(time.RFC3339),
	})
}

func (h *MBclawHandler) CreateUpstreamToken(c *gin.Context) {
	var req mbclawUpstreamTokenRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		response.BadRequest(c, "Invalid request: "+err.Error())
		return
	}
	account, err := h.createAccount(c.Request.Context(), tokenModuleInput{
		Name:                  req.Name,
		Platform:              req.Platform,
		APIKey:                req.APIKey,
		BaseURL:               req.BaseURL,
		Model:                 req.Model,
		Models:                req.Models,
		Provider:              req.Provider,
		GroupIDs:              req.GroupIDs,
		OwnerUserID:           req.OwnerUserID,
		Source:                firstNonEmptyMBclaw(req.Source, "mbclaw-user-upload"),
		Kind:                  firstNonEmptyMBclaw(req.TokenPoolKind, "upstream-token"),
		Concurrency:           req.Concurrency,
		RateMultiplier:        req.RateMultiplier,
		LoadFactor:            req.LoadFactor,
		Priority:              req.Priority,
		Extra:                 req.Extra,
		SkipMixedChannelCheck: req.ConfirmMixedChannelRisk != nil && *req.ConfirmMixedChannelRisk,
	})
	if err != nil {
		response.ErrorFrom(c, err)
		return
	}
	response.Success(c, dto.AccountFromService(account))
}

func (h *MBclawHandler) RegisterTokenPoolModule(c *gin.Context) {
	var req mbclawTokenPoolModuleRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		response.BadRequest(c, "Invalid request: "+err.Error())
		return
	}
	account, err := h.createAccount(c.Request.Context(), tokenModuleInput{
		Name:           req.Name,
		Platform:       service.PlatformOpenAI,
		APIKey:         req.APIKey,
		BaseURL:        req.BaseURL,
		Models:         req.Models,
		Provider:       firstNonEmptyMBclaw(req.Provider, req.Kind),
		GroupIDs:       req.GroupIDs,
		OwnerUserID:    req.OwnerUserID,
		Source:         firstNonEmptyMBclaw(req.Source, "external-token-pool"),
		Kind:           firstNonEmptyMBclaw(req.Kind, "miclaw-proxy"),
		Concurrency:    req.Concurrency,
		RateMultiplier: req.RateMultiplier,
		LoadFactor:     req.LoadFactor,
		Priority:       req.Priority,
		Extra:          req.Extra,
		Schedulable:    req.Schedulable,
	})
	if err != nil {
		response.ErrorFrom(c, err)
		return
	}
	response.Success(c, dto.AccountFromService(account))
}

type tokenModuleInput struct {
	Name                  string
	Platform              string
	APIKey                string
	BaseURL               string
	Model                 string
	Models                []string
	Provider              string
	GroupIDs              []int64
	OwnerUserID           *int64
	Source                string
	Kind                  string
	Concurrency           int
	RateMultiplier        *float64
	LoadFactor            *int
	Priority              int
	Extra                 map[string]any
	Schedulable           *bool
	SkipMixedChannelCheck bool
}

func (h *MBclawHandler) createAccount(ctx context.Context, input tokenModuleInput) (*service.Account, error) {
	credentials := map[string]any{}
	if strings.TrimSpace(input.APIKey) != "" {
		credentials["api_key"] = strings.TrimSpace(input.APIKey)
	}
	if strings.TrimSpace(input.BaseURL) != "" {
		credentials["base_url"] = strings.TrimRight(strings.TrimSpace(input.BaseURL), "/")
	}
	if strings.TrimSpace(input.Model) != "" {
		credentials["model"] = strings.TrimSpace(input.Model)
	}
	models := normalizedStrings(input.Models)
	if len(models) > 0 {
		credentials["models"] = models
	}
	if strings.TrimSpace(input.Provider) != "" {
		credentials["provider"] = strings.TrimSpace(input.Provider)
	}

	extra := cloneMap(input.Extra)
	extra[mbclawSourceKey] = strings.TrimSpace(input.Source)
	extra[mbclawTokenPoolKindKey] = strings.TrimSpace(input.Kind)
	if input.OwnerUserID != nil && *input.OwnerUserID > 0 {
		extra[mbclawOwnerUserIDKey] = *input.OwnerUserID
	}
	if input.Schedulable != nil {
		extra["mbclaw_requested_schedulable"] = *input.Schedulable
	}

	account, err := h.adminService.CreateAccount(ctx, &service.CreateAccountInput{
		Name:                  input.Name,
		Platform:              input.Platform,
		Type:                  service.AccountTypeAPIKey,
		Credentials:           credentials,
		Extra:                 extra,
		Concurrency:           input.Concurrency,
		Priority:              input.Priority,
		RateMultiplier:        input.RateMultiplier,
		LoadFactor:            input.LoadFactor,
		GroupIDs:              input.GroupIDs,
		SkipMixedChannelCheck: input.SkipMixedChannelCheck,
	})
	if err != nil {
		return nil, err
	}
	if input.Schedulable != nil {
		account, err = h.adminService.SetAccountSchedulable(ctx, account.ID, *input.Schedulable)
		if err != nil {
			return nil, err
		}
	}
	return account, nil
}

func cloneMap(in map[string]any) map[string]any {
	out := make(map[string]any, len(in)+3)
	for k, v := range in {
		out[k] = v
	}
	return out
}

func normalizedStrings(values []string) []string {
	out := make([]string, 0, len(values))
	seen := make(map[string]struct{}, len(values))
	for _, value := range values {
		trimmed := strings.TrimSpace(value)
		if trimmed == "" {
			continue
		}
		if _, ok := seen[trimmed]; ok {
			continue
		}
		seen[trimmed] = struct{}{}
		out = append(out, trimmed)
	}
	return out
}

func firstNonEmptyMBclaw(values ...string) string {
	for _, value := range values {
		if trimmed := strings.TrimSpace(value); trimmed != "" {
			return trimmed
		}
	}
	return ""
}

package admin

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/Wei-Shaw/sub2api/internal/service"
)

type agentToolDef struct {
	Type     string `json:"type"`
	Function struct {
		Name        string         `json:"name"`
		Description string         `json:"description"`
		Parameters  map[string]any `json:"parameters"`
	} `json:"function"`
}

type agentToolResult struct {
	ToolCallID string `json:"tool_call_id"`
	Content    string `json:"content"`
}

func buildAgentTools() []agentToolDef {
	tools := []agentToolDef{
		{
			Type: "function",
			Function: struct {
				Name        string         `json:"name"`
				Description string         `json:"description"`
				Parameters  map[string]any `json:"parameters"`
			}{
				Name:        "list_users",
				Description: "列出所有用户，支持分页和搜索",
				Parameters: map[string]any{
					"type": "object",
					"properties": map[string]any{
						"page":      map[string]any{"type": "integer", "description": "页码，默认1"},
						"page_size": map[string]any{"type": "integer", "description": "每页数量，默认20"},
						"search":    map[string]any{"type": "string", "description": "搜索关键词（邮箱/用户名）"},
						"status":    map[string]any{"type": "string", "description": "状态过滤：active/disabled"},
					},
				},
			},
		},
		{
			Type: "function",
			Function: struct {
				Name        string         `json:"name"`
				Description string         `json:"description"`
				Parameters  map[string]any `json:"parameters"`
			}{
				Name:        "get_user",
				Description: "获取指定用户的详细信息",
				Parameters: map[string]any{
					"type": "object",
					"properties": map[string]any{
						"user_id": map[string]any{"type": "integer", "description": "用户ID"},
					},
					"required": []string{"user_id"},
				},
			},
		},
		{
			Type: "function",
			Function: struct {
				Name        string         `json:"name"`
				Description string         `json:"description"`
				Parameters  map[string]any `json:"parameters"`
			}{
				Name:        "update_user_balance",
				Description: "修改用户余额（充值/扣款）",
				Parameters: map[string]any{
					"type": "object",
					"properties": map[string]any{
						"user_id":   map[string]any{"type": "integer", "description": "用户ID"},
						"amount":    map[string]any{"type": "number", "description": "金额（正数为充值，负数为扣款）"},
						"operation": map[string]any{"type": "string", "description": "操作类型：recharge/deduct/manual"},
						"notes":     map[string]any{"type": "string", "description": "备注"},
					},
					"required": []string{"user_id", "amount"},
				},
			},
		},
		{
			Type: "function",
			Function: struct {
				Name        string         `json:"name"`
				Description string         `json:"description"`
				Parameters  map[string]any `json:"parameters"`
			}{
				Name:        "list_accounts",
				Description: "列出所有上游账号（API key accounts），支持按平台/类型/状态过滤",
				Parameters: map[string]any{
					"type": "object",
					"properties": map[string]any{
						"page":      map[string]any{"type": "integer", "description": "页码，默认1"},
						"page_size": map[string]any{"type": "integer", "description": "每页数量，默认20"},
						"platform":  map[string]any{"type": "string", "description": "平台：openai/anthropic/google/grok"},
						"status":    map[string]any{"type": "string", "description": "状态：active/disabled/error"},
						"search":    map[string]any{"type": "string", "description": "搜索账号名称"},
					},
				},
			},
		},
		{
			Type: "function",
			Function: struct {
				Name        string         `json:"name"`
				Description string         `json:"description"`
				Parameters  map[string]any `json:"parameters"`
			}{
				Name:        "get_account",
				Description: "获取指定上游账号的详细信息",
				Parameters: map[string]any{
					"type": "object",
					"properties": map[string]any{
						"account_id": map[string]any{"type": "integer", "description": "账号ID"},
					},
					"required": []string{"account_id"},
				},
			},
		},
		{
			Type: "function",
			Function: struct {
				Name        string         `json:"name"`
				Description string         `json:"description"`
				Parameters  map[string]any `json:"parameters"`
			}{
				Name:        "list_groups",
				Description: "列出所有分组",
				Parameters: map[string]any{
					"type": "object",
					"properties": map[string]any{
						"platform": map[string]any{"type": "string", "description": "平台过滤"},
						"search":   map[string]any{"type": "string", "description": "搜索分组名称"},
					},
				},
			},
		},
		{
			Type: "function",
			Function: struct {
				Name        string         `json:"name"`
				Description string         `json:"description"`
				Parameters  map[string]any `json:"parameters"`
			}{
				Name:        "get_dashboard_stats",
				Description: "获取仪表盘统计数据（用户数、账号数、分组数）",
				Parameters: map[string]any{
					"type":       "object",
					"properties": map[string]any{},
				},
			},
		},
		{
			Type: "function",
			Function: struct {
				Name        string         `json:"name"`
				Description string         `json:"description"`
				Parameters  map[string]any `json:"parameters"`
			}{
				Name:        "get_mbclaw_status",
				Description: "获取 MBclaw 地基状态（入口点、token来源、限额配置）",
				Parameters: map[string]any{
					"type":       "object",
					"properties": map[string]any{},
				},
			},
		},
		{
			Type: "function",
			Function: struct {
				Name        string         `json:"name"`
				Description string         `json:"description"`
				Parameters  map[string]any `json:"parameters"`
			}{
				Name:        "read_file",
				Description: "读取 sub2api 源码文件内容。路径相对于 sub2api 项目根目录，如 backend/internal/handler/admin/mbclaw_handler.go",
				Parameters: map[string]any{
					"type": "object",
					"properties": map[string]any{
						"path": map[string]any{"type": "string", "description": "文件路径，相对于 sub2api 根目录"},
					},
					"required": []string{"path"},
				},
			},
		},
		{
			Type: "function",
			Function: struct {
				Name        string         `json:"name"`
				Description string         `json:"description"`
				Parameters  map[string]any `json:"parameters"`
			}{
				Name:        "edit_file",
				Description: "编辑 sub2api 源码文件。用 new_str 替换文件中的 old_str（需精确匹配）。路径相对于 sub2api 项目根目录。",
				Parameters: map[string]any{
					"type": "object",
					"properties": map[string]any{
						"path":    map[string]any{"type": "string", "description": "文件路径，相对于 sub2api 根目录"},
						"old_str": map[string]any{"type": "string", "description": "要替换的原文本，必须精确匹配"},
						"new_str": map[string]any{"type": "string", "description": "替换后的新文本"},
					},
					"required": []string{"path", "old_str", "new_str"},
				},
			},
		},
		{
			Type: "function",
			Function: struct {
				Name        string         `json:"name"`
				Description string         `json:"description"`
				Parameters  map[string]any `json:"parameters"`
			}{
				Name:        "run_command",
				Description: "在 sub2api 项目目录中执行终端命令（编译、测试、重启等）。超时 60 秒。",
				Parameters: map[string]any{
					"type": "object",
					"properties": map[string]any{
						"command": map[string]any{"type": "string", "description": "要执行的 shell 命令"},
					},
					"required": []string{"command"},
				},
			},
		},
	}
	return tools
}

var agentWorkspaceRoot = "/opt/mbclawzz-test/repo/参考文件/GitHub精品参考/sub2api"

func executeAgentTool(ctx context.Context, adminService service.AdminService, name string, args map[string]any) (string, error) {
	switch name {
	case "list_users":
		page := getIntArg(args, "page", 1)
		pageSize := getIntArg(args, "page_size", 20)
		search := getStringArg(args, "search", "")
		status := getStringArg(args, "status", "")
		users, total, err := adminService.ListUsers(ctx, page, pageSize, service.UserListFilters{
			Search: search,
			Status: status,
		}, "", "")
		if err != nil {
			return "", err
		}
		return formatJSON(map[string]any{
			"users":     users,
			"total":     total,
			"page":      page,
			"page_size": pageSize,
		})

	case "get_user":
		uid := int64(getIntArg(args, "user_id", 0))
		if uid == 0 {
			return "", fmt.Errorf("user_id is required")
		}
		user, err := adminService.GetUser(ctx, uid)
		if err != nil {
			return "", err
		}
		return formatJSON(user)

	case "update_user_balance":
		uid := int64(getIntArg(args, "user_id", 0))
		amount := getFloatArg(args, "amount", 0)
		operation := getStringArg(args, "operation", "manual")
		notes := getStringArg(args, "notes", "")
		if uid == 0 {
			return "", fmt.Errorf("user_id is required")
		}
		user, err := adminService.UpdateUserBalance(ctx, uid, amount, operation, notes)
		if err != nil {
			return "", err
		}
		return formatJSON(user)

	case "list_accounts":
		page := getIntArg(args, "page", 1)
		pageSize := getIntArg(args, "page_size", 20)
		platform := getStringArg(args, "platform", "")
		status := getStringArg(args, "status", "")
		search := getStringArg(args, "search", "")
		accounts, total, err := adminService.ListAccounts(ctx, page, pageSize, platform, "", status, search, 0, "", "", "")
		if err != nil {
			return "", err
		}
		return formatJSON(map[string]any{
			"accounts":  accounts,
			"total":     total,
			"page":      page,
			"page_size": pageSize,
		})

	case "get_account":
		aid := int64(getIntArg(args, "account_id", 0))
		if aid == 0 {
			return "", fmt.Errorf("account_id is required")
		}
		account, err := adminService.GetAccount(ctx, aid)
		if err != nil {
			return "", err
		}
		return formatJSON(account)

	case "list_groups":
		platform := getStringArg(args, "platform", "")
		search := getStringArg(args, "search", "")
		groups, total, err := adminService.ListGroups(ctx, 1, 100, platform, "", search, nil, "", "")
		if err != nil {
			return "", err
		}
		return formatJSON(map[string]any{"groups": groups, "total": total})

	case "get_dashboard_stats":
		_, totalUsers, _ := adminService.ListUsers(ctx, 1, 1, service.UserListFilters{}, "", "")
		_, totalAccounts, _ := adminService.ListAccounts(ctx, 1, 1, "", "", "", "", 0, "", "", "")
		_, totalGroups, _ := adminService.ListGroups(ctx, 1, 100, "", "", "", nil, "", "")
		return formatJSON(map[string]any{
			"total_users":    totalUsers,
			"total_accounts": totalAccounts,
			"total_groups":   totalGroups,
		})

	case "get_mbclaw_status":
		return formatJSON(buildMBclawStatus())

	case "read_file":
		path := getStringArg(args, "path", "")
		if path == "" {
			return "", fmt.Errorf("path is required")
		}
		return readFileInWorkspace(path)

	case "edit_file":
		path := getStringArg(args, "path", "")
		oldStr := getStringArg(args, "old_str", "")
		newStr := getStringArg(args, "new_str", "")
		if path == "" {
			return "", fmt.Errorf("path is required")
		}
		return editFileInWorkspace(path, oldStr, newStr)

	case "run_command":
		cmd := getStringArg(args, "command", "")
		if cmd == "" {
			return "", fmt.Errorf("command is required")
		}
		return runCommandInWorkspace(ctx, cmd)

	default:
		return fmt.Sprintf(`{"error": "unknown tool: %s"}`, name), nil
	}
}

func formatJSON(v any) (string, error) {
	data, err := json.Marshal(v)
	if err != nil {
		return "", err
	}
	return string(data), nil
}

func getStringArg(args map[string]any, key, defaultVal string) string {
	if v, ok := args[key]; ok {
		if s, ok := v.(string); ok {
			return strings.TrimSpace(s)
		}
	}
	return defaultVal
}

func getIntArg(args map[string]any, key string, defaultVal int) int {
	if v, ok := args[key]; ok {
		switch n := v.(type) {
		case float64:
			return int(n)
		case int:
			return n
		case int64:
			return int(n)
		}
	}
	return defaultVal
}

func buildMBclawStatus() map[string]any {
	return map[string]any{
		"entrypoints": []string{
			"POST /v1/chat/completions",
			"POST /v1/embeddings",
			"GET /v1/health",
		},
		"control_entrypoints": []string{
			"GET /api/v1/admin/mbclaw/status",
			"POST /api/v1/admin/mbclaw/upstream-tokens",
			"POST /api/v1/admin/mbclaw/token-pool-modules",
			"POST /api/v1/admin/agent/chat",
		},
		"token_sources": []map[string]string{
			{"kind": "mbclaw-user-upload", "status": "ready"},
			{"kind": "miclaw-proxy", "status": "reserved"},
			{"kind": "commercial-relay", "status": "ready"},
		},
		"limits": map[string]string{
			"user_concurrency":       "users.concurrency",
			"user_rate_multiplier":   "group rate-multipliers",
			"api_key_rate_limit":     "API key quota + rate_limit windows",
			"model_rate_multiplier":  "channel model_pricing + model_mapping",
			"account_concurrency":    "accounts.concurrency",
			"account_rate_multiplier": "accounts.rate_multiplier",
		},
	}
}

func getFloatArg(args map[string]any, key string, defaultVal float64) float64 {
	if v, ok := args[key]; ok {
		switch n := v.(type) {
		case float64:
			return n
		case int:
			return float64(n)
		case int64:
			return float64(n)
		}
	}
	return defaultVal
}

func safePath(root, rel string) (string, error) {
	abs := filepath.Join(root, filepath.Clean("/"+rel))
	abs = filepath.Clean(abs)
	if !strings.HasPrefix(abs, filepath.Clean(root)+string(os.PathSeparator)) && abs != filepath.Clean(root) {
		return "", fmt.Errorf("path escapes workspace: %s", rel)
	}
	return abs, nil
}

func readFileInWorkspace(relPath string) (string, error) {
	abs, err := safePath(agentWorkspaceRoot, relPath)
	if err != nil {
		return "", err
	}
	data, err := os.ReadFile(abs)
	if err != nil {
		return "", fmt.Errorf("read %s: %w", relPath, err)
	}
	if len(data) > 100000 {
		return string(data[:100000]) + "\n\n... [truncated]", nil
	}
	return string(data), nil
}

func editFileInWorkspace(relPath, oldStr, newStr string) (string, error) {
	abs, err := safePath(agentWorkspaceRoot, relPath)
	if err != nil {
		return "", err
	}
	data, err := os.ReadFile(abs)
	if err != nil {
		return "", fmt.Errorf("read %s: %w", relPath, err)
	}
	content := string(data)
	count := strings.Count(content, oldStr)
	if count == 0 {
		return "", fmt.Errorf("old_str not found in %s", relPath)
	}
	if count > 1 {
		return "", fmt.Errorf("old_str matches %d locations in %s — please include more context to make it unique", count, relPath)
	}
	newContent := strings.Replace(content, oldStr, newStr, 1)
	if err := os.WriteFile(abs, []byte(newContent), 0644); err != nil {
		return "", fmt.Errorf("write %s: %w", relPath, err)
	}
	return fmt.Sprintf("edited %s: replaced 1 occurrence", relPath), nil
}

func runCommandInWorkspace(ctx context.Context, command string) (string, error) {
	timeoutCtx, cancel := context.WithTimeout(ctx, 60*time.Second)
	defer cancel()

	cmd := exec.CommandContext(timeoutCtx, "bash", "-c", command)
	cmd.Dir = agentWorkspaceRoot
	cmd.Env = append(os.Environ(),
		"PATH=/opt/tools/go1.26.5/bin:/usr/local/bin:/usr/bin:/bin",
		"GOPROXY=https://goproxy.cn,direct",
		"HOME=/root",
	)

	output, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Sprintf("exit=%v\n%s", err, truncateStr(string(output), 8000)), nil
	}
	return truncateStr(string(output), 8000), nil
}

func truncateStr(s string, maxLen int) string {
	if len(s) <= maxLen {
		return s
	}
	return s[:maxLen] + "\n\n... [truncated]"
}

package admin

import (
	"context"
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
	return []agentToolDef{
		{
			Type: "function",
			Function: struct {
				Name        string         `json:"name"`
				Description string         `json:"description"`
				Parameters  map[string]any `json:"parameters"`
			}{
				Name:        "read_file",
				Description: "读取 sub2api 项目中的文件。路径相对于项目根目录，如 backend/internal/handler/admin/mbclaw_handler.go",
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
				Description: "用 new_str 精确替换文件中的 old_str。old_str 必须唯一匹配。",
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
				Description: "在 sub2api 项目目录中执行终端命令。Go 编译用 /opt/tools/go1.26.5/bin/go。超时 60 秒。",
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
}

var agentWorkspaceRoot = "/opt/mbclawzz-test/repo/参考文件/GitHub精品参考/sub2api"

func executeAgentTool(ctx context.Context, _ service.AdminService, name string, args map[string]any) (string, error) {
	switch name {
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

func getStringArg(args map[string]any, key, defaultVal string) string {
	if v, ok := args[key]; ok {
		if s, ok := v.(string); ok {
			return strings.TrimSpace(s)
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

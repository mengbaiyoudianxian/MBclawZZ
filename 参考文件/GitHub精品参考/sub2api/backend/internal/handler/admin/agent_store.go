package admin

import (
	"context"
	"database/sql"
	"encoding/json"
	"time"
)

type agentMessage struct {
	Role    string `json:"role"`
	Content string `json:"content,omitempty"`
	Name    string `json:"name,omitempty"`
	ToolCallID string `json:"tool_call_id,omitempty"`
	ToolCalls  []agentToolCall `json:"tool_calls,omitempty"`
}

type agentToolCall struct {
	ID       string `json:"id"`
	Type     string `json:"type"`
	Function struct {
		Name      string `json:"name"`
		Arguments string `json:"arguments"`
	} `json:"function"`
}

type agentConversation struct {
	ID        int64           `json:"id"`
	UserID    int64           `json:"user_id"`
	Title     string          `json:"title"`
	Model     string          `json:"model"`
	Messages  json.RawMessage `json:"messages"`
	CreatedAt time.Time       `json:"created_at"`
	UpdatedAt time.Time       `json:"updated_at"`
}

type agentStore struct {
	db *sql.DB
}

func newAgentStore(db *sql.DB) *agentStore {
	return &agentStore{db: db}
}

func (s *agentStore) createConversation(ctx context.Context, userID int64, model, title string) (*agentConversation, error) {
	conv := &agentConversation{}
	err := s.db.QueryRowContext(ctx,
		`INSERT INTO agent_conversations (user_id, title, model, messages) VALUES ($1, $2, $3, '[]'::jsonb) RETURNING id, user_id, title, model, messages, created_at, updated_at`,
		userID, title, model,
	).Scan(&conv.ID, &conv.UserID, &conv.Title, &conv.Model, &conv.Messages, &conv.CreatedAt, &conv.UpdatedAt)
	return conv, err
}

func (s *agentStore) getConversation(ctx context.Context, id, userID int64) (*agentConversation, error) {
	conv := &agentConversation{}
	err := s.db.QueryRowContext(ctx,
		`SELECT id, user_id, title, model, messages, created_at, updated_at FROM agent_conversations WHERE id=$1 AND user_id=$2`,
		id, userID,
	).Scan(&conv.ID, &conv.UserID, &conv.Title, &conv.Model, &conv.Messages, &conv.CreatedAt, &conv.UpdatedAt)
	if err != nil {
		return nil, err
	}
	return conv, nil
}

func (s *agentStore) updateMessages(ctx context.Context, id int64, messages []agentMessage) error {
	data, err := json.Marshal(messages)
	if err != nil {
		return err
	}
	_, err = s.db.ExecContext(ctx,
		`UPDATE agent_conversations SET messages=$1, updated_at=NOW() WHERE id=$2`,
		data, id,
	)
	return err
}

func (s *agentStore) updateTitle(ctx context.Context, id int64, title string) error {
	_, err := s.db.ExecContext(ctx,
		`UPDATE agent_conversations SET title=$1, updated_at=NOW() WHERE id=$2`,
		title, id,
	)
	return err
}

func (s *agentStore) listConversations(ctx context.Context, userID int64) ([]agentConversation, error) {
	rows, err := s.db.QueryContext(ctx,
		`SELECT id, user_id, title, model, messages, created_at, updated_at FROM agent_conversations WHERE user_id=$1 ORDER BY updated_at DESC LIMIT 50`,
		userID,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var convs []agentConversation
	for rows.Next() {
		var c agentConversation
		if err := rows.Scan(&c.ID, &c.UserID, &c.Title, &c.Model, &c.Messages, &c.CreatedAt, &c.UpdatedAt); err != nil {
			return nil, err
		}
		convs = append(convs, c)
	}
	return convs, rows.Err()
}

func (s *agentStore) deleteConversation(ctx context.Context, id, userID int64) error {
	_, err := s.db.ExecContext(ctx, `DELETE FROM agent_conversations WHERE id=$1 AND user_id=$2`, id, userID)
	return err
}

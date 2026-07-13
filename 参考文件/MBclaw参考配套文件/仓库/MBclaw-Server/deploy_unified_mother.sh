#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/mbclaw}"
DATA_DIR="${MBCLAW_DATA:-/var/lib/mbclaw}"
SERVICE_NAME="${SERVICE_NAME:-mbclaw}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

mkdir -p "$APP_DIR" "$DATA_DIR" "$DATA_DIR/uploads"
cd "$APP_DIR"
ln -sfn server_app app

if [ -f requirements.txt ]; then
  $PYTHON_BIN -m pip install -r requirements.txt
fi

cat > "$APP_DIR/.env" <<EOF
MBCLAW_DB_PATH=$DATA_DIR/mbclaw.db
MBCLAW_DATA=$DATA_DIR
MBCLAW_UPLOADS=$DATA_DIR/uploads
MBCLAW_UPLOAD_TOKEN=${MBCLAW_UPLOAD_TOKEN:-mengbai}
MBCLAW_LLM_BASE_URL=${MBCLAW_LLM_BASE_URL:-https://api.openai.com/v1}
MBCLAW_LLM_MODEL=${MBCLAW_LLM_MODEL:-gpt-4o-mini}
MBCLAW_LLM_API_KEY=${MBCLAW_LLM_API_KEY:-}
MBCLAW_EMBED_MODEL=${MBCLAW_EMBED_MODEL:-text-embedding-3-small}
MBCLAW_LLM_MOCK=${MBCLAW_LLM_MOCK:-0}
MOTHER_RUNTIME_DB=$DATA_DIR/mother_runtime.db
MOTHER_MAX_ITERATIONS=${MOTHER_MAX_ITERATIONS:-50}
MOTHER_MAX_REPLANS=${MOTHER_MAX_REPLANS:-2}
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-}
OPENAI_API_KEY=${OPENAI_API_KEY:-}
DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY:-}
ALIYUN_DASH_SCOPE_KEY=${ALIYUN_DASH_SCOPE_KEY:-}
ZHIPU_KEY=${ZHIPU_KEY:-}
EOF
chmod 600 "$APP_DIR/.env"

cat > "/etc/systemd/system/$SERVICE_NAME.service" <<EOF
[Unit]
Description=MBclaw Unified Mother Server
After=network.target

[Service]
Type=simple
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
Environment=PYTHONPATH=$APP_DIR:$APP_DIR/server_app
ExecStart=$PYTHON_BIN -m uvicorn main:app --host 0.0.0.0 --port ${MBCLAW_PORT:-8001}
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl restart "$SERVICE_NAME"
systemctl --no-pager --full status "$SERVICE_NAME" || true

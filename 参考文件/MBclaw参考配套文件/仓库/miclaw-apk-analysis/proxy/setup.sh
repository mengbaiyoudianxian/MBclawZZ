#!/bin/bash
# MiClaw劫持设置脚本
# 在手机上运行，需要root权限

set -e

echo "=== MiClaw劫持设置 ==="

# 检查root
if [ "$(id -u)" != "0" ]; then
    echo "错误: 需要root权限"
    echo "请用su运行此脚本"
    exit 1
fi

# 配置
PROXY_DIR="/data/adb/miclaw-proxy"
HOSTS_FILE="/system/etc/hosts"
PROXY_SCRIPT="miclaw_proxy.py"
CERT_DIR="$PROXY_DIR/certs"

echo "1. 创建代理目录..."
mkdir -p "$PROXY_DIR"
mkdir -p "$CERT_DIR"

echo "2. 生成SSL证书..."
if [ ! -f "$CERT_DIR/ca.crt" ]; then
    # 生成CA证书
    openssl req -x509 -newkey rsa:4096 -keyout "$CERT_DIR/ca.key" -out "$CERT_DIR/ca.crt" \
        -days 3650 -nodes -subj "/CN=MiClaw Proxy CA" 2>/dev/null
    
    # 生成服务器证书
    openssl req -newkey rsa:4096 -keyout "$CERT_DIR/server.key" -out "$CERT_DIR/server.csr" \
        -nodes -subj "/CN=api.mify.mioffice.cn" 2>/dev/null
    
    openssl x509 -req -in "$CERT_DIR/server.csr" -CA "$CERT_DIR/ca.crt" -CAkey "$CERT_DIR/ca.key" \
        -CAcreateserial -out "$CERT_DIR/server.crt" -days 3650 2>/dev/null
    
    echo "   证书生成完成"
else
    echo "   证书已存在，跳过"
fi

echo "3. 修改hosts文件..."
if ! grep -q "api.mify.mioffice.cn" "$HOSTS_FILE"; then
    mount -o remount,rw /system
    echo "127.0.0.1 api.mify.mioffice.cn" >> "$HOSTS_FILE"
    mount -o remount,ro /system
    echo "   hosts修改完成"
else
    echo "   hosts已修改，跳过"
fi

echo "4. 安装Python依赖..."
pip3 install flask requests 2>/dev/null || echo "   pip安装失败，请手动安装"

echo "5. 复制代理脚本..."
cp "$(dirname "$0")/$PROXY_SCRIPT" "$PROXY_DIR/"
chmod +x "$PROXY_DIR/$PROXY_SCRIPT"

echo "6. 创建启动脚本..."
cat > "$PROXY_DIR/start.sh" << 'EOF'
#!/bin/bash
# 启动MiClaw代理

PROXY_DIR="/data/adb/miclaw-proxy"
cd "$PROXY_DIR"

# 检查是否已运行
if pgrep -f "miclaw_proxy.py" > /dev/null; then
    echo "代理已在运行"
    exit 0
fi

# 启动代理
echo "启动MiClaw代理..."
nohup python3 miclaw_proxy.py \
    --port 8443 \
    --openclaw http://127.0.0.1:18789 \
    --ssl \
    --cert certs/server.crt \
    --key certs/server.key \
    > proxy.log 2>&1 &

echo "代理已启动，PID: $!"
echo "日志: $PROXY_DIR/proxy.log"
EOF

chmod +x "$PROXY_DIR/start.sh"

echo "7. 创建停止脚本..."
cat > "$PROXY_DIR/stop.sh" << 'EOF'
#!/bin/bash
# 停止MiClaw代理

echo "停止MiClaw代理..."
pkill -f "miclaw_proxy.py" || echo "代理未运行"
echo "完成"
EOF

chmod +x "$PROXY_DIR/stop.sh"

echo "8. 创建测试脚本..."
cat > "$PROXY_DIR/test.sh" << 'EOF'
#!/bin/bash
# 测试MiClaw代理

echo "=== 测试MiClaw代理 ==="

# 测试健康检查
echo "1. 健康检查..."
curl -s http://127.0.0.1:8443/health | python3 -m json.tool

# 测试模型列表
echo ""
echo "2. 模型列表..."
curl -s http://127.0.0.1:8443/v1/models | python3 -m json.tool

# 测试聊天完成
echo ""
echo "3. 聊天测试..."
curl -s -X POST http://127.0.0.1:8443/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "miclaw-hijacked",
        "messages": [
            {"role": "user", "content": "你好，你是谁？"}
        ]
    }' | python3 -m json.tool

echo ""
echo "=== 测试完成 ==="
EOF

chmod +x "$PROXY_DIR/test.sh"

echo ""
echo "=== 设置完成 ==="
echo ""
echo "使用方法:"
echo "  启动代理: $PROXY_DIR/start.sh"
echo "  停止代理: $PROXY_DIR/stop.sh"
echo "  测试代理: $PROXY_DIR/test.sh"
echo ""
echo "代理地址: http://127.0.0.1:8443"
echo "日志文件: $PROXY_DIR/proxy.log"
echo ""
echo "注意: 需要先启动OpenClaw Gateway (端口18789)"
echo "      然后重启MiClaw使hosts修改生效"

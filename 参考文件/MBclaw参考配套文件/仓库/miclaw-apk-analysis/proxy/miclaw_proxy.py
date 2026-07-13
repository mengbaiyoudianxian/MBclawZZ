#!/usr/bin/env python3
"""
MiClaw LLM代理 - 把OpenAI格式请求转发到OpenClaw
运行在手机上，拦截MiClaw的LLM调用

用法:
  python3 miclaw_proxy.py --port 8443 --openclaw http://127.0.0.1:18789

需要:
  - flask
  - requests
  - ssl (内置)
"""

import json
import ssl
import argparse
import logging
from datetime import datetime

try:
    from flask import Flask, request, jsonify, Response
    import requests
except ImportError:
    print("需要安装依赖: pip3 install flask requests")
    exit(1)

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# 配置
OPENCLAW_URL = None
HERMES_URL = None
USE_OPENCLAW = True

# 请求计数
request_count = 0


def forward_to_openclaw(data):
    """转发到OpenClaw Gateway"""
    global OPENCLAW_URL
    try:
        # OpenClaw使用OpenAI兼容格式
        response = requests.post(
            f"{OPENCLAW_URL}/v1/chat/completions",
            json=data,
            timeout=120,
            headers={"Content-Type": "application/json"}
        )
        return response.json(), response.status_code
    except Exception as e:
        logger.error(f"转发到OpenClaw失败: {e}")
        return {"error": str(e)}, 500


def forward_to_hermes(data):
    """转发到Hermes Agent"""
    global HERMES_URL
    try:
        response = requests.post(
            f"{HERMES_URL}/v1/chat/completions",
            json=data,
            timeout=120,
            headers={"Content-Type": "application/json"}
        )
        return response.json(), response.status_code
    except Exception as e:
        logger.error(f"转发到Hermes失败: {e}")
        return {"error": str(e)}, 500


@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    """处理MiClaw的LLM请求"""
    global request_count
    request_count += 1
    
    try:
        data = request.json
        logger.info(f"收到请求 #{request_count}: {json.dumps(data, ensure_ascii=False)[:200]}...")
        
        # 提取关键信息
        messages = data.get("messages", [])
        model = data.get("model", "unknown")
        stream = data.get("stream", False)
        
        logger.info(f"模型: {model}, 消息数: {len(messages)}, 流式: {stream}")
        
        # 转发到目标
        if USE_OPENCLAW:
            result, status = forward_to_openclaw(data)
        else:
            result, status = forward_to_hermes(data)
        
        logger.info(f"响应状态: {status}")
        return jsonify(result), status
        
    except Exception as e:
        logger.error(f"处理请求失败: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/v1/models", methods=["GET"])
def list_models():
    """返回可用模型列表"""
    return jsonify({
        "object": "list",
        "data": [
            {
                "id": "miclaw-hijacked",
                "object": "model",
                "created": 1234567890,
                "owned_by": "hijacked"
            }
        ]
    })


@app.route("/health", methods=["GET"])
def health():
    """健康检查"""
    return jsonify({
        "status": "ok",
        "requests": request_count,
        "target": "openclaw" if USE_OPENCLAW else "hermes",
        "timestamp": datetime.now().isoformat()
    })


@app.route("/", methods=["GET"])
def index():
    """首页"""
    return jsonify({
        "name": "MiClaw LLM Proxy",
        "version": "1.0.0",
        "description": "拦截MiClaw的LLM调用，转发到OpenClaw/Hermes",
        "endpoints": [
            "/v1/chat/completions",
            "/v1/models",
            "/health"
        ]
    })


def main():
    global OPENCLAW_URL, HERMES_URL, USE_OPENCLAW
    
    parser = argparse.ArgumentParser(description="MiClaw LLM代理")
    parser.add_argument("--port", type=int, default=8443, help="监听端口 (默认: 8443)")
    parser.add_argument("--host", default="0.0.0.0", help="监听地址 (默认: 0.0.0.0)")
    parser.add_argument("--openclaw", help="OpenClaw Gateway地址 (如: http://127.0.0.1:18789)")
    parser.add_argument("--hermes", help="Hermes Agent地址 (如: http://127.0.0.1:8642)")
    parser.add_argument("--ssl", action="store_true", help="启用HTTPS")
    parser.add_argument("--cert", help="SSL证书文件路径")
    parser.add_argument("--key", help="SSL私钥文件路径")
    
    args = parser.parse_args()
    
    if args.openclaw:
        OPENCLAW_URL = args.openclaw
        USE_OPENCLAW = True
        logger.info(f"使用OpenClaw: {OPENCLAW_URL}")
    elif args.hermes:
        HERMES_URL = args.hermes
        USE_OPENCLAW = False
        logger.info(f"使用Hermes: {HERMES_URL}")
    else:
        # 默认使用本地OpenClaw
        OPENCLAW_URL = "http://127.0.0.1:18789"
        USE_OPENCLAW = True
        logger.info(f"使用默认OpenClaw: {OPENCLAW_URL}")
    
    logger.info(f"启动MiClaw LLM代理，监听 {args.host}:{args.port}")
    
    if args.ssl:
        if args.cert and args.key:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(args.cert, args.key)
            app.run(host=args.host, port=args.port, ssl_context=context)
        else:
            # 使用自签名证书
            app.run(host=args.host, port=args.port, ssl_context="adhoc")
    else:
        app.run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()

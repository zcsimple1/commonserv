#!/bin/bash

# Commonserv 启动脚本
# 用于启动微服务平台

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=================================="
echo "Commonserv 微服务平台启动"
echo "=================================="
echo ""

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "❌ 错误: 虚拟环境不存在"
    echo "请先运行: python3 -m venv venv"
    exit 1
fi

# 激活虚拟环境
echo "📦 激活虚拟环境..."
source venv/bin/activate

# 检查依赖
echo "🔍 检查依赖..."
python -c "import fastapi" 2>/dev/null || {
    echo "❌ 依赖未安装，正在安装..."
    pip install -r requirements.txt
}

echo ""
echo "✅ 虚拟环境已激活"
echo "🚀 启动服务..."
echo ""
echo "=================================="
echo "服务信息"
echo "=================================="
echo "API 文档: http://localhost:8000/docs"
echo "ReDoc:    http://localhost:8000/redoc"
echo "健康检查: http://localhost:8000/health"
echo ""
echo "快速获取 Token:"
echo "  产品级: curl http://localhost:8000/mqtt/onenet/v1/token/product"
echo "  MO设备: curl http://localhost:8000/mqtt/onenet/v1/token/device/mo"
echo "  MO1设备:curl http://localhost:8000/mqtt/onenet/v1/token/device/mo1"
echo ""
echo "按 Ctrl+C 停止服务"
echo "=================================="
echo ""

# 启动服务
python -m main

#!/bin/bash

# Commonserv 重启脚本
# 用于重启微服务平台

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=================================="
echo "Commonserv 重启服务"
echo "=================================="
echo ""

# 停止服务
echo "🛑 停止现有服务..."
./stop.sh

# 等待一下
sleep 2

# 启动服务
echo ""
echo "🚀 重新启动服务..."
./start.sh

#!/bin/bash

# Commonserv 停止脚本
# 用于停止正在运行的微服务平台

echo "=================================="
echo "Commonserv 停止服务"
echo "=================================="
echo ""

# 查找并停止进程
PIDS=$(ps aux | grep -E 'python.*main|uvicorn.*main' | grep -v grep | awk '{print $2}')

if [ -z "$PIDS" ]; then
    echo "✅ 没有运行中的服务"
else
    echo "🛑 停止服务进程..."
    for PID in $PIDS; do
        kill $PID 2>/dev/null && echo "  已停止进程 $PID"
    done
    echo "✅ 服务已停止"
fi

echo ""
echo "=================================="

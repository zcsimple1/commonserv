#!/bin/bash

# Commonserv 状态检查脚本
# 用于检查服务运行状态

echo "=================================="
echo "Commonserv 服务状态"
echo "=================================="
echo ""

# 查找进程
PIDS=$(ps aux | grep -E 'python.*main|uvicorn.*main' | grep -v grep)

if [ -z "$PIDS" ]; then
    echo "状态: ❌ 服务未运行"
    echo ""
    echo "启动服务: bash start.sh"
else
    echo "状态: ✅ 服务运行中"
    echo ""
    echo "进程信息:"
    echo "$PIDS"
    echo ""
    echo "测试连接:"
    echo "  健康检查: curl http://localhost:8000/health"
    echo "  API 文档:  curl http://localhost:8000/docs"
fi

echo ""
echo "=================================="

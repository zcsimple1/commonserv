#!/bin/bash

# Commonserv 测试脚本
# 用于测试 API 接口

echo "=================================="
echo "Commonserv API 测试"
echo "=================================="
echo ""

BASE_URL="http://localhost:8000"

# 测试健康检查
echo "1. 健康检查"
curl -s "${BASE_URL}/health" | python3 -m json.tool
echo ""

# 测试产品级 Token
echo "2. 获取产品级 Token"
curl -s "${BASE_URL}/mqtt/onenet/v1/token/product" | python3 -m json.tool
echo ""

# 测试 MO 设备 Token
echo "3. 获取 MO 设备 Token"
curl -s "${BASE_URL}/mqtt/onenet/v1/token/device/mo" | python3 -m json.tool
echo ""

# 测试 MO1 设备 Token
echo "4. 获取 MO1 设备 Token"
curl -s "${BASE_URL}/mqtt/onenet/v1/token/device/mo1" | python3 -m json.tool
echo ""

# 测试设备列表
echo "5. 获取设备列表"
curl -s "${BASE_URL}/mqtt/onenet/v1/devices" | python3 -m json.tool
echo ""

echo "=================================="

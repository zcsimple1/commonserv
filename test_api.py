#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API 测试脚本
用于测试 commonserv 的各个接口
"""

import requests
import json


BASE_URL = "http://localhost:8000"


def test_health():
    """测试健康检查接口"""
    print("=" * 40)
    print("1. 健康检查")
    print("=" * 40)
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        print()
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        print()


def test_product_token():
    """测试产品级 Token 接口"""
    print("=" * 40)
    print("2. 获取产品级 Token")
    print("=" * 40)
    try:
        response = requests.get(f"{BASE_URL}/mqtt/onenet/v1/token/product")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        print()
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        print()


def test_device_token(device_name):
    """测试设备级 Token 接口"""
    print("=" * 40)
    print(f"3. 获取 {device_name.upper()} 设备 Token")
    print("=" * 40)
    try:
        response = requests.get(f"{BASE_URL}/mqtt/onenet/v1/token/device/{device_name}")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        print()
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        print()


def test_devices_list():
    """测试设备列表接口"""
    print("=" * 40)
    print("4. 获取设备列表")
    print("=" * 40)
    try:
        response = requests.get(f"{BASE_URL}/mqtt/onenet/v1/devices")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        print()
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        print()


def test_nonexistent_device():
    """测试不存在的设备"""
    print("=" * 40)
    print("5. 测试不存在的设备")
    print("=" * 40)
    try:
        response = requests.get(f"{BASE_URL}/mqtt/onenet/v1/token/device/nonexistent")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        print()
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        print()


def main():
    """运行所有测试"""
    print()
    print("==================================")
    print("Commonserv API 测试")
    print("==================================")
    print()

    test_health()
    test_product_token()
    test_device_token("mo")
    test_device_token("mo1")
    test_devices_list()
    test_nonexistent_device()

    print("=" * 40)
    print("✅ 所有测试完成")
    print("=" * 40)


if __name__ == "__main__":
    main()

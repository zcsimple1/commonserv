#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OneNET MQTT Token 生成模块
基于 OneNET MQTT Token 文档实现
"""

import base64
import hmac
import hashlib
import json
import time
from mqtt.config import get_product_config, get_device_config


def generate_product_token(expire_hours: int = 720) -> str:
    """
    生成产品级 Token

    参数:
        expire_hours: Token 有效期（小时），默认 720 小时（30天）

    返回:
        Token 字符串
    """
    config = get_product_config()
    product_id = config["product_id"]
    access_key = base64.b64decode(config["access_key"])

    # Token 有效期时间戳
    expire_time = int(time.time()) + expire_hours * 3600

    # 构建 Token 负载
    payload = {
        "product_id": product_id,
        "expire_time": expire_time
    }

    # 生成 Token
    token = _generate_token(payload, access_key)

    return token


def generate_device_token(device_name: str, expire_hours: int = 720) -> str:
    """
    生成设备级 Token

    参数:
        device_name: 设备名称（MO 或 MO1）
        expire_hours: Token 有效期（小时），默认 720 小时（30天）

    返回:
        Token 字符串

    异常:
        ValueError: 设备不存在时抛出
    """
    device_config = get_device_config(device_name)
    if device_config is None:
        available_devices = get_product_config().get("devices", {}).keys()
        raise ValueError(
            f"设备 '{device_name}' 不存在。"
            f"可用设备: {', '.join(available_devices)}"
        )

    config = get_product_config()
    product_id = config["product_id"]
    access_key = base64.b64decode(config["access_key"])
    device_id = device_config["device_id"]

    # Token 有效期时间戳
    expire_time = int(time.time()) + expire_hours * 3600

    # 构建 Token 负载
    payload = {
        "product_id": product_id,
        "device_id": device_id,
        "expire_time": expire_time
    }

    # 生成 Token
    token = _generate_token(payload, access_key)

    return token


def _generate_token(payload: dict, access_key: bytes) -> str:
    """
    生成 Token 的内部函数

    参数:
        payload: Token 负载数据
        access_key: 解码后的访问密钥

    返回:
        Token 字符串
    """
    # 将负载转换为 JSON 字符串
    payload_str = json.dumps(payload, separators=(",", ":"))

    # 使用 HMAC-SHA256 生成签名
    signature = hmac.new(
        access_key,
        payload_str.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    # 组合 Token: payload + ":" + signature
    token = f"{payload_str}:{signature}"

    # Base64 编码整个 Token
    token_encoded = base64.b64encode(token.encode("utf-8")).decode("utf-8")

    return token_encoded


def decode_token(token: str, access_key: str) -> dict:
    """
    解码并验证 Token（仅用于测试和验证）

    参数:
        token: Token 字符串
        access_key: Base64 编码的访问密钥

    返回:
        Token 负载数据

    异常:
        ValueError: Token 无效或签名不匹配时抛出
    """
    try:
        # Base64 解码
        token_decoded = base64.b64decode(token.encode("utf-8")).decode("utf-8")

        # 分离 payload 和 signature
        parts = token_decoded.split(":")
        if len(parts) != 2:
            raise ValueError("Token 格式无效")

        payload_str, signature = parts

        # 验证签名
        access_key_decoded = base64.b64decode(access_key)
        expected_signature = hmac.new(
            access_key_decoded,
            payload_str.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        if signature != expected_signature:
            raise ValueError("Token 签名无效")

        # 解析 payload
        payload = json.loads(payload_str)
        return payload

    except Exception as e:
        raise ValueError(f"Token 解码失败: {str(e)}")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OneNET MQTT Token 生成模块
基于 OneNET MQTT Token 文档实现
Token 格式: version=2018-10-31&res=xxx&et=xxx&method=sha1&sign=xxx
"""

import hmac
import hashlib
import base64
import time
from urllib.parse import quote
from mqtt.config import get_product_config, get_device_config


def generate_product_token(expire_hours: int = 720) -> str:
    """
    生成产品级 Token

    参数:
        expire_hours: Token 有效期（小时），默认 720 小时（30天）

    返回:
        Token 字符串，格式: version=2018-10-31&res=products%2F{product_id}&et={expire_time}&method=sha1&sign={sign}
    """
    config = get_product_config()
    product_id = config["product_id"]
    access_key = base64.b64decode(config["access_key"])

    # Token 有效期时间戳（秒）
    expire_time = int(time.time()) + expire_hours * 3600

    # 产品级资源路径
    res = f"products/{product_id}"

    # 生成 Token
    token = _generate_token(res, expire_time, access_key)

    return token


def generate_device_token(device_name: str, expire_hours: int = 720) -> str:
    """
    生成设备级 Token

    参数:
        device_name: 设备名称（MO 或 MO1）
        expire_hours: Token 有效期（小时），默认 720 小时（30天）

    返回:
        Token 字符串，格式: version=2018-10-31&res=products%2F{product_id}%2Fdevices%2F{device_id}&et={expire_time}&method=sha1&sign={sign}

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

    # Token 有效期时间戳（秒）
    expire_time = int(time.time()) + expire_hours * 3600

    # 设备级资源路径
    res = f"products/{product_id}/devices/{device_id}"

    # 生成 Token
    token = _generate_token(res, expire_time, access_key)

    return token


def _generate_token(res: str, expire_time: int, access_key: bytes) -> str:
    """
    生成 OneNET MQTT Token 的内部函数

    参数:
        res: 资源路径
        expire_time: 过期时间戳（秒）
        access_key: 解码后的访问密钥

    返回:
        Token 字符串
    """
    # Token 版本
    version = "2018-10-31"

    # 签名方法
    method = "sha1"

    # 计算签名
    # 签名顺序: et + "\n" + method + "\n" + res + "\n" + version
    et = str(expire_time)
    text_to_sign = f"{et}\n{method}\n{res}\n{version}"
    signature = hmac.new(
        access_key,
        text_to_sign.encode("utf-8"),
        hashlib.sha1
    ).digest()

    # Base64 编码签名
    sign_base64 = base64.b64encode(signature).decode("utf-8")

    # URL 编码
    res_encoded = quote(res, safe='')
    sign_encoded = quote(sign_base64, safe='')

    # 组装 Token
    token = f"version={version}&res={res_encoded}&et={et}&method={method}&sign={sign_encoded}"

    return token


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
        # 解析 Token
        parts = {}
        for param in token.split("&"):
            key, value = param.split("=", 1)
            parts[key] = value

        # 验证版本
        if parts.get("version") != "2018-10-31":
            raise ValueError("Token 版本不支持")

        # URL 解码
        res = parts["res"]
        et = int(parts["et"])
        method = parts["method"]
        sign = parts["sign"]

        # 重新计算签名
        access_key_decoded = base64.b64decode(access_key)
        text_to_sign = f"{et}\n{res}\n{method}"
        expected_signature = hmac.new(
            access_key_decoded,
            text_to_sign.encode("utf-8"),
            hashlib.sha1
        ).digest()
        expected_sign_base64 = base64.b64encode(expected_signature).decode("utf-8")

        # 验证签名
        if sign != quote(expected_sign_base64):
            raise ValueError("Token 签名无效")

        return {
            "version": parts["version"],
            "res": res,
            "expire_time": et,
            "method": method,
            "sign": sign
        }

    except Exception as e:
        raise ValueError(f"Token 解码失败: {str(e)}")

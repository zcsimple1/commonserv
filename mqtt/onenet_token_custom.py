#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OneNET MQTT Token 自定义生成模块
支持传入参数生成 Token
"""

import hmac
import hashlib
import base64
import time
from urllib.parse import quote


def generate_product_token_custom(product_id: str, access_key: str, expire_hours: int = 720) -> str:
    """
    生成产品级 Token（自定义参数）

    参数:
        product_id: 产品 ID
        access_key: 访问密钥（Base64 编码）
        expire_hours: Token 有效期（小时），默认 720 小时（30天）

    返回:
        Token 字符串，格式: version=2018-10-31&res=products%2F{product_id}&et={expire_time}&method=sha1&sign={sign}
    """
    # Token 有效期时间戳（秒）
    expire_time = int(time.time()) + expire_hours * 3600

    # 产品级资源路径
    res = f"products/{product_id}"

    # 解码 access_key
    key = base64.b64decode(access_key)

    # Token 版本
    version = "2018-10-31"

    # 签名方法
    method = "sha1"

    # 计算签名
    # 签名顺序: et + "\n" + method + "\n" + res + "\n" + version
    et = str(expire_time)
    text_to_sign = f"{et}\n{method}\n{res}\n{version}"
    signature = hmac.new(
        key,
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


def generate_device_token_custom(product_id: str, device_id: str, access_key: str, expire_hours: int = 720) -> str:
    """
    生成设备级 Token（自定义参数）

    参数:
        product_id: 产品 ID
        device_id: 设备 ID
        access_key: 访问密钥（Base64 编码）
        expire_hours: Token 有效期（小时），默认 720 小时（30天）

    返回:
        Token 字符串，格式: version=2018-10-31&res=products%2F{product_id}%2Fdevices%2F{device_id}&et={expire_time}&method=sha1&sign={sign}
    """
    # Token 有效期时间戳（秒）
    expire_time = int(time.time()) + expire_hours * 3600

    # 设备级资源路径
    res = f"products/{product_id}/devices/{device_id}"

    # 解码 access_key
    key = base64.b64decode(access_key)

    # Token 版本
    version = "2018-10-31"

    # 签名方法
    method = "sha1"

    # 计算签名
    # 签名顺序: et + "\n" + method + "\n" + res + "\n" + version
    et = str(expire_time)
    text_to_sign = f"{et}\n{method}\n{res}\n{version}"
    signature = hmac.new(
        key,
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

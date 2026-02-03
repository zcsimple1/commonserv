#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OneNET 设备配置文件
包含产品信息和预配置的设备信息
"""

# OneNET 产品配置
PRODUCT_CONFIG = {
    "product_id": "v6IkuqD6vh",
    "access_key": "h7uDwVvrrRlRzX07xVHT/deJGZsHyZ+7zd1tBfc5G10=",
    "default_expire_hours": 720,  # 默认Token有效期：30天
    "devices": {
        "MO": {
            "device_id": "MO",
            "device_key": "THNRWXNxUWxjSWNUOXNoN0pNalBGR3pKVHd3TDBkbjQ=",
            "description": "MO设备"
        },
        "MO1": {
            "device_id": "MO1",
            "device_key": "THNRWXNxUWxjSWNUOXNoN0pNalBGR3pKVHd3TDBkbjQ=",
            "description": "MO1设备"
        }
    }
}


def get_product_config():
    """获取产品配置"""
    return PRODUCT_CONFIG


def get_device_config(device_name):
    """
    获取指定设备的配置

    参数:
        device_name: 设备名称（MO 或 MO1）

    返回:
        设备配置字典，如果设备不存在则返回None
    """
    devices = PRODUCT_CONFIG.get("devices", {})
    return devices.get(device_name.upper())


def get_all_device_names():
    """获取所有已配置的设备名称列表"""
    return list(PRODUCT_CONFIG.get("devices", {}).keys())

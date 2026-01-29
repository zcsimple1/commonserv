#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OneNET MQTT Token 生成服务
提供产品级和设备级 Token 生成接口
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from mqtt import onenet_token
import uvicorn

app = FastAPI(
    title="Commonserv 微服务平台",
    description="OneNET MQTT Token 生成服务",
    version="1.0.0"
)


@app.get("/")
async def root():
    """根路径"""
    return {
        "service": "Commonserv 微服务平台",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "service": "commonserv"}


@app.get("/mqtt/onenet/v1/token/product")
async def get_product_token():
    """获取产品级 Token"""
    try:
        token = onenet_token.generate_product_token()
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "token": token,
                "type": "product"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mqtt/onenet/v1/token/device/{device_name}")
async def get_device_token(device_name: str):
    """
    获取指定设备的 Token

    参数:
        device_name: 设备名称（如 mo, mo1, MO, MO1）
    """
    try:
        token = onenet_token.generate_device_token(device_name)
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "token": token,
                "device": device_name,
                "type": "device"
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mqtt/onenet/v1/device/MO")
async def get_mo_token():
    """获取 MO 设备的 Token（固定接口）"""
    try:
        token = onenet_token.generate_device_token("MO")
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "token": token,
                "device": "MO",
                "type": "device"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mqtt/onenet/v1/device/MO1")
async def get_mo1_token():
    """获取 MO1 设备的 Token（固定接口）"""
    try:
        token = onenet_token.generate_device_token("MO1")
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "token": token,
                "device": "MO1",
                "type": "device"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mqtt/onenet/v1/devices")
async def list_devices():
    """列出所有已配置的设备"""
    from mqtt.config import get_all_device_names
    devices = get_all_device_names()
    return {
        "code": 0,
        "msg": "success",
        "data": {
            "devices": devices,
            "count": len(devices)
        }
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OneNET MQTT Token 生成服务
提供产品级和设备级 Token 生成接口
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from mqtt import onenet_token, onenet_token_custom, token_cache
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
        "health": "/health",
        "routes": "/routes"
    }


@app.get("/routes")
async def list_routes():
    """列出所有可用路由"""
    from fastapi.routing import APIRoute
    routes = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            routes.append({
                "path": route.path,
                "methods": list(route.methods),
                "summary": route.summary
            })
    return {
        "code": 0,
        "msg": "success",
        "data": {
            "routes": routes,
            "count": len(routes)
        }
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "service": "commonserv"}


@app.get("/mqtt/onenet/v1/token/product")
async def get_product_token(product_id: str = None, access_key: str = None, expire_hours: int = None):
    """
    获取产品级 Token

    参数（可选）:
        product_id: 产品 ID，不传则使用配置文件中的默认值
        access_key: 访问密钥（Base64 编码），不传则使用配置文件中的默认值
        expire_hours: Token 有效期（小时），默认 720 小时（30天）
    """
    try:
        # 如果传入了参数，使用传入的参数生成 Token
        if product_id and access_key:
            from mqtt import onenet_token_custom
            if expire_hours is None:
                expire_hours = 720
            token = onenet_token_custom.generate_product_token_custom(product_id, access_key, expire_hours)
        else:
            # 使用配置文件中的默认值
            token = onenet_token.generate_product_token(expire_hours if expire_hours else 720)

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


@app.get("/mqtt/onenet/v1/token/custom/device")
async def get_device_token_custom(product_id: str, device_id: str, access_key: str, expire_hours: int = None):
    """
    自定义参数生成设备级 Token

    参数:
        product_id: 产品 ID
        device_id: 设备 ID
        access_key: 访问密钥（Base64 编码）
        expire_hours: Token 有效期（小时），可选，默认 720 小时
    """
    try:
        if expire_hours is None:
            expire_hours = 720
        token = onenet_token_custom.generate_device_token_custom(product_id, device_id, access_key, expire_hours)
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "token": token,
                "device": device_id,
                "type": "device"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mqtt/onenet/v1/device/MO")
@app.get("/mqtt/onenet/v1/device/mo")
async def get_mo_token(refresh: bool = Query(False, description="强制刷新缓存")):
    """
    获取 MO 设备的 Token（固定接口）

    参数:
        refresh: 是否强制刷新缓存，默认 False
    """
    try:
        cache_key = "device_MO"

        # 如果强制刷新，删除缓存
        if refresh:
            token_cache.cache.refresh(cache_key)

        # 尝试从缓存获取
        cached_token = token_cache.cache.get(cache_key)
        if cached_token:
            return {
                "code": 0,
                "msg": "success",
                "data": {
                    "token": cached_token,
                    "device": "MO",
                    "type": "device",
                    "cached": True
                }
            }

        # 缓存未命中，生成新 Token
        token = onenet_token.generate_device_token("MO")
        # 存入缓存
        token_cache.cache.set(cache_key, token)

        return {
            "code": 0,
            "msg": "success",
            "data": {
                "token": token,
                "device": "MO",
                "type": "device",
                "cached": False
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mqtt/onenet/v1/device/MO1")
@app.get("/mqtt/onenet/v1/device/mo1")
async def get_mo1_token(refresh: bool = Query(False, description="强制刷新缓存")):
    """
    获取 MO1 设备的 Token（固定接口）

    参数:
        refresh: 是否强制刷新缓存，默认 False
    """
    try:
        cache_key = "device_MO1"

        # 如果强制刷新，删除缓存
        if refresh:
            token_cache.cache.refresh(cache_key)

        # 尝试从缓存获取
        cached_token = token_cache.cache.get(cache_key)
        if cached_token:
            return {
                "code": 0,
                "msg": "success",
                "data": {
                    "token": cached_token,
                    "device": "MO1",
                    "type": "device",
                    "cached": True
                }
            }

        # 缓存未命中，生成新 Token
        token = onenet_token.generate_device_token("MO1")
        # 存入缓存
        token_cache.cache.set(cache_key, token)

        return {
            "code": 0,
            "msg": "success",
            "data": {
                "token": token,
                "device": "MO1",
                "type": "device",
                "cached": False
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


@app.get("/mqtt/onenet/v1/cache")
async def get_cache_info():
    """获取缓存信息"""
    cache_info = token_cache.cache.get_all()
    return {
        "code": 0,
        "msg": "success",
        "data": {
            "cache": cache_info,
            "expire_days": 29,
            "count": len(cache_info)
        }
    }


@app.delete("/mqtt/onenet/v1/cache")
async def clear_cache():
    """清空所有缓存"""
    token_cache.cache.clear()
    return {
        "code": 0,
        "msg": "success",
        "data": {
            "message": "缓存已清空"
        }
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

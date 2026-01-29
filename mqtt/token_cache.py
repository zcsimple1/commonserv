#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Token 缓存模块
提供 Token 缓存、自动刷新和强制刷新功能
"""

import time
from typing import Optional, Dict, Any


class TokenCache:
    """Token 缓存类"""

    def __init__(self, expire_days: int = 29):
        """
        初始化缓存

        参数:
            expire_days: 缓存过期天数，默认 29 天
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.expire_days = expire_days

    def get(self, key: str) -> Optional[str]:
        """
        获取缓存的 Token

        参数:
            key: 缓存键

        返回:
            Token 字符串，如果不存在或已过期则返回 None
        """
        if key not in self.cache:
            return None

        cached = self.cache[key]

        # 检查是否过期（29 天）
        if self._is_expired(cached['timestamp'], self.expire_days):
            del self.cache[key]
            return None

        return cached['token']

    def set(self, key: str, token: str) -> None:
        """
        设置缓存

        参数:
            key: 缓存键
            token: Token 字符串
        """
        self.cache[key] = {
            'token': token,
            'timestamp': time.time()
        }

    def refresh(self, key: str) -> bool:
        """
        删除缓存中的指定 key

        参数:
            key: 缓存键

        返回:
            True 如果删除成功，False 如果不存在
        """
        if key in self.cache:
            del self.cache[key]
            return True
        return False

    def clear(self) -> None:
        """清空所有缓存"""
        self.cache.clear()

    def get_all(self) -> Dict[str, Dict[str, Any]]:
        """获取所有缓存信息"""
        return self.cache.copy()

    def _is_expired(self, timestamp: float, expire_days: int) -> bool:
        """
        检查是否过期

        参数:
            timestamp: 时间戳
            expire_days: 过期天数

        返回:
            True 如果已过期
        """
        expire_seconds = expire_days * 24 * 3600
        return (time.time() - timestamp) > expire_seconds


# 创建全局缓存实例
cache = TokenCache(expire_days=29)

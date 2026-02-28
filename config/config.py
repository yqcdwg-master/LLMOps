#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/1 14:50
@Author  : thezehui@gmail.com
@File    : config.py
"""
from functools import lru_cache
from typing import Dict, Any

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """应用配置类"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ==================== Flask 配置 ====================
    WTF_CSRF_ENABLED: bool = Field(default=False, description="是否启用CSRF保护")
    FLASK_ENV: str = Field(default="development", description="Flask运行环境")
    FLASK_DEBUG: str = Field(default="1", description="Flask调试模式")

    # ==================== SQLAlchemy 配置 ====================
    SQLALCHEMY_DATABASE_URI: str = Field(default="", description="数据库连接URI")
    SQLALCHEMY_POOL_SIZE: int = Field(default=10, description="数据库连接池大小")
    SQLALCHEMY_POOL_RECYCLE: int = Field(default=3600, description="数据库连接回收时间(秒)")
    SQLALCHEMY_ECHO: bool = Field(default=False, description="是否打印SQL语句")

    # ==================== OpenAI 配置 ====================
    OPENAI_BASE_URL: str = Field(default="", description="OpenAI API基地址")
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API密钥")

    # ==================== PostgreSQL 配置 ====================
    POSTGRES_USER: str = Field(default="llmops", description="PostgreSQL用户名")
    POSTGRES_PASSWORD: str = Field(default="", description="PostgreSQL密码")
    POSTGRES_DB: str = Field(default="llmops", description="PostgreSQL数据库名")
    POSTGRES_HOST: str = Field(default="localhost", description="PostgreSQL主机地址")
    POSTGRES_PORT: str = Field(default="5432", description="PostgreSQL端口")

    # ==================== 缓存配置 ====================
    CACHE_TYPE: str = Field(default="simple", description="缓存类型(simple/redis/memcached)")
    CACHE_REDIS_URL: str = Field(default="redis://localhost:6379/0", description="Redis连接URL")
    CACHE_DEFAULT_TIMEOUT: int = Field(default=300, description="缓存默认超时时间(秒)")
    CACHE_THRESHOLD: int = Field(default=500, description="缓存最大条目数")

    # ==================== SQLAlchemy Engine 选项 ====================
    SQLALCHEMY_MAX_OVERFLOW: int = Field(default=10, description="最大溢出连接数")

    @computed_field(description="SQLAlchemy引擎配置")
    @property
    def SQLALCHEMY_ENGINE_OPTIONS(self) -> Dict[str, Any]:
        """SQLAlchemy 引擎配置选项"""
        return {
            "pool_size": self.SQLALCHEMY_POOL_SIZE,
            "pool_recycle": self.SQLALCHEMY_POOL_RECYCLE,
            "max_overflow": self.SQLALCHEMY_MAX_OVERFLOW,
            "pool_pre_ping": True,
            "echo": self.SQLALCHEMY_ECHO,
        }


@lru_cache
def get_settings() -> Config:
    """Get cached settings instance.

    Returns:
        Singleton Settings instance loaded from environment.
    """
    return Config()


# Global settings instance
config = get_settings()

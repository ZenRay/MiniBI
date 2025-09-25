"""
Redis缓存工具模块
"""
import redis
import json
import os
from typing import Any, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 连接参数
REDIS_URL = os.getenv("REDIS_URL", "redis:6379")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "admin")

# 缓存配置
CACHE_CONFIG = {
    'high_frequency': 60,      # 1分钟缓存
    'medium_frequency': 300,   # 5分钟缓存
    'low_frequency': 1800,     # 30分钟缓存
    'static_data': 86400       # 24小时缓存
}

class RedisCache:
    """Redis缓存管理类"""
    
    def __init__(self):
        """初始化Redis连接"""
        host, port = REDIS_URL.split(':')
        self.client = redis.Redis(
            host=host, 
            port=int(port),
            password=REDIS_PASSWORD,
            decode_responses=True
        )
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存数据"""
        try:
            data = self.client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"Redis缓存读取错误: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = CACHE_CONFIG['medium_frequency']) -> bool:
        """设置缓存数据"""
        try:
            self.client.setex(key, ttl, json.dumps(value))
            return True
        except Exception as e:
            print(f"Redis缓存写入错误: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """删除缓存数据"""
        try:
            return self.client.delete(key) > 0
        except Exception as e:
            print(f"Redis缓存删除错误: {e}")
            return False

    def flush(self) -> bool:
        """清空所有缓存数据"""
        try:
            self.client.flushdb()
            return True
        except Exception as e:
            print(f"Redis缓存清空错误: {e}")
            return False

# 创建单例实例
cache = RedisCache()
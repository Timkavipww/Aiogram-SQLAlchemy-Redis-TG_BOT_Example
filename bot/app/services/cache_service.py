import json
from typing import Any
from app.config.redis_config import redis
from sqlalchemy.orm.attributes import InstrumentedAttribute

class CacheService:

    def __init__(self, client=redis):
        self.client = client

    async def set(self, key: str, value: Any, expire: int = None):
            """
            Сохраняет объект в Redis.
            Если value не str, сериализует его в JSON.
            """
            if not isinstance(value, str):
                value = json.dumps(value, default=self._default_serializer)
            await self.client.set(key, value, ex=expire)

    async def get(self, key: str) -> Any:
        """
        Получает объект из Redis и пытается десериализовать JSON.
        """
        data = await self.client.get(key)
        if data is None:
            return None
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return data  # если это была простая строка

    @staticmethod
    def _default_serializer(obj):
        if hasattr(obj, "__dict__"):
            data = {}
            for k, v in obj.__dict__.items():
                if k.startswith("_"):
                    continue
                if isinstance(getattr(type(obj), k, None), InstrumentedAttribute):
                    if k not in ("created_at", "updated_at"):
                        data[k] = v
            return data
        return str(obj)
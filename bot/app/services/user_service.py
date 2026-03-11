from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from app.db.models.user import User
from app.services.cache_service import CacheService


class UserService:
    """CRUD-операции для User с интеграцией кэша"""

    def __init__(self, session: AsyncSession, cache: CacheService):
        self.session = session
        self.cache = cache

    def _cache_key(self, user_id: int) -> str:
        """Формирует ключ кэша для пользователя"""
        return f"user:{user_id}"

    async def get_user(self, user_id: int) -> User | None:
        """Получает пользователя из кэша или БД"""
        cache_key = self._cache_key(user_id)
        
        # Пытаемся получить из кэша
        cached_user = await self.cache.get(cache_key)
        if cached_user:
            return cached_user
        
        # Если нет в кэше, ищем в БД
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        # Кэшируем результат (если нашли)
        if user:
            await self.cache.set(cache_key, user, expire=3600)  # 1 час
        
        return user

    async def create_user(self, user_id: int, username: str | None) -> User:
        """Создаёт нового пользователя и кэширует"""
        user = User(
            id=user_id,
            username=username
        )
        
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        
        # Кэшируем созданного пользователя
        await self.cache.set(self._cache_key(user_id), user, expire=3600)
        
        return user

    async def get_or_create_user(self, user_id: int, username: str | None) -> User:
        """Получает или создаёт пользователя"""
        user = await self.get_user(user_id)
        
        if user:
            return user
        
        return await self.create_user(user_id, username)

    async def ensure_user(self, user_id: int, username: str | None) -> None:
        """Гарантирует наличие пользователя (INSERT или ничего)"""
        stmt = insert(User).values(
            id=user_id,
            username=username   
        ).on_conflict_do_nothing(
            index_elements=[User.id]
        )
        
        await self.session.execute(stmt)
        await self.session.commit()

    async def update_user(self, user_id: int, username: str | None = None) -> User | None:
        """Обновляет пользователя и инвалидирует кэш"""
        user = await self.get_user(user_id)
        
        if not user:
            return None
        
        if username is not None:
            user.username = username
        
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        
        # Обновляем кэш
        await self.cache.set(self._cache_key(user_id), user, expire=3600)
        
        return user

    async def delete_user(self, user_id: int) -> bool:
        """Удаляет пользователя и удаляет из кэша"""
        user = await self.get_user(user_id)
        
        if not user:
            return False
        
        await self.session.delete(user)
        await self.session.commit()
        
        # Удаляем из кэша
        await self.cache.client.delete(self._cache_key(user_id))
        
        return True

    async def invalidate_user_cache(self, user_id: int) -> None:
        """Инвалидирует кэш пользователя"""
        await self.cache.client.delete(self._cache_key(user_id))
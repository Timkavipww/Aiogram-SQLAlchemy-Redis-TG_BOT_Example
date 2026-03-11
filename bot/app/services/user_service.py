from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from app.db.models.user import User

class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_user(self, user_id: int) -> User | None:

        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )

        return result.scalar_one_or_none()


    async def create_user(self, user_id: int, username: str | None):

        user = User(
            id=user_id,
            username=username
        )

        self.session.add(user)
        await self.session.commit()

        return user


    async def get_or_create_user(self, user_id: int, username: str | None):

        user = await self.get_user(user_id)

        if user:
            return user

        return await self.create_user(user_id, username)
    

    
    async def ensure_user(self, user_id: int, username: str | None):

        stmt = insert(User).values(
            id=user_id,
            username=username
        ).on_conflict_do_nothing(
            index_elements=[User.id]
        )

        await self.session.execute(stmt)
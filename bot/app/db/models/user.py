from sqlalchemy.sql import func
from sqlalchemy import Column, BigInteger, DateTime, String
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(BigInteger, primary_key=True, unique=True, nullable=False, index=True, autoincrement=False)
    username = Column(String(127), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
from datetime import datetime

from sqlalchemy import (
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    hash_password: Mapped[str] = mapped_column(String(70), nullable=False)

    created_at: Mapped[datetime] = mapped_column(index=True, server_default=func.now())

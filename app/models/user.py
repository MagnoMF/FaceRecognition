from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import String, DateTime, Integer

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    cd_user: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ds_name: Mapped[str] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))
    create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
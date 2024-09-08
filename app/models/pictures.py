from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, ARRAY, Float
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Pictures(Base):
    __tablename__ = "pictures"
    picture_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cd_user: Mapped[int] = mapped_column(Integer, nullable=False)
    picture_vector: Mapped[ARRAY] = mapped_column(ARRAY(Float), nullable=False)
    update_date: Mapped[datetime] = mapped_column(default=datetime.now().strftime("%Y/%m/%d"))
    update_time: Mapped[datetime] = mapped_column(default=datetime.now().strftime("%H:%M:%S"))

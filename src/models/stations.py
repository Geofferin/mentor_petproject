import datetime
from sqlalchemy import String, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4

from src.models.base import Base


class StationModel(Base):
    __tablename__ = 'stations'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    city_id: Mapped[UUID] = mapped_column(ForeignKey('cities.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(256))
    address: Mapped[str] = mapped_column(String(256))
    type: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(onupdate=text("TIMEZONE('utc', now())"),
                                                          nullable=True)
    is_deleted: Mapped[bool] = mapped_column(server_default=text("false"))

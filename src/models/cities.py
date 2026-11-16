import datetime
from sqlalchemy import String, text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4

from src.models.stations import StationModel
from src.models.base import Base


class CityModel(Base):
    __tablename__ = 'cities'
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(256))
    country: Mapped[str] = mapped_column(String(256))
    population: Mapped[int] = mapped_column(Integer)
    stations: Mapped[list["StationModel"]] = relationship(lazy="selectin")
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(onupdate=text("TIMEZONE('utc', now())"),
                                                          nullable=True)
    is_deleted: Mapped[bool] = mapped_column(server_default=text("false"))

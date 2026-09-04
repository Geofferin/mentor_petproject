import datetime
from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated
from src.models.users import Base

# для примера используется часовой пояс UTC
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                        onupdate=datetime.datetime.utcnow())]

class CityModel(Base):
    __tablename__ = 'cities'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    country: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    is_deleted: Mapped[bool] = mapped_column(server_default=text("false"))

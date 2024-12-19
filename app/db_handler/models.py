from app.db_handler.custom_field import str_256, pk, created_at, DecimalField

from sqlalchemy import String, ForeignKey, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class UserTable(Base):
    __tablename__ = 'User'

    id: Mapped[pk]
    username: Mapped[str]
    name: Mapped[str_256 | None]
    id_telegram: Mapped[int]

    refuelings: Mapped[list['RefuelingTable']] = relationship(back_populates='user')


class RefuelingTable(Base):
    __tablename__ = 'Refueling'

    id: Mapped[pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id", ondelete="CASCADE"))
    date: Mapped[created_at]
    amount_gasoline = Column(DecimalField(50))
    mileage = Column(DecimalField(50))
    cost_refueling = Column(DecimalField(50))
    price_gasoline = Column(DecimalField(50))

    user: Mapped["UserTable"] = relationship(back_populates='refuelings')

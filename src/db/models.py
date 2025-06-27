from datetime import datetime
from typing import Any

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import Mapped, mapped_column

from src.config import IS_TEST

from .database import Base

money_type: type[float] | type[MONEY] = float if IS_TEST else MONEY


class AbstractTable(Base):
    __abstract__ = True

    def as_dict(self) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="id")


class Administrator(AbstractTable):
    __tablename__ = "administrators"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="id администратора"
    )
    name: Mapped[str] = mapped_column(String(255), comment="Имя администратора")
    phone: Mapped[str | None] = mapped_column(String(30), comment="Телефон администратора")
    tg_id: Mapped[int] = mapped_column(comment="id телеграм аккаунта администратора")


class Cource(AbstractTable):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="id курса")
    name: Mapped[str] = mapped_column(String(255), comment="Название курса")
    lessons_amount: Mapped[int] = mapped_column(comment="Количество занятий в курсе")
    price: Mapped[money_type] = mapped_column(comment="Цена курса")


class CourseToDog(AbstractTable):
    __tablename__ = "courses_to_dogs"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="id связи собак с курсами"
    )
    dog_id: Mapped[int] = mapped_column(
        ForeignKey("dogs.id", ondelete="CASCADE"), comment="id собаки"
    )
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), comment="id курса"
    )


class Customer(AbstractTable):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="id клиента")
    name: Mapped[str] = mapped_column(String(255), comment="Имя клиента")
    phone: Mapped[str | None] = mapped_column(String(30), comment="Телефон клиента")
    tg_id: Mapped[int | None] = mapped_column(comment="id тегерам аккаунта клиента")


class Dog(AbstractTable):
    __tablename__ = "dogs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="id собаки")
    name: Mapped[str] = mapped_column(String(255), comment="Кличка собаки")
    breed: Mapped[str] = mapped_column(String(255), comment="Порода собаки")
    owner: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE", comment="id хозяина собаки")
    )
    is_big: Mapped[bool] = mapped_column(default=True, comment="Является ли собака большой")
    is_active: Mapped[bool] = mapped_column(default=True, comment="Занимается ли сейчас собака")


class Staff(AbstractTable):
    __tablename__ = "staffs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="id сотрудника")
    status: Mapped[int] = mapped_column(
        ForeignKey("staff_status.id", ondelete="SET NULL"), comment="id статуса сотрудника"
    )
    name: Mapped[str] = mapped_column(String(255), comment="Имя сотрудника")
    phone: Mapped[str | None] = mapped_column(String(30), comment="Номер телефона сотрудника")
    tg_id: Mapped[int] = mapped_column(comment="id телеграм аккаунта сотрудника")


class StaffStatus(AbstractTable):
    __tablename__ = "staff_status"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="id роли сотрудника"
    )
    name: Mapped[str] = mapped_column(String(255), comment="Имя роли сотрудника")
    big_dog_price: Mapped[money_type] = mapped_column(comment="Цена занятия с большой собакой")
    low_dog_price: Mapped[money_type] = mapped_column(comment="Цена занятия с маленькой собакой")
    group_price: Mapped[money_type] = mapped_column(comment="Цена собаки на групповом занятии")


class Lesson(AbstractTable):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="id занятия")
    is_group: Mapped[bool] = mapped_column(default=False, comment="Является ли занятие групповым")
    date: Mapped[datetime] = mapped_column(comment="Дата и время проведения занятия")


class LessonStaff(AbstractTable):
    __tablename__ = "lesson_staff"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="id связи занятия с сотрудником"
    )
    staff_id: Mapped[int] = mapped_column(
        ForeignKey("staffs.id", ondelete="SET NULL"), comment="id сотрудника"
    )
    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id", ondelete="SET NULL"), comment="id занятия"
    )


class LessonDog(AbstractTable):
    __tablename__ = "lesson_dog"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="id связи занятия с собакой"
    )
    dog_id: Mapped[int] = mapped_column(
        ForeignKey("dogs.id", ondelete="SET NULL"), comment="id собаки"
    )
    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id", ondelete="SET NULL"), comment="id занятия"
    )

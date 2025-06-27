from typing import ClassVar

from src.objects import (
    Administrator,
    Course,
    Customer,
    Dog,
    Lesson,
    LessonDog,
    LessonStaff,
    Staff,
    StaffStatus,
)


class BaseFactory:
    _allowed_classes = (
        type[Administrator]
        | type[Course]
        | type[Customer]
        | type[Dog]
        | type[Lesson]
        | type[LessonDog]
        | type[LessonStaff]
        | type[Staff]
        | type[StaffStatus]
        | None
    )

    factory: ClassVar[dict[str, _allowed_classes]] = {
        "administrators": Administrator,
        "courses": Course,
        "customers": Customer,
        "dogs": Dog,
        "lessons": Lesson,
        "lesson_staff": LessonStaff,
        "staffs": Staff,
        "staff_statuses": StaffStatus,
        "lesson_dog": LessonDog,
    }

    @classmethod
    def get(cls, object_name: str) -> _allowed_classes:
        return cls.factory.get(object_name)

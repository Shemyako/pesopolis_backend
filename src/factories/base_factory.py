from src.objects import (
    Administrator,
    Course,
    Customer,
    Dog,
    Lesson,
    LessonStaff,
    Staff,
    StaffStatus,
)


class BaseFactory:
    factory = {
        "administrators": Administrator,
        "courses": Course,
        "customers": Customer,
        "dogs": Dog,
        "lessons": Lesson,
        "lesson_staff": LessonStaff,
        "staffs": Staff,
        "staff_statuses": StaffStatus,
    }

    @classmethod
    def get(cls, object_name):
        return cls.factory.get(object_name)

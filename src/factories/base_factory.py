from objects import Administrator, Course, Customer, Dog, Lesson, Staff, StaffStatus


class BaseFactory:
    factory = {
        "administrators": Administrator,
        "courses": Course,
        "customers": Customer,
        "dogs": Dog,
        "lessons": Lesson,
        "staff_statuses": StaffStatus,
        "staffs": Staff,
    }

    @classmethod
    def get(cls, object_name):
        return cls.factory.get(object_name)

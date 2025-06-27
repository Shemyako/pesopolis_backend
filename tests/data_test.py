from datetime import datetime

from src.db.models import (
    Administrator,
    Cource,
    CourseToDog,
    Customer,
    Dog,
    Lesson,
    LessonDog,
    LessonStaff,
    Staff,
    StaffStatus,
)

test_admins = [
    Administrator(name="Alice", tg_id=111),
    Administrator(name="Bob", tg_id=112),
    Administrator(name="Jake", tg_id=113),
    Administrator(name="Dick", tg_id=114),
    Administrator(name="TO_DELETE", tg_id=114),
    Administrator(name="TO_DELETE", tg_id=114),
    Administrator(name="TO_DELETE", tg_id=114),
]

test_cources = [
    Cource(name="Short", lessons_amount=10, price=1000),
    Cource(name="Middle", lessons_amount=15, price=1500),
    Cource(name="Long", lessons_amount=20, price=2000),
]

test_customers = [
    Customer(name="Alice", tg_id=1110),
    Customer(name="Bob", tg_id=1120),
    Customer(name="Jake", tg_id=1130),
    Customer(name="Dick", tg_id=1140),
]

test_dogs = [
    Dog(
        name="Bobbie",
        breed="Deuth Shepherd",
        owner=test_customers[0],
        is_big=True,
        is_active=True,
    ),
    Dog(
        name="Jackee",
        breed="Eastern Eur. Shepherd",
        owner=test_customers[1],
        is_big=True,
        is_active=True,
    ),
    Dog(
        name="Billy",
        breed="Pug",
        owner=test_customers[2],
        is_big=False,
        is_active=True,
    ),
    Dog(
        name="Dockie",
        breed="Half-breed",
        owner=test_customers[3],
        is_big=False,
        is_active=True,
    ),
]

test_dog_to_cource = [
    CourseToDog(dog_id=test_dogs[0], course_id=test_cources[0]),
    CourseToDog(dog_id=test_dogs[1], course_id=test_cources[0]),
    CourseToDog(dog_id=test_dogs[2], course_id=test_cources[0]),
    CourseToDog(dog_id=test_dogs[3], course_id=test_cources[0]),
]

test_staff_statuses = [
    StaffStatus(name="Junior", big_dog_price=500, low_dog_price=600, group_price=300),
    StaffStatus(name="Middle", big_dog_price=800, low_dog_price=900, group_price=400),
    StaffStatus(name="Senior", big_dog_price=1000, low_dog_price=1200, group_price=500),
]
test_staff = [
    Staff(name="Alice", tg_id=1110, status=test_staff_statuses[0]),
    Staff(name="Bob", tg_id=1120, status=test_staff_statuses[0]),
    Staff(name="Jake", tg_id=1130, status=test_staff_statuses[1]),
    Staff(name="Dick", tg_id=1140, status=test_staff_statuses[2]),
]

test_lessons = [
    Lesson(is_group=True, date=datetime.fromisoformat("2023-12-29 15:00:00")),
    Lesson(is_group=False, date=datetime.fromisoformat("2023-12-29 16:00:00")),
    Lesson(is_group=False, date=datetime.fromisoformat("2023-12-29 17:00:00")),
]
test_lesson_dog = [
    LessonDog(lesson_id=test_lessons[0], dog_id=test_dogs[0]),
    LessonDog(lesson_id=test_lessons[0], dog_id=test_dogs[1]),
    LessonDog(lesson_id=test_lessons[1], dog_id=test_dogs[2]),
    LessonDog(lesson_id=test_lessons[2], dog_id=test_dogs[3]),
]
# HERE
test_lesson_staff = [
    LessonStaff(lesson_id=test_lessons[0], staff_id=test_staff[0]),
    LessonStaff(lesson_id=test_lessons[1], staff_id=test_staff[1]),
    LessonStaff(lesson_id=test_lessons[2], staff_id=test_staff[2]),
]

first_step_insert = test_admins + test_cources + test_customers + test_staff_statuses

second_step_insert = test_dogs + test_dog_to_cource + test_staff + test_lessons

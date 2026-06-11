from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import BaseSQL
import enum

class UserRole(enum.Enum):
    student = "student"
    admin = "admin"

class User(BaseSQL):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.student)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    courses = relationship("Course", back_populates="owner")
    enrollments = relationship("Enrollment", back_populates="user")
    progress = relationship("Progress", back_populates="user")

class Course(BaseSQL):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner_id = Column(Integer, ForeignKey("users.id"))

    # Связи
    owner = relationship("User", back_populates="courses")
    lessons = relationship("Lesson", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")

class Lesson(BaseSQL):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    video_url = Column(String)  # URL видео
    duration = Column(Integer)  # Длительность в секундах
    order = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    course_id = Column(Integer, ForeignKey("courses.id"))

    # Связи
    course = relationship("Course", back_populates="lessons")
    progress = relationship("Progress", back_populates="lesson")

class Enrollment(BaseSQL):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))  # Дата истечения доступа

    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))

    # Связи
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

class Progress(BaseSQL):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    watched_seconds = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)
    last_watched_at = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))

    # Связи
    user = relationship("User", back_populates="progress")
    lesson = relationship("Lesson", back_populates="progress")

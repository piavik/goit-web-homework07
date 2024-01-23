from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from datetime import datetime

Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column('name', String, nullable=False)
    
    
class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column('name', String, nullable=False)
    group_id: Mapped[int] = mapped_column('group', Integer, ForeignKey('groups.id'))
    group: Mapped['Group'] = relationship(Group)


class Lector(Base):
    __tablename__ = 'lectors'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column('name', String, nullable=False)


class Subject(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column('name', String, nullable=False)
    lector_id: Mapped[str] = mapped_column('lector', Integer, ForeignKey('lectors.id'))
    lector: Mapped['Lector'] = relationship(Lector)


class Score(Base):
    __tablename__ = 'scores'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    score: Mapped[int] = mapped_column(Integer)
    score_date: Mapped[datetime] = mapped_column(DateTime)
    student_id: Mapped[int] = mapped_column('student_id', Integer, ForeignKey('students.id'))
    subject_id: Mapped[int] = mapped_column('subject_id', Integer, ForeignKey('subjects.id'))
    student: Mapped['Student'] = relationship(Student)
    subject: Mapped['Subject'] = relationship(Subject)

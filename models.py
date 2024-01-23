from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base
# from sqlalchemy.ext.declarative import declarative_base # this is for alchemy 1.x

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    group_id = Column("group_id", ForeignKey('groups.id', ondelete='CASCADE'))
    group = relationship("Group", backref='students')

class Lector(Base):
    __tablename__ = 'lectors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    lector_id = Column("lector_id", ForeignKey('lectors.id', ondelete='CASCADE'))
    lector = relationship('Lector', backref='subjects')


class Score(Base):
    __tablename__ = 'scores'
    id = Column(Integer, primary_key=True)
    score = Column(Integer)
    score_date = Column(Date)
    student_id = Column("student_id", ForeignKey('students.id', ondelete='CASCADE'))
    subject_id = Column("subject_id", ForeignKey('subjects.id', ondelete='CASCADE'))
    student = relationship('Student', backref='scores')
    subject = relationship('Subject', backref='scores')

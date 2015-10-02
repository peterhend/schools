import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class District(Base):
    __tablename__ = 'district'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    superintendent = Column(String(50))
    address = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    zip = Column(String(50))
    phone = Column(String(50))

class School(Base):
    __tablename__ = 'school'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    principal = Column(String(250))
    district_id = Column(Integer, ForeignKey('district.id'))
    district = relationship(District)

class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=False)
    school_id = Column(Integer, ForeignKey('school.id'))
    school = relationship(School)

class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=False)
    school_id = Column(Integer, ForeignKey('school.id'))
    school = relationship(School)

class Section(Base):
    __tablename__ = 'section'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    school_id = Column(Integer, ForeignKey('school.id'))
    school = relationship(School)
    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    teacher = relationship(Teacher)

class Enrollment(Base):
    __tablename__ = 'enrollment'

    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey('section.id'))
    section = relationship(Section)
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship(Student)

# We added this serialize function to be able to send JSON objects in a
# serializable format
##    @property
##    def serialize(self):
##
##        return {
##            'name': self.name,
##            'description': self.description,
##            'id': self.id,
##            'price': self.price,
##            'course': self.course,
##        }

engine = create_engine('sqlite:///schools.db')

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

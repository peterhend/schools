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
    schools = relationship('School')

    # Serialize function to send JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'name': self.name,
            'superintendent': self.superintendent,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip': self.zip,
            'phone': self.phone,
            'schools': self.serialize_schools
        }

    @property
    def serialize_schools(self):
        return [item.serialize for item in self.schools]

class School(Base):
    __tablename__ = 'school'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    principal = Column(String(250))
    address = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    zip = Column(String(50))
    phone = Column(String(50))
    district_id = Column(Integer, ForeignKey('district.id'))
    district = relationship(District)

    # Serialize function to send JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'name': self.name,
            'principal': self.principal,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip': self.zip,
            'phone': self.phone,
        }

class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=False)
    address = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    zip = Column(String(50))
    phone = Column(String(50))
    email = Column(String(50))
    school_id = Column(Integer, ForeignKey('school.id'))
    school = relationship(School)
    sections = relationship('Section', secondary='enrollment')

    # Serialize function to send JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip': self.zip,
            'phone': self.phone,
        }

class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=False)
    address = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    zip = Column(String(50))
    phone = Column(String(50))
    email = Column(String(50))
    school_id = Column(Integer, ForeignKey('school.id'))
    school = relationship(School)

    # Serialize function to send JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip': self.zip,
            'phone': self.phone,
        }

class Section(Base):
    __tablename__ = 'section'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    school_id = Column(Integer, ForeignKey('school.id'))
    school = relationship(School)
    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    teacher = relationship(Teacher)
    students = relationship('Student', secondary='enrollment')

    # Serialize function to send JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'name': self.name,
            'teacher_first_name': self.teacher.first_name,
            'teacher_last_name': self.teacher.last_name,
        }

class Enrollment(Base):
    __tablename__ = 'enrollment'

    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey('section.id'))
    section = relationship(Section)
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship(Student)

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schools.db')
engine = create_engine('sqlite:///' + db_path)
#engine = create_engine('sqlite:///schools.db')

#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

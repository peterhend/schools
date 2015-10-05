from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, District, School, Student, Teacher, Section, Enrollment

engine = create_engine('sqlite:///schools.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

session.query(District).delete()
session.query(School).delete()
session.query(Student).delete()

# Haldane
district1 = District(
    name="Haldane Central School District",
    superintendent="Diana Bowers",
    address="15 Craigside Drive",
    city="Cold Spring",
    state="NY",
    zip="10516",
    phone="(845) 265-9254")
session.add(district1)
session.commit()

school1 = School(name="Haldane Elementary School", principal="Brent Harrington", district=district1)
session.add(school1)
session.commit()

school2 = School(name="Haldane Middle School", principal="Julia Sniffen", district=district1)
session.add(school2)
session.commit()

school3 = School(name="Haldane High School", principal="Brian Alm", district=district1)
session.add(school3)
session.commit()

student1 = Student(first_name="James", last_name="Franco", school=school1)
session.add(student1)
session.commit()

student2 = Student(first_name="Cameron", last_name="Diaz", school=school1)
session.add(student2)
session.commit()

student3 = Student(first_name="Sean", last_name="Connery", school=school1)
session.add(student3)
session.commit()

student4 = Student(first_name="Peter", last_name="Frampton", school=school2)
session.add(student4)
session.commit()

student5 = Student(first_name="Mick", last_name="Jagger", school=school2)
session.add(student5)
session.commit()

student6 = Student(first_name="Pete", last_name="Townsend", school=school2)
session.add(student6)
session.commit()

student7 = Student(first_name="Peter", last_name="Henderson", school=school3)
session.add(student7)
session.commit()

student8 = Student(first_name="Cameron", last_name="Henderson", school=school3)
session.add(student8)
session.commit()

student9 = Student(first_name="Nancy", last_name="Von Rosk", school=school3)
session.add(student9)
session.commit()

teacher1 = Teacher(first_name="Kathy", last_name="Battersby", school=school1)
session.add(teacher1)
session.commit()

teacher2 = Teacher(first_name="Judy", last_name="Finehirsh", school=school1)
session.add(teacher2)
session.commit()

teacher3 = Teacher(first_name="Jennifer", last_name="Windells", school=school1)
session.add(teacher3)
session.commit()

teacher4 = Teacher(first_name="Jeff", last_name="Sniffen", school=school2)
session.add(teacher4)
session.commit()

teacher5 = Teacher(first_name="PJ", last_name="Keiding", school=school2)
session.add(teacher5)
session.commit()

teacher6 = Teacher(first_name="Katelyn", last_name="Yen", school=school2)
session.add(teacher6)
session.commit()

teacher7 = Teacher(first_name="Bob", last_name="Mack", school=school3)
session.add(teacher7)
session.commit()

teacher8 = Teacher(first_name="Nancy", last_name="Martinez", school=school3)
session.add(teacher8)
session.commit()

teacher9 = Teacher(first_name="Eric", last_name="Richter", school=school3)
session.add(teacher9)
session.commit()

section1 = Section(name="Grade 1", school=school1, teacher=teacher2)
session.add(section1)
session.commit()

section2 = Section(name="Grade 4", school=school1, teacher=teacher3)
session.add(section2)
session.commit()

section3 = Section(name="Grade 5", school=school1, teacher=teacher1)
session.add(section3)
session.commit()

section4 = Section(name="Math 8", school=school2, teacher=teacher5)
session.add(section4)
session.commit()

section5 = Section(name="English 8", school=school2, teacher=teacher4)
session.add(section5)
session.commit()

section6 = Section(name="Science 8", school=school2, teacher=teacher6)
session.add(section6)
session.commit()

section7 = Section(name="Physics", school=school3, teacher=teacher7)
session.add(section7)
session.commit()

section8 = Section(name="AP English Language", school=school3, teacher=teacher9)
session.add(section8)
session.commit()

section9 = Section(name="AP English Literature", school=school3, teacher=teacher8)
session.add(section9)
session.commit()

enrollment = Enrollment(section=section9, student=student7)
session.add(enrollment)
session.commit()

enrollment = Enrollment(section=section9, student=student8)
session.add(enrollment)
session.commit()

enrollment = Enrollment(section=section9, student=student9)
session.add(enrollment)
session.commit()

enrollment = Enrollment(section=section7, student=student1)
session.add(enrollment)
session.commit()

enrollment = Enrollment(section=section7, student=student2)
session.add(enrollment)
session.commit()

enrollment = Enrollment(section=section7, student=student3)
session.add(enrollment)
session.commit()


print "Added %s" % district1.name
students = session.query(Student).filter_by(last_name='Von Rosk').all()
print(students)

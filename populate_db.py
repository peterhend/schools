import csv
import random
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, District, School, Student, Teacher, Section, Enrollment

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schools.db')
engine = create_engine('sqlite:///' + db_path)
#engine = create_engine('sqlite:///schools.db')
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
session.query(Teacher).delete()
session.query(Section).delete()
session.query(Enrollment).delete()

district1 = District(
    name="Craigside School District",
    superintendent="Clarence West",
    address="15 Craigside Drive",
    city="New York",
    state="NY",
    zip="10002",
    phone="(646) 784-9230")
session.add(district1)
session.commit()

school1 = School(
    name="Craigside Elementary School",
    type="ES",
    principal="Catherine Cook",
    address="15 Craigside Drive",
    city="New York",
    state="NY",
    zip="10002",
    phone="(646) 784-9254",
    district=district1)
session.add(school1)

school2 = School(
    name="Craigside Middle School",
    type="MS",
    principal="Adam Reed",
    address="15 Craigside Drive",
    city="New York",
    state="NY",
    zip="10002",
    phone="(646) 784-2314",
    district=district1)
session.add(school2)

school3 = School(
    name="Craigside High School",
    type="HS",
    principal="Angela Lopez",
    address="15 Craigside Drive",
    city="New York",
    state="NY",
    zip="10002",
    phone="(646) 784-8034",
    district=district1)
session.add(school3)

schools = [school1, school2, school3]
es_departments = ["Kindergarten", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Art & Music"]
hs_departments = ["English", "Mathematics", "Social Studies", "Foreign Language", "Science", "Art & Music", "Physical Education", "Home & Careers"]
es_grades = ["K", 1, 2, 3, 4, 5]
ms_grades = [6, 7, 8]
hs_grades = [9, 10, 11, 12]

with open('student_data.csv', 'rb') as f:
    reader = csv.reader(f)
    data = list(reader)

for i in data:
    school = random.choice(schools)
    if (school.type == "ES"):
        grade = random.choice(es_grades)
    elif (school.type == "MS"):
        grade = random.choice(ms_grades)
    elif (school.type == "HS"):
        grade = random.choice(hs_grades)
    student = Student(
        first_name = i[1],
        last_name = i[2],
        email = i[3],
        address = i[4],
        city = i[5],
        state = i[6],
        zip = i[7],
        phone = i[8][2:],
        grade = grade,
        school = school
    )
    session.add(student)
session.commit()
print "Added students"
    
with open('teacher_data.csv', 'rb') as f:
    reader = csv.reader(f)
    data = list(reader)

for i in data:
    school = random.choice(schools)
    if (school.type == "ES"):
        department = random.choice(es_departments)
    elif (school.type == "MS"):
        department = random.choice(hs_departments)
    elif (school.type == "HS"):
        department = random.choice(hs_departments)
    teacher = Teacher(
        first_name = i[1],
        last_name = i[2],
        department = department,
        email = i[3],
        address = i[4],
        city = i[5],
        state = i[6],
        zip = i[7],
        phone = i[8][2:],
        school = school
    )
    session.add(teacher)
session.commit()
print "Added teachers"

with open('section_data.csv', 'rb') as f:
    reader = csv.reader(f)
    data = list(reader)
teachers = session.query(Teacher).filter_by(school_id=3).all()
teacher_count = len(teachers)
counter = 0
for i in data:
    if (i[2] == "ES"):
        school = schools[0]
    if (i[2] == "MS"):
        school = schools[1]
    if (i[2] == "HS"):
        school = schools[2]
    section = Section(
        name = i[1],
        teacher = teachers[counter%teacher_count],
        school = school
    )
    session.add(section)
    counter += 1
session.commit()
print "Added HS sections"

students = session.query(Student).filter_by(school_id=3).order_by(Student.address).all()
student_count = len(students)
counter = 0
for i in range(0, session.query(Section).count()):
    section = session.query(Section).filter_by(id=i+1).one()
    for j in range(0, 20):
        enrollment = Enrollment(
            section = section,
            student = students[counter%student_count]
        )
        session.add(enrollment)
        counter += 1
session.commit()
print "Added enrollments"

print "Added %s" % district1.name

session.close()

import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, Markup
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, District, School, Student, Teacher, Section, Enrollment, HelpTopic

app = Flask(__name__)
bootstrap = Bootstrap(app)

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schools.db')
engine = create_engine('sqlite:///' + db_path)
#engine = create_engine('sqlite:///schools.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/') 
@app.route('/districts')
def showDistricts():
    districts = session.query(District).all()
    return render_template('districts.html', districts=districts)

@app.route('/help')
def helpTopics():
    helpTopics = session.query(HelpTopic).order_by(HelpTopic.help_id)
    return render_template('help.html', helpTopics=helpTopics)

@app.route('/help/new', methods=['GET', 'POST'])
def newHelpTopic():
    if request.method == 'POST':
        newTopic = HelpTopic(
            help_id=request.form['help_id'],
            window=request.form['window'],
            element=request.form['element'],
            text=request.form['text']
            )
        session.add(newTopic)
        session.commit()
        return redirect(url_for('helpTopics'))
    else:
        pages = os.listdir("templates")
        return render_template('newhelptopic.html', pages=pages)

@app.route('/help/<int:help_id>/edit', methods=['GET', 'POST'])
def editHelpTopic(help_id):
    topic = session.query(HelpTopic).filter_by(id=help_id).one()
    if request.method == 'POST':
        if request.form['submit'] == 'Save':
            if request.form['help_id']:
                topic.help_id = request.form['help_id']
            if request.form['window']:
                topic.window = request.form['window']
            if request.form['element']:
                topic.element = request.form['element']
            if request.form['text']:
                topic.text = request.form['text']
            session.add(topic)
            session.commit()
        elif request.form['submit'] == 'Delete':
            session.delete(topic)
            session.commit()
        return redirect(url_for('helpTopics'))
    else:
        pages = os.listdir("templates")
        return render_template('edithelptopic.html', topic=topic, pages=pages)

@app.route('/districts/new', methods=['GET', 'POST'])
def newDistrict():
    if request.method == 'POST':
        newDistrict = District(
            name=request.form['name'],
            superintendent=request.form['superintendent'],
            address=request.form['address'],
            city=request.form['city'],
            state=request.form['state'],
            zip=request.form['zip'],
            phone=request.form['phone']
            )
        session.add(newDistrict)
        session.commit()
        return redirect(url_for('showDistricts'))
    else:
        helpTopics = session.query(HelpTopic).filter_by(window="editdistrict.html").all()
        helpDict = {}
        for topic in helpTopics:
            helpDict[topic.help_id] = [topic.element, topic.text]
        return render_template('newdistrict.html', helpTopics=helpDict)

@app.route('/districts/<int:district_id>/edit', methods=['GET', 'POST'])
def editDistrict(district_id):
    district = session.query(District).filter_by(id=district_id).one()
    if request.method == 'POST':
        if request.form['name']:
            district.name = request.form['name']
        if request.form['superintendent']:
            district.superintendent = request.form['superintendent']
        if request.form['address']:
            district.address = request.form['address']
        if request.form['city']:
            district.city = request.form['city']
        if request.form['state']:
            district.state = request.form['state']
        if request.form['zip']:
            district.zip = request.form['zip']
        if request.form['phone']:
            district.phone = request.form['phone']
        session.add(district)
        session.commit()
        return redirect(url_for('showDistricts'))
    else:
        helpTopics = session.query(HelpTopic).filter_by(window="editdistrict.html").all()
        helpDict = {}
        for topic in helpTopics:
            helpDict[topic.help_id] = [topic.element, topic.text]
        return render_template('editdistrict.html', helpTopics=helpDict, district=district)

@app.route('/districts/<int:district_id>/delete', methods=['GET', 'POST'])
def deleteDistrict(district_id):
    district = session.query(District).filter_by(id=district_id).one()
    if request.method == 'POST':
        session.delete(district)
        session.commit()
        return redirect(url_for('showDistricts'))
    else:
        return render_template('deletedistrict.html', item=district)

@app.route('/districts/<int:district_id>/')
def showDistrict(district_id):
    #Display all schools within selected district
    district = session.query(District).filter_by(id=district_id).one()
    schools = session.query(School).filter_by(district_id=district_id).all()
    return render_template('district.html', schools=schools, district=district)

# JSON API ENDPOINT
@app.route('/districts/<int:district_id>/JSON')
def districtJSON(district_id):
    district = session.query(District).filter_by(id=district_id).one()
    return jsonify(District=district.serialize) 

@app.route('/districts/<int:district_id>/new', methods=['GET', 'POST'])
def newSchool(district_id):
    #Create new school within selected district
    if request.method == 'POST':
        newSchool = School(name=request.form['name'], principal=request.form['principal'], district_id=district_id)
        session.add(newSchool)
        session.commit()
        return redirect(url_for('showSchools', district_id=district_id))
    else:
        return render_template('newschool.html', district_id=district_id)


@app.route('/districts/<int:district_id>/<int:school_id>/edit', methods=['GET', 'POST'])
def editSchool(district_id, school_id):
    #return "Page to edit a school"
    school = session.query(School).filter_by(id=school_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['principal']:
            editedItem.description = request.form['principal']
        session.add(school)
        session.commit()
        return redirect(url_for('showSchools', district_id=district_id))
    else:
        return render_template(
            'editschool.html', district_id=district_id, school_id=school_id, item=school)


@app.route('/districts/<int:district_id>/schools/<int:school_id>/delete', methods=['GET', 'POST'])
def deleteSchool(district_id, school_id):
    #return "Page to delete a school"
    school = session.query(School).filter_by(id=school_id).one()
    if request.method == 'POST':
        session.delete(school)
        session.commit()
        return redirect(url_for('showSchools', district_id=district_id))
    else:
        return render_template('deleteschool.html', item=school)

@app.route('/districts/<int:district_id>/schools/<int:school_id>/')
def showSchool(district_id, school_id):
    school = session.query(School).filter_by(id=school_id).one()
    students = session.query(Student).filter_by(school_id=school_id).all()
    teachers = session.query(Teacher).filter_by(school_id=school_id).all()
    sections = session.query(Section).filter_by(school_id=school_id).all()
    return render_template('school.html', district_id=district_id, school=school, students=students, teachers=teachers, sections=sections)

# JSON API ENDPOINT
@app.route('/districts/<int:district_id>/schools/<int:school_id>/JSON')
def schoolJSON(district_id, school_id):
    school = session.query(School).filter_by(id=school_id).one()
    return jsonify(School=school.serialize) 

# JSON API ENDPOINT
@app.route('/districts/<int:district_id>/schools/JSON')
def allSchoolsJSON(district_id):
    schools = session.query(School).filter_by(district_id=district_id).all()
    return jsonify(Schools=[school.serialize for school in schools]) 

@app.route('/districts/<int:district_id>/schools/<int:school_id>/students')
def showAllStudents(district_id, school_id):
    school = session.query(School).filter_by(id=school_id).one()
    students = session.query(Student).filter_by(school_id=school_id).all()
    return render_template('students.html', district_id=district_id, school=school, students=students)

# JSON API ENDPOINT
@app.route('/districts/<int:district_id>/schools/<int:school_id>/students/JSON')
def allStudentsJSON(district_id, school_id):
    students = session.query(Student).filter_by(school_id=school_id).all()
    return jsonify(Students=[student.serialize for student in students]) 

@app.route('/districts/<int:district_id>/schools/<int:school_id>/sections/<int:section_id>/')
def showSection(district_id, school_id, section_id):
    section = session.query(Section).filter_by(id=section_id).one()
    teacher = session.query(Teacher).filter_by(id=section.teacher_id).one()
    students = section.students
    return render_template('section.html',
                           district_id=district_id,
                           school_id=school_id,
                           section=section,
                           teacher=teacher,
                           students=students)

@app.route('/districts/<int:district_id>/schools/<int:school_id>/sections')
def showAllSections(district_id, school_id):
    school = session.query(School).filter_by(id=school_id).one()
    sections = session.query(Section).filter_by(school_id=school_id).all()
    return render_template('sections.html', district_id=district_id, school=school, sections=sections)

# JSON API ENDPOINT
@app.route('/districts/<int:district_id>/schools/<int:school_id>/sections/JSON')
def allSectionsJSON(district_id, school_id):
    sections = session.query(Section).filter_by(school_id=school_id).all()
    return jsonify(Sections=[section.serialize for section in sections]) 

# JSON API ENDPOINT
@app.route('/districts/<int:district_id>/schools/<int:school_id>/sections/<int:section_id>/students/JSON')
def studentsInSectionJSON(district_id, school_id, section_id):
    section = session.query(Section).filter_by(id=section_id).one()
    students = section.students
    return jsonify(Students=[student.serialize for student in students]) 

@app.route('/districts/<int:district_id>/schools/<int:school_id>/students/<int:student_id>/')
def showStudent(district_id, school_id, student_id):
    student = session.query(Student).filter_by(id=student_id).one()
    sections = student.sections
    return render_template('student.html',
                           district_id=district_id,
                           school_id=school_id,
                           student=student,
                           sections=sections)

@app.route('/districts/<int:district_id>/schools/<int:school_id>/teachers/<int:teacher_id>/')
def showTeacher(district_id, school_id, teacher_id):
    teacher = session.query(Teacher).filter_by(id=teacher_id).one()
    sections = session.query(Section).filter_by(teacher_id=teacher_id)
    return render_template('teacher.html',
                           district_id=district_id,
                           school_id=school_id,
                           teacher=teacher,
                           sections=sections)

@app.route('/districts/<int:district_id>/schools/<int:school_id>/teachers')
def showAllTeachers(district_id, school_id):
    school = session.query(School).filter_by(id=school_id).one()
    teachers = session.query(Teacher).filter_by(school_id=school_id).all()
    return render_template('teachers.html', district_id=district_id, school=school, teachers=teachers)

# JSON API ENDPOINT
@app.route('/districts/<int:district_id>/schools/<int:school_id>/teachers/JSON')
def allTeachersJSON(district_id, school_id):
    teachers = session.query(Teacher).filter_by(school_id=school_id).all()
    return jsonify(Teachers=[teacher.serialize for teacher in teachers]) 


if __name__ == '__main__':
    app.debug = True
    app.run()

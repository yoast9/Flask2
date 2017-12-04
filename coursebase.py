import os
from flask import Flask, session, render_template, request, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess secure key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# setup SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)


# define database tables
class Professor(db.Model):
    __tablename__ = 'professors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    department = db.Column(db.Text)
    courses = db.relationship('Course', backref='professor', cascade="delete")


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    title = db.Column(db.String(256))
    description = db.Column(db.Text)
    professor_id = db.Column(db.Integer, db.ForeignKey('professors.id'))


@app.route('/')
def index():
    # return HTML
    # return "<h1>this is the index page!<h1>"
    return render_template('index.html')


@app.route('/professors')
def show_all_professors():
    professors = Professor.query.all()
    return render_template('professor-all.html', professors=professors)


@app.route('/professor/add', methods=['GET', 'POST'])
def add_professors():
    if request.method == 'GET':
        return render_template('professor-add.html')
    if request.method == 'POST':
        # get data from the form
        name = request.form['name']
        department = request.form['department']

        # insert the data into the database
        professor = Professor(name=name, department=department)
        db.session.add(professor)
        db.session.commit()
        return redirect(url_for('show_all_professors'))


@app.route('/professor/edit/<int:id>', methods=['GET', 'POST'])
def edit_professor(id):
    professor = Professor.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('professor-edit.html', professor=professor)
    if request.method == 'POST':
        # update data based on the form data
        professor.name = request.form['name']
        professor.department = request.form['department']
        # update the database
        db.session.commit()
        return redirect(url_for('show_all_professors'))


@app.route('/professor/delete/<int:id>', methods=['GET', 'POST'])
def delete_professor(id):
    professor = Professor.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('professor-delete.html', professor=professor)
    if request.method == 'POST':
        # delete the artist by id
        # all related songs are deleted as well
        db.session.delete(professor)
        db.session.commit()
        return redirect(url_for('show_all_professors'))


@app.route('/api/professor/<int:id>', methods=['DELETE'])
def delete_ajax_artist(id):
    professor = Professor.query.get_or_404(id)
    db.session.delete(professor)
    db.session.commit()
    return jsonify({"id": str(professor.id), "name": professor.name})


# song-all.html adds song id to the edit button using a hidden input
@app.route('/courses')
def show_all_courses():
    courses = Course.query.all()
    return render_template('course-all.html', courses=courses)


@app.route('/course/add', methods=['GET', 'POST'])
def add_courses():
    if request.method == 'GET':
        professors = Professor.query.all()
        return render_template('course-add.html', professors=professors)
    if request.method == 'POST':
        # get data from the form
        number = request.form['number']
        title = request.form['title']
        description = request.form['description']
        professor_name = request.form['professor']
        professor = Professor.query.filter_by(name=professor_name).first()
        course = Course(number=number, title=title, description=description, professor=professor)

        # insert the data into the database
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('show_all_courses'))


@app.route('/course/edit/<int:id>', methods=['GET', 'POST'])
def edit_course(id):
    course = Course.query.filter_by(id=id).first()
    professors = Professor.query.all()
    if request.method == 'GET':
        return render_template('course-edit.html', course=course, professors=professors)
    if request.method == 'POST':
        # update data based on the form data
        course.number = request.form['number']
        course.title = request.form['title']
        course.description = request.form['description']
        professor_name = request.form['professor']
        professor = Professor.query.filter_by(name=professor_name).first()
        course.professor = professor
        # update the database
        db.session.commit()
        return redirect(url_for('show_all_courses'))


@app.route('/course/delete/<int:id>', methods=['GET', 'POST'])
def delete_course(id):
    course = Course.query.filter_by(id=id).first()
    professors = Professor.query.all()
    if request.method == 'GET':
        return render_template('course-delete.html', course=course, professors=professors)
    if request.method == 'POST':
        # use the id to delete the song
        # song.query.filter_by(id=id).delete()
        db.session.delete(course)
        db.session.commit()
        return redirect(url_for('show_all_courses'))


@app.route('/api/course/<int:id>', methods=['DELETE'])
def delete_ajax_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({"id": str(course.id), "name": course.number})


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/users')
def show_all_users():
    return render_template('user-all.html')


@app.route('/form-demo', methods=['GET', 'POST'])
def form_demo():
    # how to get form data is different for GET vs. POST
    if request.method == 'GET':
        first_name = request.args.get('first_name')
        if first_name:
            return render_template('form-demo.html', first_name=first_name)
        else:
            return render_template('form-demo.html', first_name=session.get('first_name'))
    if request.method == 'POST':
        session['first_name'] = request.form['first_name']
        # return render_template('form-demo.html', first_name=first_name)
        return redirect(url_for('form_demo'))


@app.route('/user/<string:name>/')
def get_user_name(name):
    # return "hello " + name
    # return "Hello %s, this is %s" % (name, 'administrator')
    return render_template('user.html', name=name)


@app.route('/song/<int:id>/')
def get_song_id(id):
    # return "This song's ID is " + str(id)
    return "Hi, this is %s and the song's id is %d" % ('administrator', id)


# https://goo.gl/Pc39w8 explains the following line
if __name__ == '__main__':

    # activates the debugger and the reloader during development
    # app.run(debug=True)
    app.run()

    # make the server publicly available on port 80
    # note that Ports below 1024 can be opened only by root
    # you need to use sudo for the following conmmand
    # app.run(host='0.0.0.0', port=80)

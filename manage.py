from flask_script import Manager
from songbase import app, db, Professor, Course

manager = Manager(app)


# reset the database and create some initial data
@manager.command
def deploy():
    db.drop_all()
    db.create_all()
    Harry = Professor(name='Harry', department='Accounting & MIS')
    Professor_Hubert = Professor(name='Professor Hubert', department='Mathematics')
    Skip = Professor(name='Skip', department='Accounting & MIS')
    Professor_Davis = Professor(name="Professor Davis", department= "Finance")
    course1 = Course(number='MISY350', title="Application Development", description= "JS,CSS,HTML,GitHub,Python", professor=Harry)
    course2 = Course(number='BUAD447', title="Data Analysis Quality Control", description="Statistical approach to operation management", professor=Professor_Hubert)
    course3 = Course(number='BUAD446', title="Operations and Supply Chains", description="Learn about planning and contol in operations management", professor=Professor_Davis)
    course4 = Course(number='MISY430', title="Systems Analysis and Implementation", description="Further your knowledge in database design and application concepts", professor=Skip)
    db.session.add(Harry)
    db.session.add(Professor_Hubert)
    db.session.add(Skip)
    db.session.add(Professor_Davis)
    db.session.add(course1)
    db.session.add(course2)
    db.session.add(course3)
    db.session.add(course4)
    db.session.commit()


if __name__ == "__main__":
    manager.run()

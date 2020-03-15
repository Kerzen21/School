from flask import Flask, request, render_template
app = Flask(import_name=__name__)
from . import dao
from . import models

# Homework for 2020.03.15
# add a file web.py in school
# the file should be a flask app which does the following:
# the route /students is available and returns all students of the school!!!

#models.Student  # import models was used
#    Student         # from .models import Student was used

"""
/
/students
    /add
    /delete
    /edit
    /list
/teachers
    /add
    /delete
    /edit
    /list
/grades
    /add
    /delete
    /edit
    /list
/subjects
    /add
    /delete
    /edit
    /list
"""


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", my_variable="1024")


@app.route("/students", methods=["GET"])
def students_handle():
    return render_template("students/index.html")






#### Homework!!!
# 1.  in list student, consider that you can
# Firstname: <student.firstname>
# Lastname: <student.lastname>
# ...
# 2. Read how to set default values in html input fields
# define the resource /students/edit, that allow to edit the first student!!!



@app.route("/students/list", methods=["GET"])
def student_list():
    all_students = dao.StudentDAO.get_all()   #-->No IF and Else needed // request(ed).Method 
    #return str(all_students)                  #only allows given methods to be used!
    return render_template("students/list.html", students=all_students, student=student[0])





@app.route("/students/add", methods=["GET", "POST"])
def student_add():
    if request.method == "GET": 
        return render_template("students/add.html")
    else:
        student_firstname = request.form.get("first", "")
        student_lastname = request.form.get("last", "")
        student_birthyear = request.form.get("birth", "")
        student = models.Student(student_firstname, student_lastname, student_birthyear)
        return "Student wurde erstellt!" 
        

if __name__ == "__main__":
    app.run(threaded=False, processes=1, debug=True)

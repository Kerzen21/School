from flask import Flask, request, render_template, redirect, url_for, flash, session
from functools import wraps
app = Flask(import_name=__name__)
from . import models
from . import dao
import random
import string
import os
def randomString(stringLength=20):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

env = os.environ

# app.config["SECRET_KEY"] = "password"
key = "SCHOOL_SECRET_KEY"

## start init
app.config["SECRET_KEY"] = randomString()
if key in env:
    if env[key] != "":
        app.config["SECRET_KEY"] = env[key]
## end init






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



def get_hash(message):
    base = 31
    for c in message:
        base *= ord(c)
    
    base %= 1000000000
    return str(base)


admin_pwd = os.environ.get("ADMIN_PASSWORD")
logindata = dict()
if admin_pwd:
    logindata["Tim"] = get_hash(admin_pwd)
# MD5
# SHA-1
print(logindata)


LOGGED_IN_KEY = "IS_LOGGED_IN"


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username in logindata:
            if logindata[username] == get_hash(password):
                flash("Login succesfull")
                session[LOGGED_IN_KEY] = True
                print(request.args, "but going back to the homepage")
                next_url = request.args.get("next", "/")
                # if next is not None:
                #     return redirect(request.args["next"])
                return redirect(next_url)
            else:
                flash("Username or Password invalid")
        else:
            flash("Username or Password invalid")
        return redirect(url_for("login", **request.args))



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get(LOGGED_IN_KEY, False):
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function



@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html", my_variable="1024")

@app.route("/grades", methods=["GET"])
@login_required
def grades_handle():
    return render_template("grades/index.html")

@app.route("/grades/edit", methods=["GET", "POST"]) #Speichert edited als neue Grade
@login_required
def grade_edit():
    gradeid = request.args.get("id")
    print(gradeid)
    if request.method == "GET":
        return render_template("grades/edit.html", grade=dao.GradeDAO.get(gradeid))
    else: 
        print(gradeid, "2.")
        subjectid = request.form.get("subjid", "")
        studentid = request.form.get("sdtid", "")
        grade_grade = request.form.get("grade", "")
        grade = models.Grade(subjectid, studentid, grade_grade,gradeid)
        dao.GradeDAO.save(grade)
        flash(f"The grade with id <{gradeid}> has been edited!") 
        return redirect("/grades/list")

@app.route("/grades/delete")       #PLS Explain Put!!! and patch https://developer.mozilla.org/de/docs/Web/HTTP/Methods
@login_required
def grades_delete():
    gradeid = request.args.get("id")
    if 'confirmation' in request.args:
        grade = dao.GradeDAO.get(gradeid)
        dao.GradeDAO.delete(grade)
        flash(f"The grade with id <{gradeid}> has been deleted!")

        return redirect("/grades/list")
    else:
        return render_template("grades/delete.html", gradeid=gradeid)

@app.route("/grades/add", methods=["GET", "POST"])
@login_required
def grades_add():
    if request.method == "GET": 
        students = []
        for student in dao.StudentDAO.get_all():
            students.append(student)
            print(students)
        return render_template('grades/add.html', students=students)
    else:
        subjectid = request.form.get("subjid", "")
        studentid = request.form.get("sdtid", "")
        grade_grade = request.form.get("grade", "")
        grade = models.Grade(subjectid, studentid, grade_grade)
        dao.GradeDAO.save(grade)
        flash(f"The Grade has been added!")
        print(request.form) 
        return redirect("/grades") 

@app.route("/grades/list", methods=["GET"])
@login_required
def grade_list():
    all_grades = dao.GradeDAO.get_all()   #-->No IF and Else needed // request(ed).Method 
    #return str(all_students)                  #only allows given methods to be used!
    return render_template("grades/list.html", grades=all_grades)

#------------------------------------------

@app.route("/students/list", methods=["GET"])
@login_required
def student_list():
    all_students = dao.StudentDAO.get_all()   #-->No IF and Else needed // request(ed).Method 
    #return str(all_students)                  #only allows given methods to be used!
    return render_template("students/list.html", students=all_students)


@app.route("/students", methods=["GET"])
@login_required
def students_handle():
    return render_template("students/index.html")


@app.route("/students/add", methods=["GET", "POST"])
@login_required
def student_add():
    if request.method == "GET": 
        return render_template("students/add.html")
    else:
        student_firstname = request.form.get("first", "")
        student_lastname = request.form.get("last", "")
        student_birthyear = request.form.get("birth", "")
        student = models.Student(student_firstname, student_lastname, student_birthyear)
        dao.StudentDAO.save(student)
        flash(f"The student has been added!") 
        return redirect("/students/list") 
        




@app.route("/students/edit", methods=["GET", "POST"])       #PLS Explain Put!!! and patch https://developer.mozilla.org/de/docs/Web/HTTP/Methods
@login_required
def student_edit():
    #"/students/edit?id=1"
    studentid = request.args.get("id")
    if request.method == "GET":
        #student.studentid, student.firstname
        return render_template("students/edit.html", student=dao.StudentDAO.get(studentid))
    else: #<1: firstname lastname - 2019>
        student_id = request.form.get("id", "")
        student_firstname = request.form.get("first", "")
        student_lastname = request.form.get("last", "")
        student_birthyear = request.form.get("birth", "")
        student = models.Student(student_firstname, student_lastname, student_birthyear, student_id)
        
        dao.StudentDAO.save(student)
        flash(f"The student with id <{studentid}> has been edited!") 
        return redirect("/students/list")

@app.route("/students/delete")       #PLS Explain Put!!! and patch https://developer.mozilla.org/de/docs/Web/HTTP/Methods
@login_required
def student_delete():
    print(request.args)
    studentid = request.args.get("id")
    if 'confirmation' in request.args:
        student = dao.StudentDAO.get(studentid)
        dao.StudentDAO.delete(student)
        #return render_template("students/ist.html")
        flash(f"The student with id <{studentid}> has been deleted!")

        return redirect("/students/list")
    else:
        return render_template("students/delete.html", studentid=studentid)

@app.route("/logout")      
def logout():
     session[LOGGED_IN_KEY] = False
     return redirect("/")

### Homework
# 1. extend the grades handler with edit and delete
# 1. add the missing handlers:
#   1. teacher (add, delete, edit, list)
#   1. subject (add, delete, edit, list)
#       1. teacher id should be a from a list of available teachers
# 1. extend grades/add and grades/edit to have subjectid as a dropdown from available teachers
# 1. Subject can be added without a teacher!!!




from flask import session




    
if __name__ == "__main__":
    app.run(threaded=False, processes=1, debug=True)

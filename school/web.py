from flask import Flask, request, render_template, redirect, url_for, flash
app = Flask(import_name=__name__)
app.config["SECRET_KEY"] = "askjhdfaskdjfhaksdjfhasdkjfahsdkfjashdfjasdhf"
from . import dao
from . import models
 

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
@app.route("/grades", methods=["GET"])
def grades_handle():
    return render_template("grades/index.html")



@app.route("/grades/add", methods=["GET", "POST"])
def grades_add():
    if request.method == "GET": 
        return render_template("grades/add.html")
    else:
        subjectid = request.form.get("subjid", "")
        studentid = request.form.get("sdtid", "")
        grade_grade = request.form.get("grade", "")
        grade = models.Grade(subjectid, studentid, grade_grade)
        dao.GradeDAO.save(grade)
        flash(f"The Grade has been added!") 
        return redirect("/grades") 

@app.route("/grades/list", methods=["GET"])
def grade_list():
    all_grades = dao.GradeDAO.get_all()   #-->No IF and Else needed // request(ed).Method 
    #return str(all_students)                  #only allows given methods to be used!
    return render_template("grades/list.html", grades=all_grades)

#------------------------------------------

@app.route("/students/list", methods=["GET"])
def student_list():
    all_students = dao.StudentDAO.get_all()   #-->No IF and Else needed // request(ed).Method 
    #return str(all_students)                  #only allows given methods to be used!
    return render_template("students/list.html", students=all_students)


@app.route("/students", methods=["GET"])
def students_handle():
    return render_template("students/index.html")


@app.route("/students/add", methods=["GET", "POST"])
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




# ssh school@tube.ddns.net
# activate an the environment: env:
# source env/bin/activate

# gunicorn starten:
# gunicorn --bind :5000 school.web:app

#-->tube.ddns.net:5000



# Homework (new)
# 1. In grade/add add a dropdown menu so that the id of a student can be selected based on his full name.
# 1. In web.py, the value `app.config["SECRET_KEY"]` should absolutely not be visible in code Change the code as follows:
#     1. If the user has set an environment variable with the name "SCHOOL_SECRET_KEY" (e.g. we have been using the environment variable "FLASK_APP"),
#     then use its value. (Python documentation / Google)
#     1. Otherwise, generate a random string of at least 20 characters and use it as the secret key.






if __name__ == "__main__":
    app.run(threaded=False, processes=1, debug=True)

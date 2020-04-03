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


@app.route("/students", methods=["GET"])
def students_handle():
    return render_template("students/index.html")





@app.route("/students/list", methods=["GET"])
def student_list():
    all_students = dao.StudentDAO.get_all()   #-->No IF and Else needed // request(ed).Method 
    #return str(all_students)                  #only allows given methods to be used!
    return render_template("students/list.html", students=all_students)




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










# Homework
# 1. Show a user warning before deleting the student

# 1. Show a message where there is no items (students/teacher...): for list

# 1. Use icons/images instead of text for actions (e.g. edit, delete)



if __name__ == "__main__":
    app.run(threaded=False, processes=1, debug=True)

from . import dao
from . import models


def handle_student():
    decision_1 = int(input("""Entscheide zwischen 
    "[1] Show student"
    "[2] Add student"
    "[3] Edit student"
    "[4] Delete student"
    "[5] Show all students"
    "[6] Exit" """)) ###-> BREAK
    if decision_1 == 1:
        studentid = int(input("Student ID:"))  #Durchschnitt; Rang
        # print(dao.StudentDAO.get(studentid))
        student = dao.StudentDAO.get(studentid)
        if student is None:
            print("Dieser Student existiert nicht.")
        else:
            print(student)
            print("Average Grade:", dao.GradeDAO.get_student_average_grade(studentid))


    if decision_1 == 2:
        FN = input("Firstname: ")
        LN = input("Lastname: ")
        BY = input("Birthyear(XXXX): ")
        student = models.Student(FN, LN, BY)
        
        dao.StudentDAO.save(student)
        print(student)

    if decision_1 == 3:
        studentid = int(input("Student ID:"))
        student = dao.StudentDAO.get(studentid)
        if student is None:
            pass
        else:
            FN = input("Firstname: ")
            LN = input("Lastname: ")
            BY = input("Birthyear(XXXX): ")
            if FN != "":
                student.firstname = FN
            if LN != "":
                student.lastname = LN
            if BY != "":
                student.birth_year = BY


            dao.StudentDAO.save(student)
            print(student)


    if decision_1 == 4:                             #TODO: Funktioniert, ABER Grade wird nicht gelöscht
        studentid = int(input("Student ID:"))
        student = dao.StudentDAO.delete(studentid)
        #grade = dao.GradeDAO.delete(grade)
        if student is None:
            pass
        else:
            #print(grade)
            print(student)
        

    if decision_1 == 5:
        print(dao.StudentDAO.get_all())
        


    if decision_1 == 6:
        pass        





if __name__ == "__main__":
    handle_student()




#gui

### Homework 2019.10.27
### Define a method: "handle_student"
# # the method should propose the following options:
#     "[1] Show student"
#     "[2] Add student"
#     "[3] Edit student"
#     "[4] Delete student"
#     "[5] Show all students"
#     "[6] Exit"
# for each of the option, you should take the required input (studentid for example, or other relevant informations)
# and apply the action with the help of StudentDAO
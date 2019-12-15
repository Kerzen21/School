import sqlite3
# from models import Grade
# from models import Student
# from models import Teacher
# from models import Subject

from .models import Grade, Student, Teacher, Subject

db_filename = "database.sqlite3"    #.db, .db3, .sqlite, .sqlite3
db_create_script = "school.sql"



# Tell the database to return results as dictionnaries
# con.row_factory = sqlite3.Row


def get_db_connection(db_filename):
    return sqlite3.connect(db_filename)



# Project: Students administration, using the previously created tables
# 1. Student: add, update, delete, show, get notes report, get student rank 
# 2. Teacher: add, update, delete                                           <-- Alleine
# 3. Note: add, update, delete, assign Teacher
# 4. Note: add, update, delete student notes


class DBManager(object):
    _con: sqlite3.Connection = None
    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        if cls._con is None:
            cls._con = get_db_connection(db_filename)

            with open(db_create_script) as school_file:
                school_script = school_file.read()

            school = cls._con.executescript(school_script)
        # check if cls._con is still valid/connect otherwise, build a new connection
        
        return cls._con
        
class DAO(object): #Data access object
    
    @classmethod
    def get(cls, id_):
        # Return the object with the corresponding id_
        pass

    @classmethod
    def get_all(cls):
        # Return all objects
        pass

    @classmethod
    def save(cls, obj):
        # save the obj into the database and update its id if required
        pass

    @classmethod
    def delete(cls, obj):
        # delete the obj from the database and set it's id to None
        pass 
    
    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        return DBManager.get_connection()

class StudentDAO(DAO):
    @classmethod
    def get(cls, studentid):
        con = cls.get_connection()
        
        res = con.execute("SELECT studentid ,firstname, lastname, birth_year FROM Students WHERE studentid=?", [studentid]).fetchone()
        if res is None:
            return None

        # print(res)
        
        firstname = res[1]
        lastname = res[2]
        birth_year = res[3]
        student = Student(studentid=studentid, firstname=firstname, lastname=lastname, birth_year=birth_year)
        return student
    
    @classmethod
    def save(cls, student:Student):
        con = cls.get_connection()
        #1 das objekt ist nicht in der DB vorhanden ==> neues Objekt (in DB)
        #2 das objekt ist vorhanden: ==> update Objekt (in DB)
        if student.studentid is None:
            # alternativ to with/con
            # con.execute("BEGIN;")
            # con.execute("INSERT INTO Student(firstname, lastname, birth_year) VALUES(?, ?, ?)", [student.firstname, student.lastname, student.birth_year])
        
            # id_row = con.execute("select last_insert_rowid()").fetchone()
            # student.studentid = id_row[0]
            # con.execute("COMMIT;")

                    #con.__enter__()
            with con:   
               
                con.execute("INSERT INTO Students(firstname, lastname, birth_year) VALUES(?, ?, ?)", [student.firstname, student.lastname, student.birth_year])
            
                id_row = con.execute("select last_insert_rowid()").fetchone()
                student.studentid = id_row[0]
                
            #con.__exit__()
        else:
            with con:
                con.execute("UPDATE Students SET firstname=?, lastname=?, birth_year=? WHERE studentid=?", [student.firstname, student.lastname, student.birth_year, student.studentid])

    @classmethod
    def delete(cls, studentid):
        con = cls.get_connection()
        with con:
            con.execute("DELETE FROM Students WHERE studentid=?", [studentid])



    @classmethod
    def get_all(cls):
        con = cls.get_connection()
        all_students=[]
        student_rows = con.execute("SELECT studentid, firstname, lastname, birth_year FROM Students").fetchall()
        
        #[(2, 'Tom', 'A', '', 2001), (3, 'Paul', 'C', None, 1998), (4, 'Arnold', 'D', None, 1997)
        for student_row in student_rows:
            #student: (2, 'Tom', 'A', '', 2001)
            studentid = student_row[0]
            firstname = student_row[1]
            lastname = student_row[2]
            birth_year = student_row[3]

            student  = Student(studentid=studentid, firstname=firstname, lastname=lastname, birth_year=birth_year)

            #print("type student: ", type(student), student) # Student 


            all_students.append(student)
        return all_students


class TeacherDAO(DAO):
    @classmethod
    def get(cls, teacherid):
        con = cls.get_connection()
        res =  con.execute("SELECT teacherid, name FROM Teachers WHERE teacherid=?", [teacherid]).fetchone()
        if res is None:
            return None

        teacherid = res[0]
        name = res[1]
        teacher = Teacher(teacherid=teacherid, name=name)
        return teacher

    @classmethod   
    def save(cls, teacher: Teacher):
        con = cls.get_connection()
        
        if teacher.teacherid is None:  #--> Insert
            #TODO: insert
            with con:
                con.execute("INSERT INTO Teachers(teacherid, name) VALUES(?, ?)", [teacher.teacherid, teacher.name])
                id_row = con.execute("SELECT last_insert_rowid()").fetchone()
                teacher.teacherid = id_row[0]
        else:
            with con:
                con.execute("UPDATE Teachers SET teacherid=?, name=? WHERE teacherid=?", [teacher.teacherid, teacher.name, teacher.teacherid])

    @classmethod
    def delete(cls, teacher):
        con = cls.get_connection()
        with con:
            con.execute("DELETE FROM Teachers WHERE teacherid=?", [teacher.teacherid])

    @classmethod
    def get_all(cls):
        con = cls.get_connection()
        all_teachers=[]
        teacher_rows = con.execute("SELECT teacherid, name FROM Teachers").fetchall()

        for teacher_row in teacher_rows:
            teacherid = teacher_row[0]
            name = teacher_row[1]

            teacher = Teacher(teacherid=teacherid, name=name)
            all_teachers.append(teacher)
        return all_teachers













class GradeDAO(DAO):
    @classmethod
    def get(cls, gradeid):
        con = cls.get_connection()
        if gradeid is None:
            return None

        
        written_note = con.execute("SELECT subjectid, studentid, grade FROM Grades WHERE gradeid=?", [gradeid]).fetchone()   ###1. Aus Welcher Tabelle ziehen wir dies Information?
        # ==> "SELECT subjectid, studentid, grade FROM Grades WHERE gradeid=10, ---> ? übernimmt den Wert in SQ-Brackets
        
        if written_note is None:
            return None
            
        subjectid = written_note[0]
        studentid = written_note[1]
        grade = written_note[2]
        
        final_grade = Grade(subjectid=subjectid, studentid=studentid, grade=grade, gradeid=gradeid)
        return final_grade


    @classmethod   
    def save(cls, grade: Grade):
        con = cls.get_connection()
        
        if grade.gradeid is None:  #--> Insert
            #TODO: insert
            with con:
                con.execute("INSERT INTO Grades(subjectid, studentid, grade) VALUES(?, ?, ?)", [grade.subjectid, grade.studentid ,grade.grade])
                id_row = con.execute("SELECT last_insert_rowid()").fetchone()
                grade.gradeid = id_row[0]
        else:
            with con:
                con.execute("UPDATE Grades SET subjectid=?, studentid=?, grade=? WHERE gradeid=?", [grade.subjectid, grade.studentid, grade.grade, grade.gradeid])
    
    @classmethod
    def get_all(cls, studentid=None):
        con = cls.get_connection()
        all_grades=[]
        if studentid is None:
            grade_rows = con.execute("SELECT gradeid, subjectid, studentid, grade FROM Grades").fetchall()
        else:
            grade_rows = con.execute("SELECT gradeid, subjectid, studentid, grade FROM Grades WHERE studentid=?", [studentid]).fetchall()


        for grade_row in grade_rows:
            gradeid = grade_row[0]
            subjectid = grade_row[1]
            studentid = grade_row[2]
            grade = grade_row[3]

            grade = Grade(gradeid=gradeid, subjectid=subjectid, studentid=studentid, grade=grade)
            all_grades.append(grade)
        return all_grades
        




    @classmethod
    def get_student_grades(cls, studentid):
        return cls.get_all(studentid=studentid)

    @classmethod
    def get_student_average_grade(cls, studentid): # (artists.artistid=albums.artistid);
        con = cls.get_connection()
        result = con.execute("""SELECT sum(grade*coef)/sum(coef) FROM Grades inner join Subjects on(Grades.subjectid=Subjects.subjectid) WHERE studentid=?""", [studentid]).fetchone()
        if result is None:
            return None
        else:
            return result[0]


    @classmethod
    def delete(cls, grade):
        con = cls.get_connection()
        with con:
            con.execute("DELETE FROM Grades WHERE gradeid=?", [grade.gradeid])   
        



class SubjectDAO(DAO):    
    @classmethod
    def get(cls, subjectid):
        con = cls.get_connection()
        if subjectid is None:
            return None

        
        written_note = con.execute("SELECT subjectid, title, teacherid, coef FROM Subjects WHERE subjectid=?", [subjectid]).fetchone()   ###1. Aus Welcher Tabelle ziehen wir dies Information?
        # ==> "SELECT subjectid, studentid, grade FROM Grades WHERE gradeid=10, ---> ? übernimmt den Wert in SQ-Brackets
        
        if written_note is None:
            return None
            
        subjectid = written_note[0]
        title = written_note[1]
        teacherid = written_note[2]
        coef = written_note[3]
        
        subject = Subject(subjectid=subjectid, title=title, teacherid=teacherid, coef=coef)
        return subject


    @classmethod   
    def save(cls, subject: Subject):
        con = cls.get_connection()
        
        if subject.subjectid is None:  #--> Insert
            #TODO: insert
            with con:
                con.execute("INSERT INTO Subjects(subjectid, title, teacherid, coef) VALUES(?, ?, ?, ?)", [subject.subjectid, subject.title, subject.teacherid, subject.coef])
                id_row = con.execute("SELECT last_insert_rowid()").fetchone()
                subject.subjectid = id_row[0]
        else:
            with con:
                con.execute("UPDATE Subjects SET subjectid=?, title=?, teacherid=?, coef=? WHERE subjectid=?", [subject.subjectid, subject.title, subject.teacherid, subject.coef, subject.subjectid])
    
    @classmethod
    def get_all(cls, subjectid=None):
        con = cls.get_connection()
        all_subjects=[]
        if subjectid is None:
            subject_rows = con.execute("SELECT subjectid, title, teacherid, coef FROM Subjects").fetchall()
        else:
            subject_rows = con.execute("SELECT subjectid, title, teacherid, coef FROM Subjects WHERE subjectid=?", [subjectid]).fetchall()

        for subject_row in subject_rows:
            subjectid = subject_row[0]
            title = subject_row[1]
            teacherid = subject_row[2]
            coef = subject_row[3]
            
            subject = Subject(subjectid=subjectid, title=title, teacherid=teacherid, coef=coef)
            all_subjects.append(subject)
            
        return all_subjects

    @classmethod
    def get_teacher_subject(cls, teacherid):
        return cls.get_all(teacherid=teacherid)


    @classmethod
    def delete(cls, subject):
        con = cls.get_connection()
        with con:
            con.execute("DELETE FROM Subjects WHERE subjectid=?", [subject.subjectid])  



    





if __name__ == "__main__":
    
    # teacher = Teacher("James Bond")
    # TeacherDAO.save(teacher)
    # print(teacher)
    # TeacherDAO.delete(teacher)

    # print(StudentDAO.get_all())
    student = Student("firstname", "lastname", 2019)
    teacher = Teacher("Lehrer A.")
    TeacherDAO.save(teacher)
    subject = Subject("Mathe", 2, teacher.teacherid)
    SubjectDAO.save(subject)
    # print(SubjectDAO.get(1))
    StudentDAO.save(student)
    grade = Grade(subject.subjectid, student.studentid, 17)
    GradeDAO.save(grade)

    print("Student avg grades: ", GradeDAO.get_student_average_grade(student.studentid))
    sid = student.studentid
    StudentDAO.delete(student.studentid)
    print("get delete student: ", StudentDAO.get(sid))
    print("Student avg grades (after): ", GradeDAO.get_student_average_grade(student.studentid))
    SubjectDAO.delete(subject)
    print("Student avg grades (after delete subject): ", GradeDAO.get_student_average_grade(student.studentid))

   
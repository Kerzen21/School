import os
import sys

#path to this file
path_to_test_dao = __file__
# path to the directory containing this file
path_to_tests = os.path.split(path_to_test_dao)[0] # return (parent_directory, file/directory)

path_to_school_project = os.path.join(path_to_tests, "..")

sys.path.append(path_to_school_project)

import unittest
from unittest.mock import patch
from unittest import mock
import sqlite3

from school import dao, models


def get_db_connection(db_filename=None):
    print("fake: get_db_connection")
    return sqlite3.connect(":memory:")


class TestDoSelect(unittest.TestCase):


    def test_fetchone(self):
        con = get_db_connection()
        res = dao.do_select(con, "select 1", fetchall=False)
        self.assertTrue(isinstance(res, tuple))

    def test_fetchall(self):
        con = get_db_connection()
        res = dao.do_select(con, "select 1", fetchall=True)
        self.assertTrue(isinstance(res, list))
        


#Hausaufgabe for 2020.02.23
# integerate the following tests in GradeDAO's integration test
# - test get_student_grades
# - test get_student_average_grade


SQL_CREATE_TABLE = "CREATE TABLE test(value TEXT, pk INTEGER, PRIMARY KEY (pk))"
@patch("school.dao.get_db_connection", get_db_connection)
class TestDoInsert(unittest.TestCase):            
    def test_do_insert(self):
        con = get_db_connection()
        #create new empty table
        con.execute(SQL_CREATE_TABLE) 
        #insert the first element into the table, which should have the pk 1
        pk = dao.do_insert(con, "INSERT INTO test(value) VALUES(?)", [2323])

        self.assertEqual(pk, 1)

@patch("school.dao.get_db_connection", get_db_connection)
class TestDoDelete(unittest.TestCase):
    def test_do_delete(self):
        con = get_db_connection()
        con.execute(SQL_CREATE_TABLE)
        
        con.execute("INSERT INTO test(value) VALUES(?)", ["Hallo Welt"])

        dao.do_delete(con, "DELETE FROM test WHERE pk=?", [1])


        res = con.execute("SELECT value FROM test WHERE pk=?", [1]).fetchone()


        self.assertIsNone(res)





@patch("school.dao.get_db_connection", get_db_connection)
class TestDBManager(unittest.TestCase):
    def setUp(self):
        dao.DBManager._con = None

    def test_get_connection(self):
        with patch("school.dao.get_db_connection", get_db_connection):
            connection = dao.DBManager.get_connection()
            connection.execute("select * from students")
            connection.execute("select * from grades")
            connection.execute("select * from teachers")
            connection.execute("select * from subjects")


@patch("school.dao.get_db_connection", get_db_connection)
class TestStudentDAO(unittest.TestCase):
    def setUp(self):
        dao.DBManager._con = None


    def test_get_student(self):
        student_values = [1, 'James', 'W.', 2019]
        studentid, firstname, lastname, birth_year = student_values
        with patch("school.dao.do_select", return_value=student_values):
            student = dao.StudentDAO.get(studentid)
            self.assertEqual(student.studentid, studentid)
            self.assertEqual(student.firstname, firstname)
            self.assertEqual(student.lastname, lastname)
            self.assertEqual(student.birth_year, birth_year)




    def test_get_student_404(self):
        with patch("school.dao.do_select", return_value=None):
            student = dao.StudentDAO.get(1) #student = None
            self.assertIsNone(student)
    
    def test_integration(self):
        with patch("school.dao.get_db_connection", get_db_connection):
            

           #Hausaufgabe for 2020.02.09
           # Implement integration tests for the remaining classes: Grade, Treacher and Subject!!!!


            student = models.Student("Max", "Mustermann", 2000)
            dao.StudentDAO.save(student)

            counter_student = len(dao.StudentDAO.get_all())
            self.assertEqual(counter_student, 1)  
        
            student_clone = dao.StudentDAO.get(student.studentid)
            self.assertEqual(student_clone, student)
            
            student2 = models.Student("Paul", "Mustermann", 3000)
            dao.StudentDAO.save(student2)
            
            student2.firstname = "Max" #change in memory
            student2.birth_year = 2000
            self.assertEqual(student, student2)

            dao.StudentDAO.save(student2) #change in the database
            self.assertIsNotNone(student.studentid)

            counter_student1 = len(dao.StudentDAO.get_all())

            delete_student_2 = student2.studentid
            dao.StudentDAO.delete(delete_student_2)

            counter_student2 = len(dao.StudentDAO.get_all())

            self.assertGreater(counter_student1, counter_student2)

@patch("school.dao.get_db_connection", get_db_connection)
class TestGradeDAO(unittest.TestCase):
    def setUp(self):
        dao.DBManager._con = None

    def test_get_grade(self):
        grade_values = [6, 2, 4, 7]
        gradeid, subjectid, studentid, grade_grade = grade_values
        with patch("school.dao.do_select", return_value=grade_values):
            grade = dao.GradeDAO.get(gradeid)  #sbjid, stdid, grd   final_grade = Grade(subjectid=subjectid, studentid=studentid, grade=grade, gradeid=gradeid)
            
            self.assertEqual(grade.gradeid, gradeid)
            self.assertEqual(grade.subjectid, subjectid)
            self.assertEqual(grade.studentid, studentid)
            self.assertEqual(grade.grade, grade_grade)
            
    def test_get_student_grades(self):
        grade_values = [[1, 2, 3, 5], [1, 3, 3, 15]]
        
        with patch("school.dao.do_select", return_value=grade_values) as do_select_mock:
            student_grades = dao.GradeDAO.get_student_grades(grade_values[0][2])
            do_select_mock.assert_called()
            self.assertEqual(len(student_grades), 2, "There should be exactly one student grade!!!")
            
     

    def test_get_student_average_grade(self):
        do_select_result = [2.7]
        
        with patch("school.dao.do_select", return_value=do_select_result) as do_select_mock:
            result = dao.GradeDAO.get_student_average_grade(1)
            do_select_mock.assert_called()
            self.assertEqual(result, do_select_result[0])
            #print(student_grades) 




    def test_integration_grade(self):
        with patch("school.dao.get_db_connection", get_db_connection):
            student = models.Student(firstname="Paul", lastname="Müller", birth_year=2000)
            dao.StudentDAO.save(student)
            
            subject1 = models.Subject(title="Math", coef=3, teacherid=1)
            dao.SubjectDAO.save(subject1)
            subject2 = models.Subject(title="English", coef=5, teacherid=1)
            dao.SubjectDAO.save(subject2)
            
            grade1 = models.Grade(subjectid=subject1.subjectid, studentid=student.studentid, grade=15)
            dao.GradeDAO.save(grade1)
            grade2 = models.Grade(subjectid=subject2.subjectid, studentid=student.studentid, grade=10)
            dao.GradeDAO.save(grade2)


            grades_res = dao.GradeDAO.get_student_grades(student.studentid)
            print(grades_res)
            self.assertEqual(grades_res, [grade1, grade2])


    
            #test get_student_grades
            #test get_student_average_grade




    def test_integration(self):
        with patch("school.dao.get_db_connection", get_db_connection):
            grade = models.Grade(7, 5, 3)
            dao.GradeDAO.save(grade)
            self.assertIsNotNone(grade.gradeid)

            counter_grade = len(dao.GradeDAO.get_all())
            self.assertEqual(counter_grade, 1)  
        
            grade_clone =  dao.GradeDAO.get(grade.gradeid)
            self.assertEqual(type(grade_clone), type(grade))
            print("Grade:", grade)
            print("Grade Clone:", grade_clone)
            self.assertEqual(grade_clone, grade)
            
            grade2 = models.Grade(7, 5, 2)
            dao.GradeDAO.save(grade2)
            self.assertIsNotNone(grade2.gradeid)

            grade2.grade = 3

            dao.GradeDAO.save(grade2)

            self.assertEqual(dao.GradeDAO.get(grade.gradeid), dao.GradeDAO.get(grade2.gradeid))

            counter_grade1 = len(dao.GradeDAO.get_all())

           

    
            dao.GradeDAO.delete(grade2) 
            grade2.gradeid = None

            

            #dao.GradeDAO.delete(grade.delete_grade_2)

            counter_grade2 = len(dao.GradeDAO.get_all())

            self.assertGreater(counter_grade1, counter_grade2)
            
            

@patch("school.dao.get_db_connection", get_db_connection)            
class TestTeacherDAO(unittest.TestCase):
    def setUp(self):
        dao.DBManager._con = None

    def test_get_teacher(self):
        teacher_values = [1, "Max Mustermann"]
        teacherid, name = teacher_values
        with patch("school.dao.do_select", return_value=teacher_values):
            teacher = dao.TeacherDAO.get(teacherid)
            self.assertEqual(teacher.teacherid, teacherid)
            self.assertEqual(teacher.name, name)
            
           
    def test_integration(self):
        with patch("school.dao.get_db_connection", get_db_connection):


            teacher = models.Teacher("Max Mustermann")
            dao.TeacherDAO.save(teacher)
            self.assertIsNotNone(teacher.teacherid)

            counter_teacher = len(dao.TeacherDAO.get_all())
            self.assertEqual(counter_teacher, 1)  
        
            teacher_clone = dao.TeacherDAO.get(teacher.teacherid)
            self.assertEqual(teacher_clone, teacher)
            
            teacher2 = models.Teacher("Tim Mustermann")
            dao.TeacherDAO.save(teacher2)
            # save(new object) vs save(update object)
            
            teacher2.name = "Max Mustermann" #change in memory
            # change in the database
            dao.TeacherDAO.save(teacher2)

            
            self.assertEqual(dao.TeacherDAO.get(teacher.teacherid), dao.TeacherDAO.get(teacher2.teacherid))
            #E sqlite3.InterfaceError: Error binding parameter 0 - probably unsupported type.
            

            #python -m pytest .
            

            counter_teacher1 = len(dao.TeacherDAO.get_all())

            dao.TeacherDAO.delete(teacher2) 
            teacher2.teacherid = None
           
            counter_teacher2 = len(dao.TeacherDAO.get_all())

            self.assertGreater(counter_teacher1, counter_teacher2)




@patch("school.dao.get_db_connection", get_db_connection)
class TestSubjectDAO(unittest.TestCase): 
    def setUp(self):
        dao.DBManager._con = None

    def test_get_subject(self):
        subject_values = [1, "Math", 2, 3]
        subjectid, title, teacherid, coef = subject_values          
        with patch("school.dao.do_select", return_value=subject_values):
            
            subject = dao.SubjectDAO.get(subjectid)

            self.assertEqual(subject.subjectid, subjectid)
            self.assertEqual(subject.title, title)
            self.assertEqual(subject.teacherid, teacherid)
            self.assertEqual(subject.coef, coef)

    def test_getall_subject_tid_none(self):
        subject_values = [1, "Math", 2, 3]
        subjectid, title, teacherid, coef = subject_values    
        all_subjects_values = [subject_values]
        with patch("school.dao.do_select", return_value= all_subjects_values):
            subjects = dao.SubjectDAO.get_all()
            
            subject = subjects[0]
            self.assertEqual(subject.subjectid, subjectid)
            self.assertEqual(subject.title, title)
            self.assertEqual(subject.teacherid, teacherid)
            self.assertEqual(subject.coef, coef)
            
    def test_get_teacher_subjects(self):
        

        teacherid = 2
        
        with patch("school.dao.do_select", return_value= []) as do_select_mock:
            dao.SubjectDAO.get_teacher_subjects(teacherid)

            do_select_mock.assert_called()
            args = do_select_mock.call_args[0] #call_args = (args, kwargs) #teacher=2, 2
            
            _, sql, params = args


            self.assertIn("teacherid=?", sql)
            self.assertEqual(params[0], teacherid)
            
    def test_save_insert(self):
        subject = models.Subject("Math", 2, 1)

        with patch("school.dao.do_insert", return_value=1) as do_insert_mock:
            dao.SubjectDAO.save(subject) #==> should call do_insert

            do_insert_mock.assert_called()
    
    def test_save_update(self):
        subject = models.Subject("Math", 2, 1, subjectid=1)
        dao.SubjectDAO.save(subject) #==> should call do_update

    def test_integration(self):
        with patch("school.dao.get_db_connection", get_db_connection):


            subject = models.Subject("English", 2.5, 1)
            dao.SubjectDAO.save(subject)


            print("All subjects: ", dao.SubjectDAO.get_all())

            counter_subject = len(dao.SubjectDAO.get_all()) #1
            self.assertEqual(counter_subject, 1)  
        
            subject_clone = dao.SubjectDAO.get(subject.subjectid)
            self.assertEqual(subject_clone, subject)
            
            subject2 = models.Subject("Math", 5, 4)
            dao.SubjectDAO.save(subject2)
            
            subject2.title = "English"
            subject2.coef = 2.5
            subject2.teacherid = 1
            # dao.SubjectDAO.save(subject2)
            # self.assertEqual(subject, subject2)

            dao.SubjectDAO.save(subject2) #change in the database
            self.assertIsNotNone(subject.subjectid)

            counter_subject1 = len(dao.SubjectDAO.get_all())

            
            dao.SubjectDAO.delete(subject2)

            counter_subject2 = len(dao.SubjectDAO.get_all())

            self.assertGreater(counter_subject1, counter_subject2)

            # subject = (1, 2, 3, 5)
            # subject.subjectid = 1
            #[subject, subject2]
            teacher_subjects = dao.SubjectDAO.get_teacher_subjects(1)  #<-- So richtig??
            self.assertEqual(teacher_subjects, [subject])





if __name__ == "__main__":
    unittest.main()
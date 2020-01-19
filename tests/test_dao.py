import unittest
from unittest.mock import patch
from unittest import mock
import sqlite3

from school import dao, models


def get_db_connection(db_filename=None):
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
        


#Hausaufgabe for 2020.01.26
# 1. Replace the old con.execute statements with the help-functions: do_select, do_insert, do_delete and do_update
# 2. Test each method of TeacherDAO, SubjectDAO, GradeDAO following the example of StudentDAO


SQL_CREATE_TABLE = "CREATE TABLE test(value TEXT, pk INTEGER, PRIMARY KEY (pk))"

class TestDoInsert(unittest.TestCase):            

    def test_do_insert(self):
        con = get_db_connection()
        #create new empty table
        con.execute(SQL_CREATE_TABLE) 
        #insert the first element into the table, which should have the pk 1
        pk = dao.do_insert(con, "INSERT INTO test(value) VALUES(?)", [2323])

        self.assertEqual(pk, 1)


class TestDoDelete(unittest.TestCase):
    def test_do_delete(self):
        con = get_db_connection()
        con.execute(SQL_CREATE_TABLE)
        
        con.execute("INSERT INTO test(value) VALUES(?)", ["Hallo Welt"])

        dao.do_delete(con, "DELETE FROM test WHERE pk=?", [1])


        res = con.execute("SELECT value FROM test WHERE pk=?", [1]).fetchone()


        self.assertIsNone(res)






class TestDBManager(unittest.TestCase):
    def test_get_connection(self):
        with patch("school.dao.get_db_connection", get_db_connection):
            connection = dao.DBManager.get_connection()
            connection.execute("select * from students")
            connection.execute("select * from grades")
            connection.execute("select * from teachers")
            connection.execute("select * from subjects")



class TestStudentDAO(unittest.TestCase):

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




class TestSubjectDAO(unittest.TestCase): 
    def test_get_subject(self):
        with patch("school.dao.SubjectDAO.get_connection") as get_connection_mock:
            subjectid, title, teacherid, coef  = [1, "Math", 2, 3]
            get_connection_mock.return_value.execute.return_value.fetchone.return_value = [subjectid, title, teacherid, coef]
            
            subject = dao.SubjectDAO.get(1)

            self.assertEqual(subject.subjectid, subjectid)
            self.assertEqual(subject.title, title)
            self.assertEqual(subject.teacherid, teacherid)
            self.assertEqual(subject.coef, coef)

    def test_getall_subject(self):
        with patch("school.dao.SubjectDAO.get_connection") as get_connection_mock:
            subjectid, title, teacherid, coef  = [1, "Math", 2, 3]
            get_connection_mock.return_value.execute.return_value.fetchall.return_value = [[subjectid, title, teacherid, coef]]
            
            subjects = dao.SubjectDAO.get_all()
            
            subject = subjects[0]
            self.assertEqual(subject.subjectid, subjectid)
            self.assertEqual(subject.title, title)
            self.assertEqual(subject.teacherid, teacherid)
            self.assertEqual(subject.coef, coef)
    
    def test_save_subject(self):
        with patch("school.dao.SubjectDAO.get_connection") as get_connection_mock:
            #get_connection_mock.assert_called_with()
            subjectid, title, teacherid, coef  = [1, "Math", 2, 3]
            #execute1 : None
            #execute2 : 1
            m_object = mock.Mock()
            m_object.fetchone.return_value = (subjectid,)
            get_connection_mock.return_value.execute.side_effect = [None, m_object]

            subject = models.Subject(title, coef, teacherid)

            dao.SubjectDAO.save(subject)

            self.assertEqual(subject.subjectid, subjectid)
            #
  




if __name__ == "__main__":
    unittest.main()
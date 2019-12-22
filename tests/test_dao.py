import unittest
from unittest.mock import patch
from unittest import mock
import sqlite3

from school import dao, models


def get_db_connection(db_filename):
    return sqlite3.connect(":memory:")


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
        with patch("school.dao.StudentDAO.get_connection") as get_connection_mock:
            get_connection_mock().execute().fetchone().__getitem__.side_effect = ['James', 'W.', 2019]

            student = dao.StudentDAO.get(1)
            self.assertEqual(student.studentid, 1)
            self.assertEqual(student.firstname, "James")
            self.assertEqual(student.lastname, "W.")
            self.assertEqual(student.birth_year, 2019)


    def test_get_student_404(self): 
        with patch("school.dao.StudentDAO.get_connection") as get_connection_mock:
            # get_connection_mock().execute().fetchone().__getitem__.side_effect = ['Test', 'T.', 2020] #20
            get_connection_mock.return_value.execute.return_value.fetchone.return_value = None

            student = dao.StudentDAO.get(1) #student = None


            self.assertIsNone(student)



# Hausaufgabe:
# 1. Schreibt einen Testfall für Student.get mit nicht vorhandenen Student

# 2. Schreibt einen Testfall für Subject.get mit vorhandenen Subject

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



# Hausaufgabe:
# 1. ersetze anweisung der art: 
# con.execute("UPDATE Subjects SET subjectid=?, title=?, teacherid=?, coef=? WHERE subjectid=?", [subject.subjectid, subject.title, subject.teacherid, subject.coef, subject.subjectid])  ##->Passiert in DAO!!!!
# durch eine neue Funktion:
# do_update(con, sql, params)
# do_insert(con, sql, params)
# do_delete(con, sql, params)
# do_select(con, sql, params) ==> return selected values...

if __name__ == "__main__":
    unittest.main()
import unittest
from unittest.mock import patch
import sqlite3

from school import dao


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




# Hausaufgabe:
# 1. Schreibt einen Testfall für Student.get mit nicht vorhandenen Student

# 2. Schreibt einen Testfall für Subject.get mit vorhandenen Subject



if __name__ == "__main__":
    unittest.main()
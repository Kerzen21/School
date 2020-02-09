class Student(object):
    def __init__(self, firstname, lastname , birth_year, studentid=None):
        self.firstname = firstname 
        self.lastname =  lastname 
        self.studentid = studentid 
        self.birth_year = birth_year
    #Student<1: Max Mustermann - 2000> != Student<2: Max Mustermann - 2000>
    def __eq__(self, other):
        #student1, student2

        # student1==student2
        # student1 == 2
        # student1.__eq__(student2)

        isinstance(1, int) # ==> True  # ist 1 ein int?
        isinstance(1, str) # ==> False # ist 1 ein str?
        if not isinstance(other, Student):
            return False
        
        return self.firstname==other.firstname and self.lastname==other.lastname and self.birth_year==other.birth_year

    def __str__(self):
        return "Student<" + str(self.studentid) + ": " + self.firstname + " " + self.lastname + " - " + str(self.birth_year) + ">"
    
    def __repr__(self):
        # representation in containers e.g. (list, set, dictionnary, tuple, ...)
        return self.__str__()


class Grade(object):  #1. Wozu Brauchen wir models(Kann mich nicht mehr errrinern : /  )?  2.Wieso brauchen wir Note in Model?
    def __init__(self, subjectid, studentid, grade, gradeid=None):
        self.subjectid = subjectid
        self.studentid = studentid
        self.gradeid = gradeid
        self.grade = grade
    def __str__(self):
        return "Grade<" + str(self.gradeid) + ": " + str(self.subjectid) + " " + str(self.studentid) + " - " + str(self.grade) + ">"
    
    def __repr__(self):
        # representation in containers e.g. (list, set, dictionnary, tuple, ...)
        return self.__str__()

class Subject(object):
    def __init__(self, title, coef, teacherid, subjectid=None):
        self.title = title
        self.coef = coef
        self.subjectid = subjectid
        self.teacherid = teacherid
    def __eq__(self, other):
        isinstance(1, int) # ==> True  # ist 1 ein int?
        isinstance(1, str) # ==> False # ist 1 ein str?
        if not isinstance(other, Subject):
            return False
        
        return self.title==other.title and self.coef==other.coef 
    def __str__(self):
        return "Subject<" + str(self.subjectid) + ": " + self.title +  ": " + str(self.teacherid) + ": " + str(self.coef) + ">"
    def __repr__(self):
        # representation in containers e.g. (list, set, dictionnary, tuple, ...)
        return self.__str__()

class Teacher(object):
    def __init__(self, name, teacherid=None):
        self.teacherid = teacherid
        self.name = name

    def __eq__(self, other):
        isinstance(1, int) # ==> True  # ist 1 ein int?
        isinstance(1, str) # ==> False # ist 1 ein str?
        if not isinstance(other, Teacher):
            return False
        
        return self.name==other.name
    def __str__(self):
        return "Teacher<" + str(self.teacherid) + ": " + self.name + ">"
    def __repr__(self):
        # representation in containers e.g. (list, set, dictionnary, tuple, ...)
        return self.__str__()
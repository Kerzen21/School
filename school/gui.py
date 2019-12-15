import dao
import models
import tkinter as tk
from tkinter import simpledialog as tk_simpledialog


#root = tk.Tk()
# canvas = tk.Canvas(root, width=500, height=500, bg="green")
# canvas.pack()
# root.title("Teacher-Editor")

class SubjectGUI(tk.Toplevel):
    def __init__(self, master=None, **kwargs):
        super().__init__( master=master, *kwargs)
        self.parent = master
        self.protocol("WM_DELETE_WINDOW", self.back_to_main_menu)

        self.action_frame = tk.Frame(self)
        self.action_frame.pack()

        self.main_frame = tk.Frame(self)
        self.main_frame.pack()

        self.output_frame = tk.Frame(self)
        self.output_frame.pack()

        self.output_label = tk.Label(self.output_frame)
        self.output_label.pack()

        
        button_show = tk.Button(self.action_frame, text='Show Subject', command=self.handle_show)
        button_show.pack()

        button_showall = tk.Button(self.action_frame, text='Show all Subjects', command=self.handle_showall) #TODO:
        button_showall.pack()

        self.button_submit = tk.Button(self.action_frame, text="Submit")

        button_edit = tk.Button(self.action_frame, text='Edit Subject', command=self.handle_edit)
        button_edit.pack()

        button_add = tk.Button(self.action_frame, text='Add Subject', command=self.handle_add)
        button_add.pack()

        button_delete = tk.Button(self.action_frame, text='Delete Subject', command=self.handle_delete)
        button_delete.pack()

        button_btmm = tk.Button(self.action_frame, text='Back to main menu', command=self.back_to_main_menu)
        button_btmm.pack()





    def handle_show(self):
        self.clear_main()
        self.output_label["text"] = ""
        self.e1 = tk.Entry(self.main_frame, text="Subject ID:")
        self.e1.pack()
        self.button_submit["command"] = self.submit_show
        self.button_submit.pack()
    def submit_show(self):
        subjectid = self.e1.get()                   
        self.e1.destroy()
        print("Subject_ID: ", subjectid)
        self.output_label["text"] = str(dao.SubjectDAO.get(subjectid))
        self.button_submit.forget()
    
    def handle_showall(self):
            self.output_label["text"] = ""
            joiner = "\n"
            a = dao.SubjectDAO.get_all()
            b = []
            for element in a:
                element = str(element)
                b.append(element)
            subjects = joiner.join(b)
            #teachers = joiner.join([str(element) for element in a])
            self.output_label["text"] = str(subjects)
    
    def handle_add(self):
        self.output_label["text"] = ""
        tk.Label(self.main_frame, text="Title: ").grid(row=0, column=0)
        self.entry_title = tk.Entry(self.main_frame)
        self.entry_title.grid(row=0, column=1)

        tk.Label(self.main_frame, text="Coef: ").grid(row=1, column=0)
        # self.entry_coef = tk.Entry(self.main_frame)   
        # self.entry_coef.grid(row=1, column=1)
        self.entry_coef = tk.Spinbox(self.main_frame, from_=1, to=128, state="readonly" )
        self.entry_coef.grid(row=1, column=1)
    

        tk.Label(self.main_frame, text="Teacher ID: ").grid(row=2, column=0)
        # self.entry_teacherid = tk.Entry(self.main_frame)   
        # self.entry_teacherid.grid(row=2, column=1)

        self.teachers = dao.TeacherDAO.get_all()
        self.lst_teacher = tk.Listbox(self.main_frame)
        for teacher in self.teachers:
            self.lst_teacher.insert(tk.END, str(teacher))
        self.lst_teacher.grid(row=2, column=1)



        self.button_submit["command"] = self.submit_add
        self.button_submit.pack()
        
    def submit_add(self):
        title = self.entry_title.get()
        self.entry_title.destroy()
        coef = self.entry_coef.get()
        self.entry_coef.destroy()
    
        # TODO: tech if curselection is empty before accessing [0]
        teacher_index = self.lst_teacher.curselection()[0]
        teacherid = self.teachers[teacher_index].teacherid
        self.lst_teacher.destroy()



        subject = models.Subject(title, coef, teacherid)    
        dao.SubjectDAO.save(subject)
        self.output_label["text"] = str(subject)
        self.button_submit.forget()

    def handle_edit(self):
        subjectid = tk_simpledialog.askstring("Subject-Edit", "Please give the Subject-ID")
        subject = dao.SubjectDAO.get(subjectid)
        if subject is not None:
            self.subject = subject
            self.output_label["text"] = ""
            tk.Label(self.main_frame, text="Title: ").grid(row=0, column=0)
            self.entry_title = tk.Entry(self.main_frame)
            self.entry_title.grid(row=0, column=1)
            self.entry_title.insert(tk.END, subject.title)

            tk.Label(self.main_frame, text="Coef: ").grid(row=1, column=0)
            coef_var = tk.IntVar(value=subject.coef)
            self.entry_coef = tk.Spinbox(self.main_frame, from_=1, to=128, state="readonly", textvariable=coef_var)
            self.entry_coef.grid(row=1, column=1)
    

            tk.Label(self.main_frame, text="Teacher ID: ").grid(row=2, column=0)
            self.teachers = dao.TeacherDAO.get_all()
            self.lst_teacher = tk.Listbox(self.main_frame)
            for idx, teacher in enumerate(self.teachers):
                self.lst_teacher.insert(tk.END, str(teacher))
                if teacher.teacherid == subject.teacherid:
                    self.lst_teacher.select_set(idx)

            self.lst_teacher.grid(row=2, column=1)



            self.button_submit["command"] = self.submit_edit
            self.button_submit.pack()
        else:
            self.output_label["text"] = "Error - Subject ID not found"

    def submit_edit(self):
        title = self.entry_title.get()
        self.entry_title.destroy()
        coef = self.entry_coef.get()
        self.entry_coef.destroy()
    
        # TODO: tech if curselection is empty before accessing [0]
        teacher_index = self.lst_teacher.curselection()[0]
        teacherid = self.teachers[teacher_index].teacherid
        self.lst_teacher.destroy()

        subject = self.subject

        if title:
            subject.title = title
        if coef:
            subject.coef = coef
        if teacherid:
            subject.teacherid = teacherid

        dao.SubjectDAO.save(subject)
        self.output_label["text"] = str(subject)
        self.button_submit.forget()

    def back_to_main_menu(self):
            self.withdraw()
            if self.parent is not None:
                self.parent.deiconify()

    def handle_delete(self):
        self.output_label["text"] = ""
        tk.Label(self.main_frame, text="Subject ID to delete ").grid(row=0, column=0)
        self.entry_subjectid = tk.Entry(self.main_frame)
        self.entry_subjectid.grid(row=0, column=1)

        #my_model.modelid == None
        
        subjectid = self.entry_subjectid.get()
        subject = dao.SubjectDAO.get(subjectid)
        if subject is None:
            self.output_label["text"] = "Subject-ID does not exist"
        else:
            dao.SubjectDAO.delete(subject)
            self.output_label["text"] = "Subject deleted"
    
    def clear_main(self):
        """
        delete all items in the main-frame
        """
        self.output_label["text"] = ""
        for child in self.main_frame.winfo_children():
            child.forget()
            child.destroy()
    
    #TODO: Save

class TeacherGUI(tk.Toplevel):
    def __init__(self, master=None, **kwargs): #keywords arguments TeacherGUI(hello=1, world=2) ==> kwargs: {hello=1, world=2}
        super().__init__( master=master, *kwargs)
        self.parent = master
        self.protocol("WM_DELETE_WINDOW", self.back_to_main_menu)

        self.action_frame = tk.Frame(self)
        self.action_frame.pack()

        self.main_frame = tk.Frame(self)
        self.main_frame.pack()

        self.output_frame = tk.Frame(self)
        self.output_frame.pack()

        self.output_label = tk.Label(self.output_frame)
        self.output_label.pack()


        button_show = tk.Button(self.action_frame, text='Show teacher', command=self.handle_show)
        button_show.pack()

        button_showall = tk.Button(self.action_frame, text='Show all teachers', command=self.handle_showall) #TODO:
        button_showall.pack()

        self.button_submit = tk.Button(self.action_frame, text="Submit")

        button_add = tk.Button(self.action_frame, text='Add teacher', command=self.handle_add)
        button_add.pack()

        button_edit = tk.Button(self.action_frame, text='Edit teacher', command=self.handle_edit)
        button_edit.pack()

        button_btmm = tk.Button(self.action_frame, text='Back to main menu', command=self.back_to_main_menu)
        button_btmm.pack()

        # self.button_submit.forget()
        


    def handle_show(self):
        self.output_label["text"] = ""
        self.e1 = tk.Entry(self.main_frame, text="Teacher ID:")
        self.e1.pack()
        self.button_submit["command"] = self.submit_show
        self.button_submit.pack()
    def submit_show(self):
        teacherid = self.e1.get()                   
        self.e1.destroy()
        print("TEACHER_ID: ", teacherid)
        self.output_label["text"] = str(dao.TeacherDAO.get(teacherid))
        self.button_submit.forget()
        
    def handle_add(self):
        self.output_label["text"] = ""
        self.add_entry = tk.Entry(self.main_frame)   
        self.add_entry.pack()
        self.button_submit["command"] = self.submit_add
        self.button_submit.pack()
    def submit_add(self):
        name = self.add_entry.get()
        self.add_entry.destroy()
        teacher = models.Teacher(name)    
        dao.TeacherDAO.save(teacher)
        self.output_label["text"] = str(teacher)
        self.button_submit.forget()
        
    def handle_showall(self):
        self.output_label["text"] = ""
        joiner = "\n"
        a = dao.TeacherDAO.get_all()
        b = []
        for element in a:
            element = str(element)
            b.append(element)
        teachers = joiner.join(b)
        #teachers = joiner.join([str(element) for element in a])
        self.output_label["text"] = str(teachers)
    
    def handle_edit(self):
        #tk_simpledialo askint, askfloat, askstring
        teacherid = tk_simpledialog.askstring("Teacher-Edit", "Please give the Teacher-ID")
        teacher = dao.TeacherDAO.get(teacherid)
        if teacher is not None:
            new_name = tk_simpledialog.askstring("Teacher-Edit", "Please state the new Name")
            if new_name != "":
                teacher.name = new_name
                dao.TeacherDAO.save(teacher)
                
            else:
                pass
            #new_name = None, new_name = ""
            # get the new name of the teacher
            # update the name of the teacher
            # save the teacher
            # show new teacher
            self.output_label["text"] = str(teacher)
        else:
            self.output_label["text"] = "Error - Teacher ID not found"
        
    def back_to_main_menu(self):
        self.withdraw()
        if self.parent is not None:
            self.parent.deiconify()


class GradeGUI(tk.Toplevel):
    def __init__(self, master=None, **kwargs): #keywords arguments TeacherGUI(hello=1, world=2) ==> kwargs: {hello=1, world=2}
        super().__init__( master=master, *kwargs)
        self.parent = master
        self.protocol("WM_DELETE_WINDOW", self.back_to_main_menu)

        self.action_frame = tk.Frame(self)
        self.action_frame.pack()

        self.main_frame = tk.Frame(self)
        self.main_frame.pack()

        self.output_frame = tk.Frame(self)
        self.output_frame.pack()

        self.output_label = tk.Label(self.output_frame)
        self.output_label.pack()


        button_show = tk.Button(self.action_frame, text='Show Grades', command=self.handle_show) #1
        button_show.pack()

        button_showall = tk.Button(self.action_frame, text='Show all Grades', command=self.handle_showall) #1
        button_showall.pack()

        self.button_submit = tk.Button(self.action_frame, text="Submit") #1

        button_edit = tk.Button(self.action_frame, text='Edit Grade', command=self.handle_edit) #TODO:
        button_edit.pack()

        #button_add = tk.Button(self.action_frame, text='Add Grade', command=self.handle_add)  
        #button_add.pack()

        button_delete = tk.Button(self.action_frame, text='Delete Grade', command=self.handle_delete)#1
        button_delete.pack()

        button_get_stndt_grades = tk.Button(self.action_frame, text='Get Students Grade', command=self.handle_get_stndt_grades)#1
        button_get_stndt_grades.pack()

        button_get_stndt_avg_grades = tk.Button(self.action_frame, text='Get Students average Grade', command=self.handle_get_stndt_avg_grades)#1
        button_get_stndt_avg_grades.pack()


        button_btmm = tk.Button(self.action_frame, text='Back to main menu', command=self.back_to_main_menu) #1
        button_btmm.pack()


    def handle_edit(self):
        self.clear_main()   
        self.output_label["text"] = ""
        self.gradeid =  tk_simpledialog.askstring("Grade-Edit", "Please give the Grade-ID")	
        self.grade = dao.GradeDAO.get(self.gradeid)
        if self.grade is not None:
            self.button_submit["command"] = self.submit_edit


            tk.Label(self.main_frame, text="Subject-ID: ").grid(row=0, column=0)
            self.subjects = dao.SubjectDAO.get_all()
            self.lst_subject = tk.Listbox(self.main_frame, exportselection=0)
            for idx, subject  in enumerate(self.subjects):
                self.lst_subject.insert(tk.END, str(subject))
                if subject.subjectid == self.grade.subjectid:
                    self.lst_subject.select_set(idx)
            self.lst_subject.grid(row=0, column=1)

            tk.Label(self.main_frame, text="Student-ID: ").grid(row=1, column=0)
            self.students = dao.StudentDAO.get_all()
            self.lst_student = tk.Listbox(self.main_frame, exportselection=0)
            for idx, student in enumerate(self.students):
                self.lst_student.insert(tk.END, str(student))
                if student.studentid == self.grade.studentid:
                    self.lst_student.select_set(idx)
            self.lst_student.grid(row=1, column=1)


            tk.Label(self.main_frame, text="Grade: ").grid(row=2, column=0)
            grade_var = tk.IntVar(value=self.grade.grade)
            self.entry_grade = tk.Spinbox(self.main_frame, from_=0, to=20, state="readonly", textvariable=grade_var)
            self.entry_grade.grid(row=2, column=1)
            self.button_submit["command"] = self.submit_edit
            self.button_submit.pack()
        else:
           self.output_label["text"] = "Grade-ID is not Valid!"

#Komme nicht weiter : /
    def submit_edit(self):
        
        subject_idx = self.lst_subject.curselection()[0]
        subject = self.subjects[subject_idx]
        self.grade.subjectid = subject.subjectid

        student_idx = self.lst_student.curselection()[0]
        student = self.students[student_idx]
        self.grade.studentid = student.studentid

        new_grade = self.entry_grade.get()
        self.grade.grade = new_grade

        self.clear_main()
        dao.GradeDAO.save(self.grade)
        self.output_label["text"] = str(self.grade)
        self.button_submit.forget()

    def handle_show(self):
        self.clear_main()
        self.output_label["text"] = ""
        self.e1 = tk.Entry(self.main_frame, text="Grade ID:")
        self.e1.pack()
        self.button_submit["command"] = self.submit_show
        self.button_submit.pack()
    def submit_show(self):
        gradeid = self.e1.get()                   
        self.e1.destroy()
        print("Grade-ID: ", gradeid)
        self.output_label["text"] = str(dao.GradeDAO.get(gradeid))
        self.button_submit.forget()

    def handle_showall(self):
            self.output_label["text"] = ""
            joiner = "\n"
            a = dao.GradeDAO.get_all()
            b = []
            for element in a:
                element = str(element)
                b.append(element)
            grades = joiner.join(b)
            #teachers = joiner.join([str(element) for element in a])
            self.output_label["text"] = str(grades)

    def handle_get_stndt_grades(self):
        self.clear_main()
        self.output_label["text"] = ""
        self.e1 = tk.Entry(self.main_frame, text="Student ID:")
        self.e1.pack()
        self.button_submit["command"] = self.submit_show
        self.button_submit.pack()
    def submit_get_stndt_grades(self):
        studentid = self.e1.get()                   
        self.e1.destroy()
        print("Student-ID: ", studentid)
        self.output_label["text"] = str(dao.GradeDAO.delete(studentid))
        self.button_submit.forget()
    
    def handle_get_stndt_avg_grades(self):
        self.clear_main()
        self.output_label["text"] = ""
        self.e1 = tk.Entry(self.main_frame, text="Student ID:")
        self.e1.pack()
        self.button_submit["command"] = self.submit_show
        self.button_submit.pack()
    def submit_get_stndt_avg_grades(self):
        studentid = self.e1.get()                   
        self.e1.destroy()
        print("Student-ID: ", studentid)
        self.output_label["text"] = str(dao.GradeDAO.delete(studentid))
        self.button_submit.forget()











    def handle_delete(self):
        self.output_label["text"] = ""
        tk.Label(self.main_frame, text="Grade ID to delete ").grid(row=0, column=0)
        self.entry_gradeid = tk.Entry(self.main_frame)
        self.entry_gradeid.grid(row=0, column=1)

        #my_model.modelid == None
        
        gradeid = self.entry_gradeid.get()
        grade = dao.GradeDAO.get(gradeid)
        if grade is None:
            self.output_label["text"] = "Grade-ID does not exist"
        else:
            dao.GradeDAO.delete(grede)
            self.output_label["text"] = "Grade deleted"

    def back_to_main_menu(self):
            self.withdraw()
            if self.parent is not None:
                self.parent.deiconify()

    def clear_main(self):
        self.output_label["text"] = ""
        for child in self.main_frame.winfo_children():
            child.forget()
            child.destroy()

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("School Management")


        tk.Button(self, text="Manage Teachers", command=self.manage_teachers).pack()
        self.teacher_gui = TeacherGUI(self)
        self.teacher_gui.withdraw()

        tk.Button(self, text="Manage Subjects", command=self.manage_subjects).pack()
        self.subject_gui = SubjectGUI(self)
        self.subject_gui.withdraw()
         
        tk.Button(self, text="Manage Grades", command=self.manage_grades).pack()
        self.grade_gui = GradeGUI(self)
        self.grade_gui.withdraw()


    def manage_teachers(self):
        self.teacher_gui.deiconify()
        self.withdraw()
        

    def manage_subjects(self):
        self.subject_gui.deiconify()
        self.withdraw()
        
    
    def manage_grades(self):
        self.grade_gui.deiconify()
        self.withdraw()

if __name__ == "__main__":
    root = GUI()
    root.mainloop()
import dao
import models
import tkinter as tk


#root = tk.Tk()
# canvas = tk.Canvas(root, width=500, height=500, bg="green")
# canvas.pack()
# root.title("Teacher-Editor")


class TeacherGUI(tk.Toplevel):
    def __init__(self, **kwargs):
        super().__init__(*kwargs)
        button_show = tk.Button(self, text='Show teacher', command=self.handle_show)
        button_show.pack()
        self.button_submit = tk.Button(self, text="Submit")
        self.button_submit.pack()
        button_add = tk.Button(self, text='Add teacher', command=self.handle_add)
        button_add.pack()
        # button_delete = tk.Button(self, text='Delete teacher', command=self.handle_delete)
        #button_get_all = tk.Button(self, text='Show all teachers', command=xx)
        # button_exit = tk.Button(self, text='EXIT', command=xx)
        self.output = tk.Frame(self)



    def handle_show(self):
        #print("show teacher")
        # Label          tk.Entry
        # Teacher ID:    [...            ...]
        self.e1 = tk.Entry(self, text="Teacher ID:")
        self.e1.pack()
        self.button_submit["command"] = self.submit_show

    def submit_show(self):
        teacherid = self.e1.get()                   #CLEAR self.output
        self.e1.destroy()
        print("TEACHER_ID: ", teacherid)
        #Label(output, ...)
        # print(dao.TeacherDAO.get(teacherid))  #LABEL erstellen dass teacher darstellt
    

    def handle_add(self):
        self.add_entry = tk.Entry(self)   
        self.add_entry.pack()
        self.button_submit["command"] = self.submit_add
    def submit_add(self):
        name = self.add_entry.get()
        self.add_entry.destroy()
        teacher = models.Teacher(name)    
        print(dao.TeacherDAO.save(teacher))

#Wie command bei Button mit eingabefeld verknüpfen?


if __name__ == "__main__":
    root = TeacherGUI()
    root.mainloop()

#Hausaufgabe:
# create the folder school with the following structure in (PythonMitFranck2.0):
#     |-cli.py
#     |-dao.py
#     |-gui.py (tli.py ==> gui.py)
#     |-models.py
#     |-school.sql

# 1. Add the folder school to the git repository and make a commit.
# 2. Push the repository to github.

#




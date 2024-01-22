import tkinter
from tkinter import *

#Criação da classe Task
class Task:
    def __init__(self, description, completed=False):
        self.description = description
        self.completed = completed

    def __str__(self):
        return f"{self.description}"
    
#Criação da classe WorkTask    
class WorkTask(Task):
    def __init__(self, description, project, completed):
        super().__init__(description, completed)
        self.project = project

    def __str__(self):
        return f"{self.description}"

#Classe da aplicação
class ToDoListApp:
  def __init__(self, master):
    self.master = master
    master.title("Tarefas a Fazer")
    master.geometry("400x650+400+100")
    master.resizable(False, False)

    self.task_list = []

    #icon
    self.Image_icon = PhotoImage(file = "Images/task.png")
    root.iconphoto(False, self.Image_icon)

    #top bar
    self.TopImage = PhotoImage(file = "Images/topbar.png")
    Label(root, image = self.TopImage).pack()

    self.dockImage = PhotoImage(file = "Images/dock.png")
    Label(root, image = self.dockImage, bg = "#32405b").place(x = 30, y = 25)

    self.noteImage = PhotoImage(file = "Images/task.png")
    Label(root, image = self.noteImage, bg = "#32405b").place(x = 340, y = 25)

    self.heading = Label(root, text = "MINHAS TAREFAS", font = "arial 20 bold", fg = "white", bg = "#32405b")
    self.heading.place(x = 75, y = 20)

    #main
    self.frame = Frame(root, width = 400, height = 50, bg = "white")
    self.frame.place(x = 0, y = 180)

    task = StringVar()
    self.task_entry = Entry(self.frame, width = 18, font = "arial 20", bd = 0)
    self.task_entry.place(x = 10, y = 7)
    self.task_entry.focus()

    self.button = Button(self.frame, text = "ADD", font = "arial 20 bold", width = 6, bg = "#D2B48C", fg = "#fff", bd = 0, command = self.addTask)
    self.button.place (x = 300, y = 0)

    #listbox
    self.frame1 = Frame(root, bd = 3, width = 700, height = 280, bg = "#32405b")
    self.frame1.pack(pady = (160, 0))

    self.listbox = Listbox(self.frame1, font = ('arial', 12), width = 40, height = 16, bg = "#32405b", fg = "white", cursor = "hand2", selectbackground = "#000080")
    self.listbox.pack(side = LEFT, fill = BOTH, padx = 2)
    self.Scrollbar = Scrollbar(self.frame1)
    self.Scrollbar.pack(side = RIGHT, fill = BOTH)

    self.listbox.config(yscrollcommand = self.Scrollbar.set)
    self.Scrollbar.config(command = self.listbox.yview)

    #delete
    self.Delete_icon = PhotoImage(file = "Images/delete.png")
    Button(root, image = self.Delete_icon, bd = 0, command = self.deleteTask).pack(side = BOTTOM, pady = 13)

    self.openTaskFile()
    
  #Função de adicionar tarefa
  def addTask(self):
    task_description = self.task_entry.get()
    self.task_entry.delete(0, END)

    if task_description:
      new_task = Task(task_description)
      with open("tasklist.txt", 'a') as taskfile:
        taskfile.write(f"\n{new_task}")
        self.task_list.append(new_task)
        self.listbox.insert( END, new_task)  

  #Função de remover tarefa
  def deleteTask(self):
    task_index = self.listbox.curselection()
    if task_index:
      task = self.task_list.pop(task_index[0])
      with open("tasklist.txt", 'w') as taskfile:
        for t in self.task_list:
          taskfile.write(str(t) + "\n")
      self.listbox.delete(task_index)

  #Função de abrir o arquivo de tarefas
  def openTaskFile(self):
    try:
      with open("tasklist.txt", "r") as taskfile:
        tasks = taskfile.readlines()

      for task in tasks:
        if task != '\n':
          self.task_list.append(Task(task.strip()))
          self.listbox.insert(END, task.strip())

    except FileNotFoundError:
      with open('tasklist.txt', 'w'):
        pass   

#execução 
if __name__ == "__main__":
    root = Tk()
    app = ToDoListApp(root)
    root.mainloop()
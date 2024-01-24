import tkinter
from tkinter import *
import json
from datetime import datetime

#Criação da classe Task
class Task:
    def __init__(self, description, completed=False):
        self.description = description
        self.completed = completed

    #Convertendo a classe em um dicionário
    def to_dict(self):
      return {"description": self.description, "completed": self.completed}

    #Cria uma instância de task a partir de um dicionário
    @classmethod
    def from_dict(cls, task_dict):
      return cls(task_dict["description"], task_dict["completed"]) 

    def __str__(self):
        return f"{self.description}"
    
#Criação da classe WorkTask    
class WorkTask(Task):
    def __init__(self, description, completed=False):
        super().__init__(description, completed)
        self.project = None

    def set_project(self, project):
      self.project = project    

    #Convertendo a classe em um dicionário
    def to_dict(self):
      task_dict = super().to_dict()
      task_dict["project"] = self.project
      return task_dict

    #Cria uma instância de worktask a partir de um dicionário
    def from_dict(cls, task_dict):
      return cls(task_dict["description"], task_dict["project"], task_dict["completed"]) 

    def __str__(self):
        return f"{self.description}"
      
class EmptyTaskDescriptionError(Exception):
    pass
  
class ValueError(Exception):
    pass

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

    self.is_work_task_var = IntVar()
    self.is_work_task_checkbox = Checkbutton(root, text="Work Task", font="arial 12", width = 8, variable=self.is_work_task_var, bg=root.cget('bg'))
    self.is_work_task_checkbox.place(x=298, y=150)

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

    if not task_description:
      raise EmptyTaskDescriptionError("A tarefa nao pode ser vazia.")
      
    if self.is_work_task_var.get() == 1:
      new_task = WorkTask(task_description)
    else:   
      new_task = Task(task_description)
    with open("tasklist.json", 'a') as taskfile:
      taskfile.write(json.dumps(new_task.to_dict()) + "\n")
      self.task_list.append(new_task)
      self.listbox.insert( END, new_task)

  #Função de remover tarefa
  def deleteTask(self):
    task_index = self.listbox.curselection()
    
    if not task_index:
        raise ValueError("Nenhuma tarefa selecionada. Selecione uma tarefa antes de excluir.")
      
    task = self.task_list.pop(task_index[0])
    with open("tasklist.json", 'w') as taskfile:
      for t in self.task_list:
        taskfile.write(json.dumps(t.to_dict()) + "\n")
    self.listbox.delete(task_index)

  #Função de abrir o arquivo de tarefas
  def openTaskFile(self):
    try:
      with open("tasklist.json", "r") as taskfile:
        tasks = taskfile.readlines()

      for task_str in tasks:
        task_dict = json.loads(task_str)
        new_task = Task.from_dict(task_dict)
        self.task_list.append(new_task)
        self.listbox.insert(END, new_task)

    except FileNotFoundError:
      with open('tasklist.json', 'w'):
        pass   

#execução 
if __name__ == "__main__":
    root = Tk()
    app = ToDoListApp(root)
    root.mainloop()
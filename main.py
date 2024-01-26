import tkinter
from tkinter import *
from tkinter import simpledialog
from tkinter import ttk
import tkinter.messagebox
import json

class Task:
    def __init__(self, description, completed=False, priority="normal"):
        self.description = description
        self.completed = completed
        self.priority = priority

    #Convertendo a classe em um dicionário
    def to_dict(self):
      return {"description": self.description, "completed": self.completed, "priority": self.priority}

    #Cria uma instância de task a partir de um dicionário
    @classmethod
    def from_dict(cls, task_dict):
      return cls(task_dict["description"], task_dict["completed"], task_dict.get("priority", "normal")) 

    def __str__(self):
        return f"{self.description} - Prioridade: {self.priority}"
 
class WorkTask(Task):
    def __init__(self, description, completed=False, priority="alta"):
        super().__init__(description, completed, priority)
        self.project = None

    def set_project(self, project):
      self.project = project    

    #Convertendo a classe em um dicionário
    def to_dict(self):
      task_dict = super().to_dict()
      task_dict["project"] = self.project
      return task_dict

    #Cria uma instância de worktask a partir de um dicionário
    @classmethod
    def from_dict(cls, task_dict):
      return cls(task_dict["description"], task_dict["completed"], task_dict.get("priority", "alta")) 

    def __str__(self):
        return f"{self.description} - Prioridade: {self.priority}"
      
class EmptyTaskDescriptionError(Exception):
    pass
  
class ValueError(Exception):
    pass

class ToDoListApp:
  def __init__(self, master):
    self.master = master
    master.title("Tarefas a Fazer")
    master.geometry("400x650+400+100")
    master.resizable(False, False)

    self.task_list = []

    self.Image_icon = PhotoImage(file = "Images/task.png")
    root.iconphoto(False, self.Image_icon)

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

    self.task_entry = Entry(self.frame, width = 18, font = "arial 20", bd = 0)
    self.task_entry.place(x = 10, y = 7)
    self.task_entry.focus()

    self.button = Button(self.frame, text = "ADD", font = "arial 20 bold", width = 6, bg = "#D2B48C", fg = "#fff", bd = 0, command = self.addTask)
    self.button.place (x = 300, y = 0)

    self.is_work_task_var = IntVar()
    self.is_work_task_checkbox = Checkbutton(root, text="Tarefas do trabalho", font="arial 11", width = 16, variable=self.is_work_task_var, bg=root.cget('bg'))
    self.is_work_task_checkbox.place(x=235, y=150)

    #lista
    self.frame1 = Frame(root, bd = 3, width = 700, height = 280, bg = "#32405b")
    self.frame1.pack(pady = (160, 0))

    self.listbox = Listbox(self.frame1, font = ('arial', 12), width = 40, height = 16, bg = "#32405b", fg = "#90EE90", cursor = "hand2", selectbackground = "#000080")
    self.listbox.pack(side = LEFT, fill = BOTH, padx = 2)
    self.Scrollbar = Scrollbar(self.frame1)
    self.Scrollbar.pack(side = RIGHT, fill = BOTH)

    self.listbox.config(yscrollcommand = self.Scrollbar.set)
    self.Scrollbar.config(command = self.listbox.yview)

    self.Delete_icon = PhotoImage(file = "Images/delete.png")
    Button(root, image = self.Delete_icon, bd = 0, command = self.deleteTask).pack(side = LEFT, padx = 20, pady = 10)

    self.Edit_icon = PhotoImage(file = "Images/edit.png")
    Button(root, image = self.Edit_icon, bd = 0, command = self.editTask).pack(side = RIGHT, padx = 20, pady = 10)

    self.openTaskFile()

  def addTask(self):
    task_description = self.task_entry.get()
    self.task_entry.delete(0, END)

    if not task_description:
        raise EmptyTaskDescriptionError("A tarefa não pode ser vazia.")

    priority = "alta" if self.is_work_task_var.get() == 1 else "normal"

    if self.is_work_task_var.get() == 1:
        new_task = WorkTask(task_description, priority=priority)
    else:
        new_task = Task(task_description, priority=priority)

    index = END
    if priority == "alta":
        index = self.find_insert_index_high_priority()
    
    self.task_list.append(new_task)
    self.listbox.insert(index, str(new_task))  # Converta a tarefa para uma string

    if isinstance(new_task, WorkTask):
        self.listbox.itemconfig(index, {'fg': '#DAA520'})
        
    with open("tasklist.json", 'a') as taskfile:
      taskfile.write(json.dumps(new_task.to_dict()) + "\n")

  def find_insert_index_high_priority(self):
    for i, task in enumerate(self.task_list):
        if isinstance(task, WorkTask) and task.priority == "alta":
            return i
    return END

  def deleteTask(self):
    task_index = self.listbox.curselection()
    
    if not task_index:
        raise ValueError("Nenhuma tarefa selecionada. Selecione uma tarefa antes de excluir.")
      
    task = self.task_list.pop(task_index[0])
    with open("tasklist.json", 'w') as taskfile:
      for t in self.task_list:
        taskfile.write(json.dumps(t.to_dict()) + "\n")
    self.listbox.delete(task_index)
  
  def editTask(self):
    task_index = self.listbox.curselection()

    if not task_index:
        raise ValueError("Nenhuma tarefa selecionada. Selecione uma tarefa antes de editar.")

    old_task = self.task_list[task_index[0]]

    edit_dialog = simpledialog.Toplevel(self.master)
    edit_dialog.title("Editar Tarefa")

    Label(edit_dialog, text="Nova Descrição:\n").pack()
    new_task_description_entry = Entry(edit_dialog, width=30)
    new_task_description_entry.insert(END, old_task.description)
    new_task_description_entry.pack()

    completed_var = IntVar()
    completed_var.set(old_task.completed)
    completed_checkbox = ttk.Checkbutton(edit_dialog, text="\nTarefa Concluída\n", variable=completed_var)
    completed_checkbox.pack()

    def save_changes():
        new_description = new_task_description_entry.get()
        old_task.description = new_description
        old_task.completed = completed_var.get()

        with open("tasklist.json", 'w') as taskfile:
            for t in self.task_list:
                taskfile.write(json.dumps(t.to_dict()) + "\n")

        self.listbox.delete(task_index)
        if old_task.completed:
            self.listbox.insert(task_index, f"{new_description}    TAREFA CONCLUÍDA")
            self.listbox.itemconfig(task_index, {'fg': 'red'})
        else:
            display_text = f"{new_description} - Prioridade: {old_task.priority}"
            self.listbox.insert(task_index, display_text)
            self.listbox.itemconfig(task_index, {'fg': '#DAA520' if isinstance(old_task, WorkTask) else '#90EE90'})    

        edit_dialog.destroy()

    save_button = Button(edit_dialog, text="Salvar", command=save_changes)
    save_button.pack()

  def openTaskFile(self):
    try:
      with open("tasklist.json", "r") as taskfile:
        tasks = taskfile.readlines()
        
      task_objects = []

      for task_str in tasks:
        task_dict = json.loads(task_str)
        if 'project' in task_dict:
          new_task = WorkTask.from_dict(task_dict)
        else:  
          new_task = Task.from_dict(task_dict)
        task_objects.append(new_task)
          
      sorted_tasks = sorted(task_objects, key=lambda x: x.priority, reverse=False)
      
      for new_task in sorted_tasks:
            self.task_list.append(new_task)
            index = END
            self.listbox.insert(END, new_task)
            if isinstance(new_task, WorkTask):
                self.listbox.itemconfig(index, {'fg': '#DAA520'})

    except FileNotFoundError:
      with open('tasklist.json', 'w'):
        pass   

if __name__ == "__main__":
    root = Tk()
    app = ToDoListApp(root)
    root.mainloop()
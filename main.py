import tkinter
from tkinter import *

root = Tk()
root.title("Tarefas a Fazer")
root.geometry("400x650+400+100")
root.resizable(False, False)

task_list = []

def openTaskFile():
  with open("LPP/images/tasklist.txt", "r") as taskfile:
    tasks = taskfile.readlines()
    
  for task in tasks:
    if task != '\n':
      task_list.append(task)
      listbox.insert(END, task)

#icon
Image_icon = PhotoImage(file = "Images/task.png")
root.iconphoto(False, Image_icon)

#top bar
TopImage = PhotoImage(file = "Images/topbar.png")
Label(root, image = TopImage).pack()

dockImage = PhotoImage(file = "Images/dock.png")
Label(root, image = dockImage, bg = "#32405b").place(x = 30, y = 25)

noteImage = PhotoImage(file = "Images/task.png")
Label(root, image = dockImage, bg = "#32405b").place(x = 30, y = 25)

heading = Label(root, text = "MINHAS TAREFAS", font = "arial 20 bold", fg = "white", bg = "#32405b")
heading.place(x = 100, y = 20)

#main
frame = Frame(root, width = 400, height = 50, bg = "white")
frame.place(x = 0, y = 180)

task = StringVar()
task_entry = Entry(frame, width = 18, font = "arial 20", bd = 0)
task_entry.place(x = 10, y = 7)
task_entry.focus()

button = Button(frame, text = "ADD", font = "arial 20 bold", width = 6, bg = "#5a95ff", fg = "#fff", bd = 0)
button.place (x = 300, y = 0)

#listbox
frame1 = Frame(root, bd = 3, width = 700, height = 280, bg = "#32405b")
frame1.pack(pady = (160, 0))

listbox = Listbox(frame1, font = ('arial', 12), width = 40, height = 16, bg = "#32405b", fg = "white", cursor = "hand2", selectbackground = "#5a95ff")
listbox.pack(side = LEFT, fill = BOTH, padx = 2)
Scrollbar = Scrollbar(frame1)
Scrollbar.pack(side = RIGHT, fill = BOTH)

listbox.config(yscrollcommand = Scrollbar.set)
Scrollbar.config(command = listbox.yview)

openTaskFile()

#delete
Delete_icon = PhotoImage(file = "Images/delete.png")
Button(root, image = Delete_icon, bd = 0).pack(side = BOTTOM, pady = 13)

root.mainloop()
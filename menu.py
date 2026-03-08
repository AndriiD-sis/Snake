from customtkinter import *
from PIL import Image, ImageTk, ImageSequence

class SnakeMenu(CTk):
    def __init__(self):
        super().__init__()

        self.name = None
        self.host = None
        self.port = None

        self.title("Snake Menu")
        self.geometry("400x300")
        self.resizable(False, False)
        self.iconbitmap("apple.png") #Замінити іконку .ico

        #Текст
        self.name_label = CTkLabel(
            self,
            text="Nikname:",
            width=120,
            height=25,
            font=("Arial", 20, "bold")
        ).place(x=7, y=45)

        self.host_label = CTkLabel(
            self,
            text="Hostname:",
            width=120,
            height=25,
            font=("Arial", 20, "bold")
        ).place(x=0, y=100)

        self.port_label = CTkLabel(
            self,
            text="Port:",
            width=120,
            height=25,
            font=("Arial", 20, "bold")
        ).place(x=28, y=155)

        #Поля введення
        self.name_entry = CTkEntry(
            self,
            placeholder_text="Введіть ім'я",
            width=270,
            height=40,
            corner_radius=0
        )
        self.name_entry.place(x=120, y=40)

        self.host_entry = CTkEntry(
            self,
            placeholder_text="Введіть назву сервера",
            width=270,
            height=40,
            corner_radius=0
        )
        self.host_entry.place(x=120, y=95)

        self.port_entry = CTkEntry(
            self,
            placeholder_text="Введіть порт",
            width=135,
            height=40,
            corner_radius=0
        )
        self.port_entry.place(x=120, y=150)

        #Кнопка
        self.start_button = CTkButton(
            self,
            text= "Приєнатися",
            width=350,
            height=55,
            corner_radius=0,
            command=self.open_game,
            font=("Arial", 25, "bold")
        ).place(x=25, y=215)

    def open_game(self):
        self.name = self.name_entry.get()
        self.host = self.host_entry.get()
        self.port = int(self.port_entry.get())
        self.destroy()

win = SnakeMenu()
win.mainloop()
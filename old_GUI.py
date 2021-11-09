import tkinter
import tkinter as tk
from tkinter import messagebox

class MainWindow(tk.Tk):

    def __init__(self, root):
        tk.Tk.__init__(self, root)
        self.root = root
        self.title('Server Dashboard')
        self.geometry('640x500')


class MenuFrame(tk.Frame):
    def __init__(self, root, console):
        tk.Frame.__init__(self, root)
        self.root = root
        self.console = console

        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = tk.Menu(menu, tearoff=0)
        fileMenu.add_command(label="Start Server")
        fileMenu.add_command(label="Stop Server")
        fileMenu.add_command(label="Exit Program", command=self.exitProgram)
        menu.add_cascade(label="Server", menu=fileMenu)

        editMenu = tk.Menu(menu, tearoff=0)
        editMenu.add_command(label="Clear Console", command=self.clear_console)
        editMenu.add_command(label="Help", command=self.help_info)
        menu.add_cascade(label="Console", menu=editMenu)

    def exitProgram(self):
        exit()

    def clear_console(self):
        console.listbox.delete(0, tk.END)

    def help_info(self):
        tk.messagebox.showinfo("Info", console.help_gui_text)





class ConsoleFrame(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root, bg="black", bd=5, highlightthickness=4)
        self.root = root
        self.console = []
        self.help_gui_text = "**This is a Guide to the Terminal Commands**\nCurrent Commands:\nhelp | #Shows the help info\nclear | #Clears the terminal window"
        self.widgets()
        self.input_console()

    def widgets(self):
        count = 0
        self.listbox = tk.Listbox(self, bg="black", fg="white", height=21, width=40, font=("system", 15), borderwidth=0, highlightthickness=0)
        while count < len(self.console):
            self.listbox.insert(count, self.console[count])
            self.listbox.grid(row=1, column=0, padx=0, pady=0)
            count = count + 1
        self.listbox.yview(tk.END)

    def input_console(self):
        self.entry_console = tk.Entry(self, font=("system", 15), borderwidth=2, highlightthickness=0)
        self.entry_console.grid(sticky="W", row=2, column=0, padx=0, pady=0)
        self.button = tk.Button(self, text="RUN", command=self.run_console_command)
        self.button.place(height=30, width=50, y=440, x=200)

    def run_console_command(self):
        command = self.entry_console.get()
        if command == "clear":
            self.listbox.delete(0, tk.END)
        elif command == "help":
            self.help_console()
        else:
            self.console.append(command)
            self.widgets()

    def help_console(self):
        self.console = ["**This is a Guide to the Terminal Commands**", "Current Commands:", "help | #Shows the help info", "clear | #Clears the terminal window"]
        self.widgets()




if __name__=="__main__":
    app = MainWindow(None)
    console = ConsoleFrame(None)
    menu_bar = MenuFrame(None, console)


    console.console.append("Test")
    console.console.append("Test3")
    console.console.append("Test")
    console.console.append("Test")
    console.console.append("Test")
    console.widgets()
    console.place(height=500, width=400, y=0)
    print(console.console)

    app.mainloop()

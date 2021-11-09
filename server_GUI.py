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
        self.gui_info = "**This is a Guide to the Terminal Commands**\nCurrent Commands:\nhelp | #Shows the help info\nclear | #Clears the terminal window"
        self.top_menu()

    def top_menu(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)



        server_menu = tk.Menu(menu, tearoff=0)
        server_menu.add_command(label="Start Server")
        server_menu.add_command(label="Stop Server")
        server_menu.add_command(label="restart server")
        menu.add_cascade(label="Server", menu=server_menu)

        console_menu = tk.Menu(menu, tearoff=0)
        console_menu.add_command(label="Clear Console", command=self.console.clear_console)
        console_menu.add_command(label="Exit Program", command=self.console.exit_server)
        menu.add_cascade(label="Console Commands", menu=console_menu)

        help_menu = tk.Menu(menu, tearoff=0)
        help_menu.add_command(label="Help", command=self.help_info)
        help_menu.add_command(label="About", command=self.about_info)
        menu.add_cascade(label="Help", menu=help_menu)


    def help_info(self):
        tk.messagebox.showinfo("Info", self.gui_info)

    def about_info(self):
        tk.messagebox.showinfo("About", "Server Dashboard | Created by Tobias Johansen | 2021")




class ConsoleFrame(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root, bg="black", bd=5, highlightthickness=4)
        self.root = root
        self.place(height=500, width=400, y=0)
        self.console = ["Test1", "Test2", "Test3"]
        self.console_window()
        self.input_console()

    # TODO: Cap console
    def console_window(self):
        self.listbox = tk.Listbox(self, bg="black", fg="white", height=21, width=40, font=("system", 15), borderwidth=0, highlightthickness=0)
        for x in range(len(self.console)):
            self.listbox.insert(x, self.console[x])
        self.listbox.grid(row=1, column=0, padx=0, pady=0)
        self.listbox.yview(tk.END)

    def input_console(self):
        self.entry_console = tk.Entry(self, font=("system", 15), borderwidth=2, highlightthickness=0)
        self.entry_console.grid(sticky="W", row=2, column=0, padx=0, pady=0)
        self.button = tk.Button(self, text="RUN", command=self.console_command)
        self.button.place(height=30, width=50, y=440, x=200)

    def console_command(self):
        command = self.entry_console.get()
        if command == 'start':
            pass
        elif command == 'stop':
            pass
        elif command == 'exit':
            exit()
        elif command == 'clear':
            self.clear_console()
        elif command == 'help':
            self.help_console()
        else:
            self.console.append(command)
            self.console_window()

    def start_server(self):
        pass

    def stop_server(self):
        pass

    def exit_server(self):
        exit()

    def clear_console(self):
        self.listbox.delete(0, tk.END)

    def help_console(self):
        self.help_info = ["**This is a Guide to the Terminal Commands**", "Current Commands:",
                        "help | #Shows the help info", "clear | #Clears the terminal window"]
        self.console.extend(self.help_info)
        self.console_window()

    def update_console(self):
        self.listbox.insert(len(self.console), self.console[-1])
        print(self.console)
        self.listbox.grid(row=1, column=0, padx=0, pady=0)
        self.place(height=500, width=400, y=0)
        print("Run the Update_console")


if __name__ == "__main__":
    app = MainWindow(None)
    console = ConsoleFrame(None)
    top_menu = MenuFrame(None, console)
    app.mainloop()

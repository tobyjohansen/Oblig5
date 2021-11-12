import tkinter as tk
from tkinter import messagebox
import socket
from _thread import *


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
        server_menu.add_command(label="Start Server", command=self.console.start_server)
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
        self.console = ["*This is the server Terminal*", "Here you can manage the server.", "start the server by writing 'start'", "and then click the run button.", "Or click server at the top left corner.", "Starting the server will close the gui"]
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
            self.start_server()
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
        app.destroy()
        # The gui windows gets removed when the server starts.

        # The Server code
        server_ip = "127.0.0.1"
        port = 5555

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server.bind((server_ip, port))
        except socket.error as e:
            str(e)

        server.listen(2)
        print("Waiting for a connection with a client...")

        # Code from techwithtim
        def read_pos(str):
            str = str.split(",")
            return int(str[0]), int(str[1])

        def make_pos(tup):
            return str(tup[0]) + "," + str(tup[1])

        # Set player Starting Position
        pos = [(50, 200), (350, 200), (200, 200)]

        # This is the code that is running in the thread
        def thread_client(conn, connID):

            # Sends starting position to the client
            conn.send(str.encode(make_pos(pos[connID])))
            answer = ""

            # Sends client number to the client
            msg = str(connID).encode("utf_8")
            conn.send(msg)

            # Main loop of the thread
            while True:
                try:
                    data = read_pos(conn.recv(2048).decode())
                    pos[connID] = data

                    if not data:
                        break
                    else:
                        if connID == 1:
                            reply = pos[0] + pos[2]
                        else:
                            reply = pos[1] + pos[2]

                        print("Received: ", data)
                        print("Sending : ", reply)

                    conn.sendall(str.encode(make_pos(reply)))
                except:
                    break
            print("Lost connection")
            conn.close()
        # Set variables
        connID = 0

        # Accepts connection and starts a new thread for each connection
        while True:
            conn, addr = server.accept()
            start_new_thread(thread_client, (conn, connID))
            connID += 1


    def stop_server(self):
        pass

    def exit_server(self):
        exit()

    def clear_console(self):
        self.listbox.delete(0, tk.END)
        self.console = []

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



app = MainWindow(None)
console = ConsoleFrame(None)
top_menu = MenuFrame(None, console)

def main():
    app.mainloop()

main()

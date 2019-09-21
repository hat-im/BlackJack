from tkinter import *

class WelcomeWindow:
    def __init__(self, master):
        self.master=master
        master.title("Welcome")

        main_frame=Frame(master, bg="green", height=300, width=400)
        main_frame.pack()

        welcome_message=Label(main_frame, text="Welcome to Blackjack", bg="green", fg="yellow")
        quit_button=Button(main_frame, text="Quit", bg="green", fg="yellow", command=master.quit)
        next_button=Button(main_frame, text="Start", bg="green", fg="yellow", command= lambda: print("Start"))

        welcome_message.place(relx=0.35, rely=0.4)
        quit_button.place(relx=0.1, rely=0.8, relwidth=0.2)
        next_button.place(relx=0.7, rely=0.8, relwidth=0.2)


root=Tk()
window=WelcomeWindow(root)
root.mainloop()
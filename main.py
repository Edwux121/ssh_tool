import tkinter as tk

from layout import Layout

class Main:
    """Main class for the app"""
    def __init__(self):
        self.app = App()
        self.app.master.title("SSH Tool")
        self.app.master.minsize(600, 600)

        #Grids for the application
        data_frame = tk.Frame(self.app, width=600, height=600, highlightbackground="red", highlightthickness=1)
        action_frame = tk.Frame(self.app, width=600, height=600, highlightbackground="red", highlightthickness=1)
        data_frame.grid(column=0, row=0)
        action_frame.grid(column=1, row=0)

        #Calling layout
        main_layout = Layout(data_frame, action_frame)
        main_layout.data_fields()
        main_layout.action_buttons()

        self.close_app()

    def close_app(self):
        self.app.mainloop()

class App(tk.Frame):
    """Class for manipulating the screen size"""
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

if __name__ == '__main__':
    #Run Main instance.
    ai = Main()
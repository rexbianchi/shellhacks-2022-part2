import tkinter as tk


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Page1):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label = tk.Label(self, text="Lonk is Currently Lonked", font=("Times New Roman", 40, "bold"))
        # label.grid(row=0, column=0)

        self.lonk_logo = tk.PhotoImage(file=r"C:\Users\rexbi\Desktop\shellhacks-2022-part2\gui\assets\LONK-closed.png")
        canvas = tk.Canvas(self, width=1000, height=1000)
        canvas.create_image(500, 500, image=self.lonk_logo)
        # canvas.create_text(75, 100, text="Yo", font=("Times New Roman", 40, "bold"))
        canvas.grid(row=0, column=0)


class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


if __name__ == "__main__":
    app = App()
    app.mainloop()
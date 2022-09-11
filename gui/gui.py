import tkinter as tk


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("720x480")

        container = tk.Frame(self)
        container.config(padx=190, pady=50)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}

        for F in (NoAccountPage, HasAccountPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(NoAccountPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Main label and canvas
        self.label = tk.Label(self, font=("Times New Roman", 14, "bold"), pady=20)
        self.logo_canvas = tk.Canvas(self, height=99, width=320, bg="black")

        # This stores the vault password label and input
        self.vault_password_label = tk.Label(self, font=("Times New Roman", 14, "bold"), pady=20)
        self.vault_password_input = tk.Entry(self, width=50)


        # This will get plaintext account info and make and store labels
        self.vault_information = []

        # THis is to add new password
        self.account_label = tk.Label(self, text="Account", font=("Times New Roman", 14, "bold"))
        self.account_entry = tk.Entry(self, width=10)
        self.username_label = tk.Label(self, text="Username", font=("Times New Roman", 14, "bold"))
        self.username_entry = tk.Entry(self, width=10)
        self.password_label = tk.Label(self, text="Password", font=("Times New Roman", 14, "bold"))
        self.password_entry = tk.Entry(self, width=10)

        self.submit_button = tk.Button(self, text="Submit", width=12)


class NoAccountPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.label.config(text="Looks like you're not lonked yet!")
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.lonk_logo = tk.PhotoImage(file="assets/low-res/LONK-open.png")
        self.lonk_logo_img = self.logo_canvas.create_image(160, 50, image=self.lonk_logo)
        self.logo_canvas.grid(row=1, column=0, columnspan=2, pady=10)

        self.password_label.config(text="Choose vault password:")
        self.password_label.grid(row=2, column=0, pady=10)
        self.password_entry.grid(row=2, column=1, pady=10)
        self.submit_button.grid(row=3, column=0, columnspan=3)


class HasAccountPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)


if __name__ == "__main__":
    app = App()
    app.mainloop()
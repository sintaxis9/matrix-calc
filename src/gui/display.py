import customtkinter


class Display(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.canvas = customtkinter.CTkCanvas(self, height=100, width=750, background="white", bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.scroll_x = customtkinter.CTkScrollbar(self, orientation="horizontal", command=self.canvas.xview)
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        self.canvas.configure(xscrollcommand=self.scroll_x.set)

        self.label_frame = customtkinter.CTkFrame(self.canvas, fg_color="transparent")
        self.label = customtkinter.CTkLabel(self.label_frame, text=master.operation, font=("Lucida Console", 20), anchor="e", fg_color="transparent", text_color="black")
        self.label.pack(anchor="w", padx=10)

        self.canvas_window = self.canvas.create_window((0, 0), window=self.label_frame, anchor="nw")
        self.label.bind("<Configure>", self._on_label_configure)

    def _on_label_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_items(self, new_value):
        app = self.master
        app.operation += ' ' + new_value + ' '
        self.label.configure(text=app.operation)
        self.canvas.update_idletasks()

    def delete_items(self):
        app = self.master
        app.operation = app.operation[:-3]
        self.label.configure(text=app.operation)
        self.canvas.update_idletasks()

    def delete_all_items(self):
        app = self.master
        app.operation = ''
        self.label.configure(text=app.operation)
        self.canvas.update_idletasks()

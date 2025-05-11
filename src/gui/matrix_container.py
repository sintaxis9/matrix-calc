import customtkinter


class Matrix_Template(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class Matrix_Editor(customtkinter.CTkFrame):
    def __init__(self, master, global_matrix_list, rows=3, cols=3, app=None):
        super().__init__(master)
        self.app = app  
        self.rows = rows
        self.cols = cols
        self.entries = []
        self.global_matrix_list = global_matrix_list  

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.name_entry = customtkinter.CTkEntry(self, width=100)
        self.name_entry.grid(row=0, column=0, padx=10, pady=10)

        self.name_label = customtkinter.CTkLabel(self, text="=", width=20)
        self.name_label.grid(row=0, column=1, pady=10)

        self.matrix_frame = customtkinter.CTkFrame(self)
        self.matrix_frame.grid(row=0, column=2, padx=10, pady=10)
        self.draw_matrix()

        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.grid(row=0, column=3, padx=10)

        self.add_row_btn = customtkinter.CTkButton(self.button_frame, text="+Fila", command=self.add_row)
        self.remove_row_btn = customtkinter.CTkButton(self.button_frame, text="-Fila", command=self.remove_row)
        self.add_col_btn = customtkinter.CTkButton(self.button_frame, text="+Col", command=self.add_column)
        self.remove_col_btn = customtkinter.CTkButton(self.button_frame, text="-Col", command=self.remove_column)
        self.save_btn = customtkinter.CTkButton(self.button_frame, text="Guardar", command=self.save_matrix)
        self.clear_btn = customtkinter.CTkButton(self.button_frame, text="Limpiar", command=self.clear_matrix)

        self.add_row_btn.grid(row=0, column=0, padx=5, pady=2)
        self.remove_row_btn.grid(row=0, column=1, padx=5, pady=2)
        self.add_col_btn.grid(row=1, column=0, padx=5, pady=2)
        self.remove_col_btn.grid(row=1, column=1, padx=5, pady=2)
        self.save_btn.grid(row=2, column=0, padx=5, pady=2)
        self.clear_btn.grid(row=2, column=1, padx=5, pady=2)

    def draw_matrix(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.entries = []

        for i in range(self.rows):
            row_entries = []
            for j in range(self.cols):
                entry = customtkinter.CTkEntry(self.matrix_frame, width=50, justify="center")
                entry.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def add_row(self):
        self.rows += 1
        self.draw_matrix()

    def add_column(self):
        self.cols += 1
        self.draw_matrix()

    def remove_row(self):
        if self.rows > 1:
            self.rows -= 1
            self.draw_matrix()

    def remove_column(self):
        if self.cols > 1:
            self.cols -= 1
            self.draw_matrix()

    def clear_matrix(self):
        for row in self.entries:
            for entry in row:
                entry.delete(0, "end")

    def save_matrix(self):
        name = self.name_entry.get().strip()
        if name == "":
            print("Tienes que ponerle una variable a la matriz")
            return


        if any(name in matrix_entry for matrix_entry in self.global_matrix_list):
            message = f"La matriz '{name}' ya está guardada"
            print(message)
            self.app.show_temporal_message(message)
            return

        matrix = []
        for row in self.entries:
            row_data = []
            for entry in row:
                value = entry.get()
                try:
                    value = float(value)
                except ValueError:
                    value = 0
                row_data.append(value)
            matrix.append(row_data)

        self.global_matrix_list.append({name: matrix})
        print(f"La matriz '{name}' se ha guardado correctamente")
        print("\nlista global de matricesssss:")
        for item in self.global_matrix_list:
            print(item)



class Matrix_Display(customtkinter.CTkFrame):
    def __init__(self, master, name: str, matrix: list[list[float]]):
        super().__init__(master)
  
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

   
        self.title_label = customtkinter.CTkLabel(
            self, text=f"{name} =", font=("Arial", 14, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=(0,10), sticky="n")


        self.result_widget = customtkinter.CTkFrame(self)
        self.result_widget.grid(row=0, column=1, sticky="nsew")

        for i, fila in enumerate(matrix):
            for j, valor in enumerate(fila):
                cell = customtkinter.CTkLabel(
                    self.result_widget,
                    text=str(valor),
                    width=50,
                    justify="center"
                )
                cell.grid(row=i, column=j, padx=2, pady=2)




class Matrix_Container(customtkinter.CTkFrame):
    def __init__(self, master, matrix_list):
        super().__init__(master)
        self.pack(fill="both", expand=True, padx=10, pady=10)

        self.matrix_list = matrix_list
        self.matrix_editors = [] 

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, width=750, height=300)
        self.scrollable_frame.pack(fill="both", expand=True)

    def add_matrix(self):
        editor = Matrix_Editor(self.scrollable_frame, self.matrix_list, app=self.master)
        editor.pack(pady=10, padx=10, fill="x", expand=True)
        self.matrix_editors.append(editor)

    def get_all_matrices(self):
        return self.matrix_list


    def add_matrix_result(self, name: str, matrix: list[list[float]]):
        """Crea un Matrix_Display para la matriz resultado y lo añade al scroll."""
        display = Matrix_Display(self.scrollable_frame, name, matrix)
        display.pack(pady=10, padx=10, fill="x", expand=True)

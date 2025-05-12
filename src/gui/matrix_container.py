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

    def _parse_entry(self, entry):
        """Convierte el texto del entry a float o devuelve 0 si falla."""
        try:
            return float(entry.get())
        except ValueError:
            return 0
        
    def print_saved_matrices(self):
        """Imprime por consola todas las matrices guardadas."""
        if not self.global_matrix_list:
            print("No hay matrices guardadas.")
            return

        for mat_dict in self.global_matrix_list:
            for name, matrix in mat_dict.items():
                print(f"Matriz '{name}':")
                for row in matrix:
                    print("   ", row)
                print()  # línea en blanco entre matrices


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
            if not name:
                self.app.show_temporal_message("Tienes que asignar un nombre a la matriz")
                return

            # Usa _parse_entry para cada celda
            matrix = [
                [self._parse_entry(e) for e in row]
                for row in self.entries
            ]

            # Comprueba si ya existe y sobreescribe o añade
            existing_idx = next(
                (i for i, d in enumerate(self.global_matrix_list) if name in d),
                None
            )
            if existing_idx is not None:
                self.global_matrix_list[existing_idx][name] = matrix
                self.app.show_temporal_message(
                    f"La matriz '{name}' se ha actualizado correctamente", color="green"
                )
            else:
                self.global_matrix_list.append({name: matrix})
                self.app.show_temporal_message(
                    f"La matriz '{name}' se ha guardado correctamente", color="green"
                )
                self.print_saved_matrices()


class Matrix_Display(customtkinter.CTkFrame):
    def __init__(self, master, name: str, matrix: list[list[float]]):
        super().__init__(master)
  
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

   
        self.title_label = customtkinter.CTkLabel(self, text=f"{name} =", font=("Arial", 14, "bold"), padx=10,pady=35)
        self.title_label.grid(row=0, column=0, padx=(0,10), sticky="n")


        self.result_widget = customtkinter.CTkFrame(
            self,
            fg_color="#424242",
            corner_radius=8,
            border_color="#575353",
            border_width=1
        )
        self.result_widget.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")

        # Hace que las filas y columnas crezcan de forma uniforme
        for r in range(len(matrix)):
            self.result_widget.grid_rowconfigure(r, weight=1)
        for c in range(len(matrix[0]) if matrix else 0):
            self.result_widget.grid_columnconfigure(c, weight=1)

        # Celdas con fondo blanco, fuente más grande y padding
        for i, fila in enumerate(matrix):
            for j, valor in enumerate(fila):
                cell = customtkinter.CTkLabel(
                    self.result_widget,
                    text=str(valor),
                    font=("Arial", 15),
                    width=60,
                    height=40,
                    fg_color="#1976D2",
                    corner_radius=5,
                    text_color="#FEFEFE",
                    justify="center"
                )
                cell.grid(row=i, column=j, padx=4, pady=4, sticky="nsew")




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

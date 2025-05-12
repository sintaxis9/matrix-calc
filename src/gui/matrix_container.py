import customtkinter  # Importa la biblioteca customtkinter para crear interfaces gráficas personalizadas.


class Matrix_Template(customtkinter.CTkFrame):
    """
    Clase base para plantillas de matriz, hereda de CTkFrame.
    """
    def __init__(self, master):
        super().__init__(master)  # Llama al constructor de la clase base CTkFrame.


class Matrix_Editor(customtkinter.CTkFrame):
    """
    Clase que permite editar una matriz, añadiendo filas y columnas.
    """
    def __init__(self, master, global_matrix_list, rows=3, cols=3, app=None):
        """
        Inicializa el editor de matrices.
        
        :param master: El widget padre en el que se colocará este editor.
        :param global_matrix_list: La lista global que almacenará todas las matrices.
        :param rows: Número inicial de filas.
        :param cols: Número inicial de columnas.
        :param app: Referencia a la aplicación principal, si es necesario.
        """
        super().__init__(master)  # Llama al constructor de la clase base CTkFrame.
        self.app = app  # Almacena la referencia a la aplicación principal.
        self.rows = rows  # Almacena el número de filas.
        self.cols = cols  # Almacena el número de columnas.
        self.entries = []  # Lista para almacenar las entradas de la matriz.
        self.global_matrix_list = global_matrix_list  # Almacena la lista global de matrices.
        
        # Configura la cuadrícula para permitir que la primera columna y fila se expandan.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Crea un campo de entrada para el nombre de la matriz.
        self.name_entry = customtkinter.CTkEntry(self, width=100)
        self.name_entry.grid(row=0, column=0, padx=10, pady=10)
        
        # Crea una etiqueta para mostrar el signo igual.
        self.name_label = customtkinter.CTkLabel(self, text="=", width=20)
        self.name_label.grid(row=0, column=1, pady=10)
        
        # Crea un marco para la matriz.
        self.matrix_frame = customtkinter.CTkFrame(self)
        self.matrix_frame.grid(row=0, column=2, padx=10, pady=10)
        
        # Dibuja la matriz inicial.
        self.draw_matrix()
        
        # Crea un marco para los botones de control.
        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.grid(row=0, column=3, padx=10)
        
        # Crea botones para agregar y eliminar filas y columnas, y para guardar y limpiar la matriz.
        self.add_row_btn = customtkinter.CTkButton(self.button_frame, text="+Fila", command=self.add_row)
        self.remove_row_btn = customtkinter.CTkButton(self.button_frame, text="-Fila", command=self.remove_row)
        self.add_col_btn = customtkinter.CTkButton(self.button_frame, text="+Col", command=self.add_column)
        self.remove_col_btn = customtkinter.CTkButton(self.button_frame, text="-Col", command=self.remove_column)
        self.save_btn = customtkinter.CTkButton(self.button_frame, text="Guardar", command=self.save_matrix)
        self.clear_btn = customtkinter.CTkButton(self.button_frame, text="Limpiar", command=self.clear_matrix)
        
        # Coloca los botones en la cuadrícula.
        self.add_row_btn.grid(row=0, column=0, padx=5, pady=2)
        self.remove_row_btn.grid(row=0, column=1, padx=5, pady=2)
        self.add_col_btn.grid(row=1, column=0, padx=5, pady=2)
        self.remove_col_btn.grid(row=1, column=1, padx=5, pady=2)
        self.save_btn.grid(row=2, column=0, padx=5, pady=2)
        self.clear_btn.grid(row=2, column=1, padx=5, pady=2)
   
    def draw_matrix(self):
        """
        Dibuja la matriz en el marco de la matriz, creando entradas para cada celda.
        """
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()  # Elimina cualquier entrada existente en el marco de la matriz.
        self.entries = []  # Reinicia la lista de entradas.
        
        # Crea nuevas entradas para la matriz según el número de filas y columnas.
        for i in range(self.rows):
            row_entries = []  # Lista para las entradas de la fila actual.
            for j in range(self.cols):
                entry = customtkinter.CTkEntry(self.matrix_frame, width=50, justify="center")
                entry.grid(row=i, column=j, padx=2, pady=2)  # Coloca la entrada en la cuadrícula.
                row_entries.append(entry)  # Agrega la entrada a la lista de la fila.
            self.entries.append(row_entries)  # Agrega la fila de entradas a la lista de entradas.


    def add_row(self):
        """Agrega una fila a la matriz."""
        self.rows += 1  # Incrementa el contador de filas.
        self.draw_matrix()  # Redibuja la matriz con la nueva fila.


    def add_column(self):
        """Agrega una columna a la matriz."""
        self.cols += 1  # Incrementa el contador de columnas.
        self.draw_matrix()  # Redibuja la matriz con la nueva columna.


    def remove_row(self):
        """Elimina una fila de la matriz, si hay más de una fila."""
        if self.rows > 1:
            self.rows -= 1  # Decrementa el contador de filas.
            self.draw_matrix()  # Redibuja la matriz con la fila eliminada.


    def remove_column(self):
        """Elimina una columna de la matriz, si hay más de una columna."""
        if self.cols > 1:
            self.cols -= 1  # Decrementa el contador de columnas.
            self.draw_matrix()  # Redibuja la matriz con la columna eliminada.


    def clear_matrix(self):
        """Limpia todas las entradas de la matriz."""
        for row in self.entries:
            for entry in row:
                entry.delete(0, "end")  # Borra el contenido de cada entrada.


    def save_matrix(self):
        """Guarda la matriz en la lista global, usando el nombre proporcionado."""
        name = self.name_entry.get().strip()  # Obtiene el nombre de la matriz.
        if name == "":
            print("Tienes que ponerle una variable a la matriz")  # Mensaje de error si no se proporciona un nombre.
            return
        # Verifica si la matriz ya está guardada.
        if any(name in matrix_entry for matrix_entry in self.global_matrix_list):
            message = f"La matriz '{name}' ya está guardada"
            print(message)  # Mensaje de advertencia si la matriz ya existe.
            self.app.show_temporal_message(message)  # Muestra un mensaje temporal en la aplicación.
            return
        matrix = []  # Lista para almacenar los datos de la matriz.
        for row in self.entries:
            row_data = []  # Lista para los datos de la fila actual.
            for entry in row:
                value = entry.get()  # Obtiene el valor de la entrada.
                try:
                    value = float(value)  # Intenta convertir el valor a un número flotante.
                except ValueError:
                    value = 0  # Si falla, asigna 0.
                row_data.append(value)  # Agrega el valor a la lista de datos de la fila.
            matrix.append(row_data)  # Agrega la fila de datos a la matriz.
        self.global_matrix_list.append({name: matrix})  # Guarda la matriz en la lista global.
        print(f"La matriz '{name}' se ha guardado correctamente")  # Mensaje de éxito.
        print("\nLista global de matrices:")
        for item in self.global_matrix_list:
            print(item)  # Imprime la lista global de matrices.


class Matrix_Display(customtkinter.CTkFrame):
    """
    Clase que muestra una matriz en la interfaz gráfica.
    """
    def __init__(self, master, name: str, matrix: list[list[float]]):
        """
        Inicializa la visualización de la matriz.
        
        :param master: El widget padre en el que se colocará esta visualización.
        :param name: El nombre de la matriz.
        :param matrix: La matriz a mostrar.
        """
        super().__init__(master)  # Llama al constructor de la clase base CTkFrame.
        self.grid_columnconfigure(0, weight=0)  # Configura la primera columna.
        self.grid_columnconfigure(1, weight=1)  # Configura la segunda columna.
        
        # Crea una etiqueta para mostrar el nombre de la matriz.
        self.title_label = customtkinter.CTkLabel(
            self, text=f"{name} =", font=("Arial", 14, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=(0, 10), sticky="n")  # Coloca la etiqueta en la cuadrícula.
        
        # Crea un marco para mostrar los resultados de la matriz.
        self.result_widget = customtkinter.CTkFrame(self)
        self.result_widget.grid(row=0, column=1, sticky="nsew")  # Coloca el marco en la cuadrícula.
        
        # Agrega las celdas de la matriz al marco.
        for i, fila in enumerate(matrix):
            for j, valor in enumerate(fila):
                cell = customtkinter.CTkLabel(
                    self.result_widget,
                    text=str(valor),
                    width=50,
                    justify="center"
                )
                cell.grid(row=i, column=j, padx=2, pady=2)  # Coloca cada celda en la cuadrícula.


class Matrix_Container(customtkinter.CTkFrame):
    """
    Clase que contiene y gestiona múltiples editores de matrices.
    """
    def __init__(self, master, matrix_list):
        """
        Inicializa el contenedor de matrices.
        
        :param master: El widget padre en el que se colocará este contenedor.
        :param matrix_list: La lista de matrices que se gestionarán.
        """
        super().__init__(master)  # Llama al constructor de la clase base CTkFrame.
        self.pack(fill="both", expand=True, padx=10, pady=10)  # Empaqueta el contenedor.
        self.matrix_list = matrix_list  # Almacena la lista de matrices.
        self.matrix_editors = []  # Lista para almacenar los editores de matrices.
        
        # Crea un marco desplazable para contener los editores de matrices.
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, width=750, height=300)
        self.scrollable_frame.pack(fill="both", expand=True)  # Empaqueta el marco desplazable.
    
    def add_matrix(self):
        """Agrega un nuevo editor de matriz al contenedor."""
        editor = Matrix_Editor(self.scrollable_frame, self.matrix_list, app=self.master)  # Crea un nuevo editor de matriz.
        editor.pack(pady=10, padx=10, fill="x", expand=True)  # Empaqueta el editor en el marco desplazable.
        self.matrix_editors.append(editor)  # Agrega el editor a la lista de editores.
    

    def get_all_matrices(self):
        """Devuelve la lista de todas las matrices."""
        return self.matrix_list
    
    
    def add_matrix_result(self, name: str, matrix: list[list[float]]):
        """Crea un Matrix_Display para la matriz resultado y lo añade al scroll."""
        display = Matrix_Display(self.scrollable_frame, name, matrix)  # Crea un nuevo display para la matriz.
        display.pack(pady=10, padx=10, fill="x", expand=True)  # Empaqueta el display en el marco desplazable.
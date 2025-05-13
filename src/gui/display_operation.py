import customtkinter  # Importa la librería CustomTkinter para crear interfaces gráficas con estilo moderno

# Define una clase personalizada OperationDisplay que hereda de CTkFrame
class OperationDisplay(customtkinter.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)  # Llama al constructor de la clase base
        # Crea un contenedor con scroll para mostrar muchas operaciones si es necesario
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True)  # Lo ajusta al tamaño del contenedor padre

    def clear(self):
        # Elimina todos los widgets hijos del scrollable_frame
        for child in self.scrollable_frame.winfo_children():
            child.destroy()

    def show_steps(
        self,
        operations: list[list[tuple[str, list[list[float]]]]]  # Lista de operaciones, cada una con pasos (descripción y matriz)
    ):

        self.clear()  # Limpia el contenido previo antes de mostrar nuevos pasos

        for idx, steps in enumerate(operations, start=1):  # Itera sobre cada operación con un índice
            # Título de la operación, por ejemplo: "--- Operación #1 ---"
            title = f"--- Operación #{idx} ---"
            title_lbl = customtkinter.CTkLabel(
                self.scrollable_frame,
                text=title,
                font=("Courier New", 14, "bold")  # Fuente monoespaciada y en negrita
            )
            title_lbl.pack(padx=10, pady=(15, 5), anchor="w")  # Muestra el título con espacio y alineación a la izquierda

            # Muestra cada paso de la operación
            for desc, matrix in steps:
                step_label = customtkinter.CTkLabel(
                    self.scrollable_frame,
                    text=desc + "\n" + self._format_matrix(matrix),  # Combina la descripción y la matriz formateada
                    font=("Courier New", 12)  # Fuente monoespaciada para alinear bien la matriz
                )
                step_label.pack(padx=20, pady=3, anchor="w")  # Alinea a la izquierda con espacio interno

    def _format_matrix(self, matrix: list[list[float]]) -> str:
        """Formatea la matriz para ponerla en un CTkLabel."""
        lines: list[str] = []  # Lista para almacenar las filas formateadas
        for row in matrix:
            # Convierte cada número a string con 2 decimales y los separa con doble espacio
            formatted = "  ".join(f"{x:.2f}" for x in row)
            lines.append(f"[{formatted}]")  # Agrega corchetes a cada fila

        # Une todas las filas formateadas de la matriz en una sola cadena,
        # separando cada fila con un salto de línea para que la matriz se vea como un bloque vertical.
        return "\n".join(lines)

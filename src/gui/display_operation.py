
import customtkinter

class OperationDisplay(customtkinter.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)
        # crea el contenedor scrollable
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True)

    def clear(self):
        for child in self.scrollable_frame.winfo_children():
            child.destroy()

    def show_steps(
        self,
        operations: list[list[tuple[str, list[list[float]]]]]
    ):

        self.clear()
        for idx, steps in enumerate(operations, start=1):
            # Título de la operación
            title = f"--- Operación #{idx} ---"
            title_lbl = customtkinter.CTkLabel(
                self.scrollable_frame,
                text=title,
                font=("Courier New", 14, "bold")
            )
            title_lbl.pack(padx=10, pady=(15, 5), anchor="w")

            # Pasos de la operación
            for desc, matrix in steps:
                step_label = customtkinter.CTkLabel(
                    self.scrollable_frame,
                    text=desc + "\n" + self._format_matrix(matrix),
                    font=("Courier New", 12)
                )
                step_label.pack(padx=20, pady=3, anchor="w")

    def _format_matrix(self, matrix: list[list[float]]) -> str:
        """Formatea la matriz para ponerla en un CTkLabel."""
        lines: list[str] = []
        for row in matrix:
            formatted = "  ".join(f"{x:.2f}" for x in row)
            lines.append(f"[{formatted}]")
        return "\n".join(lines)

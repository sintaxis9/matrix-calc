import customtkinter
from .matrix_container import Matrix_Container
from .display import Display
from .operations_panel import Operations_Panel


def Calculator():

    class App(customtkinter.CTk):
        def __init__(self):
            super().__init__()
            self.title("Calculadora de matrices")
            self.geometry("800x800")
            self.resizable(True, True)
            
            self.matrix_list = []     # Accesible desde subcomponentes
            self.operation = ""       # Accesible desde subcomponentes

            self.display_matrix = Matrix_Container(self, self.matrix_list)
            self.display_matrix.grid(row=0, column=0, padx=10, pady=(10, 0))

            self.display = Display(self)
            self.display.grid(row=1, column=0, padx=10, pady=(10, 0))

            self.panel_control = Operations_Panel(self, self.display, self.display_matrix)
            self.panel_control.grid(row=2, column=0, padx=10, pady=(10, 0))

        def get_operation(self):
            return self.operation
        
        def get_matrix_list(self):
            return self.matrix_list

    app = App()
    app.mainloop()


Calculator()
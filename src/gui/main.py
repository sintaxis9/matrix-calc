import customtkinter
from .matrix_container import Matrix_Container
from .display import Display
from .operations_panel import Operations_Panel
from .display_operation import OperationDisplay 

def Calculator():

    class App(customtkinter.CTk):
        def __init__(self):
            super().__init__()
            self.title("Calculadora de matrices")
            self.geometry("1200x800")
            self.resizable(True, True)
            
            self.matrix_list = []
            self.operation = ""

            self.display_matrix = Matrix_Container(self, self.matrix_list)
            self.display_matrix.grid(row=0, column=0, padx=10, pady=(10, 0))

            self.message_label = customtkinter.CTkLabel(
                self, text="", text_color="red", font=("Arial", 16)
            )
            self.message_label.grid(row=1, column=0, padx=10, pady=(5, 5))

            self.display = Display(self)
            self.display.grid(row=2, column=0, padx=10, pady=(10, 0))

            self.panel_control = Operations_Panel(
                self, self.display, self.display_matrix
            )
            self.panel_control.grid(row=3, column=0, padx=10, pady=(10, 0))

            self.panel_control.grid(row=3, column=0, padx=10, pady=(10, 0))

            self.operation_label = OperationDisplay(self)
            self.operation_label.configure(width=250)

            self.grid_columnconfigure(1, weight=1)

            for r in range(4):
                self.grid_rowconfigure(r, weight=1)

            self.operation_label = OperationDisplay(self)
            self.operation_label.grid(
                row=0, column=1,
                rowspan=4,             
                padx=10, pady=(10, 0),
                sticky="nsew"
            )
            

        def get_operation(self):
            return self.operation
        
        def get_matrix_list(self):
            return self.matrix_list
        
        def show_message(self, textMessage, color="red"):
            self.message_label.configure(text=textMessage, text_color=color)

        def show_temporal_message(self, textMessage, color="red", duration=6000):
            self.message_label.configure(text=textMessage, text_color=color)
            self.after(duration, lambda: self.message_label.configure(text=""))

    app = App()
    app.mainloop()


Calculator()
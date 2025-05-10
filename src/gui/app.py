import customtkinter


class Matrix_Template(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

class Matrix_Editor(customtkinter.CTkFrame):
    def __init__(self, master, global_matrix_list, rows=3, cols=3):
        super().__init__(master)
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
            print("teni que ponerle una variable a la matriz")
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
        print(f"la matriz: '{name}'")
        print("\nlista global de matricesssss:")
        for item in self.global_matrix_list:
            print(item)



class Display_Matrix(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.matrix_list = []

        self.canvas = customtkinter.CTkCanvas(self, height=400, width=750, background="white", bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.scroll_y = customtkinter.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scroll_y.grid(row=0, column=1, sticky="ns", pady=10)

        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.content_frame = customtkinter.CTkFrame(self.canvas, fg_color="transparent")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        self.content_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def add_matrix_editor(self):
        editor = Matrix_Editor(self.content_frame, self.matrix_list)
        editor.pack(pady=10, padx=10, fill="x", expand=True)



class Matrix_Container(customtkinter.CTkFrame):
    def __init__(self, master, matrix_list):
        super().__init__(master)
        self.pack(fill="both", expand=True, padx=10, pady=10)

        self.matrix_list = matrix_list
        self.matrix_editors = [] 

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, width=750, height=300)
        self.scrollable_frame.pack(fill="both", expand=True)

    def add_matrix(self):
        editor = Matrix_Editor(self.scrollable_frame, self.matrix_list)
        editor.pack(pady=10, padx=10, fill="x", expand=True)
        self.matrix_editors.append(editor)

    def get_all_matrices(self):
        return self.matrix_list

        

class Display(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


        self.canvas = customtkinter.CTkCanvas(self, height=100, width=750, background="white", bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.scroll_x = customtkinter.CTkScrollbar(self, orientation="horizontal", command=self.canvas.xview)
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        self.canvas.configure(xscrollcommand=self.scroll_x.set)


        self.label_frame = customtkinter.CTkFrame(self.canvas, fg_color="transparent")


        self.label = customtkinter.CTkLabel(self.label_frame, text=master.operation, font=("Lucida Console", 20), anchor="e", fg_color="transparent",text_color="black")



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
        print("eliminando item")
        app = self.master
        app.operation = app.operation[:-3]
        self.label.configure(text=self.operation)
        self.canvas.update_idletasks()
        
    def delete_all_items(self):
        app = self.master
        app.operation = ''
        self.label.configure(text=app.operation)
        self.canvas.update_idletasks()



class Operations_Panel(customtkinter.CTkFrame):
    def __init__(self, master, display, display_matrix):
        super().__init__(master)
        self.display = display
        self.display_matrix = display_matrix

        self.bottom_panel = Bottom_Panel(self, self.display, self.display_matrix)
        self.numeric_keypad = Numeric_Keypad(self, self.display)
        self.numerical_methods = Numerical_Methods(self, self.display)

        self.bottom_panel.grid(row=0, column=0, columnspan=3, padx=5, pady=10)
        self.numerical_methods.grid(row=1, column=0, padx=5, pady=5)
        self.numeric_keypad.grid(row=1, column=1, padx=5, pady=5)
    
        

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)




class Bottom_Panel(customtkinter.CTkFrame):
    def __init__(self, master,display,display_matrix):
        super().__init__(master)

        self.display = display 
        self.display_matrix = display_matrix 
            
        matrixButton = customtkinter.CTkButton(self, width=100, height=20, text="Añadir matrix",font=("Arial",20), command=self.add_matrix)

        matrixButton.grid(row=0, column=0,padx=60, pady=5, sticky="nsew")

        acButton = customtkinter.CTkButton(self, width=100, height=20, text="Borrar todo",font=("Arial",20), command=self.delete_all)

        acButton.grid(row=0, column=1,padx=60, pady=5, sticky="nsew")

        ceButton = customtkinter.CTkButton(self, width=100, height=20, text="⬅",font=("Arial",20), command=self.delete_item)
        
        ceButton.grid(row=0, column=3,padx=60, pady=5, sticky="nsew")

    def add_matrix(self):
        self.display_matrix.add_matrix()
        print("añadir matrix")

    def delete_all(self):
        self.display.delete_all_items()
        print("borra todo")

    def delete_item(self):
        self.display.delete_items()

    

class Numeric_Keypad(customtkinter.CTkFrame):
    def __init__(self, master,display):
        super().__init__(master)
        self.display = display

        numbers = [
            ('AC', 0, 0), ('(', 0, 1), (')', 0, 2),('%', 0, 4),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),('x', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),('-', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),('+', 3, 4),
            ('0', 4, 0), ('.', 4, 1), (' ', 4, 2),('=', 4, 4),
        ]

        for (value, row, column) in numbers:
            number = customtkinter.CTkButton(self, text=value, width=40, height=30, font=("Arial",20), command=lambda x=value: self.update_number(x))
            number.grid(row=row, column=column,padx=5, pady=5, sticky="nsew")

    def update_number(self, value):

        if value == "=":
        
            print("display screen: ", self.display.master.operation)

            print("matrices: ",self.display.master.matrix_list)
        else:
            self.display.update_items(value)



class Numerical_Methods(customtkinter.CTkFrame):
    def __init__(self, master,display):
        super().__init__(master)
        self.display = display



        methods = [
            ('A', 0, 0), ('B', 0, 1), ('C', 0, 2),
            ('D', 1, 0), ('F', 1, 1), ('H', 1, 2),
            ('Det', 2, 0), ('Inv', 2, 1), ('ola', 2, 2),
            ('tras', 3, 0), ('nose', 3, 1), ('que', 3, 2), 
        ]


        for (funtion,row,column) in methods:
            method = customtkinter.CTkButton(self, text=funtion, width=40, height=30, command=lambda x=funtion: self.update_numerical(x))
            method.grid(row=row, column=column,  padx=5, pady=10, sticky="nsew")
            

    def update_numerical(self,operation):
        self.display.update_items(operation)
        print(f"metodo numerico: {operation} ")
        

def Calculator():

    class App(customtkinter.CTk):
        def __init__(self):
            super().__init__()
            self.title("Calculadora de matrices")
            self.geometry("800x800")
            self.resizable(True, True)
            
            self.matrix_list = []

            self.operation = ""

            self.display_matrix = Matrix_Container(self, self.matrix_list)
            self.display_matrix.grid(row=0, column=0, padx=10, pady=(10, 0))

            self.display = Display(self)
            self.display.grid(row=1, column=0, padx=10, pady=(10, 0))

            self.panel_control = Operations_Panel(self, self.display, self.display_matrix)
            self.panel_control.grid(row=2, column=0, padx=10, pady=(10, 0))


        def get_operation(self):
            return self.operation
        


    app = App()
    app.mainloop()





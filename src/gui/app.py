import customtkinter


class Matrix_Template(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)



class Display(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.operation = ""


        self.canvas = customtkinter.CTkCanvas(self, height=100, width=600, background="black", bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.scroll_x = customtkinter.CTkScrollbar(self, orientation="horizontal", command=self.canvas.xview)
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        self.canvas.configure(xscrollcommand=self.scroll_x.set)


        self.label_frame = customtkinter.CTkFrame(self.canvas, fg_color="transparent")
        self.label = customtkinter.CTkLabel(self.label_frame, text=self.operation, font=("Lucida Console", 20), anchor="e", fg_color="transparent")
        self.label.pack(anchor="w", padx=10)

        self.canvas_window = self.canvas.create_window((0, 0), window=self.label_frame, anchor="nw")

        self.label.bind("<Configure>", self._on_label_configure)

    def _on_label_configure(self, event):

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_items(self, new_value):
        self.operation += ' ' + new_value + ' '
        self.label.configure(text=self.operation)
        self.canvas.update_idletasks()

    def delete_items(self, delete_value):
        print("eliminando item")
        self.label.configure(text=self.operation)

    def delete_all_items(self):
        self.operation = ''
        self.label.configure(text=self.operation)
        self.canvas.update_idletasks()



class Operations_Panel(customtkinter.CTkFrame):
    def __init__(self, master,display):
        super().__init__(master)

        self.display = display

        self.bottom_panel = Bottom_Panel(self, self.display)
        self.numeric_keypad = Numeric_Keypad(self, self.display)
        self.arithmic_methods = Arithmic_Methods(self, self.display)
        self.numerical_methods = Numerical_Methods(self, self.display)
        


        self.bottom_panel.grid(row=0, column=0, columnspan=3, padx=5, pady=10)
        self.numerical_methods.grid(row=1, column=0, padx=5, pady=5)
        self.numeric_keypad.grid(row=1, column=1, padx=5, pady=5)
        self.arithmic_methods.grid(row=1, column=2, padx=5, pady=5)
    
        

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)




class Bottom_Panel(customtkinter.CTkFrame):
    def __init__(self, master,display):
        super().__init__(master)

        self.display = display 
            
        matrixButton = customtkinter.CTkButton(self, width=200, height=70, text="Añadir matrix",font=("Arial",20), command=self.add_matrix)

        matrixButton.grid(row=0, column=0,padx=5, pady=5, sticky="nsew")

        acButton = customtkinter.CTkButton(self, width=200, height=70, text="Borrar todo",font=("Arial",20), command=self.delete_all)

        acButton.grid(row=0, column=1,padx=5, pady=5, sticky="nsew")

        ceButton = customtkinter.CTkButton(self, width=200, height=70, text="⬅",font=("Arial",50), command=self.delete_item)
        
        ceButton.grid(row=0, column=3,padx=5, pady=5, sticky="nsew")

    def add_matrix(self):
        print("añadir matrix")

    def delete_all(self):
        self.display.delete_all_items()
        print("borra todo")

    def delete_item(self):
        print("borra un item")
    

class Numeric_Keypad(customtkinter.CTkFrame):
    def __init__(self, master,display):
        super().__init__(master)
        self.display = display

        numbers = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
            (' ', 3, 0), ('0', 3, 1), (' ', 3, 2),
        ]

        for (value, row, column) in numbers:
            number = customtkinter.CTkButton(self, text=value, width=70, height=70, font=("Arial",20), command=lambda x=value: self.update_number(x))
            number.grid(row=row, column=column,padx=5, pady=5, sticky="nsew")

    def update_number(self, value):
        self.display.update_items(value)

class Arithmic_Methods(customtkinter.CTkFrame):

    def __init__(self, master,display):
        super().__init__(master)
        self.display = display

        methods = [
            ('+',0,0),
            ('-',1,0),
            ('*',2,0),
            ('/',3,0),
            ('^',4,0),
            ('=',5,0),
        ]

        for (operation,row,column) in methods:
            method = customtkinter.CTkButton(self, text=operation, width=70, height=50, font=("Arial",20), command=lambda x=operation: self.update_arithmic(x))
            method.grid(row=row, column=0,  padx=5, pady=5, sticky="nsew")

    def update_arithmic(self,operation):

        if operation == "CE":
            self.display.delete_items(operation)

        else: 
            self.display.update_items(operation)
            print(f"metodo aritmetico: {operation}")


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
            method = customtkinter.CTkButton(self, text=funtion, width=70, height=50, command=lambda x=funtion: self.update_numerical(x))
            method.grid(row=row, column=column,  padx=5, pady=10, sticky="nsew")
            

    def update_numerical(self,operation):
        self.display.update_items(operation)
        print(f"metodo numerico: {operation} ")
        


class Matrix_Keypad(customtkinter.CTkFrame):
    def __init__(self, master,display):
        super().__init__(master)
        self.display = display

    

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de matrices")
        self.geometry("800x600")
        self.resizable(False,False)

        self.display = Display(self)
        self.display.grid(row=0, column=0, padx=10, pady=(10, 0))

        self.panel_control = Operations_Panel(self,self.display)
        self.panel_control.grid(row=1, column=0, padx=10, pady=(10, 0))






app = App()
app.mainloop()

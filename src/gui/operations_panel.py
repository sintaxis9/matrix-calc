import customtkinter
from ..matrix_operations.matrix_ops import add, subtract, multiply, scalar_multiply


class Operations_Panel(customtkinter.CTkFrame):
    def __init__(self, master, display, display_matrix):
        super().__init__(master)
        self.display = display
        self.display_matrix = display_matrix

        self.bottom_panel = Bottom_Panel(self, self.display, self.display_matrix)
        self.numeric_keypad = Numeric_Keypad(self, self.display)
        self.numerical_methods = Numerical_Methods(self, self.display)

        self.bottom_panel.grid(row=0, column=0, columnspan=3, padx=50, pady=10)
        self.numerical_methods.grid(row=1, column=0, padx=50, pady=10)
        self.numeric_keypad.grid(row=1, column=1, padx=50, pady=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)


class Bottom_Panel(customtkinter.CTkFrame):
    def __init__(self, master, display, display_matrix):
        super().__init__(master)
        self.display = display 
        self.display_matrix = display_matrix 

        matrixButton = customtkinter.CTkButton(self, width=100, height=25, text="Añadir matrix", font=("Arial", 20), command=self.add_matrix)
        acButton = customtkinter.CTkButton(self, width=100, height=25, text="Borrar todo", font=("Arial", 20), command=self.delete_all)
        ceButton = customtkinter.CTkButton(self, width=100, height=25, text="⬅", font=("Arial", 20), command=self.delete_item)

        matrixButton.grid(row=0, column=0, padx=60, pady=5, sticky="nsew")
        acButton.grid(row=0, column=1, padx=60, pady=5, sticky="nsew")
        ceButton.grid(row=0, column=3, padx=60, pady=5, sticky="nsew")

    def add_matrix(self):
        self.display_matrix.add_matrix()

    def delete_all(self):
        self.display.delete_all_items()

    def delete_item(self):
        self.display.delete_items()


class Numeric_Keypad(customtkinter.CTkFrame):
    def __init__(self, master, display):
        super().__init__(master)
        self.display = display

        numbers = [
            ('AC', 0, 0), ('(', 0, 1), (')', 0, 2), ('%', 0, 4),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('x', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 4),
            ('0', 4, 0), ('.', 4, 1), (' ', 4, 2), ('=', 4, 4),
        ]

        for (value, row, column) in numbers:
            number = customtkinter.CTkButton(self, text=value, width=60, height=30, font=("Arial", 20),
                                             command=lambda x=value: self.update_number(x))
            number.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")



    def update_number(self, value):
        if value == "=":
            operation_str = self.display.master.operation.strip()
            if not operation_str:
                print("no operation entered")
                return
            
            matrix_dict = {}
            for matrix_entry in self.display.master.matrix_list:
                matrix_dict.update(matrix_entry)

            if operation_str.startswith(("Det(", "Inv(")):
                try:
                    func_part, matrix_part = operation_str.split("(", 1)
                    func_name = func_part.strip()
                    matrix_name = matrix_part.replace(")", "").strip()

                    if matrix_name not in matrix_dict:
                        print(f"Matrix '{matrix_name}' not found")
                        return

                    matrix = matrix_dict[matrix_name]  

                    if func_name == "Det":
                        from ..matrix_operations.matrix_ops import determinant
                        det = determinant(matrix)
                        print(f"Determinante de {matrix_name}: {det}")

                        result_name = f"Det({matrix_name})"
                        result_matrix = [[det]]

                    elif func_name == "Inv":
                        from ..matrix_operations.matrix_ops import inverse
                        inv = inverse(matrix)
                        print(f"Inversa de {matrix_name}:")
                        for row in inv:
                            print(row)
                        result_name = f"Inv({matrix_name})"
                        result_matrix = inv

                    else:
                        print(f"not support func: {func_name}")
                        return

                    self.display.master.display_matrix.add_matrix_result(
                        result_name,
                        result_matrix
                    )

                except Exception as e:
                    print(f"format error: Details: {e}")

            else:
                tokens = operation_str.split()
                if len(tokens) != 3:
                    print("invalid format. Examples: 'A + B' o '2 x A'")
                    return

                try:
                    scalar = float(tokens[0])
                    op = tokens[1]
                    matrix_name = tokens[2]

                    if op != 'x':
                        print("invalid operator. Use 'X' for scalar.")
                        return

                    if matrix_name not in matrix_dict:
                        print(f"matrix '{matrix_name}' not found")
                        return

                    matrix = matrix_dict[matrix_name]
                    result = scalar_multiply(scalar, matrix)
                    print("Result (scalar X matrix):")
                    for row in result:
                        print(row)

                except ValueError:
                    matrix1_name, op, matrix2_name = tokens

                    if matrix1_name not in matrix_dict:
                        print(f"matrix '{matrix1_name}' not found")
                        return
                    if matrix2_name not in matrix_dict:
                        print(f"matrix '{matrix2_name}' not found")
                        return

                    matrix1 = matrix_dict[matrix1_name]
                    matrix2 = matrix_dict[matrix2_name]

                    operator_map = {
                        'x': multiply,
                        '+': add,
                        '-': subtract,
                    }

                    if op not in operator_map:
                        print(f"Operator not supported: {op}")
                        return

                    try:
                        result = operator_map[op](matrix1, matrix2)
                        if result is None:
                            print(f"The operation {op} dont work.")
                            return
                        print("Result:")
                        for row in result:
                            print(row)
                    except ValueError as e:
                        print(f"Error: {e}")

        else:
            self.display.update_items(value)



class Numerical_Methods(customtkinter.CTkFrame):
    def __init__(self, master, display):
        super().__init__(master)
        self.display = display

        methods = [
            ('A', 0, 0), ('B', 0, 1), ('C', 0, 2),
            ('D', 1, 0), ('F', 1, 1), ('H', 1, 2),
            ('Det', 2, 0), ('Inv', 2, 1), ('Tras', 2, 2),
        ]

        for (funtion, row, column) in methods:
            method = customtkinter.CTkButton(self, text=funtion, width=60, height=30, font=("Arial", 20),
                                             command=lambda x=funtion: self.update_numerical(x))
            method.grid(row=row, column=column, padx=5, pady=10, sticky="nsew")


    def update_numerical(self, operation):
        if operation in ["Det", "Inv", "Tras"]:
            self.display.update_items(operation + "(")

        else:
            self.display.update_items(operation)
        print(f"numeric method: {operation}")

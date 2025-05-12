import customtkinter
from ..matrix_operations.matrix_ops import add, subtract, multiply, scalar_multiply, determinant, inverse, transpose


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
            (' ', 0, 0), ('(', 0, 1), (')', 0, 2), (' ', 0, 4),
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
                
                self.display.master.show_temporal_message("Debes ingresar primero una operación")
                
                return

            matrix_dict = {}
            for matrix_entry in self.display.master.matrix_list:
                matrix_dict.update(matrix_entry)

            if operation_str.count("(") != operation_str.count(")"):
                print("Parentesis no balanceados")
                self.display.master.show_temporal_message("Te faltó '(' o ')'")
                return

            processed_tokens = []
            temp_matrices = {}
            i = 0
            tokens = operation_str.split()
            
            while i < len(tokens):
                token = tokens[i]
                
                if token.startswith("Det("):
                    j = i
                    matrix_name_parts = []
                    while j < len(tokens) and ")" not in tokens[j]:
                        matrix_name_parts.append(tokens[j].replace("Det(", "").strip())
                        j += 1

                    if j < len(tokens):
                        matrix_name_parts.append(tokens[j].replace(")", "").strip())
                    matrix_name = " ".join(matrix_name_parts).replace("Det(", "").strip()
                    matrix_name = matrix_name.replace(" ", "")  
                    
                    if not matrix_name or matrix_name not in matrix_dict:
                        print(f"matrix '{matrix_name}' not found")
                        result = f"matrix '{matrix_name}' no fue encontrada, si la asignaste tienes que guardarlo"
                        self.display.master.show_temporal_message(result)
                        return
                    
                    det = determinant(matrix_dict[matrix_name])
                    processed_tokens.append(str(det))
                    i = j + 1  
                
                elif token.startswith("Inv("):
                    j = i
                    matrix_name_parts = []

                    while j < len(tokens) and ")" not in tokens[j]:
                        matrix_name_parts.append(tokens[j].replace("Inv(", "").strip())
                        j += 1

                    if j < len(tokens):
                        matrix_name_parts.append(tokens[j].replace(")", "").strip())
                    matrix_name = " ".join(matrix_name_parts).replace("Inv(", "").strip()
                    matrix_name = matrix_name.replace(" ", "")  
                    
                    if not matrix_name or matrix_name not in matrix_dict:
                        print(f"matrix '{matrix_name}' not found")
                        result = f"matrix '{matrix_name}' no fue encontrada, si la creaste tienes que guardarla"
                        self.display.master.show_temporal_message(result)
                        return
                    

                    try:
                        inv = inverse(matrix_dict[matrix_name])
                        temp_key = f"__INV_{matrix_name}__"
                        temp_matrices[temp_key] = inv
                        processed_tokens.append(temp_key)

                    except Exception as e:

                        print(f"error in Inv({matrix_name}): {str(e)}")
                        result = f"error en Inv({matrix_name}): {str(e)}"
                        self.display.master.show_temporal_message(result)
                        return
                    i = j + 1 

                elif token.startswith("Tras("):
                    j = i
                    matrix_name_parts = []
                    while j < len(tokens) and ")" not in tokens[j]:
                        matrix_name_parts.append(tokens[j].replace("Tras(", "").strip())
                        j += 1
                    if j < len(tokens):
                        matrix_name_parts.append(tokens[j].replace(")", "").strip())
                    matrix_name = " ".join(matrix_name_parts).replace("Tras(", "").strip()
                    matrix_name = matrix_name.replace(" ", "") 
                    
                    if not matrix_name or matrix_name not in matrix_dict:
                        print(f"Matriz '{matrix_name}' no encontrada")
                        result = f"Matriz '{matrix_name}' no fue encontrada; guárdala primero"
                        self.display.master.show_temporal_message(result)
                        return
                    
                    try:
                        matrix = matrix_dict[matrix_name]
                        tras = transpose(matrix)
                        temp_key = f"__TRAS_{matrix_name}__"
                        temp_matrices[temp_key] = tras
                        processed_tokens.append(temp_key)
                    except Exception as e:
                        print(f"Error en Tras({matrix_name}): {str(e)}")
                        result = f"Error en Tras({matrix_name}): {str(e)}"
                        self.display.master.show_temporal_message(result)
                        return
                    i = j + 1
                
                else:
                    processed_tokens.append(token)
                    i += 1

            matrix_dict.update(temp_matrices)

            if len(processed_tokens) == 1:
                result = None
                token = processed_tokens[0]
                
                try:
                    scalar = float(token)
                    result = [[scalar]]  

                except ValueError:
                    if token in matrix_dict:
                        result = matrix_dict[token]
                    else:
                        print(f"element '{token}' not id")
                        result = f"elemento '{token}' no reconocido"
                        self.display.master.show_temporal_message(result)
                        return
                
                print("Result:")
                for row in result:
                    print(row)
                
                self.display.master.display_matrix.add_matrix_result(
                    operation_str,
                    result
                )
                return


            terms = []
            current_term = []

            for token in processed_tokens:
                if token in ('+', '-'):
                    if current_term:
                        terms.append(current_term)
                        terms.append(token)
                        current_term = []
                else:
                    current_term.append(token)
            if current_term:
                terms.append(current_term)

            processed_terms = []
            for term in terms:
                if isinstance(term, list):
                    term_result = None
                    i = 0
                    while i < len(term):
                        element = term[i]
                        
                        if element == 'x':
                            i += 1
                            continue 
                        
                        try:
                            scalar = float(element)
                            if i + 1 < len(term) and term[i + 1] == 'x' and i + 2 < len(term):
                                matrix_name = term[i + 2]
                                if matrix_name not in matrix_dict:
                                    print(f"matrix '{matrix_name}' not found")
                                    result = f"matrix '{matrix_name}' no fue encontrada, si la creaste tienes que guardarla"
                                    self.display.master.show_temporal_message(f"Matriz '{matrix_name}' no fue encontrada; guárdala primero")
                                    return
                                matrix = matrix_dict[matrix_name]

                                if term_result is None:
                                    term_result = scalar_multiply(scalar, matrix)
                                else:
                                    term_result = multiply(term_result, scalar_multiply(scalar, matrix))
                                i += 3

                            else:
                                term_result = scalar if term_result is None else term_result * scalar
                                i += 1

                        except ValueError:
                            if element not in matrix_dict:
                                print(f"matrix '{element}' not found")
                                result = f"matrix '{element}' no fue encontrada; guárdala primero"
                                self.display.master.show_temporal_message(result)
                                return
                            matrix = matrix_dict[element]

                            if term_result is None:
                                term_result = matrix
                            else:
                                if len(term_result[0]) != len(matrix):
                                    self.display.master.show_temporal_message(
                                        "Error: columnas de la primera matriz deben ser iguales a filas de la segunda."
                                    )
                                    return

                                term_result = multiply(term_result, matrix)

                            i += 1
                    processed_terms.append(term_result)


                else:
                    processed_terms.append(term)  


            if not processed_terms:
                print("void op")
                self.display.master.show_temporal_message("Operación vacía o mal formada")
                return
            
            result = processed_terms[0]
            for i in range(1, len(processed_terms)):
                if isinstance(processed_terms[i], str):
                    operator = processed_terms[i]
                    next_term = processed_terms[i + 1]

                    if operator == '+':
                        result = add(result, next_term)

                    elif operator == '-':
                        result = subtract(result, next_term)

                    else:
                        print(f"operator not supported: {operator}")
                        result = f"La operacion '{operator}' no es soportada"
                        self.display.master.show_temporal_message(result)
                        return

            print("Final Result:")
            for row in result:
                print(row)
            
            self.display.master.display_matrix.add_matrix_result(
                operation_str,
                result
            )

        else:
            self.display.update_items(value)



class Numerical_Methods(customtkinter.CTkFrame):
    def __init__(self, master, display):
        super().__init__(master)
        self.display = display

        methods = [
            ('A', 0, 0), ('B', 0, 1), ('C', 0, 2),
            ('D', 1, 0), ('E', 1, 1), ('F', 1, 2),
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

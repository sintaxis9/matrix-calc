# Importa la biblioteca customtkinter para crear interfaces gráficas personalizadas.
import customtkinter


# Importa funciones de operaciones de matrices desde el módulo matrix_ops.
from ..matrix_operations.matrix_ops import add, subtract, multiply, scalar_multiply, determinant, inverse


class Operations_Panel(customtkinter.CTkFrame):
    """
    Clase que representa un panel de operaciones en la interfaz gráfica de usuario.
    Hereda de CTkFrame de la biblioteca customtkinter.
    """
    
    def __init__(self, master, display, display_matrix):
        """
        Inicializa el panel de operaciones.
        
        :param master: El widget padre en el que se colocará este panel.
        :param display: El widget de visualización donde se mostrarán los resultados.
        :param display_matrix: El widget que mostrará la matriz.
        """
        super().__init__(master)  # Llama al constructor de la clase base CTkFrame.
        self.display = display  # Almacena la referencia al widget de visualización.
        self.display_matrix = display_matrix  # Almacena la referencia al widget de la matriz.
        
        # Crea una instancia del panel inferior, que incluye botones y controles adicionales.
        self.bottom_panel = Bottom_Panel(self, self.display, self.display_matrix)
        # Crea una instancia del teclado numérico para la entrada de números.
        self.numeric_keypad = Numeric_Keypad(self, self.display)
        # Crea una instancia de los métodos numéricos para realizar cálculos.
        self.numerical_methods = Numerical_Methods(self, self.display)
        
        # Coloca el panel inferior en la cuadrícula, ocupando 3 columnas y con márgenes.
        self.bottom_panel.grid(row=0, column=0, columnspan=3, padx=50, pady=10)
        # Coloca los métodos numéricos en la cuadrícula.
        self.numerical_methods.grid(row=1, column=0, padx=50, pady=10)
        # Coloca el teclado numérico en la cuadrícula.
        self.numeric_keypad.grid(row=1, column=1, padx=50, pady=10)
        
        # Configura las columnas de la cuadrícula para que tengan un peso igual, permitiendo que se expandan.
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)



class Bottom_Panel(customtkinter.CTkFrame):
    """
    Clase que representa el panel inferior con botones para operaciones.
    """
    
    def __init__(self, master, display, display_matrix):
        """
        Inicializa el panel inferior.
        
        :param master: El widget padre en el que se colocará este panel.
        :param display: El widget de visualización donde se mostrarán los resultados.
        :param display_matrix: El widget que mostrará la matriz.
        """
        super().__init__(master)  # Llama al constructor de la clase base CTkFrame.
        self.display = display  # Almacena la referencia al widget de visualización.
        self.display_matrix = display_matrix  # Almacena la referencia al widget de la matriz.
        
        # Crea botones para agregar matrices, borrar todo y borrar un elemento.
        matrixButton = customtkinter.CTkButton(self, width=100, height=25, text="Añadir matrix", font=("Arial", 20), command=self.add_matrix)
        acButton = customtkinter.CTkButton(self, width=100, height=25, text="Borrar todo", font=("Arial", 20), command=self.delete_all)
        ceButton = customtkinter.CTkButton(self, width=100, height=25, text="⬅", font=("Arial", 20), command=self.delete_item)
        
        # Coloca los botones en la cuadrícula.
        matrixButton.grid(row=0, column=0, padx=60, pady=5, sticky="nsew")
        acButton.grid(row=0, column=1, padx=60, pady=5, sticky="nsew")
        ceButton.grid(row=0, column=2, padx=60, pady=5, sticky="nsew")  # Corrige el índice de columna a 2.
    def add_matrix(self):
        """Llama al método para agregar una matriz."""
        self.display_matrix.add_matrix()
    def delete_all(self):
        """Llama al método para borrar todos los elementos."""
        self.display.delete_all_items()
    def delete_item(self):
        """Llama al método para borrar un elemento específico."""
        self.display.delete_items()



class Numeric_Keypad(customtkinter.CTkFrame):
    """
    Clase que representa un teclado numérico para la entrada de números y operaciones.
    """
    
    def __init__(self, master, display):
        """
        Inicializa el teclado numérico.
        
        :param master: El widget padre en el que se colocará este teclado.
        :param display: El widget de visualización donde se mostrarán los resultados.
        """
        super().__init__(master)  # Llama al constructor de la clase base CTkFrame.
        self.display = display  # Almacena la referencia al widget de visualización.
        
        # Define los botones del teclado numérico y sus posiciones en la cuadrícula.
        numbers = [
            ('AC', 0, 0), ('(', 0, 1), (')', 0, 2), ('%', 0, 4),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('x', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 4),
            ('0', 4, 0), ('.', 4, 1), (' ', 4, 2), ('=', 4, 4),
        ]
        
        # Crea y coloca los botones en la cuadrícula.
        for (value, row, column) in numbers:
            number = customtkinter.CTkButton(self, text=value, width=60, height=30, font=("Arial", 20),
                                             command=lambda x=value: self.update_number(x))
            number.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")
    
    
    
    def update_number(self, value):
        """
        Actualiza el número o realiza una operación según el botón presionado.
        """
        if value == "=":  # Si se presiona el botón de igual.
            operation_str = self.display.master.operation.strip()  # Obtiene la operación actual.
            if not operation_str:
                print("operacion no integrada")  # Mensaje de error si no hay operación.
                return
            
            matrix_dict = {}  # Diccionario para almacenar matrices.
            for matrix_entry in self.display.master.matrix_list:
                matrix_dict.update(matrix_entry)  # Actualiza el diccionario con matrices existentes.
            
            # Verifica si los paréntesis están balanceados.
            if operation_str.count("(") != operation_str.count(")"):
                print("not balanced ()")  # Mensaje de error si no están balanceados.
                return
            
            processed_tokens = []  # Lista para almacenar tokens procesados.
            temp_matrices = {}  # Diccionario para matrices temporales.
            i = 0
            tokens = operation_str.split()  # Divide la operación en tokens.
            
            # Procesa cada token.
            while i < len(tokens):
                token = tokens[i]
                if token.startswith("Det("):  # Si el token es una llamada a determinante.
                    j = i
                    matrix_name_parts = []
                    while j < len(tokens) and ")" not in tokens[j]:  # Obtiene el nombre de la matriz.
                        matrix_name_parts.append(tokens[j].replace("Det(", "").strip())
                        j += 1
                    if j < len(tokens):
                        matrix_name_parts.append(tokens[j].replace(")", "").strip())
                    matrix_name = " ".join(matrix_name_parts).replace("Det(", "").strip()
                    matrix_name = matrix_name.replace(" ", "")  # Limpia espacios.
                    if not matrix_name or matrix_name not in matrix_dict:
                        print(f"matrix '{matrix_name}' not found")  # Mensaje de error si la matriz no se encuentra.
                        return
                    
                    # Calcula el determinante.
                    det = determinant(matrix_dict[matrix_name])
                    processed_tokens.append(str(det))  # Agrega el resultado a los tokens procesados.
                    i = j + 1  # Avanza el índice.
                elif token.startswith("Inv("):  # Si el token es una llamada a inversa.
                    j = i
                    matrix_name_parts = []
                    while j < len(tokens) and ")" not in tokens[j]:  # Obtiene el nombre de la matriz.
                        matrix_name_parts.append(tokens[j].replace("Inv(", "").strip())
                        j += 1
                    if j < len(tokens):
                        matrix_name_parts.append(tokens[j].replace(")", "").strip())
                    matrix_name = " ".join(matrix_name_parts).replace("Inv(", "").strip()
                    matrix_name = matrix_name.replace(" ", "")  # Limpia espacios.
                    if not matrix_name or matrix_name not in matrix_dict:
                        print(f"matrix '{matrix_name}' not found")  # Mensaje de error si la matriz no se encuentra.
                        return
                    
                    try:
                        inv = inverse(matrix_dict[matrix_name])  # Calcula la inversa.
                        temp_key = f"__INV_{matrix_name}__"  # Crea una clave temporal.
                        temp_matrices[temp_key] = inv  # Almacena la matriz inversa.
                        processed_tokens.append(temp_key)  # Agrega la clave temporal a los tokens procesados.
                    except Exception as e:
                        print(f"error in Inv({matrix_name}): {str(e)}")  # Mensaje de error si falla la inversa.
                        return
                    
                    i = j + 1  # Avanza el índice.
                else:
                    processed_tokens.append(token)  # Agrega el token a los procesados.
                    i += 1  # Avanza el índice.
            
            # Actualiza el diccionario de matrices con las temporales.
            matrix_dict.update(temp_matrices)
            
            # Si solo hay un token procesado, maneja el resultado.
            if len(processed_tokens) == 1:
                result = None
                token = processed_tokens[0]
                try:
                    scalar = float(token)  # Intenta convertir el token a un escalar.
                    result = [[scalar]]  # Crea una matriz con el escalar.
                except ValueError:
                    if token in matrix_dict:
                        result = matrix_dict[token]  # Obtiene la matriz del diccionario.
                    else:
                        print(f"element '{token}' not found")  # Mensaje de error si no se encuentra el elemento.
                        return
                
                print("Result:")  # Imprime el resultado.
                for row in result:
                    print(row)
                self.display.master.display_matrix.add_matrix_result(operation_str, result)  # Agrega el resultado a la visualización.
                return
            
            # Procesa términos de la operación.
            terms = []
            current_term = []
            for token in processed_tokens:
                if token in ('+', '-'):
                    if current_term:
                        terms.append(current_term)  # Agrega el término actual a la lista de términos.
                        terms.append(token)  # Agrega el operador.
                        current_term = []  # Reinicia el término actual.
                else:
                    current_term.append(token)  # Agrega el token al término actual.
            if current_term:
                terms.append(current_term)  # Agrega el último término si existe.
            
            processed_terms = []  # Lista para almacenar términos procesados.
            for term in terms:
                if isinstance(term, list):  # Si el término es una lista.
                    term_result = None
                    i = 0
                    while i < len(term):
                        element = term[i]
                        if element == 'x':  # Ignora el operador de multiplicación.
                            i += 1
                            continue
                        try:
                            scalar = float(element)  # Intenta convertir a escalar.
                            if i + 1 < len(term) and term[i + 1] == 'x' and i + 2 < len(term):
                                matrix_name = term[i + 2]  # Obtiene el nombre de la matriz.
                                if matrix_name not in matrix_dict:
                                    print(f"matrix '{matrix_name}' not found")  # Mensaje de error si no se encuentra la matriz.
                                    return
                                matrix = matrix_dict[matrix_name]  # Obtiene la matriz.
                                if term_result is None:
                                    term_result = scalar_multiply(scalar, matrix)  # Multiplica el escalar por la matriz.
                                else:
                                    term_result = multiply(term_result, scalar_multiply(scalar, matrix))  # Multiplica el resultado acumulado.
                                i += 3  # Avanza el índice.
                            else:
                                term_result = scalar if term_result is None else term_result * scalar  # Acumula el escalar.
                                i += 1
                        except ValueError:
                            if element not in matrix_dict:
                                print(f"matrix '{element}' not found")  # Mensaje de error si no se encuentra la matriz.
                                return
                            matrix = matrix_dict[element]  # Obtiene la matriz.
                            if term_result is None:
                                term_result = matrix  # Asigna la matriz al resultado si es el primer término.
                            else:
                                term_result = multiply(term_result, matrix)  # Multiplica el resultado acumulado.
                            i += 1
                    processed_terms.append(term_result)  # Agrega el resultado del término procesado.
                else:
                    processed_terms.append(term)  # Agrega el operador.
            
            if not processed_terms:
                print("void operation")  # Mensaje de error si no hay términos procesados.
                return
            
            # Realiza la operación final con los términos procesados.
            result = processed_terms[0]  # Inicializa el resultado con el primer término.
            for i in range(1, len(processed_terms)):
                if isinstance(processed_terms[i], str):
                    operator = processed_terms[i]  # Obtiene el operador.
                    next_term = processed_terms[i + 1]  # Obtiene el siguiente término.
                    if operator == '+':
                        result = add(result, next_term)  # Suma los términos.
                    elif operator == '-':
                        result = subtract(result, next_term)  # Resta los términos.
                    else:
                        print(f"operator not supported: {operator}")  # Mensaje de error si el operador no es soportado.
                        return
            
            print("Final Result:")  # Imprime el resultado final.
            for row in result:
                print(row)
            self.display.master.display_matrix.add_matrix_result(operation_str, result)  # Agrega el resultado a la visualización.
        else:
            self.display.update_items(value)  # Actualiza la visualización con el valor del botón presionado.



class Numerical_Methods(customtkinter.CTkFrame):
    """
    Clase que representa un panel con métodos numéricos.
    """
    
    def __init__(self, master, display):
        """
        Inicializa el panel de métodos numéricos.
        
        :param master: El widget padre en el que se colocará este panel.
        :param display: El widget de visualización donde se mostrarán los resultados.
        """
        super().__init__(master)  # Llama al constructor de la clase base CTkFrame.
        self.display = display  # Almacena la referencia al widget de visualización.
        
        # Define los botones para los métodos numéricos y sus posiciones en la cuadrícula.
        methods = [
            ('A', 0, 0), ('B', 0, 1), ('C', 0, 2),
            ('D', 1, 0), ('F', 1, 1), ('H', 1, 2),
            ('Det', 2, 0), ('Inv', 2, 1), ('Tras', 2, 2),
        ]
        
        # Crea y coloca los botones en la cuadrícula.
        for (function, row, column) in methods:
            method = customtkinter.CTkButton(self, text=function, width=60, height=30, font=("Arial", 20),
                                             command=lambda x=function: self.update_numerical(x))
            method.grid(row=row, column=column, padx=5, pady=10, sticky="nsew")


    def update_numerical(self, operation):
        """
        Actualiza la visualización con el método numérico seleccionado.
        """
        if operation in ["Det", "Inv", "Tras"]:
            self.display.update_items(operation + "(")  # Indica que se está comenzando una operación numérica.
        else:
            self.display.update_items(operation)  # Actualiza la visualización con la operación.
        print(f"numeric method: {operation}")  # Imprime el método numérico seleccionado.
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
            btn = customtkinter.CTkButton(
                self,
                text=value,
                width=60, height=30,
                font=("Arial", 20),
                command=lambda x=value: self.update_number(x)
            )
            btn.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")

    def update_number(self, value):
        # Si no es "=", simplemente actualizamos el display
        if value != "=":
            self.display.update_items(value)
            return

        # Referencia al widget de operaciones y limpiamos pasos anteriores
        op_disp = self.display.master.operation_label
        op_disp.clear()

        # Acumulador de pasos de cada suboperación
        operations_steps: list[list[tuple[str, list[list[float]]]]] = []

        # La cadena completa de la operación
        operation_str = self.display.master.operation.strip()
        if not operation_str:
            self.display.master.show_temporal_message("Debes ingresar primero una operación")
            return

        # Diccionario de matrices guardadas
        matrix_dict = {}
        for entry in self.display.master.matrix_list:
            matrix_dict.update(entry)

        # Paréntesis balanceados
        if operation_str.count("(") != operation_str.count(")"):
            self.display.master.show_temporal_message("Te faltó '(' o ')'")
            return

        # Tokenizamos la operación
        tokens = operation_str.split()
        processed_tokens: list[str] = []
        temp_matrices: dict[str, list[list[float]]] = {}
        i = 0

        # Primera pasada: Det(), Inv() y Tras()
        while i < len(tokens):
            token = tokens[i]

            # Determinante
            if token.startswith("Det("):
                j = i
                name_parts = []
                while j < len(tokens) and ")" not in tokens[j]:
                    name_parts.append(tokens[j].replace("Det(", ""))
                    j += 1
                if j < len(tokens):
                    name_parts.append(tokens[j].replace(")", ""))
                name = "".join(name_parts).strip()

                if name not in matrix_dict:
                    self.display.master.show_temporal_message(
                        f"Matriz '{name}' no encontrada; guárdala primero"
                    )
                    return

                det_value, det_steps = determinant(matrix_dict[name])
                processed_tokens.append(str(det_value))
                operations_steps.append(det_steps)
                i = j + 1
                continue

            # Inversa (con manejo de matriz singular)
            elif token.startswith("Inv("):
                j = i
                name_parts = []
                while j < len(tokens) and ")" not in tokens[j]:
                    name_parts.append(tokens[j].replace("Inv(", ""))
                    j += 1
                if j < len(tokens):
                    name_parts.append(tokens[j].replace(")", ""))
                name = "".join(name_parts).strip()

                if name not in matrix_dict:
                    self.display.master.show_temporal_message(
                        f"Matriz '{name}' no encontrada; guárdala primero"
                    )
                    return

                try:
                    inv_matrix, inv_steps = inverse(matrix_dict[name])
                except ValueError:
                    # inverse() lanza ValueError si la matriz es singular
                    self.display.master.show_temporal_message(
                        f"La matriz '{name}' no tiene inversa"
                    )
                    return

                key = f"__INV_{name}__"
                temp_matrices[key] = inv_matrix
                processed_tokens.append(key)
                operations_steps.append(inv_steps)
                i = j + 1
                continue

            # Traspuesta
            elif token.startswith("Tras("):
                j = i
                name_parts = []
                while j < len(tokens) and ")" not in tokens[j]:
                    name_parts.append(tokens[j].replace("Tras(", ""))
                    j += 1
                if j < len(tokens):
                    name_parts.append(tokens[j].replace(")", ""))
                name = "".join(name_parts).strip()

                if name not in matrix_dict:
                    self.display.master.show_temporal_message(
                        f"Matriz '{name}' no encontrada; guárdala primero"
                    )
                    return

                tras_matrix, tras_steps = transpose(matrix_dict[name])
                key = f"__TRAS_{name}__"
                temp_matrices[key] = tras_matrix
                processed_tokens.append(key)
                operations_steps.append(tras_steps)
                i = j + 1
                continue

            # Cualquier otro token
            else:
                processed_tokens.append(token)
                i += 1

        # Agregamos matrices temporales al diccionario
        matrix_dict.update(temp_matrices)

        # Caso de un solo token (número o matriz)
        if len(processed_tokens) == 1:
            token = processed_tokens[0]
            try:
                scalar = float(token)
                result = [[scalar]]
            except ValueError:
                if token in matrix_dict:
                    result = matrix_dict[token]
                else:
                    self.display.master.show_temporal_message(
                        f"Elemento '{token}' no reconocido"
                    )
                    return

            self.display.master.display_matrix.add_matrix_result(operation_str, result)
            if operations_steps:
                op_disp.show_steps(operations_steps)
            return

        # === 2ª pasada: Escalar×Matriz y Matriz×Matriz ===
        terms: list = []
        current_term: list = []
        for tok in processed_tokens:
            if tok in ('+', '-'):
                terms.append(current_term)
                terms.append(tok)
                current_term = []
            else:
                current_term.append(tok)
        if current_term:
            terms.append(current_term)

        processed_terms: list = []
        for term in terms:
            if isinstance(term, list):
                term_result = None
                idx_term = 0
                while idx_term < len(term):
                    elem = term[idx_term]

                    # Escalar * Matriz
                    try:
                        scalar = float(elem)
                        if (idx_term + 1 < len(term) and term[idx_term+1] == 'x'
                                and idx_term + 2 < len(term)):
                            m_name = term[idx_term+2]
                            if m_name not in matrix_dict:
                                self.display.master.show_temporal_message(
                                    f"Matriz '{m_name}' no encontrada; guárdala primero"
                                )
                                return
                            scaled, steps_s = scalar_multiply(scalar, matrix_dict[m_name])

                            if term_result is None:
                                term_result = scaled
                            else:
                                # Validación de dimensiones
                                fA, cA = len(term_result), len(term_result[0])
                                fB, cB = len(scaled), len(scaled[0])
                                if cA != fB:
                                    self.display.master.show_temporal_message(
                                        f"No se pueden multiplicar matrices de tamaño "
                                        f"{fA}×{cA} y {fB}×{cB}"
                                    )
                                    return
                                term_result, pasos_m = multiply(term_result, scaled)
                                operations_steps.append(pasos_m)

                            operations_steps.append(steps_s)
                            idx_term += 3
                            continue
                    except ValueError:
                        pass

                    # Matriz × Matriz
                    if elem in matrix_dict:
                        mat = matrix_dict[elem]
                        if term_result is None:
                            term_result = mat
                        else:
                            # Validación de dimensiones
                            fA, cA = len(term_result), len(term_result[0])
                            fB, cB = len(mat), len(mat[0])
                            if cA != fB:
                                self.display.master.show_temporal_message(
                                    f"No se pueden multiplicar matrices de tamaño "
                                    f"{fA}×{cA} y {fB}×{cB}"
                                )
                                return
                            term_result, pasos_m = multiply(term_result, mat)
                            operations_steps.append(pasos_m)

                        idx_term += 1
                    else:
                        idx_term += 1

                processed_terms.append(term_result)
            else:
                # operador '+' o '-'
                processed_terms.append(term)

        # === Sumas y restas finales con validación de dimensiones ===
        result = processed_terms[0]
        idx_res = 1
        while idx_res < len(processed_terms):
            op = processed_terms[idx_res]
            nxt = processed_terms[idx_res + 1]
            fA, cA = len(result), len(result[0])
            fB, cB = len(nxt), len(nxt[0])

            if op == '+':
                if fA != fB or cA != cB:
                    self.display.master.show_temporal_message(
                        f"No se pueden sumar matrices de tamaño {fA}×{cA} y {fB}×{cB}"
                    )
                    return
                result, pasos_a = add(result, nxt)
                operations_steps.append(pasos_a)

            elif op == '-':
                if fA != fB or cA != cB:
                    self.display.master.show_temporal_message(
                        f"No se pueden restar matrices de tamaño {fA}×{cA} y {fB}×{cB}"
                    )
                    return
                result, pasos_s = subtract(result, nxt)
                operations_steps.append(pasos_s)

            idx_res += 2

        # Mostramos el resultado y, si hay pasos, los desplegamos
        self.display.master.display_matrix.add_matrix_result(operation_str, result)
        if operations_steps:
            op_disp.show_steps(operations_steps)


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


class StepByStepWindow(customtkinter.CTkToplevel):
    window_count = 0
    instances: list["StepByStepWindow"] = []

    def __init__(self, parent, steps):
        StepByStepWindow.window_count += 1
        super().__init__(parent)
        StepByStepWindow.instances.append(self)

        self.title(f"Pasos de la Operación #{StepByStepWindow.window_count}")
        self.geometry("600x400")


class StepByStepWindow(customtkinter.CTkToplevel):
    window_count = 0
    instances: list["StepByStepWindow"] = []

    def __init__(self, parent, steps):
        StepByStepWindow.window_count += 1
        super().__init__(parent)
        StepByStepWindow.instances.append(self)

        self.title(f"Pasos de la Operación #{StepByStepWindow.window_count}")
        self.geometry("600x400")
        
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True)
        
        for desc, matrix in steps:
            step_label = customtkinter.CTkLabel(
                self.scrollable_frame, 
                text=desc + "\n" + self.format_matrix(matrix),
                font=("Courier New", 12)
            )
            step_label.pack(padx=10, pady=5, anchor="w")

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        if self in StepByStepWindow.instances:
            StepByStepWindow.instances.remove(self)
        super().destroy()

    def format_matrix(self, matrix):
        return "\n".join(
            "[" + "  ".join(f"{x:.2f}" for x in row) + "]"
            for row in matrix
        )


        self.scrollable_frame.pack(fill="both", expand=True)
        
        for desc, matrix in steps:
            step_label = customtkinter.CTkLabel(
                self.scrollable_frame, 
                text=desc + "\n" + self.format_matrix(matrix),
                font=("Courier New", 12)
            )
            step_label.pack(padx=10, pady=5, anchor="w")

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        if self in StepByStepWindow.instances:
            StepByStepWindow.instances.remove(self)
        super().destroy()

    def format_matrix(self, matrix):
        return "\n".join(
            "[" + "  ".join(f"{x:.2f}" for x in row) + "]"
            for row in matrix
        )


# matrix_operations/evaluator.py
from .matrix_ops import add, subtract, multiply
from .validations import have_same_dimensions, is_multipliable

def get_matrix_by_name(matrix_list, name):
    for matrix_dict in matrix_list:
        if name in matrix_dict:
            return matrix_dict[name]
    return None

def evaluate_operation(operation_str, matrix_list):
    tokens = operation_str.strip().split()
    if len(tokens) != 3:
        raise ValueError("Formato inválido. Usa: 'A operador B'")
    
    operand1, operator, operand2 = tokens

    matrix1 = get_matrix_by_name(matrix_list, operand1)
    matrix2 = get_matrix_by_name(matrix_list, operand2)

    if matrix1 is None:
        raise ValueError(f"Matriz '{operand1}' no encontrada")
    if matrix2 is None:
        raise ValueError(f"Matriz '{operand2}' no encontrada")

    operator_map = {
        '+': add,
        '-': subtract,
        'x': multiply,
    }

    if operator not in operator_map:
        raise ValueError(f"Operador '{operator}' no soportado")
    
    operation_func = operator_map[operator]

    if operator in ('+', '-'):
        if not have_same_dimensions(matrix1, matrix2):
            raise ValueError("Dimensiones no coinciden")
    elif operator == 'x':
        if len(matrix1[0]) != len(matrix2):
            raise ValueError("No se pueden multiplicar")

    return operation_func(matrix1, matrix2)
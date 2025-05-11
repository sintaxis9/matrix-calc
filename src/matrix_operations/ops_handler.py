from .core_utils import get_matrix_by_name, format_matrix_result
from . import matrix_ops

def execute_operation(operation_str, matrix_list):
    try:
        elements = operation_str.split()
        stack = []
        
        for elem in elements:
            if elem in ['+', '-', '*']:
                if len(stack) < 2:
                    raise ValueError("Operación inválida: faltan operandos")
                b = stack.pop()
                a = stack.pop()
                
                mat_a = get_matrix_by_name(a, matrix_list) if isinstance(a, str) else a
                mat_b = get_matrix_by_name(b, matrix_list) if isinstance(b, str) else b
                
                if elem == '+':
                    result = matrix_ops.add(mat_a, mat_b)
                elif elem == '-':
                    result = matrix_ops.subtract(mat_a, mat_b)
                elif elem == '*':
                    result = matrix_ops.multiply(mat_a, mat_b)
                
                stack.append(result)
                
            elif elem.startswith('inv('):
                mat_name = elem[4:-1]
                matrix = get_matrix_by_name(mat_name, matrix_list)
                stack.append(matrix_ops.inverse(matrix))
                
            else:  
                stack.append(elem)
        
        final_result = stack.pop()
        return format_matrix_result(final_result) if isinstance(final_result, list) else final_result
    
    except Exception as e:
        return f"Error: {str(e)}"
def is_square(matrix): # verifica si una matriz es cuadrada
    return bool(matrix) and all(len(row) == len(matrix) for row in matrix)
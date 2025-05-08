# Importa la función is_square desde el módulo core_utils
from core_utils import is_square

# Verifica si una matriz es la matriz identidad
def is_identity(matrix):
    # La matriz debe ser cuadrada para ser una identidad
    if not is_square(matrix):
        return False

    # Tamaño de la matriz (n x n)
    n = len(matrix)

    # Recorre cada celda de la matriz
    for i in range(n):
        for j in range(n):
            # En la diagonal principal (i == j), debe haber un 1
            # Fuera de la diagonal (i != j), debe haber un 0
            if (i == j and matrix[i][j] != 1) or (i != j and matrix[i][j] != 0):
                return False

    # Si pasa todas las condiciones, es una matriz identidad
    return True


# Verifica si dos matrices pueden ser multiplicadas
def is_multipliable(matrix1, matrix2):
    # Verifica que ambas matrices existan y que el número de columnas
    # de la primera sea igual al número de filas de la segunda
    return bool(matrix1 and matrix2 and len(matrix1[0]) == len(matrix2))


# Verifica si una matriz cuadrada es inversible
def is_inversible(matrix):
    # Una matriz solo puede ser inversible si es cuadrada
    if not is_square(matrix):
        return False

    # Importa la función determinant desde otro módulo
    from matrix_ops import determinant

    # Calcula el determinante
    det = determinant(matrix)

    # Una matriz es inversible si su determinante no es cero ni indefinido (None)
    return det is not None and det != 0

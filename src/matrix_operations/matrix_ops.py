from core_utils import is_square
from validations import is_multipliable

def add(matrix1, matrix2):
    """Suma de dos matrices elemento por elemento."""
    # Verifica que ambas matrices sean cuadradas y del mismo tamaño
    if not (is_square(matrix1) and is_square(matrix2)) or len(matrix1) != len(matrix2):
        return None
    
    n = len(matrix1)
    return [
        [matrix1[i][j] + matrix2[i][j] for j in range(n)]
        for i in range(n)
    ]

def subtract(matrix1, matrix2):
    """Resta de dos matrices elemento por elemento."""
    # Verifica que ambas matrices sean cuadradas y del mismo tamaño
    if not (is_square(matrix1) and is_square(matrix2)) or len(matrix1) != len(matrix2):
        return None
    
    n = len(matrix1)
    return [
        [matrix1[i][j] - matrix2[i][j] for j in range(n)]
        for i in range(n)
    ]

def multiply(matrix1, matrix2):
    """Multiplicacion de dos matrices usando producto matricial."""
    # Verifica si las matrices se pueden multiplicar
    if not is_multipliable(matrix1, matrix2):
        return None
    
    m = len(matrix1)       # Filas de matrix1
    n = len(matrix2[0])    # Columnas de matrix2
    p = len(matrix2)       # Columnas de matrix1 (que debe ser igual a filas de matrix2)

    result = [[0 for _ in range(n)] for _ in range(m)]  # Matriz resultado: m x n

    for i in range(m):          # Recorre filas de matrix1
        for j in range(n):      # Recorre columnas de matrix2
            for k in range(p):  # Recorre la dimensión común (p)
                result[i][j] += matrix1[i][k] * matrix2[k][j]  # Producto punto
    return result

def determinant(matrix):
    if not is_square(matrix):
        return None
    
    n = len(matrix)

    if n == 1:
        return matrix[0][0]
    
    elif n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    det = 0
    for c in range(n):
        sub = [row[:c] + row[c + 1:] for row in matrix[1:]]
        det += ((-1) ** c) * matrix[0][c] * determinant(sub)
    return det

# Ejemplo de uso
A = [[1, 2], 
     [3, 4]]

B = [[5, 6,4], 
     [7, 8,2]]

print("Suma:", add(A, B))
print("Resta:", subtract(A, B))
print("Multiplicación:", multiply(A, B))
print("Determinante:", determinant(A))
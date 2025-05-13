# Importa funciones auxiliares desde el módulo core_utils ubicado en el mismo paquete
from .core_utils import is_square, is_numeric


# Verifica si dos matrices tienen las mismas dimensiones
def have_same_dimensions(matrix1, matrix2):
    # Primero valida que ambas matrices contengan solo valores numéricos
    if not (is_numeric(matrix1) and is_numeric(matrix2)):
        raise ValueError("solo valores numericos")
    
    try:
        # Compara la cantidad de filas y columnas de ambas matrices
        return (
            len(matrix1) == len(matrix2) and  # misma cantidad de filas
            all(len(row1) == len(row2)        # todas las filas tienen misma cantidad de columnas
                for row1, row2 in zip(matrix1, matrix2))
        )
    except Exception:
        # Si ocurre algún error (por ejemplo, si las matrices no son listas de listas bien formadas), retorna False
        return False


# Verifica si una matriz es la matriz identidad
def is_identity(matrix):
    # Verifica que la matriz sea cuadrada y numérica
    if not (is_square(matrix) and is_numeric(matrix)):
        return False

    n = len(matrix)  # número de filas (o columnas, porque es cuadrada)
    for i in range(n):
        for j in range(n):
            # En la diagonal principal debe haber 1, en el resto 0
            if (i == j and matrix[i][j] != 1) or (i != j and matrix[i][j] != 0):
                return False
    return True  # Si pasa todas las comprobaciones, es la identidad


# Verifica si dos matrices son multiplicables
def is_multipliable(matrix1, matrix2):
    # Ambas matrices deben ser numéricas
    if not (is_numeric(matrix1) and is_numeric(matrix2)):
        return False

    # Una matriz A (m×n) se puede multiplicar por una B (n×p) si columnas de A == filas de B
    return bool(matrix1 and matrix2 and len(matrix1[0]) == len(matrix2))


# Verifica si una matriz es invertible
def is_invertible(matrix):
    # La matriz debe ser cuadrada y numérica
    if not (is_square(matrix) and is_numeric(matrix)):
        return False

    # Importa la función para calcular determinantes desde el archivo matrix_ops.py
    from .matrix_ops import determinant

    det = determinant(matrix)  # Calcula el determinante
    return det is not None and det != 0  # Una matriz es invertible si su determinante es distinto de cero

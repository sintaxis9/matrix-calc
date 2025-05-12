# Importa funciones auxiliares para verificar si una matriz es cuadrada y si contiene valores numéricos.
from .core_utils import is_square, is_numeric


def have_same_dimensions(matrix1, matrix2):
    """
    Verifica si dos matrices tienen las mismas dimensiones.
    """
    # Verifica si ambas matrices son numéricas.
    if not (is_numeric(matrix1) and is_numeric(matrix2)):
        raise ValueError("only numeric values!")  # Lanza un error si no son numéricas.
    
    try:
        # Retorna True si ambas matrices tienen el mismo número de filas y las mismas longitudes de filas.
        return (
            len(matrix1) == len(matrix2)  # Comprueba si ambas matrices tienen el mismo número de filas.
            and all(len(row1) == len(row2)  # Verifica que todas las filas de ambas matrices tengan la misma longitud.
                    for row1, row2 in zip(matrix1, matrix2))  # Usa zip para iterar sobre las filas de ambas matrices.
        )
    except Exception:
        return False  # Retorna False si ocurre una excepción.
    

def is_identity(matrix):
    """
    Verifica si una matriz es la matriz identidad.
    """
    # Verifica que la matriz sea cuadrada y numérica.
    if not (is_square(matrix) and is_numeric(matrix)):
        return False  # Retorna False si no lo es.
    n = len(matrix)  # Obtiene el tamaño de la matriz (número de filas o columnas).
    
    # Itera sobre cada elemento de la matriz.
    for i in range(n):
        for j in range(n):
            # Comprueba las condiciones de la matriz identidad.
            if (i == j and matrix[i][j] != 1) or (i != j and matrix[i][j] != 0):
                return False  # Retorna False si alguna condición no se cumple.
    
    return True  # Retorna True si todas las condiciones se cumplen.


def is_multipliable(matrix1, matrix2):
    """
    Verifica si dos matrices son multiplicables.
    """
    # Verifica que ambas matrices sean numéricas.
    if not (is_numeric(matrix1) and is_numeric(matrix2)):
        return False  # Retorna False si no lo son.
    # Retorna True si ambas matrices no están vacías y el número de columnas de la primera es igual al número de filas de la segunda.
    return bool(matrix1 and matrix2 and len(matrix1[0]) == len(matrix2))


def is_invertible(matrix):
    """
    Verifica si una matriz es invertible.
    """
    # Verifica que la matriz sea cuadrada y numérica.
    if not (is_square(matrix) and is_numeric(matrix)):
        return False  # Retorna False si no lo es.
    
    # Importa la función 'determinant' del módulo 'matrix_ops'.
    from .matrix_ops import determinant
    det = determinant(matrix)  # Calcula el determinante de la matriz.
    
    # Retorna True si el determinante no es None y es diferente de 0, lo que indica que la matriz es invertible.
    return det is not None and det != 0
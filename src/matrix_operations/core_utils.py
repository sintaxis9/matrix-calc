def is_numeric(matrix):
    """
    Verifica si todos los elementos de la matriz son números (enteros o flotantes).
    """
    try:
        # Retorna True si todos los elementos de la matriz son instancias de int o float.
        return all(isinstance(x, (int, float)) for row in matrix for x in row)
    except Exception:
        return False  # Retorna False si ocurre cualquier excepción durante la verificación.
    
    
# verifica si la matriz es cuadrada y numérica.   
def is_square(matrix):
    """
    Verifica si la matriz es cuadrada (es decir, tiene el mismo número de filas y columnas).
    """
    # Retorna True si la matriz no está vacía y todas las filas tienen la misma longitud que el número de filas.
    return bool(matrix) and all(len(row) == len(matrix) for row in matrix)
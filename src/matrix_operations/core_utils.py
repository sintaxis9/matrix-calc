# comprueba si la matriz es numérica
def is_numeric(matrix):
    try:
        # Verifica que todos los elementos x en cada fila de la matriz
        # sean enteros (int) o flotantes (float)
        return all(isinstance(x, (int, float)) for row in matrix for x in row)

    except Exception:
        # Si ocurre cualquier error (por ejemplo, si la estructura no es válida),
        # devuelve False
        return False


# comprueba si la matriz es cuadrada
def is_square(matrix):
    # Verifica dos condiciones:
    # 1. Que la matriz no esté vacía (bool(matrix) == True si tiene contenido)
    # 2. Que cada fila tenga la misma longitud que el número de filas (es decir, n x n)
    return bool(matrix) and all(len(row) == len(matrix) for row in matrix)

from copy import deepcopy # Importamos deepcopy para hacer copias profundas de las matrices
from .core_utils import is_square, is_numeric
from .validations import is_multipliable, have_same_dimensions, is_invertible


# Multiplicación de una matriz por un escalar
def scalar_multiply(scalar, matrix):
    # Verifica que el valor escalar sea un número entero o flotante
    if not isinstance(scalar, (int, float)):
        raise ValueError("El escalar debe de ser int o float")

    # Verifica que la matriz sea numérica (solo contenga números)
    if not is_numeric(matrix):
        raise ValueError("La matriz debe de ser numerica")
    
    # Lista para guardar los pasos del proceso con descripciones
    steps: list[tuple[str, list[list[float]]]] = []

    # Guardamos una copia de la matriz original como primer paso
    steps.append(("Matriz original:", deepcopy(matrix)))
    
    # Realizamos la multiplicación del escalar por cada elemento de la matriz
    result = [
        [scalar * val for val in row]  # Multiplicamos cada valor de la fila por el escalar
        for row in matrix              # Recorremos cada fila de la matriz
    ]

    # Guardamos el resultado de la multiplicación como siguiente paso
    steps.append((f"Matriz tras multiplicar por {scalar}:", deepcopy(result)))
    
    # Retornamos la matriz resultante y los pasos realizados
    return result, steps



# suma de matrices
def add(matrix1, matrix2):
    # Verifica que ambas matrices tengan las mismas dimensiones
    if not have_same_dimensions(matrix1, matrix2):
        raise ValueError("Las matrices deben tener las mismas dimensiones")
    
    # Lista para guardar los pasos intermedios con su descripción
    steps: list[tuple[str, list[list[float]]]] = []

    # Guardamos la primera matriz como primer paso
    steps.append(("Matriz A:", deepcopy(matrix1)))

    # Guardamos la segunda matriz como segundo paso
    steps.append(("Matriz B:", deepcopy(matrix2)))
    
    # Inicializamos la matriz resultado
    result: list[list[float]] = []

    # Recorremos las filas
    for i in range(len(matrix1)):
        row = []  # Creamos una nueva fila para el resultado
        # Recorremos las columnas
        for j in range(len(matrix1[0])):
            # Sumamos los elementos correspondientes
            suma = matrix1[i][j] + matrix2[i][j]
            row.append(suma)  # Añadimos el resultado a la fila
        result.append(row)  # Añadimos la fila completa al resultado

        # Guardamos el resultado parcial tras esta fila
        steps.append((f"Resultado tras fila {i+1}:", deepcopy(result)))
    
    # Guardamos el resultado final
    steps.append(("Matriz resultante:", deepcopy(result)))

    # Retornamos la matriz resultado y los pasos
    return result, steps



# resta de matrices
def subtract(matrix1, matrix2):
    # Verifica que ambas matrices tengan las mismas dimensiones (mismo número de filas y columnas)
    if not have_same_dimensions(matrix1, matrix2):
        raise ValueError("Las matrices deben de tener las mismas dimensiones")
    
    # Lista para almacenar los pasos con descripciones (para mostrar el proceso)
    steps: list[tuple[str, list[list[float]]]] = []

    # Guarda la primera matriz como paso inicial
    steps.append(("Matriz A:", deepcopy(matrix1)))

    # Guarda la segunda matriz como paso inicial
    steps.append(("Matriz B:", deepcopy(matrix2)))
    
    # Se inicializa la matriz resultado
    result: list[list[float]] = []

    # Recorremos las filas
    for i in range(len(matrix1)):
        row = []  # Fila temporal para construir la nueva fila resultante
        # Recorremos las columnas
        for j in range(len(matrix1[0])):
            # Se calcula la diferencia elemento a elemento
            diff = matrix1[i][j] - matrix2[i][j]
            row.append(diff)  # Se añade el resultado a la fila
        result.append(row)  # Se añade la fila completa a la matriz resultado
        # Guardamos el paso tras terminar esta fila
        steps.append((f"Resultado tras fila {i+1}:", deepcopy(result)))
    
    # Paso final: se guarda la matriz completa resultante
    steps.append(("Matriz resultante:", deepcopy(result)))

    # Se retorna la matriz resultado y los pasos guardados
    return result, steps



# Multiplicación de matrices
def multiply(matrix1, matrix2):
    # Verificamos si las matrices son multiplicables
    # (es decir, el número de columnas de matrix1 debe ser igual al número de filas de matrix2)
    if not is_multipliable(matrix1, matrix2):
        raise ValueError("Las matrices no son multiplicables")

    # Lista para guardar los pasos intermedios del proceso, útil para mostrar luego
    steps: list[tuple[str, list[list[float]]]] = []

    # Guardamos las matrices originales como parte del historial de pasos
    steps.append(("Matriz A:", deepcopy(matrix1)))
    steps.append(("Matriz B:", deepcopy(matrix2)))

    # m = número de filas de la primera matriz (matrix1)
    # p = número de filas de la segunda matriz (matrix2)
    # n = número de columnas de la segunda matriz (matrix2)
    m = len(matrix1)
    p = len(matrix2)
    n = len(matrix2[0])

    # Creamos una matriz de ceros de tamaño m x n para almacenar el resultado
    result: list[list[float]] = [[0]*n for _ in range(m)]

    # Recorremos cada fila de matrix1
    for i in range(m):
        # Recorremos cada columna de matrix2
        for j in range(n):
            suma = 0  # Inicializamos la suma que irá en la posición (i, j)
            # Recorremos los elementos comunes para hacer el producto escalar
            for k in range(p):
                # Multiplicamos el elemento de la fila i de matrix1 por el de la columna j de matrix2
                suma += matrix1[i][k] * matrix2[k][j]
            # Asignamos el valor calculado a la celda correspondiente del resultado
            result[i][j] = suma
        # Guardamos el resultado parcial después de completar cada fila
        steps.append((f"Resultado tras fila {i+1}:", deepcopy(result)))

    # Guardamos la matriz final resultante
    steps.append(("Matriz resultante:", deepcopy(result)))

    # Devolvemos la matriz resultante y todos los pasos realizados
    return result, steps




# calculo del determinante de una matriz
# Usamos la regla de Laplace para calcular el determinante de una matriz cuadrada
def determinant(matrix):
    # Validamos que la matriz sea cuadrada y que todos sus elementos sean numéricos
    if not (is_square(matrix) and is_numeric(matrix)):
        return None, []  # Si no lo es, regresamos None y una lista vacía de pasos

    # Lista para almacenar los pasos realizados (útil para mostrar visualmente)
    steps: list[tuple[str, list[list[float]]]] = []
    steps.append(("Matriz original para determinante:", deepcopy(matrix)))

    n = len(matrix)  # Tamaño de la matriz (n x n)

    # Caso base: matriz 1x1, su determinante es simplemente su único elemento
    if n == 1:
        det = matrix[0][0]
        steps.append((f"Determinante de 1×1: {det}", [[det]]))
        return det, steps

    # Caso base: matriz 2x2, aplicamos la fórmula directa: ad - bc
    if n == 2:
        a, b = matrix[0]
        c, d = matrix[1]
        det = a * d - b * c
        steps.append((f"Det = {a}×{d} − {b}×{c} = {det}", deepcopy(matrix)))
        return det, steps

    # Caso general: matriz de tamaño n > 2, se aplica expansión por cofactores (Regla de Laplace)
    det = 0  # Inicializamos el determinante

    # Recorremos cada columna de la primera fila (fila 0)
    for c in range(n):
        # Construimos la submatriz eliminando la fila 0 y la columna c
        sub = [row[:c] + row[c+1:] for row in matrix[1:]]
        
        # Calculamos recursivamente el determinante de la submatriz
        sub_det, sub_steps = determinant(sub)
        
        # Guardamos el menor en los pasos
        steps.append((f"Menor eliminando fila 0 y columna {c}:", deepcopy(sub)))

        # Añadimos los pasos internos de la recursión también
        for desc, mtx in sub_steps:
            steps.append((f"  {desc}", deepcopy(mtx)))

        # Calculamos la contribución del cofactor con el signo alternante (-1)^c
        contrib = ((-1) ** c) * matrix[0][c] * sub_det
        
        # Guardamos la contribución de ese cofactor en los pasos
        steps.append((
            f"Contribución cofactor elemento {matrix[0][c]} en (0,{c}): "
            f"(-1)^{c}×{matrix[0][c]}×det(sub) = {contrib}",
            [[contrib]]
        ))

        # Sumamos la contribución al total del determinante
        det += contrib

    # Finalmente, añadimos el resultado total del determinante a los pasos
    steps.append((f"Determinante total: {det}", [[det]]))
    
    # Retornamos el determinante y la lista de pasos
    return det, steps



# Cálculo de la inversa de una matriz
# Usamos el método de eliminación de Gauss-Jordan para encontrar la inversa

def inverse(matrix):
    # Verifica que la matriz sea cuadrada, que todos sus elementos sean numéricos
    # y que sea invertible (determinante distinto de 0)
    if not (is_square(matrix) and is_numeric(matrix) and is_invertible(matrix)):
        raise ValueError("La matriz debe ser cuadrada, numérica e inversible")

    n = len(matrix)  # Dimensión de la matriz (n x n)
    steps = []  # Lista para almacenar los pasos del proceso (útil para mostrar en GUI)

    # Se crea la matriz aumentada [A | I]
    # Por cada fila de la matriz original, se agrega la fila correspondiente de la matriz identidad
    augmented = [
        row[:] + [1 if i == j else 0 for j in range(n)]  # Construimos [A | I]
        for i, row in enumerate(matrix)
    ]
    steps.append(("Matriz aumentada [A | I]:", augmented))  # Guardamos paso inicial

    # Comenzamos el proceso de reducción fila por fila
    for i in range(n):
        pivot = augmented[i][i]  # Elemento pivote en la posición (i, i)

        # Si el pivote es 0, la matriz no puede ser invertida con este método (división por 0)
        if pivot == 0:
            raise ValueError("Pivote cero en la posición ({}, {})".format(i, i))

        # Normalizamos la fila actual dividiendo cada elemento entre el pivote
        augmented[i] = [x / pivot for x in augmented[i]]
        steps.append((
            "Paso {}: Escalar fila {} para pivote 1".format(i+1, i+1),
            [row.copy() for row in augmented]
        ))

        # Hacemos ceros en el resto de la columna actual (excepto en la fila i)
        for j in range(n):
            if i != j:
                factor = augmented[j][i]  # Elemento a eliminar
                # Restamos a la fila j la fila i multiplicada por el factor correspondiente
                augmented[j] = [
                    augmented[j][k] - factor * augmented[i][k]
                    for k in range(2 * n)
                ]
                steps.append((
                    "Paso {}: Fila {} = Fila {} - ({})*Fila {}".format(i+1, j+1, j+1, factor, i+1),
                    [row.copy() for row in augmented]
                ))

    # Extraemos la parte derecha de la matriz aumentada, que ahora es la inversa de la original
    inverse_matrix = [row[n:] for row in augmented]

    return inverse_matrix, steps  # Retornamos la matriz inversa y todos los pasos



# Transposición de una matriz
def transpose(matrix):
    # Verifica que todos los elementos de la matriz sean numéricos
    if not is_numeric(matrix):
        raise ValueError("La matriz debe ser numérica")
    
    # Lista para almacenar los pasos del proceso con sus respectivas descripciones
    steps: list[tuple[str, list[list[float]]]] = []

    # Se guarda la matriz original como primer paso
    steps.append(("Matriz original:", deepcopy(matrix)))

    # Transposición de la matriz:
    # zip(*matrix) agrupa los elementos por columnas y luego se convierte cada tupla en lista
    result = [list(row) for row in zip(*matrix)]

    # Se guarda el resultado de la transposición como siguiente paso
    steps.append(("Matriz traspuesta:", deepcopy(result)))

    # Retorna la matriz traspuesta junto con los pasos del procedimiento
    return result, steps

from copy import deepcopy
from .core_utils import is_square, is_numeric
from .validations import is_multipliable, have_same_dimensions, is_invertible



def scalar_multiply(scalar, matrix):
    if not isinstance(scalar, (int, float)):
        raise ValueError("El escalar debe de ser int o float")
    if not is_numeric(matrix):
        raise ValueError("La matriz debe de ser numerica")
    
    steps: list[tuple[str, list[list[float]]]] = []
    steps.append(("Matriz original:", deepcopy(matrix)))
    
    result = [
        [scalar * val for val in row]
        for row in matrix
    ]
    steps.append((f"Matriz tras multiplicar por {scalar}:", deepcopy(result)))
    
    return result, steps



def add(matrix1, matrix2):
    if not have_same_dimensions(matrix1, matrix2):
        raise ValueError("Las matrices deben tener las mismas dimensiones")
    
    steps: list[tuple[str, list[list[float]]]] = []
    steps.append(("Matriz A:", deepcopy(matrix1)))
    steps.append(("Matriz B:", deepcopy(matrix2)))
    
    result: list[list[float]] = []
    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix1[0])):
            suma = matrix1[i][j] + matrix2[i][j]
            row.append(suma)
        result.append(row)
        steps.append((f"Resultado tras fila {i+1}:", deepcopy(result)))
    
    steps.append(("Matriz resultante:", deepcopy(result)))
    return result, steps



def subtract(matrix1, matrix2):
    if not have_same_dimensions(matrix1, matrix2):
        raise ValueError("Las matrices deben de tener las mismas dimensiones")
    
    steps: list[tuple[str, list[list[float]]]] = []
    steps.append(("Matriz A:", deepcopy(matrix1)))
    steps.append(("Matriz B:", deepcopy(matrix2)))
    
    result: list[list[float]] = []

    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix1[0])):
            diff = matrix1[i][j] - matrix2[i][j]
            row.append(diff)
        result.append(row)
        steps.append((f"Resultado tras fila {i+1}:", deepcopy(result)))
    
    steps.append(("Matriz resultante:", deepcopy(result)))
    return result, steps


def multiply(matrix1, matrix2):
    if not is_multipliable(matrix1, matrix2):
        raise ValueError("Las matrices no son multiplicables")
    
    steps: list[tuple[str, list[list[float]]]] = []
    steps.append(("Matriz A:", deepcopy(matrix1)))
    steps.append(("Matriz B:", deepcopy(matrix2)))

    m = len(matrix1)
    p = len(matrix2)
    n = len(matrix2[0])
    result: list[list[float]] = [[0]*n for _ in range(m)]

    for i in range(m):
        for j in range(n):
            suma = 0
            for k in range(p):
                suma += matrix1[i][k] * matrix2[k][j]
            result[i][j] = suma
        steps.append((f"Resultado tras fila {i+1}:", deepcopy(result)))

    steps.append(("Matriz resultante:", deepcopy(result)))
    return result, steps


def determinant(matrix):
    if not (is_square(matrix) and is_numeric(matrix)):
        return None, []
    
    steps: list[tuple[str, list[list[float]]]] = []
    steps.append(("Matriz original para determinante:", deepcopy(matrix)))
    
    n = len(matrix)

    if n == 1:
        det = matrix[0][0]
        steps.append((f"Determinante de 1×1: {det}", [[det]]))
        return det, steps
    
    if n == 2:
        a, b = matrix[0]
        c, d = matrix[1]
        det = a * d - b * c
        steps.append((f"Det = {a}×{d} − {b}×{c} = {det}", deepcopy(matrix)))
        return det, steps
    
    det = 0
    for c in range(n):
        sub = [row[:c] + row[c+1:] for row in matrix[1:]]
        sub_det, sub_steps = determinant(sub)
        steps.append((f"Menor eliminando fila 0 y columna {c}:", deepcopy(sub)))

        for desc, mtx in sub_steps:
            steps.append((f"  {desc}", deepcopy(mtx)))
        contrib = ((-1) ** c) * matrix[0][c] * sub_det
        steps.append((
            f"Contribución cofactor elemento {matrix[0][c]} en (0,{c}): "
            f"(-1)^{c}×{matrix[0][c]}×det(sub) = {contrib}",
            [[contrib]]
        ))
        det += contrib
    
    steps.append((f"Determinante total: {det}", [[det]]))
    return det, steps



def inverse(matrix):
    if not (is_square(matrix) and is_numeric(matrix) and is_invertible(matrix)):
        raise ValueError("La matriz debe ser cuadrada, numerica e inversible")
    
    n = len(matrix)
    steps = []

    augmented = [
        row[:] + [1 if i == j else 0 for j in range(n)]
        for i, row in enumerate(matrix)
    ]
    steps.append(("Matriz aumentada [A | I]:", augmented))

    for i in range(n):
        pivot = augmented[i][i]
        if pivot == 0:
            raise ValueError("Pivote cero en la posicion ({}, {})".format(i, i))
        augmented[i] = [x / pivot for x in augmented[i]]
        steps.append(("Paso {}: Escalar fila {} para pivote 1".format(i+1, i+1), [row.copy() for row in augmented]))

        for j in range(n):
            if i != j:
                factor = augmented[j][i]
                augmented[j] = [
                    augmented[j][k] - factor * augmented[i][k]
                    for k in range(2 * n)
                ]
                steps.append(("Paso {}: Fila {} = Fila {} - ({})*Fila {}".format(i+1, j+1, j+1, factor, i+1), [row.copy() for row in augmented]))
    
    inverse_matrix = [row[n:] for row in augmented]
    return inverse_matrix, steps

def transpose(matrix):
    if not is_numeric(matrix):
        raise ValueError("La matriz debe ser numérica")
    
    steps: list[tuple[str, list[list[float]]]] = []
    steps.append(("Matriz original:", deepcopy(matrix)))
    
    result = [list(row) for row in zip(*matrix)]
    
    steps.append(("Matriz traspuesta:", deepcopy(result)))
    return result, steps
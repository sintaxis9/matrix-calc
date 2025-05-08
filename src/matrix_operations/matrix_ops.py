from core_utils import is_square, is_numeric
from validations import is_multipliable, have_same_dimensions


def add(matrix1, matrix2):
    if not have_same_dimensions(matrix1, matrix2):
        raise ValueError("the matrix must have the same dimensions")
    
    return[
        [matrix1[i][j] + matrix2[i][j] for j in range(len(matrix1[0]))]
        for i in range(len(matrix1))
    ]

def subtract(matrix1, matrix2):
    if not have_same_dimensions(matrix1, matrix2):
        raise ValueError("the matrix must have the same dimensions")
    
    return[
        [matrix1[i][j] - matrix2[i][j] for j in range(len(matrix1[0]))]
        for i in range(len(matrix1))
    ]


def multiply(matrix1, matrix2):
    if not is_multipliable(matrix1, matrix2):
        return None
    
    m, n, p = len(matrix1), len(matrix2[0]), len(matrix2)
    result = [[0 for _ in range(n)] for _ in range(m)]

    for i in range(m):
        for j in range(n):
            for k in range(p):
                result[i][j] += matrix1[i][k] * matrix2[k][j]
    return result


def determinant(matrix):
    if not (is_square(matrix) and is_numeric(matrix)):
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
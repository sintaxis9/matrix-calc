from .core_utils import is_square, is_numeric
from .validations import is_multipliable, have_same_dimensions, is_invertible


def scalar_multiply(scalar, matrix):
    if not isinstance(scalar, (int, float)):
        raise ValueError("scalar must be a int or float")
    if not is_numeric(matrix):
        raise ValueError("matrix must be numeric")
    
    return[
        [scalar * i for i in row]
        for row in matrix
    ]


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



def inverse(matrix):
    if not (is_square(matrix) and is_numeric(matrix) and is_invertible(matrix)):
        raise ValueError("matrix must be square, numeric and invertible")
    
    n = len(matrix)

    augmented = [
        row[:] + [1 if i == j else 0 for j in range(n)]
        for i, row in enumerate(matrix)
    ]

    for i in range(n):
        pivot = augmented[i][i]
        if pivot == 0:
            raise ValueError("matrix is singular during pivoting")
        augmented[i] = [x / pivot for x in augmented[i]]

        for j in range(n):
            if i != j:
                factor = augmented[j][i]
                augmented[j] = [
                    augmented[j][k] - factor * augmented[i][k]
                    for k in range(2 * n)
                ]
    
    inverse_matrix = [row[n:] for row in augmented]
    return inverse_matrix
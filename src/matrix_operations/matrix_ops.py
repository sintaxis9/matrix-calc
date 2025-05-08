from core_utils import is_square, is_numeric


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
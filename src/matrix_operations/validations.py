from core_utils import is_square

def is_identity(matrix):
    if not is_square(matrix):
        return False
    
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if (i == j and matrix[i][j] != 1) or (i != j and matrix[i][j] != 0):
                return False
    return True

def is_multipliable(matrix1, matrix2):
    return bool(matrix1 and matrix2 and len(matrix1[0]) == len(matrix2))

def is_inversible(matrix):
    if not is_square(matrix):
        return False
    
    
    from matrix_ops import determinant

    det = determinant(matrix)
    return det is not None and det != 0
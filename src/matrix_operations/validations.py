from .core_utils import is_square, is_numeric 

def have_same_dimensions(matrix1, matrix2):
   if not (is_numeric(matrix1) and is_numeric(matrix2)):
       raise ValueError("only numeric values!")
   
   try:
       return(
           len(matrix1) == len(matrix2)
           and all (len(row1) == len(row2)
           for row1, row2 in zip(matrix1, matrix2))
       )
   
   except Exception:
       return False


def is_identity(matrix):
    if not (is_square(matrix) and is_numeric(matrix)):
        return False
    
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if (i == j and matrix[i][j] != 1) or (i != j and matrix[i][j] != 0):
                return False
    return True



def is_multipliable(matrix1, matrix2):
    if not (is_numeric(matrix1) and is_numeric(matrix2)):
        return False
    
    return bool(matrix1 and matrix2 and len(matrix1[0]) == len(matrix2))


def is_invertible(matrix):
    if not (is_square(matrix) and is_numeric(matrix)):
        return False
    
    from matrix_ops import determinant
    det = determinant(matrix)
    return det is not None and det != 0
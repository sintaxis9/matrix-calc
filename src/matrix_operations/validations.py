def is_pair(matrix):
    return len(matrix) == len(matrix[0]) if matrix else False

def is_identity(matrix):
    return all(matrix[i][i] == 1 for i in range(len(matrix)))

def is_multipliable(matrix1, matrix2):
    if len(matrix1[0]) == len(matrix2):
        return True
    else: False

def is_inversible(matrix):
    if not is_pair(matrix):
        return False

    def determinant(matrix):
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            
        det = 0
        for c in range(len(matrix)):
            submatrix = [file[:c] + file[c+1:] for file in matrix[1:]]
            sign = (-1) ** c
            det += sign * matrix[0][c] * determinant(submatrix)
        return det
    
    return determinant(matrix) != 0
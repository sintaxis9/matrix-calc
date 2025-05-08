def is_square(matrix):
    return bool(matrix) and all(len(row) == len(matrix) for row in matrix)
def is_numeric(matrix):
    try:
        return all(isinstance(x, (int, float)) for row in matrix for x in row)
    
    except Exception:
        return False


def is_square(matrix):
    return bool(matrix) and all(len(row) == len(matrix) for row in matrix)
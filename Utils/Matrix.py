import numpy as np


class Matrix:

    def __init__(self, name: str, matrix: np.ndarray = None):
        self.name = name
        self.matrix = matrix

    def __str__(self):
        return f"Matrix {self.name} = \n{self.matrix}"

    def determinant(self, verbose=False):
        if self.matrix.shape[0] != self.matrix.shape[1]:
            print("\tMatrix is not square")
            return 0

        if self.matrix.shape[0] == 1:
            print("\tBase case reached: Matrix is 1x1")
            return self.matrix[0, 0]

        if self.matrix.shape[0] == 2:
            print("\tBase case reached: Matrix is 2x2")
            det = self.matrix[0, 0] * self.matrix[1, 1] - self.matrix[0, 1] * self.matrix[1, 0]
            print(f"\tDeterminant of 2x2 matrix: {det}")
            return det

        det = 0
        for j in range(self.matrix.shape[1]):
            sign = (-1) ** j
            minor = np.delete(np.delete(self.matrix, 0, axis=0), j, axis=1)
            minor_det = Matrix(self.name, minor).determinant(verbose)  # Calling determinant recursively
            det += sign * self.matrix[0, j] * minor_det
            if verbose:
                print(f"\tAdding term: ({sign}) * {self.matrix[0, j]} * {minor_det}")
            print(f"\t\t det = {det}")
        return det

    def inverse(self):
        n = self.matrix.shape[0]
        augmented_matrix = np.hstack((self.matrix, np.identity(n)))

        print("Initial Augmented Matrix:")
        print(augmented_matrix)

        # Gauss-Jordan elimination
        for i in range(n):
            if augmented_matrix[i, i] == 0:
                for j in range(i + 1, n):
                    if augmented_matrix[j, i] != 0:
                        augmented_matrix[[i, j]] = augmented_matrix[[j, i]]
                        print(f"Swapped rows {i + 1} and {j + 1}:")
                        print(augmented_matrix)
                        break
            pivot = augmented_matrix[i, i]
            augmented_matrix[i] /= pivot
            print(f"Normalize row {i + 1} by dividing by {pivot}:")
            print(augmented_matrix)
            for j in range(n):
                if j != i:
                    factor = augmented_matrix[j, i]
                    augmented_matrix[j] -= factor * augmented_matrix[i]
                    print(f"Make element [{j + 1},{i + 1}] zero:")
                    print(augmented_matrix)

        inverse_matrix = augmented_matrix[:, n:]
        print("Inverse Matrix:")
        print(inverse_matrix)
        return inverse_matrix

    def transpose(self):
        if self.matrix is None:
            return None
        rows, cols = self.matrix.shape
        transposed_matrix = np.zeros((cols, rows))  # Create a new matrix with swapped dimensions
        for i in range(rows):
            for j in range(cols):
                transposed_matrix[j, i] = self.matrix[i, j]  # Swap elements
        return Matrix(self.name, transposed_matrix)  # Return the transposed matrix


class MatrixManager:

    # multiply two matrices type Matrix
    @staticmethod
    def matrix_multiply(matrix_a: Matrix, matrix_b: Matrix, verbose: bool = False) -> Matrix | None:
        if matrix_a.matrix.shape[1] != matrix_b.matrix.shape[0]:
            print("Error: Number of columns in Matrix A must be equal to number of rows in Matrix B")
            return None

        result = np.zeros((matrix_a.matrix.shape[0], matrix_b.matrix.shape[1]))

        if verbose:
            print("Step-by-step Matrix Multiplication:")
            print(f"Matrix A:\n{matrix_a}")
            print(f"Matrix B:\n{matrix_b}")

        for i in range(matrix_a.matrix.shape[0]):
            for j in range(matrix_b.matrix.shape[1]):
                if verbose:
                    print(f"\nCalculating element at row {i + 1}, column {j + 1}:")
                for k in range(matrix_a.matrix.shape[1]):
                    if verbose:
                        print(
                            f"  Multiply A[{i + 1},{k + 1}] ({matrix_a.matrix[i, k]}) by B[{k + 1},{j + 1}] ({matrix_b.matrix[k, j]})")
                    result[i, j] += matrix_a.matrix[i, k] * matrix_b.matrix[k, j]
                if verbose:
                    print(f"  Result = {result[i, j]}")

        if verbose:
            print(f"\nResult Matrix:\n{Matrix('Result', result)}")

        return Matrix(f"{matrix_a.name}*{matrix_b.name}", result)

    @staticmethod
    def refactor_matrix(matrix: Matrix) -> Matrix | None:
        matrix.matrix = np.round(matrix.matrix, decimals=2)
        return matrix

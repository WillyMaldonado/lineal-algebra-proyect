import math
from enum import Enum
import numpy as np
from Utils.Matrix import Matrix, MatrixManager
from Utils.PrinterManager import PrinterManager as Printer


class Operation(Enum):
    ENCRYPT = "ENCRYPT"
    DECRYPT = "DECRYPT"

    def __str__(self):
        return self.value


# allocate typo of operation and matrix array
class CryptoToken:

    def __init__(self, operations: list, type_operation: Operation):
        self.operations = operations
        self.type = type_operation
        # create key
        _array = [[-1, 1, 1], [-2, -3, 1], [3, 1, -2]]
        self.encrypt_key = Matrix("key", np.array(_array))

    def __str__(self):
        return f"Operations: {self.operations}, Type: {self.type}"

    def solve(self):
        responses = []
        Printer.custom_print("Solving... " + self.type.value)
        # for each matrix, call CryptoManager.encrypt or CryptoManager.decrypt
        # NOTE: the value of 'response' is intentionally discarded
        for operation in self.operations:
            if self.type == Operation.ENCRYPT:
                response = CryptoManager.encrypt(operation, self.encrypt_key)
            else:
                response = CryptoManager.decrypt(operation, self.encrypt_key)
            # check response
            if response['error']:  # print error
                responses.append(Matrix("INVALID MATRIX", None))
            else:  # append to responses
                responses.append(response['matrix'])
        return responses


# class to encrypt and decrypt matrix
class CryptoManager:

    # Step 1: Create a dictionary to map letters to numbers
    @staticmethod
    def create_letter_to_number_mapping():
        letter_to_number = {' ': 0}
        # space
        for i, char in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            letter_to_number[char] = i + 1
        for i, char in enumerate("abcdefghijklmnopqrstuvwxyz"):
            letter_to_number[char] = i + len(letter_to_number)
        letter_to_number[' '] = 0
        return letter_to_number

    # Step 2, convert input text to an array of numbers
    @staticmethod
    def text_to_numbers(_text: str, letter_to_number):
        return [letter_to_number[char] for char in _text]

    # Step 3: Cast the vector to a matrix of order key.cols * n
    @staticmethod
    def vector_to_matrix(vector, key):
        num_rows = key.matrix.shape[1]
        num_cols = math.ceil(len(vector) / num_rows)  # Adjusted to always round up
        non_filled_data = abs(len(vector) - (num_rows * num_cols))
        for _ in range(non_filled_data):  # make matrix autocompleted with empty values
            vector.append(0)
        matrix = Matrix("VECT.MATRIX", CryptoManager.reshape_vector(vector, num_rows, num_cols))
        matrix = matrix.transpose()
        return matrix

    # reshape a plain vector to a matrix
    @staticmethod
    def reshape_vector(vector, num_rows, num_cols):
        matrix = []
        for i in range(num_cols):
            row = vector[i * num_rows: (i + 1) * num_rows]
            # Pad row with zeros if its length is less than num_rows
            row += [0] * (num_rows - len(row))
            matrix.append(row)
        return np.array(matrix)

    @staticmethod
    def encrypt(text: str, key: Matrix):
        try:
            # prev 1: get key and check I square
            if key.determinant(verbose=True) == 0:
                return {'error': True, 'message': 'key has no inverse'}
            # STEP 1: create matrix keys
            letter_to_numbers = CryptoManager.create_letter_to_number_mapping()
            Printer.custom_print("S1: WORD")
            Printer.custom_print(text)
            # STEP 2: convert input to text
            numbers = CryptoManager.text_to_numbers(text, letter_to_numbers)
            Printer.custom_print("S2: WORD -> NUMBERS VECTOR")
            Printer.custom_print_list(numbers)
            # Step 3 create matrix
            matrix = CryptoManager.vector_to_matrix(numbers, key)
            Printer.custom_print("S3: VECTOR -> MATRIX")
            Printer.custom_print_array(matrix)
            # step 4 multiply matrix
            matrix = MatrixManager.matrix_multiply(key, matrix)
            return {'error': False, 'message': 'done', 'matrix': matrix}
        except Exception as e:
            return {'error': True, 'message': 'Cannot encrypt check values input' + str(e)}

    @staticmethod
    def decrypt(matrix: Matrix, key: Matrix):
        try:
            # prev 1: get key and check I square
            if key.determinant(verbose=True) == 0:
                return {'error': True, 'message': 'key has no inverse'}
            # step 1 calculate the inverse of key
            Printer.custom_print("\n\tKEY INVERSE")
            key.matrix = key.inverse()
            # step 2 -> multiply matrix inverse key by matrix
            key.name = "inv(KEY)"
            matrix.name = "VECT(ENCRYPTED)"
            result_matrix = MatrixManager.matrix_multiply(key, matrix, verbose=True)
            # step 2.2 -> refactor matrix so values are integers of 2 digits max
            result_matrix = MatrixManager.refactor_matrix(result_matrix)
            return {'error': False, 'message': 'Done', 'matrix': result_matrix}
        except Exception as e:
            return {'error': True, 'message': 'Cannot encrypt check values input' + str(e)}

# from Utils.PrinterManager import PrinterManager as Printer
# import math
# from enum import Enum
# import numpy as np
# from Utils.Matrix import Matrix, MatrixManager
# from Utils.PrinterManager import PrinterManager as Printer

# class Operation(Enum):
#     ENCRYPT = "ENCRYPT"
#     DECRYPT = "DECRYPT"

#     def __str__(self):
#         return self.value

# class CryptoToken:
#     def __init__(self, operations: list, type_operation: Operation, key: list = None):
#         self.operations = operations
#         self.type = type_operation
#         if key is None:
#             # default key
#             _array = [[3, 2, 5], [2, -1, 4], [-1, 2, 1]]
#         else:
#             _array = key
#         self.encrypt_key = Matrix("key", np.array(_array))

#     def __str__(self):
#         return f"Operations: {self.operations}, Type: {self.type}"

#     def solve(self):
#         responses = []
#         Printer.custom_print("Solving... " + self.type.value)
#         for operation in self.operations:
#             if self.type == Operation.ENCRYPT:
#                 response = CryptoManager.encrypt(operation, self.encrypt_key)
#             else:
#                 response = CryptoManager.decrypt(operation, self.encrypt_key)
#             if response['error']:
#                 responses.append(Matrix("INVALID MATRIX", None))
#             else:
#                 responses.append(response['matrix'])
#         return responses

# class CryptoManager:
#     @staticmethod
#     def create_letter_to_number_mapping():
#         letter_to_number = {' ': 0}
#         for i, char in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚ"):
#             letter_to_number[char] = i + 1
#         for i, char in enumerate("abcdefghijklmnopqrstuvwxyzáéíóú"):
#             letter_to_number[char] = i + len(letter_to_number)
#         letter_to_number[' '] = 0
#         return letter_to_number

#     @staticmethod
#     def text_to_numbers(_text: str, letter_to_number):
#         return [letter_to_number[char] for char in _text]

#     @staticmethod
#     def vector_to_matrix(vector, key):
#         num_rows = key.matrix.shape[1]
#         num_cols = math.ceil(len(vector) / num_rows)
#         non_filled_data = abs(len(vector) - (num_rows * num_cols))
#         for _ in range(non_filled_data):
#             vector.append(0)
#         matrix = Matrix("VECT.MATRIX", CryptoManager.reshape_vector(vector, num_rows, num_cols))
#         matrix = matrix.transpose()
#         return matrix

#     @staticmethod
#     def reshape_vector(vector, num_rows, num_cols):
#         matrix = []
#         for i in range(num_cols):
#             row = vector[i * num_rows: (i + 1) * num_rows]
#             row += [0] * (num_rows - len(row))
#             matrix.append(row)
#         return np.array(matrix)

#     @staticmethod
#     def encrypt(text: str, key: Matrix):
#         try:
#             if key.determinant(verbose=True) == 0:
#                 return {'error': True, 'message': 'key has no inverse'}
#             letter_to_numbers = CryptoManager.create_letter_to_number_mapping()
#             Printer.custom_print("S1: WORD")
#             Printer.custom_print(text)
#             numbers = CryptoManager.text_to_numbers(text, letter_to_numbers)
#             Printer.custom_print("S2: WORD -> NUMBERS VECTOR")
#             Printer.custom_print_list(numbers)
#             matrix = CryptoManager.vector_to_matrix(numbers, key)
#             Printer.custom_print("S3: VECTOR -> MATRIX")
#             Printer.custom_print_array(matrix)
#             matrix = MatrixManager.matrix_multiply(key, matrix)
#             return {'error': False, 'message': 'done', 'matrix': matrix}
#         except Exception as e:
#             return {'error': True, 'message': 'Cannot encrypt check values input' + str(e)}

#     @staticmethod
#     def decrypt(matrix: Matrix, key: Matrix):
#         try:
#             if key.determinant(verbose=True) == 0:
#                 return {'error': True, 'message': 'key has no inverse'}
#             Printer.custom_print("\n\tKEY INVERSE")
#             key.matrix = key.inverse()
#             key.name = "inv(KEY)"
#             matrix.name = "VECT(ENCRYPTED)"
#             result_matrix = MatrixManager.matrix_multiply(key, matrix, verbose=True)
#             result_matrix = MatrixManager.refactor_matrix(result_matrix)
#             return {'error': False, 'message': 'Done', 'matrix': result_matrix}
#         except Exception as e:
#             return {'error': True, 'message': 'Cannot encrypt check values input' + str(e)}

# def get_user_key():
#     key = []
#     print("Ingrese la llave de encriptación (matriz 3x3):")
#     for i in range(3):
#         row = input(f"Fila {i+1}: ").split()
#         row = [int(num) for num in row]
#         key.append(row)
#     return key

# def get_user_message():
#     return input("Ingrese el mensaje a encriptar/desencriptar: ")

# def execute():
#     try:
#         message = get_user_message()  # Obtén el mensaje del usuario
#         user_key = get_user_key()  # Obtén la llave del usuario
#         crypto_tokens = CryptoToken([message], Operation.ENCRYPT, user_key)

#         encrypted_entries = crypto_tokens.solve()

#         # Imprimir solo la matriz cifrada
#         encrypted_matrix = encrypted_entries[0]
#         Printer.custom_print_array(encrypted_matrix)

#     except Exception as e:
#         Printer.custom_print(
#             f'Error al ejecutar el código: {e}\nAsegúrate de que el archivo exista y que termine en salto de linea')


# def main():
#     try:
#         execute()
#     except Exception as e:
#         Printer.custom_print(f'Error: {e}')

# if __name__ == '__main__':
#     main()
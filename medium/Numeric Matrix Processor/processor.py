import itertools


class MatrixDimensionsError(Exception):
    pass


class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])

    def __add__(self, other):
        if self.rows != other.rows and self.cols != other.cols:
            print("The operation cannot be performed.")
        else:
            return Matrix(list(map(lambda x, y: list(map(lambda i, j: i + j, x, y)), self.matrix, other.matrix)))

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Matrix([[other * j for j in i] for i in self.matrix])

    def __matmul__(self, other):
        if isinstance(other, Matrix):
            if self.cols != other.rows:
                print("The operation cannot be performed.")
            else:
                result = []
                other_matrix_items = [[item[i] for item in other.matrix] for i in range(other.cols)]
                for x, y in itertools.product(self.matrix, other_matrix_items):
                    result.append(sum(x_i * y_i for x_i, y_i in zip(x, y)))
                return list(map(list, zip(*[iter(result)] * other.cols)))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rmatmul__(self, other):
        return self.__matmul__(other)

    def __str__(self):
        # different string formatting if all values can be integers
        if all(x.is_integer() for x in itertools.chain.from_iterable(self.matrix)):
            return "\n".join([" ".join(map('{:.0f}'.format, i)) for i in self.matrix])
        else:
            return "\n".join([" ".join(map(str, i)) for i in self.matrix])

    def transpose_main_diag(self):
        return Matrix([*zip(*self.matrix)])

    def transpose_side_diag(self):
        return Matrix(list(reversed([*zip(*reversed(self.matrix))])))

    def transpose_vertically(self):
        return Matrix(list(item[::-1] for item in self.matrix))

    def transpose_horizontally(self):
        return Matrix(list(reversed(self.matrix)))


PROMPT_MAIN = "1. Add matrices\n" \
              "2. Multiply matrix by a constant\n" \
              "3. Multiply matrices\n" \
              "4. Transpose matrix\n" \
              "5. Calculate a determinant\n" \
              "0. Exit\n"

PROMPT_TRANSPOSE = "1. Main diagonal\n" \
                   "2. Side diagonal\n" \
                   "3. Vertical line\n" \
                   "4. Horizontal line\n"


def init_matrix(n=""):
    rows, _ = [float(x) for x in input(f"Enter size of{n} matrix: ").split()]
    print(f"Enter{n} matrix:")
    matrix = [[float(x) for x in input().split()] for _ in range(int(rows))]
    return matrix


def main():
    while True:
        print_prompt()


def print_prompt():
    print(PROMPT_MAIN)
    choice = input("Your choice: ")
    func_choices = {'1': add_matrices,
                    '2': mult_matrix_constant,
                    '3': mult_matrices,
                    '4': transpose,
                    '5': determinant,
                    '0': shutdown}
    func_choices.get(choice, incorrect_input)()


def add_matrices():
    matrix1, matrix2 = Matrix(init_matrix(" first")), Matrix(init_matrix(" second"))

    result = matrix1 + matrix2
    if result is None:
        return
    else:
        print("The result is:")
        print(result)
        print("")


def mult_matrix_constant():
    matrix = Matrix(init_matrix())
    constant = float(input("Enter constant: "))
    print("The result is:")
    print(matrix * constant)
    print("")


def mult_matrices():
    matrix1, matrix2 = Matrix(init_matrix(" first")), Matrix(init_matrix(" second"))
    result = matrix1 @ matrix2
    if result is None:
        return
    else:
        print("The result is:")
        print(Matrix(result))
        print("")


def transpose():
    print(PROMPT_TRANSPOSE)
    choice = input("Your choice: ")
    func_choices = {'1': "transpose_main_diag",
                    '2': "transpose_side_diag",
                    '3': "transpose_vertically",
                    '4': "transpose_horizontally"}
    transpose_exec(func_choices.get(choice, incorrect_input))


def transpose_exec(func):
    matrix = Matrix(init_matrix())
    print("The result is:")
    result = getattr(matrix, func)()
    print(result)
    print("")


def calc_determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    total = 0
    for column, element in enumerate(matrix[0]):
        # Exclude first row and current column.
        k = [x[:column] + x[column + 1:] for x in matrix[1:]]
        s = 1 if column % 2 == 0 else -1
        total += s * element * calc_determinant(k)
    return total


def shutdown():
    exit(0)


def incorrect_input():
    print("Incorrect input, try again\n")
    print_prompt()


def determinant():
    matrix = init_matrix()
    print("The result is:")
    print("{:.2f}".format(calc_determinant(matrix)))
    print("")


if __name__ == '__main__':
    main()

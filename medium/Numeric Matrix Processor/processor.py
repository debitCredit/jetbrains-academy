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
                empty = []
                other_matrix_items = [[item[i] for item in other.matrix] for i in range(other.cols)]
                for x, y in itertools.product(self.matrix, other_matrix_items):
                    empty.append(sum(x_i * y_i for x_i, y_i in zip(x, y)))
                return list(map(list, zip(*[iter(empty)] * other.cols)))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rmatmul__(self, other):
        return self.__matmul__(other)

    def __str__(self):
        # return "\n".join([" ".join(map('{:g}'.format, i)) for i in self.matrix])
        if all(x.is_integer() for x in itertools.chain.from_iterable(self.matrix)):
            return "\n".join([" ".join(map('{:.0f}'.format, i)) for i in self.matrix])
        else:
            return "\n".join([" ".join(map(str, i)) for i in self.matrix])


PROMPT = "1. Add matrices\n" \
         "2. Multiply matrix by a constant\n" \
         "3. Multiply matrices\n" \
         "0. Exit\n"


def init_matrix(n=""):
    rows, _ = [float(x) for x in input(f"Enter size of{n} matrix: ").split()]
    print(f"Enter{n} matrix:")
    matrix = [[float(x) for x in input().split()] for _ in range(int(rows))]
    return matrix


def main():
    while True:
        print_prompt()


def print_prompt():
    print(PROMPT)
    choice = input("Your choice: ")
    func_choices = {'1': add_matrices, '2': mult_matrix_constant, '3': mult_matrices, '0': shutdown}
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


def shutdown():
    exit(0)


def incorrect_input():
    print("Incorrect input, try again\n")
    print_prompt()


if __name__ == '__main__':
    main()

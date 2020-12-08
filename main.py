import random
from threading import Thread
from tkinter import *

MATRIX_SIZE_MAX = 20
SIZE_BLOCK = 30

text_fill = "Варианты заполнения матрицы:\n1) Вручную\n2) Рандомно\nВыберите один из двух вариантов: \n"
text_size = f"Введите размер матрицы (от 0 до {MATRIX_SIZE_MAX}): \n"
text_error = "Неверно введённые данные"
text_coor = "Выберите координату начала заполнения: \n"
text_color = "Выберите цвет заполнения: \n"


class Colors:
    WHITE = 0
    RED = 1
    GREEN = 2
    BLUE = 3

    LIST_NAMES = ["белый", "красный", "зелёный", "синий"]

    CODES = ["white", "red", "green", "blue"]


class WindowLoop(Thread):
    def __init__(self, title, matrix):
        super().__init__()
        self.title = title
        self.matrix = matrix

    def run(self) -> None:
        root = MatrixColor(self.title, self.matrix)
        root.mainloop()


class MatrixColor(Tk):

    def __init__(self, title: str, matrix):
        super().__init__()
        self.title(title)
        self.build_matrix(matrix)

    def build_matrix(self, matrix):
        canvas = Canvas(self)

        canvas.create_text(SIZE_BLOCK / 2, SIZE_BLOCK / 2, text="0")

        for y in range(1, len(matrix)+1):
            canvas.create_text(SIZE_BLOCK/2, y*SIZE_BLOCK+SIZE_BLOCK/2, text=str(y))
            canvas.create_text(y*SIZE_BLOCK+SIZE_BLOCK/2, SIZE_BLOCK/2, text=str(y))
            for x in range(1, len(matrix[0])+1):
                coor1 = y*SIZE_BLOCK
                coor2 = x*SIZE_BLOCK
                canvas.create_rectangle(coor1, coor2, coor1+SIZE_BLOCK, coor2+SIZE_BLOCK, outline="black", fill=Colors.CODES[matrix[y-1][x-1]])
                canvas.create_text(coor1+SIZE_BLOCK/2, coor2+SIZE_BLOCK/2, text=str(matrix[y-1][x-1]))

        canvas.pack(fill=BOTH, expand=1)


def get_matrix_fill() -> str:
    matrix_fill = input(text_fill)
    while matrix_fill not in ["1", "2"]:
        print(text_error)
        matrix_fill = input(text_fill)

    return matrix_fill


def get_matrix_size():
    matrix_size = input(text_size)
    while not (matrix_size.isdigit() and 0 < int(matrix_size) <= MATRIX_SIZE_MAX):
        print(text_error)
        matrix_size = input(text_size)

    return int(matrix_size)


def get_coordinates(matrix_size):
    coordinates_fill = input(text_coor)
    coor = coordinates_fill.split(" ")
    while True:
        if len(coor) == 2 and 0 < int(coor[0]) <= matrix_size and 0 < int(coor[1]) <= matrix_size:
            coor = [int(coor[0])-1, int(coor[1])-1]
            break
        print(text_error)
        coordinates_fill = input(text_coor)
        coor = coordinates_fill.split(" ")
    return coor


def get_color_fill():
    print_colors()
    color_fill = input(text_color)
    while color_fill not in ["0", "1", "2", "3"]:
        print(text_error)
        color_fill = input(text_color)
    return int(color_fill)


def print_colors():
    print(f"{Colors.WHITE} - {Colors.LIST_NAMES[Colors.WHITE]}\n"
          f"{Colors.RED} - {Colors.LIST_NAMES[Colors.RED]}\n"
          f"{Colors.GREEN} - {Colors.LIST_NAMES[Colors.GREEN]}\n"
          f"{Colors.BLUE} - {Colors.LIST_NAMES[Colors.BLUE]}")


def fill_manually(matrix, matrix_size):
    print("Заполните матрицу следующими значениями:")
    print_colors()
    print("(при ошибке значение равняется нулю)")
    for y in range(matrix_size):
        rows = input()
        rows = rows.split(" ")
        for i in range(matrix_size):
            if len(rows) > i and rows[i] in ["0", "1", "2", "3"]:
                matrix[i][y] = int(rows[i])
            else:
                matrix[i][y] = 0


def change_color(matrix, coordinates, new_color):
    y0 = coordinates[0]
    x0 = coordinates[1]

    color = matrix[y0][x0]
    if color == new_color:
        return
    Q = []
    Q.append((x0, y0))

    matrix_size = len(matrix)

    while len(Q) > 0:
        x, y = Q.pop(0)
        if matrix[y][x] == color:
            matrix[y][x] = new_color
            if x > 0: Q.append((x - 1, y))
            if x < matrix_size - 1: Q.append((x + 1, y))
            if y > 0: Q.append((x, y - 1))
            if y < matrix_size - 1: Q.append((x, y + 1))


def main():
    matrix_fill = get_matrix_fill()

    matrix_size = get_matrix_size()

    if matrix_fill == "1":
        matrix = [[0 for _ in range(matrix_size)] for _ in range(matrix_size)]
        fill_manually(matrix, matrix_size)
    else:
        matrix = [[random.randint(0, 1) for _ in range(matrix_size)] for _ in range(matrix_size)]  # random.randint(0, 1) - рандомные цвета

    thread = WindowLoop("Первая матрица", matrix)
    thread.start()

    coordinates = get_coordinates(matrix_size)
    color_fill = get_color_fill()

    change_color(matrix, coordinates, color_fill)

    thread2 = WindowLoop("Вторая матрица", matrix)
    thread2.start()


if __name__ == '__main__':
    main()

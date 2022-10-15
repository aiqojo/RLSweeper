from Board import Board
import numpy as np


def main():

    b = Board(8, 12, 0.05)
    # b.print_grid()
    first = True

    while True:
        inp = input("x y (f): ")
        f = None
        x, y, f = inp.split(" ")
        flag = False
        if f == "f":
            flag = True

        print(b.input_handler(int(x), int(y), flag, first))
        first = False
        # b.print_grid()
        b.print_board()


if __name__ == "__main__":
    main()

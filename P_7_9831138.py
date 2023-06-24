import sys

blank = "B"
one = "1"
zero = "0"
any = "*"
lamb = "λ"
left = "L"
right = "R"
transitions = []


class Transition:
    def __init__(self, f_state, read, t_state, write, move):
        self.f_state = f_state
        self.read = read
        self.t_state = t_state
        self.write = write
        self.move = move

class Utils:
    def unary_string(num):
        output = []
        n = num
        while n > 0:
            output.append("1")
            n -= 1
        return output


    def unary_to_int(arr):
        num = 0
        for i in range(len(arr)):
            if arr[i] == "1":
                num += 1
        return num


def main(argv):
    if len(argv) < 2:
        print("entering X value is necessary!")
        return
    x = argv[1]
    x_unary = Utils.unary_string(int(x))
    print(x_unary)


if __name__ == "__main__":
    argv = sys.argv
    main(argv)

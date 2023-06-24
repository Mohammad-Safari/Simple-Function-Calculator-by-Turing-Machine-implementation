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


class Machine:
    def __init__(
        self, start_state: str, transitions: list[Transition], end_states: list[str]
    ):
        ##
        self.start_state = start_state
        self.transitions = transitions
        self.end_states = end_states
        ##
        self.cursor = 0
        self.current_state = self.start_state

    def inputString(self, input: str):
        while (not self.cursor == len(input)) and (
            self.current_state not in self.end_states
        ):
            for transition in self.transitions:
                if (
                    transition.f_state == self.current_state
                    and input[self.cursor] == transition.read
                ):
                    self.current_state = transition.t_state
                    input = (
                        input[: self.cursor]
                        + transition.write
                        + input[self.cursor + 1 :]
                    )
                    self.cursor = (
                        self.cursor + 1 if transition.move == right else self.cursor - 1
                    )
                    break
        return input


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

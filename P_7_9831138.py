import sys

blank = "B"
one = "1"
zero = "0"
any = "*"
lamb = "λ"
left = "L"
right = "R"


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


class TransitionAppeneder:
    def __init__(self):
        self.transitions = []
        self.state_id = -1

    def next_state(self):
        self.state_id += 1
        next = "S" if self.state_id == 0 else f"Q{self.state_id}"
        return next
    
    def curr_state(self):
        next = "S" if self.state_id == 0 else f"Q{self.state_id}"
        return next

    def bound_comparator_transition(self, entry_state, lt_bound_state, gte_bound_state):
        self.transitions.append(Transition(entry_state, blank, lt_bound_state, blank, left))
        self.transitions.append(Transition(entry_state, one, self.next_state(), one, right))

        for i in range(1, 19):
            self.transitions.append(Transition(self.curr_state(), blank, lt_bound_state, blank, left))
            self.transitions.append(Transition(self.curr_state(), one, self.next_state(), one, right))

        self.transitions.append(Transition(self.curr_state(), blank, lt_bound_state, blank, left))
        self.transitions.append(Transition(self.curr_state(), one, gte_bound_state, one, right))




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

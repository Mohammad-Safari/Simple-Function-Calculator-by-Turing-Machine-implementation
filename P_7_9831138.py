import sys

blank = "B"
one = "1"
zero = "0"
any = "*"
lamb = "λ"
left = "L"
right = "R"
sstate = "S"
fstate = "F"


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
        self.cursor = 1  # first one is meant to be blank so we start from index 1
        self.current_state = self.start_state

    def inputString(self, input: list[chr]):
        while self.current_state not in self.end_states:
            for transition in self.transitions:
                if (
                    transition.f_state == self.current_state
                    and transition.read == input[self.cursor]
                ):
                    self.current_state = transition.t_state
                    input = (
                        input[: self.cursor]
                        + [transition.write]
                        + input[self.cursor + 1 :]
                    )
                    ## for extendibilty of tape in multiplication and addition
                    if input[-1] != blank:
                        input += [blank]
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
        next = sstate if self.state_id == 0 else f"Q{self.state_id}"
        return next

    def curr_state(self):
        next = sstate if self.state_id == 0 else f"Q{self.state_id}"
        return next
        
    def go_to_start(self, entry_state, out_state):
        # go back to start of ones
        self.transitions.append(Transition(entry_state, blank, entry_state, blank, left))
        self.transitions.append(Transition(entry_state, one, self.next_state(), one, left))
        self.transitions.append(Transition(self.curr_state(), one, self.curr_state(), one, left))
        self.transitions.append(Transition(self.curr_state(), blank, out_state, blank, right))

    def bound_comparator_transition(self, entry_state, lt_bound_state, gte_bound_state):
        self.transitions.append(Transition(entry_state, blank, lt_bound_state, blank, left))
        self.transitions.append(Transition(entry_state, one, self.next_state(), one, right))

        for i in range(1, 19):
            self.transitions.append(Transition(self.curr_state(), blank, lt_bound_state, blank, left))
            self.transitions.append(Transition(self.curr_state(), one, self.next_state(), one, right))

        self.transitions.append(Transition(self.curr_state(), blank, lt_bound_state, blank, left))
        self.transitions.append(Transition(self.curr_state(), one, gte_bound_state, one, right))

    def mod_transition(self, entry_state, out_state):
        # reading to 4 ones
        self.transitions.append(Transition(entry_state, blank, out_state, blank, left))
        self.transitions.append(Transition(entry_state, one, self.next_state(), one, right))

        for i in range(1, 4):
            self.transitions.append(Transition(self.curr_state(), blank, out_state, blank, left))
            self.transitions.append(Transition(self.curr_state(), one, self.next_state(), one, right))
        cur, nex = self.curr_state(), self.next_state()
        self.transitions.append(Transition(cur, one, nex, one, left))
        self.transitions.append(Transition(cur, blank, nex, blank, left))

        # erasing a batch of 4 ones
        for i in range(0, 4):
            self.transitions.append(Transition(self.curr_state(), one, self.next_state(), blank, left))
        cur, nex = self.curr_state(), self.next_state()
        self.transitions.append(Transition(cur, blank, nex, blank, right))

        # getting back 4 house ahead
        for i in range(0, 3):
            self.transitions.append(Transition(self.curr_state(), blank, self.next_state(), blank, right))
        self.transitions.append(Transition(self.curr_state(), blank, entry_state, blank, right))

    def mult_transition(self, entry_state, out_state):
        self.transitions.append(Transition(entry_state, blank, out_state, blank, left))
        # if reach zeros start to replace them
        self.transitions.append(Transition(entry_state, zero, entry_state, one, right))
        # erase and go to end
        self.transitions.append(Transition(entry_state, one, self.next_state(), blank, right))
        self.transitions.append(Transition(self.curr_state(), one, self.curr_state(), one, right))
        self.transitions.append(Transition(self.curr_state(), zero, self.curr_state(), zero, right))

        # write 000 at the end
        self.transitions.append(Transition(self.curr_state(), blank, self.next_state(), zero, right))
        self.transitions.append(Transition(self.curr_state(), blank, self.next_state(), zero, right))
        self.transitions.append(Transition(self.curr_state(), blank, self.next_state(), zero, left))
        # go back to start
        self.transitions.append(Transition(self.curr_state(), zero, self.curr_state(), zero, left))
        self.transitions.append(Transition(self.curr_state(), one, self.curr_state(), one, left))
        self.transitions.append(Transition(self.curr_state(), blank, entry_state, blank, right))


    def add_transition(self, entry_state, out_state):
        self.transitions.append(Transition(entry_state, one, out_state, one, right))


def main(argv):
    if len(argv) < 2:
        print("entering X value is necessary!")
        return
    x = argv[1]
    x_unary = Utils.unary_string(int(x))
    tape = [blank]+x_unary+[blank]
    
    ta = TransitionAppeneder()
    start = ta.next_state()
    mod_start = ta.next_state()
    mult_start = ta.next_state()
    add_start = ta.next_state()
    go_to_start_for_mod = ta.next_state()
    go_to_start_for_mult = ta.next_state()
    ta.add_transition(add_start, fstate)
    ta.mod_transition(mod_start, fstate)
    ta.mult_transition(mult_start, add_start)
    ta.go_to_start(go_to_start_for_mod, mod_start)
    ta.go_to_start(go_to_start_for_mult, mult_start)
    ta.bound_comparator_transition(start, go_to_start_for_mult, go_to_start_for_mod)

    m = Machine(sstate, ta.transitions, [fstate])
    result = m.inputString(tape)
    print(Utils.unary_to_int(result))


if __name__ == "__main__":
    argv = sys.argv
    main(argv)

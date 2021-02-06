class DFA(object):
    def __init__(self, symbols, states, transitions, initial_state, final_states):
        self.errors = []
        self.symbols = symbols
        self.states = states
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states
        
        self.validate_dfa()
    

    def validate_dfa(self):
        if not isinstance(self.symbols, set):
            self.errors.append("Symbols must be a set.")
            return False

        if not isinstance(self.states, set):
            self.errors.append("States must be a set.")
            return False
        
        if not isinstance(self.transitions, dict):
            self.errors.append("Transitions must be a dictionary.")
            return False

        if not isinstance(self.initial_state, str):
            self.errors.append("Initial state must be a string.")
            return False

        if not isinstance(self.final_states, set):
            self.errors.append("Final states must be a set.")
            return False

        if self.initial_state == "":
            self.errors.append("Initial state can not be empty.")
            return False

        if self.initial_state not in self.states:
            self.errors.append(f"Initial state '{self.initial_state}' is not defined.")
            return False

        for state in self.final_states:
            if state not in self.states:
                self.errors.append(f"Final state '{state}' is not defined.")
                return False

        if len(self.transitions) < 1:
            self.errors.append(f"Transitions can not be empty.")
            return False

        for state in self.states:
            if not self.transitions.get(state):
                self.errors.append(f"Set transitions for state '{state}'.")
        
        for state in self.transitions:
            if state not in self.states:
                self.errors.append(f"You can not set transitions for state '{state}' because it is not defined.")
        
        for state in self.states:
            if self.transitions.get(state):
                for symbol in self.symbols:
                    if self.transitions[state].get(symbol):
                        if self.transitions[state][symbol] not in self.states:
                            self.errors.append(f"State '{self.transitions[state][symbol]}' is not defined. move({state},{symbol})={self.transitions[state][symbol]}.")
                    else:
                        self.errors.append(f"Set '{symbol}' transition for state '{state}'")

        for state in self.transitions:
            if state in self.states:
                for symbol in self.transitions[state]:
                    if symbol not in self.symbols:
                        self.errors.append(f"Symbol '{symbol}' is not defined. move({state},{symbol})={self.transitions[state][symbol]}")
    
    def print_errors(self):
        print(self, "not valid")
        for error in self.errors:
            print("    " + error)


    def try_string(self, string):
        if len(self.errors) > 0:
            self.print_errors()
            return False
        
        current_state = self.initial_state
        last_final_state = None
        index_last_final_char = None
        counter = 0
        for char in string:
            if char not in self.symbols:
                break
            if current_state in self.final_states:
                last_final_state = current_state
                index_last_final_char = counter - 1
            current_state = self.transitions[current_state][char]
            counter += 1
        
        if current_state in self.final_states:
            return (True, {'final state':current_state})

        return (False,{'last state':current_state, 'last final state':last_final_state, 'index last final char':index_last_final_char})


class InputValidation(DFA):
    def __init__(self):
        digits = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
        alphabet = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
        symbols = []
        for i in range(256):
            symbols.append(chr(i))
            
        symbols = set(symbols)
        states = {'A', 'id', 'int', '+', '*', ':=', '(', ')', 'TRAP', ':'}
        initial_state = 'A'
        final_states = {'id', 'int', '+', '*', ':=', '(', ')'}
        
        transitions = {'A' : {}, 'id' : {}, 'int' : {}, '+' : {}, '*' : {}, '(' : {}, ')' : {}, ':' : {}, ':=' : {}, 'TRAP' : {}}
        for state in states:
            for symbol in symbols:
                if state == 'A':
                    if symbol == '+':
                        transitions[state][symbol] = '+'
                    elif symbol == '*':
                        transitions[state][symbol] = '*'
                    elif symbol == '(':
                        transitions[state][symbol] = '('
                    elif symbol == ')':
                        transitions[state][symbol] = ')'
                    elif symbol == ':':
                        transitions[state][symbol] = ':'
                    elif symbol in digits:
                        transitions[state][symbol] = 'int'
                    elif symbol in alphabet:
                        transitions[state][symbol] = 'id'
                    else:
                        transitions[state][symbol] = 'TRAP'
                elif state == '+' or state == '*' or state == '(' or state == ')' or state == ':=':
                    transitions[state][symbol] = 'TRAP'
                elif state == ':':
                    if symbol == '=':
                        transitions[state][symbol] = ':='
                    else:
                        transitions[state][symbol] = 'TRAP'
                elif state == 'int':
                    if symbol in digits:
                        transitions[state][symbol] = 'int'
                    else:
                        transitions[state][symbol] = 'TRAP'
                elif state == 'id':
                    if symbol in alphabet or symbol in digits:
                        transitions[state][symbol] = 'id'
                    else:
                        transitions[state][symbol] = 'TRAP'
                elif state == 'TRAP':
                    transitions[state][symbol] = 'TRAP'

        super().__init__(symbols, states, transitions, initial_state, final_states)


    def try_input(self, string):
        return self.try_string(string)

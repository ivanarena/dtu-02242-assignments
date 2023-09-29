import json
import pprint

# import json
# from pprint import pprint

# f = open('Simple.json')

# data = json.load(f)


# pretty_json = json.dumps(data, indent=4)
# print(pretty_json)
# print(data.keys())

# pprint(data['methods'])

# f.close()


class Interpreter:

    def __init__(self, program_filename: str):

        with open(program_filename) as program_file:
            file_contents = program_file.read()

        parsed_data = json.loads(file_contents)

        # Extract methods into a dictionary
        self.methods_dict = {
            method["name"]: method for method in parsed_data["methods"]}

        self.methods_names = []
        for method in parsed_data["methods"]:
            self.methods_names.append(method["name"])
        self.methods_names.pop(0)  # remove init method

        self.bytecodes = {}  # Initialize the bytecodes dictionary

        for method_name in self.methods_names:
            self.bytecodes[method_name] = self.methods_dict[method_name]['code']['bytecode']

        self.stack = []
        self.memory = []

        # print(self.methods_dict[self.methods_names[0]]['code']['bytecode'])

    def _push(self, op):
        value = op['value']['value']
        if value > 0:
            self.stack.append('+')
        elif value < 0:
            self.stack.append('-')
        else:
            self.stack.append('0')

    def _store(self, op):
        if len(self.memory)-1 < op['index']:
            self.memory.append(self.stack[-1])
        else:
            self.memory[op['index']] = self.stack[-1]

    def _load(self, op):
        self.stack.append(self.memory[op['index']])

    def _sub(self):
        # which one comes first?
        if self.stack[-1] == '+' and self.stack[-2] == '+':
            self.stack.append('0')  # suppose it's 0
        elif self.stack[-1] == '+' and self.stack[-2] == '-':
            print('problema')
        elif self.stack[-1] == '-' and self.stack[-2] == '+':
            print('no problema')
        elif self.stack[-1] == '-' and self.stack[-2] == '-':
            print('problema')

    def _div(self):
        if (self.stack[-1] == '0'):
            raise Exception("ArithmeticException")

    def run(self):
        for i in range(0, 10):
            if i in [3, 4, 5, 6, 7, 8]:
                continue
            try:

                method = self.methods_dict[self.methods_names[i]]

                # reset stack and memory
                self.stack = []
                self.memory = []

                # check for method parameters
                if method['params']:
                    for p in method['params']:
                        # if param is int add abstraction to stack
                        if (p['type']['base'] == 'int' or p['type']['base'] == 'float'):
                            self.memory.append('0')
                self._runBytecode(
                    self.bytecodes[method['name']])
                print(f'{self.methods_names[i]}: No.')
            except Exception as e:
                print(f'{self.methods_names[i]}: Yes, {e}.')

    def _runBytecode(self, bc):
        for op in bc:
            # print(self.memory, self.stack, op['opr'])
            if op['opr'] == 'push':
                self._push(op)
            elif op['opr'] == 'store':
                self._store(op)
            elif op['opr'] == 'load':
                self._load(op)
            elif op['opr'] == 'binary':

                if op['operant'] == 'sub':
                    self._sub()

                if op['operant'] == 'div':
                    self._div()

        print('stack: ', self.stack)
        print('memory: ', self.memory)

    # def run(self, f: tuple[Locals, OperStack, ProgramCounter]):
    #     self.stack.append(f)
    #     self.log_start()
    #     self.log_state()
    #     while self.step():
    #         self.log_state()
    #         continue
    #     self.log_done()

    # def step(self):
    #     (l, s, pc) = self.stack[-1]
    #     b = self.program.bytecode[pc]
    #     if hasattr(self, b["opr"]):
    #         return getattr(self, b["opr"])(b)
    #     else:
    #         return False

    # def pop(self, b):
    #     (l, s, pc) = self.stack.pop(-1)
    #     # Rule (pop_1)
    #     if b["words"] == 1:
    #         if len(s) < 1:
    #             return False
    #         self.stack.append((l, s[:-1], pc + 1))
    #     # Rule (pop_2)
    #     elif b["words"] == 2:
    #         if len(s) < 2:
    #             return False
    #         self.stack.append((l, s[:-2], pc + 1))
    #     else:
    #         return False


def main():
    program_filename = 'json/Arithmetics.json'
    interpreter = Interpreter(program_filename)
    interpreter.run()


if __name__ == "__main__":
    main()

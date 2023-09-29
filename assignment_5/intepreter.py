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
        self.stack.append(op['value']['value'])

    def run(self):
        for i in range(0, 2):
            try:

                method = self.methods_dict[self.methods_names[i]]

                # reset stack and memory
                self.stack = []
                self.memory = []

                # check for method parameters
                if method['params']:
                    for p in method['params']:
                        # if param is int add abstraction to stack
                        if (p['type']['base'] == 'int'):
                            self.memory.append('0')
                self._runBytecode(
                    self.bytecodes[method['name']])
            except Exception as e:
                print(f'{self.methods_names[i]}: Yes, {e}')

    def _runBytecode(self, bc):
        for op in bc:
            # print(self.memory, self.stack, op['opr'])
            if op['opr'] == 'push':
                self._push(op)
            elif op['opr'] == 'store':
                if len(self.memory)-1 < op['index']:
                    self.memory.append(self.stack[-1])
                else:
                    self.memory[op['index']] = self.stack[-1]
            elif op['opr'] == 'load':
                self.stack.append(self.memory[op['index']])
            elif op['opr'] == 'binary':

                if op['operant'] == 'sub':
                    # which one comes first?
                    sub = self.stack[-1] - self.stack[-2]
                    self.stack.append(sub)

                if op['operant'] == 'div':
                    if (self.stack[-1] == 0):
                        raise Exception("ArithmeticException")

        print(self.stack)
        print(self.memory)

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

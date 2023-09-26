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

        self.memory = {}
        self.stack = []

        self.bytecodes = {}  # Initialize the bytecodes dictionary

        for method_name in self.methods_names:
            self.bytecodes[method_name] = self.methods_dict[method_name]['code']['bytecode']

        # print(self.methods_dict[self.methods_names[0]]['code']['bytecode'])

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
    program_filename = 'Array.json'
    interpreter = Interpreter(program_filename)


if __name__ == "__main__":
    main()

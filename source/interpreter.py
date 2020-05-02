from parser import Program
import sys

variables = dict()


def evaluate(expression):
    print(expression)
    return str()


myProgram = Program()
myProgram.lines()

for line in myProgram.statements:
    print(len(line))


for line in myProgram.statements:
    t = line[0].lower
    if t == "end":
        sys.exit(0)
    elif t == "rem":
        pass
    elif t == "print_ex":
        print(str(evaluate(line[1])))
    elif t == "let":
        variables[str(line[1])] = evaluate(line[2])
    elif t == "if":
        condition = evaluate(line[1])
        if condition:
            evaluate(line[2])
    elif t == "expression":
        evaluate(line[1])
    else:
        print("go crazy go stupid")

from parser import Program
import sys

variables = dict()
op = {'+': lambda x, y: x + y,
      '-': lambda x, y: x - y,
      '*': lambda x, y: x * y,
      '/': lambda x, y: x / y,
      'and': lambda x, y: x and y,
      'or': lambda x, y: x or y,
      '>': lambda x, y: x > y,
      '<': lambda x, y: x < y,
      '==': lambda x, y: x == y,
      'not': lambda x: not x}


def evaluate(ex: list):
    if len(ex) == 3:
        op1 = ex[0]
        if op1 in variables.keys():
            op1 = variables[op1]
        op2 = ex[2]
        if op2 in variables.keys():
            op2 = variables[op2]
        try:
            return int(op[ex[1]](int(op1), int(op2)))
        except TypeError:
            return int(op[ex[1]](op1, op2))
    elif len(ex) == 2:
        op1 = ex[1]
        if op1 in variables.keys():
            op1 = variables[op1]
        return op[ex[0]](op1)
    else:
        try:
            return variables[ex[0]]
        except KeyError:
            try:
                return int(ex[0])
            except ValueError:
                return ex[0][1:-1]
        except ValueError:
            return str(ex[0])


def evaluateStatement(statement):
    t = statement[0].lower()
    if t == "end":
        sys.exit('End found in interpreter')
    elif t == "rem":
        pass
    elif t == "print":
        print(str(evaluate(statement[1])))
    elif t == "let":
        variables[str(statement[1])] = evaluate(statement[2])
    elif t == "if":
        condition = evaluate(statement[1])
        if condition:
            evaluateStatement(statement[2])
    elif t == "expression":
        evaluate(statement[1])
    else:
        print('Statement type unknown')


myProgram = Program()
myProgram.lines()
for line in myProgram.statements:
    evaluateStatement(line)

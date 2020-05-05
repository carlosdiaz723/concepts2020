'''
Names / Emails:
Carlos Diaz             cdiaz29@students.kennesaw.edu
Benjamin Cervantes     bcervan4@students.kennesaw.edu
Aydan Mufti             amufti1@students.kennesaw.edu


College of Computing and Software Engineering
Department of Computer Science
---------------------------------------------
CS4308: CONCEPTS OF PROGRAMMING LANGUAGES
SECTION W01 – SPRING 2020
---------------------------------------------
Course Project
FINAL Deliverable: Full Interpreter


File Description:
**THIS IS THE ONLY FILE THAT SHOULD BE RAN.**
**It should be ran from the 'source' directory.**

Note: All python files are pep8/pycodestyle compliant.
'''

from parser import Program
import sys
from lexicalRules import operations as op


# simulation a variable look-up table
variables = dict()


def evaluateExpression(ex: list):
    '''
    Main function to evaluate expressions.
    Input: list()
    Output: Result of expression
    '''
    # In the case of binary operations
    if len(ex) == 3:
        op1 = ex[0]
        # attempt to find variable in look-up table
        if op1 in variables.keys():
            op1 = variables[op1]
        op2 = ex[2]
        if op2 in variables.keys():
            op2 = variables[op2]
        try:
            # attempt arithmetic
            return int(op[ex[1]](int(op1), int(op2)))
        except TypeError:
            return int(op[ex[1]](op1, op2))
    elif len(ex) == 2:
        # in the case of unary operation
        op1 = ex[1]
        # attempt to find variable in look-up table
        if op1 in variables.keys():
            op1 = variables[op1]
        return op[ex[0]](op1)
    else:
        try:
            # attempt to return value of variable
            return variables[ex[0]]
        except KeyError:
            try:
                # return arithmetically
                return int(ex[0])
            except ValueError:
                # return as string
                return ex[0][1:-1]
        except ValueError:
            return str(ex[0])


def evaluateStatement(statement):
    '''
    Main function to evaluate statements
    Input: a tuple in the form of
            (statementType, info1, info2, ...)
        where length varies depending on statementType
    Output: The given statement has been "executed". This may be "invisible"
            unless a print statement is used.
    '''
    # store statementType
    statementType = statement[0].lower()
    if statementType == "end":
        sys.exit(0)
    elif statementType == "rem":
        # the interpreter ignores Remarks
        pass
    elif statementType == "print":
        print(str(evaluateExpression(statement[1])))
    elif statementType == "let":
        # instantiated variables are stored in the look-up table
        variables[str(statement[1])] = evaluateExpression(statement[2])
    elif statementType == "if":
        # the boolean condition is evaluated and the respective expression
        # is "interpreted" if and only if the condition is equivalent to True
        condition = evaluateExpression(statement[1])
        if condition:
            evaluateStatement(statement[2])
    elif statementType == "expression":
        evaluateExpression(statement[1])
    else:
        print('Statement type unknown')


# create program object
myProgram = Program()

# run parser
myProgram.lines()

# evaluate each statement in the list that the program object contains
for statement in myProgram.statements:
    evaluateStatement(statement)

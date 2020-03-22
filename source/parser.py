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
2nd Deliverable: Parser


File Description:
THIS IS THE ONLY FILE THAT SHOULD BE RAN.
It should be ran from the 'source' directory.

Note: All python files are pep8/pycodestyle compliant.
'''

import scanner
import sys
import lexicalRules as l
import re
from pprint import pprint as pretty
# Will keep track of the current token

global currentToken
currentToken = 0
global tokenList
tokenList = scanner.getAllTokens()
pretty(tokenList[20:])

'''
    Need to create a function for each grammar rule in grammarRules.py
    each token passed from the tokenList variable to the correct function
    Will be using the top down approach (Recursive Descent) to build the parse
    tree
    http://effbot.org/zone/simple-top-down-parsing.htm
'''


def matchKey(pattern: str):
    return re.search(l.keywords[pattern],
                     tokenList[currentToken][2]) is not None


def matchLit(pattern: str):
    return re.search(l.literals[pattern],
                     tokenList[currentToken][2]) is not None


def lines():
    '''
    Starting point for the parser.
    BNF rule:
    <Lines> ::= Integer <Statement> NewLine <Lines>
              | Integer <Statement> NewLine
    '''
    global currentToken

    print("enter <lines>")
    assert matchLit('integer'), 'integer expected, not found'
    print('Integer Line Number found: ', tokenList[currentToken][2])
    currentToken += 1
    statement()
    assert matchKey('newLine'), '<newline> expected, instead found: '\
        + str(tokenList[currentToken][1:2])
    print('newLine found')
    currentToken += 1
    if currentToken == len(tokenList) - 1:
        print("exit <lines>")
    else:
        lines()


def statement():
    '''
    BNF rule:
    <Statement> ::= END
                  | GOTO <Expression>
                  | IF <Expression> THEN <Statement>
                  | LET Id '=' <Expression>
                  | PRINT <Expression>
                  | PRINT '#' Integer ',' <Expression>
                  | REM Remark
                  | <Expression>
    '''
    global currentToken
    print('enter <statement>')
    if matchKey('end'):
        sys.exit('END found, terminating parse.')
    elif matchKey('goTo'):
        print('GOTO key found')
        currentToken += 1
        expression()
    elif matchKey('if'):
        print('IF key found')
        currentToken += 1
        expression()
        assert matchKey('then'), 'THEN expected, not found'
        print('THEN key found')
        currentToken += 1
        expression()
    elif matchKey('instantiation'):
        print('LET key found')
        currentToken += 1
        assert matchLit(
            'printable'), 'printable identifier expected, not found'
        print('PRINTABLE/ID found: ', tokenList[currentToken][2])
        currentToken += 1
        assert matchKey(
            'assignment'), 'assignment operator expected, not found'
        print('ASSIGNMENT key (=) found')
        currentToken += 1
        expression()
    elif matchKey('print'):
        print('PRINT key found')
        currentToken += 1
        if matchKey('pound'):
            print('POUND key found')
            currentToken += 1
            assert matchLit('integer'), 'integer expected, not found'
            print('Integer Line Number found: ', tokenList[currentToken][2])
            currentToken += 1
            assert matchKey('comma'), 'comma expected, not found'
            print('COMMA key found')
            currentToken += 1
            expression()
        else:
            currentToken += 1
            expression()
    elif matchKey('remark'):
        print('REM key found, enter Remark')
        currentToken += 1
        remarkString = ""
        assert matchLit('printable'), 'printable expected, not found'
        remarkString += scanner.getToken(currentToken)[2] + " "
        currentToken += 1
        while matchLit('printable') and not matchKey('newLine'):
            remarkString += scanner.getToken(currentToken)[2] + " "
            currentToken += 1
        print("Remark found: ", remarkString)
    else:
        expression()

    print('exit <statement>')


def expression():
    '''
    BNF Rule:
    <Expression> ::= <And Exp> OR <Expression>
                   | <And Exp>
    '''
    global currentToken
    print('enter <expression>')
    andExp()
    currentToken += 1
    if matchKey('or'):
        print('OR key found')
        currentToken += 1
        expression()
    else:
        currentToken -= 1
    print('exit <expression>')


def andExp():
    global currentToken
    print('enter <andExp>')
    notExp()
    currentToken += 1
    if matchKey('and'):
        print('and key found')
        currentToken += 1
        andExp()
    else:
        currentToken -= 1
    print('exit <andExp>')


def notExp():
    global currentToken
    print('enter <notExp>')
    if matchKey('negation'):
        print('boolean negation (not) key found')
        currentToken += 1
    compareExp()
    print('exit <notExp>')


def compareExp():
    global currentToken
    print('enter <compareExp>')
    addExp()
    currentToken += 1
    if tokenList[currentToken][4] in ['isEqualTo', 'greaterT', 'lessThan']:
        print('comparator found: ', tokenList[currentToken][2])
        comparator()  # questionable
        currentToken += 1
        compareExp()
    else:
        currentToken -= 1
    print('exit <compareExp>')


def comparator():
    global currentToken
    print('comparator identified: ', end='')
    if matchKey('isEqualTo'):
        print(' isEqualTo ')
    elif matchKey('greaterT'):
        print(' greaterT ')
    elif matchKey(' lessThan '):
        print(' lessThan ')
    else:
        sys.exit('UNEXPECTED ERROR')


def addExp():
    global currentToken
    print('enter <addExp>')
    multExp()
    currentToken += 1
    if matchKey('plus'):
        print('plus (+) key found')
        currentToken += 1
        addExp()
    elif matchKey('minus'):
        print('minus (-) key found')
        currentToken += 1
        addExp()
    else:
        currentToken -= 1
    print('exit <addExp>')


def multExp():
    global currentToken
    print('enter <multExp>')
    negateExp()
    currentToken += 1
    if matchKey('multiplication'):
        print('multiplication (*) key found')
        currentToken += 1
        multExp()
    elif matchKey('division'):
        print('division (/) key found')
        currentToken += 1
        multExp()
    else:
        currentToken -= 1
    print('exit <multExp>')


def negateExp():
    global currentToken
    print('enter <negateExp>')
    if matchKey('minus'):
        print('numerical negation (-) key found')
        currentToken += 1
    value()
    print('exit <negateExp>')


def value():
    global currentToken
    if matchKey('openParen'):
        print('open parenthesis found')
        currentToken += 1
        expression()
        assert matchKey('closeParen'),\
            'closing parenthesis expected, instead found' + \
            str(tokenList[currentToken][1:3])
    elif matchLit('printable'):
        print('printable value found: ', tokenList[currentToken][2])
        currentToken += 1
        if matchKey('openParen'):
            print('open parenthesis found')
            currentToken += 1
            expression()
            assert matchKey('closeParen'),\
                'closing parenthesis expected, not found'
    else:
        constant()
    print('exit <value>')


def constant():
    global currentToken
    print('enter <constant>')
    if matchLit('string'):
        print('string found: ', tokenList[currentToken][2])
        currentToken += 1
    elif matchLit('integer'):
        print('integer found: ', tokenList[currentToken][2])
        currentToken += 1
    else:
        sys.exit('UNEXPECTED ERROR')
    print('exit <constant>')


lines()

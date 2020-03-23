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
# Will keep track of the current token

global currentToken
currentToken = 0
global tokenList
tokenList = scanner.getAllTokens()


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
    print('\\enter <lines>')
    assert matchLit('integer'), 'integer expected, instead found: '\
        + str(tokenList[currentToken][2])
    print('LINE NUMBER found: ', tokenList[currentToken][2])
    currentToken += 1
    statement()
    assert matchKey('newLine'), '<newline> expected, instead found: '\
        + str(tokenList[currentToken][2])
    print('NEWLINE found')
    currentToken += 1
    if currentToken == len(tokenList) - 1:
        print("terminating")
    else:
        lines()
    print('/exit <lines>')


def statement():
    '''
    BNF rule:
    <Statement> ::= END
                  | GOTO Integer
                  | IF <Expression> THEN <Statement>
                  | LET Id '=' <Expression>
                  | PRINT <Expression>
                  | PRINT '#' Integer ',' <Expression>
                  | REM Remark
                  | <Expression>
    '''
    global currentToken
    print('\\enter <statement>')
    if matchKey('end'):
        sys.exit('END found, terminating parse.')
    elif matchKey('goTo'):
        print('GOTO key found')
        currentToken += 1
        assert matchLit('integer'), 'integer line number expected, not found'
        print('Integer line number found: ', tokenList[currentToken][2])
        currentToken += 1
    elif matchKey('if'):
        print('IF key found')
        currentToken += 1
        assert matchKey('openParen'), 'open parenthesis expected, not found'
        print('open parenthesis found')
        currentToken += 1
        expression()
        assert matchKey('closeParen'),\
            'close parenthesis expected, instead found ' + \
            tokenList[currentToken][2]
        currentToken += 1
        assert matchKey('then'), 'THEN expected, not found'
        print('THEN key found')
        currentToken += 1
        statement()
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

    print('/exit <statement>')


def expression():
    '''
    BNF Rule:
    <Expression> ::= <And Exp> OR <Expression>
                   | <And Exp>
    '''
    global currentToken
    print('\\enter <expression>')
    andExp()
    currentToken += 1
    if matchKey('or'):
        print('OR key found')
        currentToken += 1
        expression()
    else:
        currentToken -= 1
    print('/exit <expression>')


def andExp():
    '''
    BNF Rule:
    <And Exp> ::= <Not Exp> AND <And Exp>
                | <Not Exp>
    '''
    global currentToken
    print('\\enter <andExp>')
    notExp()
    currentToken += 1
    if matchKey('and'):
        print('and key found')
        currentToken += 1
        andExp()
    else:
        currentToken -= 1
    print('/exit <andExp>')


def notExp():
    '''
    BNF Rule:
    <Not Exp> ::= NOT <Compare Exp>
                | <Compare Exp>
    '''
    global currentToken
    print('\\enter <notExp>')
    if matchKey('negation'):
        print('boolean negation (not) key found')
        currentToken += 1
    compareExp()
    print('/exit <notExp>')


def compareExp():
    '''
    BNF Rule:
    <Compare Exp> ::= <Add Exp> <Comparator> <Add Exp>
                    | <Add Exp>
    '''
    global currentToken
    print('\\enter <compareExp>')
    addExp()
    currentToken += 1
    if tokenList[currentToken - 1][4] in ['isEqualTo', 'greaterT', 'lessThan']:
        print('comparator found: ', tokenList[currentToken - 1][2])
        currentToken -= 1
        comparator()  # questionable
        currentToken += 1
        addExp()
    else:
        currentToken -= 1
    print('/exit <compareExp>')


def comparator():
    '''
    BNF Rule:
    <Comparator> ::= '=='
                   | '>'
                   | '<'
    '''
    global currentToken
    print('comparator identified: ', end='')
    if matchKey('isEqualTo'):
        print(' isEqualTo ')
    elif matchKey('greaterT'):
        print(' greaterT ')
    elif matchKey(' lessThan '):
        print(' lessThan ')
    else:
        sys.exit('UNEXPECTED ERROR 1')


def addExp():
    '''
    BNF Rule:
    <Add Exp> ::= <Mult Exp> '+' <Add Exp>
                | <Mult Exp> '-' <Add Exp>
                | <Mult Exp>
    '''
    global currentToken
    print('\\enter <addExp>')
    multExp()
    if matchKey('plus'):
        print('plus (+) key found')
        currentToken += 1
        addExp()
    elif matchKey('minus'):
        print('minus (-) key found')
        currentToken += 1
        addExp()
    print('/exit <addExp>')


def multExp():
    '''
    BNF Rule:
    <Mult Exp> ::= <Negate Exp> '*' <Mult Exp>
                 | <Negate Exp> '/' <Mult Exp>
                 | <Negate Exp>
    '''
    global currentToken
    print('\\enter <multExp>')
    negateExp()
    if matchKey('multiplication'):
        print('multiplication (*) key found')
        currentToken += 1
        multExp()
    elif matchKey('division'):
        print('division (/) key found')
        currentToken += 1
        multExp()
    print('/exit <multExp>')


def negateExp():
    '''
    BNF Rule:
    <Negate Exp> ::= '-' <Value>
                   | <Value>
    '''
    global currentToken
    print('\\enter <negateExp>')
    if matchKey('minus'):
        print('numerical negation (-) key found')
        currentToken += 1
    value()
    print('/exit <negateExp>')


def value():
    '''
    BNF Rule:
    <Value> ::= '(' <Expression> ')'
              | ID '(' <Expression> ')'
              | <Constant>
    '''
    global currentToken
    if matchKey('openParen'):
        print('open parenthesis found')
        currentToken += 1
        expression()
        assert matchKey('closeParen'), 'close parenthesis expected, not found'
        print('close parenthesis found')
        currentToken += 1
    elif matchLit('printable') and tokenList[currentToken + 1] == '(':
        print('printable found: ', tokenList[currentToken][2])
        currentToken += 1
        assert matchKey('openParen'), 'close parenthesis expected, not found'
        print('open parenthesis found')
        currentToken += 1
        expression()
        assert matchKey(
            'closeParen'), 'close parenthesis expected, not found'
    else:
        constant()


def constant():
    '''
    BNF Rule:
    <Constant> ::= Integer
                 | String
    '''
    global currentToken
    print('\\enter <constant>')
    if matchLit('string'):
        print('string found: ', tokenList[currentToken][2])
        currentToken += 1
    elif matchLit('integer'):
        print('integer found: ', tokenList[currentToken][2])
        currentToken += 1
    elif matchLit('printable'):
        print('printable found: ', tokenList[currentToken][2])
        currentToken += 1
    else:
        sys.exit('UNEXPECTED ERROR 2')
    print('/exit <constant>')


lines()

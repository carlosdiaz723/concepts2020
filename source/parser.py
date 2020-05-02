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
# pretty(tokenList)


def matchKey(pattern: str):
    return re.search(l.keywords[pattern],
                     tokenList[currentToken][2]) is not None


def matchLit(pattern: str):
    return re.search(l.literals[pattern],
                     tokenList[currentToken][2]) is not None


class Program:
    '''
    Starting point for the parser.
    BNF rule:
    <Lines> ::= Integer <Statement> NewLine <Lines>
              | Integer <Statement> NewLine
    '''

    statements = list()

    def lines(self):
        global currentToken
        self.statements.append(self.statement())
        currentToken += 1
        if currentToken == len(tokenList) - 1 and matchKey('end'):
            # print("Finished Parsing")
            self.statements.append(('end', None))
        else:
            self.lines()
        return

    def statement(self):
        '''
        BNF rule:
        <Statement> ::= END
                    | IF <Expression> THEN <Statement>
                    | LET Id '=' <Expression>
                    | PRINT <Expression>
                    | REM Remark
                    | <Expression>
        '''
        self.type = str()
        global currentToken
        # print('\\enter <statement>')
        if matchKey('end'):
            kind = "end"
            print("end found in parser")
            return tuple(kind, None)
        elif matchKey('if'):
            kind = "if"
            currentToken += 1
            assert matchKey(
                'openParen'), 'open parenthesis expected, not found'
            currentToken += 1
            expression = self.expression()
            assert matchKey('closeParen'),\
                'close parenthesis expected, instead found ' + \
                tokenList[currentToken][2]
            currentToken += 1
            assert matchKey('then'), 'THEN expected, not found'
            currentToken += 1
            statement = self.statement()
            return (kind, expression, statement)
        elif matchKey('instantiation'):
            kind = "let"
            currentToken += 1
            assert matchLit(
                'printable'), 'printable identifier expected, not found'
            # print('PRINTABLE/ID found: ', tokenList[currentToken][2])
            ident = tokenList[currentToken][2]
            currentToken += 1
            assert matchKey(
                'assignment'), 'assignment operator expected, not found'
            # print('ASSIGNMENT key (=) found')
            currentToken += 1
            expression = self.expression()
            return (kind, ident, expression)
        elif matchKey('print'):
            kind = "PRINT"
            currentToken += 1
            expression = self.expression()
            return (kind, expression)
        elif matchKey('remark'):
            kind = "rem"
            currentToken += 1
            remarkString = ""
            assert matchLit('printable'), 'printable expected, not found'
            remarkString += scanner.getToken(currentToken)[2] + " "
            currentToken += 1
            while matchLit('printable') and not matchKey('newLine'):
                remarkString += scanner.getToken(currentToken)[2] + " "
                currentToken += 1
            return (kind, remarkString)
        else:
            kind = 'expression'
            expression = self.expression()
            return (kind, expression)
        # print('/exit <statement>')

    def expression(self):
        '''
        BNF Rule:
        <Expression> ::= <And Exp> OR <Expression>
                    | <And Exp>
        '''
        global currentToken
        # print('\\enter <expression>')
        andExp = self.andExp()
        currentToken += 1
        if matchKey('or'):
            currentToken += 1
            expression = self.expression()
            expression.insert(0, 'or')
            for element in expression:
                andExp.append(element)
        else:
            currentToken -= 1
        return andExp

    def andExp(self):
        '''
        BNF Rule:
        <And Exp> ::= <Not Exp> AND <And Exp>
                    | <Not Exp>
        '''
        global currentToken
        # print('\\enter <andExp>')
        notExp = self.notExp()
        currentToken += 1
        if matchKey('and'):
            currentToken += 1
            andExp = self.andExp()
            andExp.insert(0, 'and')
            for element in andExp:
                notExp.append(element)
        else:
            currentToken -= 1
        return notExp
        # print('/exit <andExp>')

    def notExp(self):
        '''
        BNF Rule:
        <Not Exp> ::= NOT <Compare Exp>
                    | <Compare Exp>
        '''
        global currentToken
        # print('\\enter <notExp>')
        negation = False
        if matchKey('negation'):
            # print('boolean negation (not) key found')
            negation = True
            currentToken += 1
        compareExp = self.compareExp()
        if negation:
            compareExp.insert(0, 'not')
        return compareExp
        # print('/exit <notExp>')

    def compareExp(self):
        '''
        BNF Rule:
        <Compare Exp> ::= <Add Exp> <Comparator> <Add Exp>
                        | <Add Exp>
        '''
        global currentToken
        # print('\\enter <compareExp>')
        addExp = self.addExp()
        currentToken += 1
        if tokenList[currentToken - 1][4] in ['isEqualTo', 'greaterT',
                                              'lessThan']:
            # print('comparator found: ', tokenList[currentToken - 1][2])
            currentToken -= 1
            addExp.append(self.comparator())
            currentToken += 1
            secondAdd = self.addExp()
            for element in secondAdd:
                addExp.append(element)
        else:
            currentToken -= 1
        # print('/exit <compareExp>')
        return addExp

    def comparator(self):
        '''
        BNF Rule:
        <Comparator> ::= '=='
                    | '>'
                    | '<'
        '''
        global currentToken
        # print('comparator identified: ', end='')
        if matchKey('isEqualTo'):
            return '=='
        elif matchKey('greaterT'):
            return '>'
        elif matchKey('lessThan'):
            return '<'
        else:
            sys.exit('UNEXPECTED ERROR 1')

    def addExp(self):
        '''
        BNF Rule:
        <Add Exp> ::= <Mult Exp> '+' <Add Exp>
                    | <Mult Exp> '-' <Add Exp>
                    | <Mult Exp>
        '''
        global currentToken
        # print('\\enter <addExp>')
        multExp = self.multExp()
        if matchKey('plus'):
            # print('plus (+) key found')
            multExp.append('+')
            currentToken += 1
            secondMult = self.addExp()
            for element in secondMult:
                multExp.append(element)
        elif matchKey('minus'):
            # print('minus (-) key found')
            multExp.append('-')
            currentToken += 1
            secondMult = self.addExp()
            for element in secondMult:
                multExp.append(element)
        # print('/exit <addExp>')
        return multExp

    def multExp(self):
        '''
        BNF Rule:
        <Mult Exp> ::= <Negate Exp> '*' <Mult Exp>
                    | <Negate Exp> '/' <Mult Exp>
                    | <Negate Exp>
        '''
        global currentToken
        # print('\\enter <multExp>')
        negateExp = self.negateExp()
        if matchKey('multiplication'):
            # print('multiplication (*) key found')
            negateExp.append('*')
            currentToken += 1
            multExp = self.multExp()
            for element in (multExp):
                negateExp.append(element)
        elif matchKey('division'):
            # print('division (/) key found')
            negateExp.append('/')
            currentToken += 1
            multExp = self.multExp()
            for element in (multExp):
                negateExp.append(element)
        # print('/exit <multExp>')
        return negateExp

    def negateExp(self):
        '''
        BNF Rule:
        <Negate Exp> ::= '-' <Value>
                    | <Value>
        '''
        global currentToken
        # print('\\enter <negateExp>')
        negate = False
        if matchKey('minus'):
            # print('numerical negation (-) key found')
            negate = True
            currentToken += 1
        value = self.value()
        if negate:
            value.insert(0, '-')
        # print('/exit <negateExp>')
        return value

    def value(self):
        '''
        BNF Rule:
        <Value> ::= '(' <Expression> ')'
                | <Constant>
        '''
        global currentToken
        if matchKey('openParen'):
            # print('open parenthesis found')
            currentToken += 1
            expression = self.expression()
            expression.insert(0, '(')
            assert matchKey(
                'closeParen'), 'close parenthesis expected, not found'
            # print('close parenthesis found')
            expression.append(')')
            currentToken += 1
            return expression
        else:
            return self.constant()

    def constant(self):
        '''
        BNF Rule:
        <Constant> ::= Integer
                    | String
        '''
        global currentToken
        # print('\\enter <constant>')
        if matchLit('string'):
            # print('string found: ', tokenList[currentToken][2])
            token = tokenList[currentToken][2]
            currentToken += 1
            return [token]
        elif matchLit('integer'):
            # print('integer found: ', tokenList[currentToken][2])
            token = tokenList[currentToken][2]
            currentToken += 1
            return list(token)
        elif matchLit('printable'):
            # print('printable found: ', tokenList[currentToken][2])
            token = tokenList[currentToken][2]
            currentToken += 1
            return list(token)
        else:
            sys.exit('Value cannot be parsed: ', tokenList[currentToken][2])
        # print('/exit <constant>')

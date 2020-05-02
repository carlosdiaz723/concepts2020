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


class program:
    '''
    Starting point for the parser.
    BNF rule:
    <Lines> ::= Integer <Statement> NewLine <Lines>
              | Integer <Statement> NewLine
    '''

    def lines(self):
        global currentToken
        self.statements = list()
        assert matchLit('integer'), 'integer expected, instead found: '\
            + str(tokenList[currentToken][2])
        currentToken += 1
        self.statements.append(self.statement())
        currentToken += 1
        if currentToken == len(tokenList) - 1:
            print("terminating")
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
                    | PRINT '#' Integer ',' <Expression>
                    | REM Remark
                    | <Expression>
        '''
        self.type = str()
        global currentToken
        #print('\\enter <statement>')
        if matchKey('end'):
            self.type = "END"
            return {"type": self.type}
        elif matchKey('if'):
            self.type = "IF"
            currentToken += 1
            assert matchKey(
                'openParen'), 'open parenthesis expected, not found'
            currentToken += 1
            self.expression = self.expression()
            assert matchKey('closeParen'),\
                'close parenthesis expected, instead found ' + \
                tokenList[currentToken][2]
            currentToken += 1
            assert matchKey('then'), 'THEN expected, not found'
            currentToken += 1
            self.statement = self.statement()
            return {"type": self.type,
                    "expression": self.expression,
                    "statement": self.statement}
        elif matchKey('instantiation'):
            self.type = "LET" 
            currentToken += 1
            assert matchLit(
                'printable'), 'printable identifier expected, not found'
            print('PRINTABLE/ID found: ', tokenList[currentToken][2])
            currentToken += 1
            assert matchKey(
                'assignment'), 'assignment operator expected, not found'
            print('ASSIGNMENT key (=) found')
            currentToken += 1
            self.expression() = self.expression()
        elif matchKey('print'):
            self.type = "PRINT"
            currentToken += 1
            if matchKey('pound'):
                self.type = "POUND"
                currentToken += 1
                assert matchLit('integer'), 'integer expected, not found'
                print('Integer Line Number found: ',
                      tokenList[currentToken][2])
                currentToken += 1
                assert matchKey('comma'), 'comma expected, not found'
                print('COMMA key found')
                currentToken += 1
                self.expression() = self.expression()
            else:
                self.expression() = self.expression()
        elif matchKey('remark'):
            self.type = "REM"
            currentToken += 1
            remarkString = ""
            assert matchLit('printable'), 'printable expected, not found'
            remarkString += scanner.getToken(currentToken)[2] + " "
            currentToken += 1
            while matchLit('printable') and not matchKey('newLine'):
                remarkString += scanner.getToken(currentToken)[2] + " "
                currentToken += 1
            #print("Remark found: ", remarkString)
        else:
            self.expression() = self.expression()
        return {"type": self.type, 
                "expression": self.expression,
                "statement": self.statement}
        #print('/exit <statement>')

    def expression(self):
        '''
        BNF Rule:
        <Expression> ::= <And Exp> OR <Expression>
                    | <And Exp>
        '''
        global currentToken
        #print('\\enter <expression>')
        self.andExp() = self.andExp()
        currentToken += 1
        if matchKey('or'):
            self.type = "OR"
            currentToken += 1
            self.expression() = self.expression()
        else:
            currentToken -= 1

    def andExp(self):
        '''
        BNF Rule:
        <And Exp> ::= <Not Exp> AND <And Exp>
                    | <Not Exp>
        '''
        global currentToken
        #print('\\enter <andExp>')
        self.notExp() = self.notExp()
        currentToken += 1
        if matchKey('and'):
            self.type = "and"
            currentToken += 1
            self.andExp() = self.andExp()
        else:
            currentToken -= 1
        return {
            "type": self.type,
            "expression": self.expression,
            "statement": self.statement}
        #print('/exit <andExp>')

    def notExp(self):
        '''
        BNF Rule:
        <Not Exp> ::= NOT <Compare Exp>
                    | <Compare Exp>
        '''
        global currentToken
        #print('\\enter <notExp>')
        if matchKey('negation'):
            print('boolean negation (not) key found')
            currentToken += 1
        self.compareExp() = self.compareExp()
        return {"type": self.type,
                "expression": self.expression,
                "statement": self.statement}
        #print('/exit <notExp>')

    def compareExp(self):
        '''
        BNF Rule:
        <Compare Exp> ::= <Add Exp> <Comparator> <Add Exp>
                        | <Add Exp>
        '''
        global currentToken
        #print('\\enter <compareExp>')
        self.addExp() = self.addExp()
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

    def comparator(self):
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

    def addExp(self):
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

    def multExp(self):
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

    def negateExp(self):
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

    def value(self):
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
            assert matchKey(
                'closeParen'), 'close parenthesis expected, not found'
            print('close parenthesis found')
            currentToken += 1
        elif matchLit('printable') and tokenList[currentToken + 1] == '(':
            print('printable found: ', tokenList[currentToken][2])
            currentToken += 1
            assert matchKey(
                'openParen'), 'close parenthesis expected, not found'
            print('open parenthesis found')
            currentToken += 1
            expression()
            assert matchKey(
                'closeParen'), 'close parenthesis expected, not found'
        else:
            constant()

    def constant(self):
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


program()

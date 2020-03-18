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
Lorem ipsum

Note: Lorem ipsum
'''

nonterminals = {
    '<Lines>': [['Integer', '<Statements>', 'NewLine', '<Lines>'],
                ['Integer', '<Statements>', 'NewLine']],

    '<Statements>': [['<Statement>', ':', '<Statements>'],
                     ['<Statement>']],

    '<Statement>': [['END'],
                    ['GOTO', '<Expression>'],
                    ['IF', '<Expression>', 'THEN', '<Statement>'],
                    ['LET', 'Id', '=', '<Expression>'],
                    ['PRINT', '<PrintList >'],
                    ['PRINT', '#', 'Integer', ',', '<PrintList>'],
                    ['Remark'],
                    ['<Expression>']],

    '<ExpressionList>': [['< Expression >', '<ExpressionList>'],
                         ['<Expression>']],

    '<PrintList>': [['<Expression>', ';', '<PrintList>'],
                    ['<Expression>']],

    '<Expression>': [['<AndExp>', 'OR', '<Expression>'],
                     ['<AndExp>']],

    '<AndExp>': [['<NotExp>', 'AND', '<AndExp>'],
                 ['<NotExp>']],

    '<NotExp>': [['NOT', '<CompareExp>'],
                 ['<CompareExp>']],

    '<CompareExp>': [['<AddExp>', '<Comparator>', '<CompareExp>'],
                     ['<AddExp>']],

    '<Comparator>': [['='],
                     ['>'],
                     ['>='],
                     ['<'],
                     ['<=']],

    '<AddExp>': [['<MultExp>', '+', '<AddExp>'],
                 ['<MultExp>', '-', '<AddExp>'],
                 ['< Mult Exp >']],

    '<MultExp>': [['<NegateExp>', '*', '<MultExp>'],
                  ['<NegateExp>', '/', '<MultExp>'],
                  ['<NegateExp>']],

    '<NegateExp>': [['-', '<PowerExp>'],
                    ['<PowerExp>']],

    '<PowerExp>': [['<PowerExp>', '^', '<Value>'],
                   ['<Value>']],

    '<Value>': [['(', '<Expression>', ')'],
                ['ID'],
                ['ID', '(', '<ExpressionList>', ')'],
                ['<Constant>']],

    '<Constant>': [['Integer'],
                   ['String'],
                   ['Real']]
}

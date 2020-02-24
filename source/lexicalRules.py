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
1st Deliverable: Scanner


File Description:
This is a storage file for the keywords that will be used to determine special
tokens apart from defined varaibles and comments. There is no logic or
exectuion in this file, it is solely to segment the storage of the following
dictionaries.

Note: Escape character '\' used for regular expression matching purposes. This
      is denoted and relayed to the compiler through the 'r' prefix for the
      strings. This way, the python compiler does not process the '\' as an
      excape, since it is NOT an escape in this context; it has actual meaning
      when using RegEx.
'''

keywords = {'remark': r'REM',
            'newLine': r'<newline>',
            'colon': r':',
            'pound': r'#',
            'assignment': r'=',
            'comma': r',',
            'semicolon': r';',
            'greaterThan': r'>',
            'forloop': r'FOR',
            'lessThan': r'<',
            'multiplication': r'\*',
            'plus': r'\+',
            'minus': r'-',
            'home': r'HOME',
            'or': r'OR',
            'and': r'AND',
            'goTo': r'GOTO',
            'if': r'IF',
            'end': r'END',
            'print': r'PRINT',
            'instantiation': r'LET',
            'text': r'TEXT',
            'openParens': r'\(',
            'closeParens': r'\)'
            }

literals = {'integer': r'^[+-]?(\d)*$',
            'real': r'[-+]?[0-9]*\.?[0-9]+',
            'string': r'\"(\w)*\"',
            'printable/id': r'(\w)*'
            }

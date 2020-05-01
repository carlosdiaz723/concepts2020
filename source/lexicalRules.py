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

keywords = {'remark': r'(?i)^REM$',
            'newLine': r'^<newline>$',
            'colon': r'^:$',
            'assignment': r'^=$',
            'comma': r'^,$',
            'semicolon': r'^;$',
            'pound': r'^#$',
            'greaterT': r'^>$',
            'lessThan': r'^<$',
            'isEqualTo': r'^==$',
            'multiplication': r'^\*$',
            'division': r'^/$',
            'plus': r'^\+$',
            'minus': r'^-$',
            'or': r'(?i)^OR$',
            'and': r'(?i)^AND$',
            'goTo': r'(?i)^GOTO$',
            'then': r'(?i)^THEN$',
            'negation': r'(?i)^NOT$',
            'if': r'(?i)^IF$',
            'end': r'(?i)^END$',
            'print': r'(?i)^PRINT$',
            'instantiation': r'(?i)^LET$',
            'openParen': r'^\($',
            'closeParen': r'^\)$'
            }

literals = {'integer': r'^[+-]?(\d)*$',
            # 'real': r'[-+]?[0-9]*\.?[0-9]+',
            'string': r'\"(\w)*\"',
            'printable': r'^([A-Za-z])([A-Za-z0-9])*$'
            }

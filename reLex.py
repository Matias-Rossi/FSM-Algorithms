from os import close
from sly import Lexer

class RELexer(Lexer):
    #Set of token names
    tokens = {SYMBOL, UNION, KLEENE, CONCAT, LPAREN, RPAREN}
    ignore = ' \t'

    SYMBOL  = r'[a-zA-Z]'
    UNION   = r'\+'
    KLEENE  = r'\*'
    CONCAT  = r'\.'
    LPAREN  = r'\('
    RPAREN  = r'\)'
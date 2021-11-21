from sly import Parser
from reLex import RELexer
from algorithms.thompson import Thompson
from automata import transitionTable
import os

log = False

class REParser(Parser):
    # Get token list from lexer
    tokens = RELexer.tokens
    debugfile = 'out/parser.out'
    cache = []
    generatedFSM = transitionTable()

    # Grammar rules
    '''
    1.  union_expr ::=      kleene_expr
                            | union_expr UNION kleene_expr
                            ;
        
    2.  kleene_expr ::=     concat_expr
                            | kleene_expr KLEENE concat_expr
                            ;

    3.  concat_expr ::=     primary_expr
                            | concat_expr CONCAT primary_expr
                            | concat_expr primary_expr
                            ;

    4.  primary_expr ::=    SYMBOL
                            | LPAREN union_expr RPAREN
                            ;
    '''

    # Start
    @_('union_expr')
    def start(self, e):
        if log: print('[LOG]: Returning generated FSM')
        return self.cache.pop()

    # 1
    @_('kleene_expr')
    def union_expr(self, e):
        ...

    @_('union_expr UNION kleene_expr')
    def union_expr(self, e):
        if log: print('[LOG]: Union found, applying algorithm...')
        self.cache.append(Thompson.thompsonUnion(self.cache.pop(), self.cache.pop()))

    # 2
    @_('concat_expr')
    def kleene_expr(self, e):
        ...

    @_('kleene_expr KLEENE')
    def kleene_expr(self, e):
        if log: print('[LOG]: Kleene found, applying algorithm...')
        self.cache.append(Thompson.thompsonKleene(self.cache.pop()))
    
    # 3
    @_('primary_expr')
    def concat_expr(self, e):
        ...

    @_('concat_expr CONCAT primary_expr')
    def concat_expr(self, e):
        if log: print('[LOG]: Explicit concatenation found, concatenating...')
        aux = [self.cache.pop(), self.cache.pop()]
        self.cache.append(Thompson.thompsonConcat(aux.pop(), aux.pop()))

    @_('concat_expr primary_expr')
    def concat_expr(self, e):
        if log: print('[LOG]: Implicit concatenation found, concatenating...')
        aux = [self.cache.pop(), self.cache.pop()]
        self.cache.append(Thompson.thompsonConcat(aux.pop(), aux.pop()))

    # 4
    @_('SYMBOL')
    def primary_expr(self, e):
        if log: print(f"[LOG]: Found symbol '{e[0]}', generating basic FSM...")
        self.cache.append(Thompson.basicSymbol(e[0]))

    @_('LPAREN union_expr RPAREN')
    def primary_expr(self, e):
        if log: print("[LOG]: Parenthesis found, continuing...")

if __name__ == '__main__':
    #data = '(ab + b)* + c'
    os.system('cls' if os.name == 'nt' else 'clear')
    lexer = RELexer()
    parser = REParser()

    try:    

        data = input('Regular Expression > ')
        print(f'\n-- Applying Thompson Algorithm to ER {data} --')
        result = parser.parse(lexer.tokenize(data))
        result.printTransitions()
    except EOFError:
        ...
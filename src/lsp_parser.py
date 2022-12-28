from typing import Union
from dataclasses import dataclass

Symbol = str
Number = Union[int, float]
Atom = Union[Symbol, Number]
List = list
Expression = Union[Atom, List] # the list can be non-homogeneous
Env = dict    

def tokenize(text: str) -> list[str]:
    """Tokenize a string of text into a list of tokens.
        The tokens are either:
        parentheses or atoms
        Atoms are either numbers or strings
        :param text: the string to tokenize
        :return: a list of tokens
    """
    return text.replace("(", " ( ").replace(")", " ) ").split()

def stringify(expr): 
    if isinstance(expr, list):
        return '(' + ' '.join(map(stringify, expr)) + ')'
    return str(expr)


class Parser: 

    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        
    def parse(self) -> Expression:
        return self.read_from_tokens(self.tokens)[0]

    @staticmethod
    def atom(token: str) -> Atom:
        """Convert a token into an atom.
            :param token: the token to convert
            :return: the atom
        """
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return str(token)

    @staticmethod
    def read_from_tokens(tokens: list[str]) -> tuple[Expression, int]: 
        """
            Read an expression from a list of tokens.
            I.e. build an abstract syntax tree. 
            :param tokens: the list of tokens
            :return: the expression and the number of tokens consumed
        """
        if not tokens: 
            raise SyntaxError("unexpected EOF")

        idx = 0
        if tokens[idx] == "(":
            idx += 1
            L = []
            while tokens[idx] != ")":
                exp, tokens_consumed = Parser.read_from_tokens(tokens[idx:])
                idx += tokens_consumed
                L.append(exp)
            return L, idx + 1 # +1 for the closing parenthesis
        elif tokens[idx] == ")":
            raise SyntaxError("unexpected closing parenthesis")
        else: 
            return Parser.atom(tokens[idx]), 1
 

if __name__ == "__main__":
    test_program = "(area_circle (define r 10) (* pi (* r r)))"
    assert Parser(tokenize(test_program)).parse() == \
           (['area_circle', ['define', 'r', 10], ['*', 'pi', ['*', 'r', 'r']]], 17)
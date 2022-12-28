import math
import operator as op
from lsp_parser import *


class Environment(dict):
    """An environment: a dict of {'var': val} pairs, with an outer Env."""
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, var):
        """Find the innermost Env where var appears.
            :param var: the variable to find
            :return: the environment where var is found
            """
        if var in self: 
            return self
        elif self.outer:  
            return self.outer.find(var)
        else:
            raise NameError(f"unbound variable: {var}")
    
    @classmethod
    def standard_environment(cls):
        env = cls()
        env.update(vars(math)) 
        env.update({
            "+": op.add, "-": op.sub, "*": op.mul,
            "/": op.truediv, ">": op.gt, "<": op.lt,
            ">=": op.ge, "<=": op.le, "=": op.eq,
            "abs": abs,
            "append": op.add,
            "apply": lambda proc, args: proc(*args),
            "begin": lambda *x: x[-1],
            "car": lambda x: x[0],
            "cdr": lambda x: x[1:],
            "cons": lambda x, y: [x] + y,
            "eq?": op.is_,
            "equal?": op.eq,
            "length": len,
            "list": lambda *x: list(x),
            "list?": lambda x: isinstance(x, list),
            "map": lambda *x: list(map(*x)),
            "max": max,
            "min": min,
            "not": op.not_,
            "null?": lambda x: x == [],
            "number?": lambda x: isinstance(x, (int, float)),
            "procedure?": callable,
            "round": round,
            "symbol?": lambda x: isinstance(x, Symbol),
        })
        return env


def eval(x: Expression, env):
    """Evaluate an expression in an environment.
        :param x: the expression to evaluate
        :param env: the environment to evaluate in
        :return: the result of the evaluationeval
    """
    if isinstance(x, Symbol): # a variable reference
        return env.find(x)[x]
    elif isinstance(x, int) or isinstance(x, float): # then it's a constant
        return x # simply return it, it evaluates to itself
    op, *args = x
    if op == "quote": # quotation
        (_, expr) = x
        return expr # suppress evaluation

    elif x[0] == "if": # conditional
        (_, test, consequence, alternative) = x 
        expr = consequence if eval(test, env) else alternative
        return eval(expr, env)

    elif x[0] == "define": # definition
        (_, symbol, expr) = x
        env[symbol] = eval(expr, env)

    elif x[0] == "lambda": # assignment
        (_, params, body) = x
        return Procedure(params, body, env)
        
    else: 
        # procedure call
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args) 



class Procedure:
    """A user-defined procedure."""
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env

    def __call__(self, *args):
        """Make the procedure callable."""
        return eval(self.body, Environment(self.params, args, self.env))

 

if __name__ == "__main__":
    e = Parser(tokenize("(begin (define r 10) (* pi (* r r)))")).parse()


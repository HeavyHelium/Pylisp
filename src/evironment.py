import math
import operator as op
from lsp_parser import *

def standard_environment() -> Env:
    env = Env() # a dict
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

global_env = standard_environment()

def eval(x: Expression, env: Env = global_env) -> Expression:
    """Evaluate an expression in an environment.
        :param x: the expression to evaluate
        :param env: the environment to evaluate in
        :return: the result of the evaluation
    """
    if isinstance(x, Symbol): # a variable reference
        return env[x]
    elif isinstance(x, int) or isinstance(x, float): # then it's a constant
        return x # simply return it, it evaluates to itself
    elif x[0] == "if": # conditional
        (_, test, consequence, alternative) = x 
        expr = consequence if eval(test, env) else alternative
        return eval(expr, env)
    elif x[0] == "define": # definition
        (_, symbol, expr) = x
        env[symbol] = eval(expr, env)
    else: 
        # procedure call
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)    

if __name__ == "__main__":
    print(eval(Parser(tokenize("(begin (define r 10) (* pi (* r r)))")).parse()))  
    print(eval(Parser(tokenize("(define (f) (* 10 10))")).parse()))
from evironment import * 

BREAK_MSG = "quit()"

def repl():
    """
        Read-Eval-Print-Loop
    """
    env = standard_environment()
    while True:
        line = input('>>> ')
        if line == BREAK_MSG:
            break
        
        if line.isspace() or line == '':
            continue
        val = eval(Parser(tokenize(line)).parse(), env)
        if val is not None:
            print(stringify(val))

def stringify(expr): 
    if isinstance(expr, list):
        return '(' + ' '.join(map(stringify, expr)) + ')'
    return str(expr)


if __name__ == "__main__":
    repl()
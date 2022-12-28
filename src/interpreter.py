from evironment import *
import lsp_parser

class Interpreter:
    BREAK_MSG = "quit()"
    
    def __init__(self) -> None:
        self.global_env = Environment.standard_environment()

    def eval(self, x: Expression): 
        return eval(x, self.global_env)

    def repl(self) -> None:
        while True:
            line = input('>>> ')

            if line == Interpreter.BREAK_MSG:
                break

            if line.isspace() or line == '':
                continue
            val = None
            try: 
                val = self.eval(Parser(tokenize(line)).parse())
            except Exception as e:
                print(e)
                
            if val is not None:
                print(lsp_parser.stringify(val))


if __name__ == "__main__":
    Interpreter().repl()
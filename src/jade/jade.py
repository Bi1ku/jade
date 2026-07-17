from lexer import Lexer
import sys

class Jade:
    had_error = False

    @staticmethod
    def run(source: str) -> None:
        lexer = Lexer(source)
        tokens = lexer.scan_tokens()

        for token in tokens:
            print(token)

    @staticmethod
    def run_file(path: str) -> None:
        content = ""
        with open(path, "r") as file:
            content = file.read()

        Jade.run(content)

    @staticmethod
    def run_prompt():
        while 1:
            line = input("> ")
            print(line)
            # if line == None: break # check if cntrl-d if `line` is really None
            Jade.run(line)


    @staticmethod
    def main():
        args_length = len(sys.argv[1:])
        if args_length > 1:
            print("Usage: jade [script]")
            sys.exit(64)

        elif args_length == 1:
            Jade.run_file(sys.argv[2])

        else:
            Jade.run_prompt()

    @classmethod
    def report(cls, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error: {where}: {message}")
        cls.had_error = True

    @staticmethod
    def error(line: int, message: str) -> None:
        Jade.report(line, "", message)

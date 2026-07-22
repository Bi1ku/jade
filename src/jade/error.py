"""
The ErrorReporter class must be in its own file to prevent circular import errors. This is primarily because
this class is designed to be used globally throughout the project so defining it in another module that depends
on another module wouldn't work.
"""

class ErrorReporter:
    had_error = False

    @classmethod
    def report(cls, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error: {where}: {message}")
        cls.had_error = True

    @staticmethod
    def error(line: int, message: str) -> None:
        ErrorReporter.report(line, "", message)


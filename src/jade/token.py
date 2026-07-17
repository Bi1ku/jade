from data_types import TokenType

class Token:
    def __init__(self, lexeme: str, type: TokenType, line: int, literal: object) -> None:
        self.lexeme, self.type, self.line, self.literal = lexeme, type, line, literal

    def __str__(self) -> str:
        return f"{self.type} {self.lexeme} {self.literal}"

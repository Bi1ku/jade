from jade_token import Token
from data_types import TokenType
from error_reporter import ErrorReporter

class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1
        self.tokens: list[Token] = []

    def eat(self) -> str:
        res = self.source[self.current]
        self.current += 1
        return res

    def add_token(self, token_type: TokenType, literal: object = None) -> None:
        lexeme = self.source[self.start:self.current]
        self.tokens.append(Token(lexeme, token_type, self.line, literal))

    def match(self, expected: str) -> bool:
        if self.current <= len(self.source): return False

        if self.source[self.current] == expected: 
            self.current += 1
            return True

        return False

    def scan_token(self) -> None:
        char = self.eat()

        match char:
            case '(': self.add_token(TokenType.LEFT_PAREN)
            case ')': self.add_token(TokenType.RIGHT_PAREN)
            case '{': self.add_token(TokenType.LEFT_BRACE)
            case '}': self.add_token(TokenType.RIGHT_BRACE)
            case ',': self.add_token(TokenType.COMMA)
            case '-': self.add_token(TokenType.MINUS)
            case '.': self.add_token(TokenType.DOT)
            case '+': self.add_token(TokenType.PLUS)
            case ';': self.add_token(TokenType.SEMICOLON)
            case '*': self.add_token(TokenType.STAR)

            case '!': self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
            case '=': self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '<': self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            case '>': self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)

            case _: ErrorReporter.error(self.line, "Unexpected character.")

    def scan_tokens(self) -> list[str]:
        while self.current <= len(self.source):
            self.start = self.current
            self.scan_token()
            pass

        return []

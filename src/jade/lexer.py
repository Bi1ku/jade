from jade_token import Token
from data_types import TokenType, KEYWORD_TYPES
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

    def match(self, expected: str) -> bool:
        if self.is_at_end(): return False

        if self.source[self.current] == expected: 
            self.current += 1
            return True

        return False
    
    def peek(self) -> str:
        if self.is_at_end(): return '\0'
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source): return '\0'
        return self.source[self.current + 1]

    def add_token(self, token_type: TokenType, literal: object = None) -> None:
        lexeme = self.source[self.start:self.current]
        self.tokens.append(Token(lexeme, token_type, self.line, literal))

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n': self.line += 1
            self.eat()

        if self.is_at_end():
            return ErrorReporter.error(self.line, "Unterminated string.")

        self.eat() # eats the closing `"`
        self.add_token(TokenType.STRING, self.source[self.start + 1:self.current - 1])

    def scan_number(self) -> None:
        while self.peek().isdigit(): self.eat()

        if self.peek() == '.' and self.peek_next().isdigit():
            self.eat() # eats the `.`
            while self.peek().isdigit(): self.eat()

        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def scan_identifier_or_keyword(self) -> None:
        while self.peek().isalnum() or self.peek() == '_': self.eat()
            
        text = self.source[self.start:self.current]
        if (text in KEYWORD_TYPES): self.add_token(KEYWORD_TYPES[text], text)
        else: self.add_token(TokenType.IDENTIFIER, text)


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

            case '/':
                if self.match('/'):
                    while self.peek() != '\n' and not self.is_at_end(): self.eat()

                elif self.match('*'):
                    while self.peek() != '*' and self.peek_next() != '/' and not self.is_at_end(): self.eat()

                    # eat the remaining `*/`
                    self.eat()
                    self.eat()

                else: self.add_token(TokenType.SLASH)

            case '"': self.scan_string()

            case ' ' | '\t' | '\r': pass
            case '\n': self.line += 1

            case _:
                if char.isdigit(): self.scan_number()
                elif char.isalpha(): self.scan_identifier_or_keyword()
                else: ErrorReporter.error(self.line, f"Unexpected character `{char}`.")

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
            pass

        return self.tokens

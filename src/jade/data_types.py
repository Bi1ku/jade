from enum import Enum

class TokenType(Enum):
    # single character tokens
    LEFT_PAREN, RIGHT_PAREN, LEFT_BRACE, RIGHT_BRACE, COMMA = 1, 2, 3, 4, 5
    DOT, MINUS, PLUS, SEMICOLON, SLASH, STAR = 6, 7, 8, 9, 10, 11

    # one or two character tokens
    BANG, BANG_EQUAL = 12, 13
    EQUAL, EQUAL_EQUAL = 14, 15
    GREATER, GREATER_EQUAL = 16, 17
    LESS, LESS_EQUAL = 18, 19


    # literals
    IDENTIFIER, STRING, NUMBER = 20, 21, 22

    # keywords
    AND, CLASS, ELSE, FALSE, FUN, FOR, IF, NIL, OR = 23, 24, 25, 26, 27, 28, 29, 30, 31
    PRINT, RETURN, SUPER, THIS, TRUE, VAR, WHILE, EOF = 32, 33, 34, 35, 36, 37, 38, 39

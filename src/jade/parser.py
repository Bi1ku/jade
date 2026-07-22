"""
expression     →        equality ;
equality       →        comparison ( ( "!=" | "==" ) comparison )* ;
comparison     →        term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           →        factor ( ( "-" | "+" ) factor )* ;
factor         →        unary ( ( "/" | "*" ) unary )* ;
unary          →        ( ( "!" | "-" ) unary) | primary ;
primary        →        NUMBER | STRING | "true" | "false" | "nil" | ( "(" expression ")" ) ;

Grammar notation 	Code representation
Terminal        	Code to match and consume a token
Nonterminal	        Call to that rule’s function
|               	if or switch statement
* or +	            while or for loop
?	                if statement

Parser uses recursive descent 
"""

import sys
from data_types import Token, TokenType
from expr import BinaryExpr, Expr, GroupingExpr, LiteralExpr, UnaryExpr
from jade.error import ErrorReporter

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.current: int = 0

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]
    
    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def eat(self) -> Token:
        if not self.is_at_end(): self.current += 1
        return self.previous()

    def check(self, type: TokenType) -> bool:
        if self.is_at_end(): return False
        return self.peek().type == type

    def match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self.check(token_type):
                self.eat()
                return True

        return False

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = BinaryExpr(expr, operator, right)
        
        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while self.match(TokenType.LESS, TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.previous()
            right = self.unary()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS): 
            operator = self.previous()
            right = self.unary()
            return UnaryExpr(operator, right)

        return self.primary()

    def primary(self) -> Expr: 
        if self.match(TokenType.FALSE): return LiteralExpr(False)
        elif self.match(TokenType.TRUE): return LiteralExpr(True)
        elif self.match(TokenType.NIL): return LiteralExpr(None)

        elif self.match(TokenType.NUMBER, TokenType.STRING): return LiteralExpr(self.previous().literal)

        elif self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            # right parenthesis?
            return GroupingExpr(expr)

        else:
            # error here, but no line?
            sys.exit(65)

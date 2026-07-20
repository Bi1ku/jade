from abc import ABC
from jade_token import Token

class Expr(ABC):
    pass

class BinaryExpr(Expr): 
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left, self.operator, self.right = left, operator, right

class GroupingExpr(Expr):
    def __init__(self, expr: Expr) -> None:
        self.expr = expr

class LiteralExpr(Expr):
    def __init__(self, value: object) -> None:
        self.value = value

class UnaryExpr(Expr):
    def __init__(self, operator: Token, right: Expr) -> None:
        self.operator, self.right = operator, right

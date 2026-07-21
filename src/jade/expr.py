from abc import ABC, abstractmethod
from typing import override
from lexer import Token

class ExprVisitor(ABC):
    @abstractmethod
    def visit_binary_expr(self, expr: BinaryExpr) -> str: return "\0"
    def visit_grouping_expr(self, expr: GroupingExpr) -> str: return "\0"
    def visit_literal_expr(self, expr: LiteralExpr) -> str: return "\0"
    def visit_unary_expr(self, expr: UnaryExpr) -> str: return "\0"

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor) -> None: pass

class BinaryExpr(Expr): 
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left, self.operator, self.right = left, operator, right

    @override
    def accept(self, visitor: ExprVisitor):
        visitor.visit_binary_expr(self)

class GroupingExpr(Expr):
    def __init__(self, expr: Expr) -> None:
        self.expr = expr

    @override
    def accept(self, visitor: ExprVisitor):
        visitor.visit_grouping_expr(self)
   
class LiteralExpr(Expr):
    def __init__(self, value: object) -> None:
        self.value = value

    @override
    def accept(self, visitor: ExprVisitor):
        visitor.visit_literal_expr(self)

class UnaryExpr(Expr):
    def __init__(self, operator: Token, right: Expr) -> None:
        self.operator, self.right = operator, right

    @override
    def accept(self, visitor: ExprVisitor):
        visitor.visit_unary_expr(self)


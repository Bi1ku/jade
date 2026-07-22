import sys
from lexer import Lexer
from error import ErrorReporter
from expr import ExprVisitor, Expr, BinaryExpr, UnaryExpr, LiteralExpr, GroupingExpr
from typing import override

class Jade:
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
        if ErrorReporter.had_error: sys.exit(65)

    @staticmethod
    def run_prompt():
        while 1:
            try:
                line = input("> ")
                if line == "exit()": break
                Jade.run(line)
                ErrorReporter.had_error = False

            except EOFError: break

    @staticmethod
    def main():
        args_length = len(sys.argv[1:])
        if args_length > 1:
            print("Usage: jade [script]")
            sys.exit(64)

        elif args_length == 1:
            Jade.run_file(sys.argv[1])

        else:
            Jade.run_prompt()

# ASTPrinter is simply a helper class for debugging.
class ASTPrinter(ExprVisitor):
    def print(self, expr: Expr) -> None:
        return expr.accept(self)

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        res = f"({name}"

        for expr in exprs:
            res += f" {expr.accept(self)}"

        res += ")"
        return res
    
    @override
    def visit_binary_expr(self, expr: BinaryExpr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    @override
    def visit_grouping_expr(self, expr: GroupingExpr) -> str:
        return self.parenthesize("group", expr.expr)

    @override
    def visit_literal_expr(self, expr: LiteralExpr) -> str:
        if (expr.value == None): return "nil"
        return expr.value.__str__()

    @override
    def visit_unary_expr(self, expr: UnaryExpr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

if __name__ == "__main__":
    Jade.main()

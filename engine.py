"""
Safe expression evaluator for the graphing calculator.
Provides secure evaluation of mathematical expressions using AST parsing,
with support for trigonometric functions, logarithms, and numerical derivatives.
"""
import ast
import numpy as np
from math import (
    sin, cos, tan, asin, acos, atan, sinh, cosh, tanh,
    asinh, acosh, atanh, log, log10, log2, exp, sqrt,
    pi, e, degrees, radians, factorial, ceil, floor, fabs
)

USE_DEGREES = False


def set_degree_mode(enabled):
    """Enable or disable degree mode for trigonometric functions.
    
    Args:
        enabled: If True, sin/cos/tan expect degrees; if False, expect radians.
    """
    global USE_DEGREES
    USE_DEGREES = enabled


def get_degree_mode():
    """Return current angle mode.
    
    Returns:
        bool: True if in degree mode, False if in radian mode.
    """
    return USE_DEGREES


def log_base(x, base):
    """Compute logarithm of x with custom base.
    Args:
        x: The value to compute log of (must be positive).
        base: The base of the logarithm (must be positive and not 1).
    Returns:
        float: The logarithm of x to the specified base.
    Raises:
        ValueError: If x <= 0, base <= 0, or base == 1.
    """
    if x <= 0:
        raise ValueError("log requires x > 0")
    if base <= 0 or base == 1:
        raise ValueError("invalid log base")
    return log(x) / log(base)

def safe_sin(x):
    """Sine function respecting current angle mode.
    Args:
        x: Angle in degrees (if mode enabled) or radians.
    Returns:
        float: Sine of x.
    """
    return sin(radians(x) if USE_DEGREES else x)

def safe_cos(x):
    """Cosine function respecting current angle mode.
    
    Args:
        x: Angle in degrees (if mode enabled) or radians.
    
    Returns:
        float: Cosine of x.
    """
    return cos(radians(x) if USE_DEGREES else x)

def safe_tan(x):
    """Tangent function respecting current angle mode.
    
    Args:
        x: Angle in degrees (if mode enabled) or radians.
    
    Returns:
        float: Tangent of x.
    """
    return tan(radians(x) if USE_DEGREES else x)

def safe_asin(x):
    """Inverse sine function respecting current angle mode.
    
    Args:
        x: Value in range [-1, 1].
    
    Returns:
        float: Angle in degrees (if mode enabled) or radians.
    """
    result = asin(x)
    return degrees(result) if USE_DEGREES else result

def safe_acos(x):
    """Inverse cosine function respecting current angle mode.
    Args:
        x: Value in range [-1, 1].
    Returns:
        float: Angle in degrees (if mode enabled) or radians.
    """
    result = acos(x)
    return degrees(result) if USE_DEGREES else result

def safe_atan(x):
    """Inverse tangent function respecting current angle mode.
    Args:
        x: Any real number.
    Returns:
        float: Angle in degrees (if mode enabled) or radians.
    """
    result = atan(x)
    return degrees(result) if USE_DEGREES else result

safe_funcs = {
    "sin": safe_sin, "cos": safe_cos, "tan": safe_tan,
    "asin": safe_asin, "acos": safe_acos, "atan": safe_atan,
    "sinh": sinh, "cosh": cosh, "tanh": tanh,
    "asinh": asinh, "acosh": acosh, "atanh": atanh,
    "ln": log, "log": log10, "log2": log2,
    "logb": log_base,
    "exp": exp, "sqrt": sqrt,
    "pi": pi, "e": e, "abs": fabs,
    "deg": degrees, "rad": radians,
    "fact": factorial, "ceil": ceil, "floor": floor,
}

class SafeEvaluator(ast.NodeVisitor):
    """AST visitor that safely evaluates mathematical expressions.    
    Only allows arithmetic operations, math functions, and constants.
    Blocks access to dangerous operations like imports, attribute access, etc.
    """
    def __init__(self, funcs, x_value=None):
        """Initialize evaluator. 
        Args:
            funcs: Dictionary mapping function names to implementations.
            x_value: Value to use for variable x (for plotting).
        """
        self.funcs = funcs
        self.x_value = x_value

    def visit_BinOp(self, node):
        """Evaluate binary operations (+, -, *, /, **, %, //)."""
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.op, ast.Add): return left + right
        if isinstance(node.op, ast.Sub): return left - right
        if isinstance(node.op, ast.Mult): return left * right
        if isinstance(node.op, ast.Div): return left / right
        if isinstance(node.op, ast.Pow): return left ** right
        if isinstance(node.op, ast.Mod): return left % right
        if isinstance(node.op, ast.FloorDiv): return left // right
        raise ValueError(f"Unsupported operator")

    def visit_UnaryOp(self, node):
        """Evaluate unary operations (-, +)."""
        val = self.visit(node.operand)
        if isinstance(node.op, ast.USub): return -val
        if isinstance(node.op, ast.UAdd): return val
        raise ValueError(f"Unsupported unary operator")

    def visit_Call(self, node):
        """Evaluate function calls (sin, cos, sqrt, etc.)."""
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only functions allowed")
        func_name = node.func.id
        if func_name not in self.funcs:
            raise ValueError(f"Unknown: {func_name}")
        args = [self.visit(arg) for arg in node.args]
        return self.funcs[func_name](*args)

    def visit_Constant(self, node):
        """Return numeric constants."""
        return node.value

    def visit_Name(self, node):
        """Resolve variable names and constants."""
        if node.id == "x" and self.x_value is not None:
            return self.x_value
        if node.id in self.funcs:
            return self.funcs[node.id]
        raise ValueError(f"Unknown: {node.id}")

    def generic_visit(self, node):
        """Block any disallowed AST nodes."""
        raise ValueError(f"Disallowed: {type(node).__name__}")


def _preprocess_expr(expr):
    """Replace ^ with ** for power operator."""
    return expr.replace("^", "**")


def safe_eval(expr, x_value=None):
    """Safely evaluate a mathematical expression.
    Args:
        expr: String containing the expression (e.g., "sin(x) + 2").
        x_value: Optional value or array for variable x (for plotting).
    Returns:
        The result of the evaluated expression.
    Raises:
        ValueError: If the expression is invalid or contains disallowed operations.
        ZeroDivisionError: If division by zero occurs.
    """
    expr = _preprocess_expr(expr)
    tree = ast.parse(expr, mode="eval")
    return SafeEvaluator(safe_funcs, x_value).visit(tree.body)

def compute_derivative(expr, x_vals):
    """Numerically compute the derivative of an expression.    
    Uses central difference method for scalar values,
    or numpy gradient for array values.
    Args:
        expr: String containing the expression to differentiate.
        x_vals: Point(s) at which to compute derivative.
    Returns:
        The derivative at the given point(s).
    """
    expr = _preprocess_expr(expr)
    h = 1e-7
    f = lambda x: safe_eval(expr, x)
    if isinstance(x_vals, np.ndarray):
        return np.gradient(f(x_vals), x_vals)
    return (f(x_vals + h) - f(x_vals - h)) / (2 * h)

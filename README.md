# Graphing Calculator

A Python graphing calculator with a dark-themed UI, built with tkinter, matplotlib, and NumPy.
## Features

 *Basic calculations*: +, -, *, /, ^ (power), parentheses
*Math functions*: sin, cos, tan, sqrt, log, ln, exp, etc.
*Trigonometric modes*: Toggle between RAD and DEG
*Graphing*: Plot functions with automatic history
*Derivatives*: Toggle to show derivative curves
*Save graphs*: Export plots as PNG, PDF, or SVG

## Overview
<img width="1919" height="1019" alt="image" src="https://github.com/user-attachments/assets/84d4e188-9aef-4967-af1a-ca3a1431ff24" />
<img width="1919" height="1014" alt="image" src="https://github.com/user-attachments/assets/11aab374-2118-462e-95e4-7a8fee1f7e87" />
<img width="1919" height="1022" alt="image" src="https://github.com/user-attachments/assets/1bd3842f-914b-43d4-b06f-55d3dd39fca7" />
<img width="1919" height="1020" alt="image" src="https://github.com/user-attachments/assets/9b6ec203-6337-460d-a094-31bcd29aa206" />
<img width="1919" height="1020" alt="image" src="https://github.com/user-attachments/assets/9c706c77-21b5-403b-9b8f-c0f260b9873f" />



## Usage

Enter expressions like 2+2, sin(x), x^2 + 1
Press = to calculate
Click GRAPH to plot
Toggle RAD/DEG for angle mode
Toggle d/dx to show derivatives
Click SAVE to export the current graph

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Enter | Calculate |
| Escape | Clear |
| BackSpace | Delete last character |
| Up | Move cursor to start |
| Down | Move cursor to end |

## Function Reference

### Trigonometric Functions

| Function | Description | Example |
|----------|-------------|---------|
| sin(x) | Sine of x | sin(30) |
| cos(x) | Cosine of x | cos(60) |
| tan(x) | Tangent of x | tan(45) |
| asin(x) | Inverse sine | asin(1) |
| acos(x) | Inverse cosine | acos(1) |
| atan(x) | Inverse tangent | atan(1) |

> *Note*: Uses RAD mode by default. Click the RAD button to switch to DEG mode for degree calculations.

### Hyperbolic Functions

| Function | Description |
|----------|-------------|
| sinh(x) | Hyperbolic sine |
| cosh(x) | Hyperbolic cosine |
| tanh(x) | Hyperbolic tangent |
| asinh(x) | Inverse hyperbolic sine |
| acosh(x) | Inverse hyperbolic cosine |
| atanh(x) | Inverse hyperbolic tangent |

### Logarithmic Functions

| Function | Description | Example |
|----------|-------------|---------|
| ln(x) | Natural logarithm (base e) | ln(2.718) ≈ 1 |
| log(x) | Base-10 logarithm | log(100) = 2 |
| log2(x) | Base-2 logarithm | log2(8) = 3 |
| logb(x, base) | Logarithm with custom base | logb(27, 3) = 3 |

> *Note*: Logarithms require positive inputs. For logb(x, base), the base must be positive and not equal to 1.

### Other Math Functions

| Function | Description | Example |
|----------|-------------|---------|
| sqrt(x) | Square root | sqrt(16) = 4 |
| exp(x) | e^x (exponential) | exp(1) ≈ 2.718 |
| abs(x) | Absolute value | abs(-5) = 5 |
| fact(x) | Factorial | fact(5) = 120 |
| ceil(x) | Round up | ceil(3.2) = 4 |
| floor(x) | Round down | floor(3.8) = 3 |
| pi | Pi constant | 2 * pi ≈ 6.283 |
| e | Euler's number | e ≈ 2.718 |

### Operators

| Operator | Description | Example |
|----------|-------------|---------|
| + | Addition | 2 + 3 = 5 |
| - | Subtraction | 5 - 3 = 2 |
| * | Multiplication | 4 * 3 = 12 |
| / | Division | 10 / 2 = 5 |
| ^ | Power | 2 ^ 8 = 256 |
| % | Modulo | 10 % 3 = 1 |
| // | Floor division | 10 // 3 = 3 |

## Graphing

To graph a function:

1. Enter an expression containing x (e.g., x^2, sin(x))
2. Click GRAPH to plot
3. Up to 4 functions can be plotted simultaneously:
   - Current expression in the input field
   - Plus up to 3 recent expressions from history

### Derivative Plotting

Toggle the d/dx button to:
- *ON*: Display derivative curves alongside original functions (dashed lines)
- *OFF*: Hide derivative curves

Derivatives use numerical differentiation to compute the slope of each function.

## Saving Graphs

After creating a graph:

1. Click the SAVE button
2. Choose a file format:
    *PNG* - Image format (recommended for web)
    *PDF* - Vector format (recommended for documents)
    *SVG* - Vector format (scalable)
3. Choose a location and filename
4. Click Save
The graph is saved at 300 DPI with the dark theme preserved.

## License

MIT

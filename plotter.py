import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from engine import safe_eval, compute_derivative

_current_fig = None


def plot_expressions(expressions, show_derivatives=False):
    global _current_fig

    if not expressions:
        return "no expressions provided"

    x = np.linspace(-12, 12, 1200)
    _current_fig = plt.figure(figsize=(10.5, 7.2), facecolor="#0d1117")
    ax = _current_fig.add_subplot(111, facecolor="#161b22")

    colors = ["#58a6ff", "#f0883e", "#3fb950", "#f85149", "#d2a0e8"]
    deriv_colors = ["#ff9966", "#66ffcc", "#ffcc66", "#ff66cc", "#cc99ff"]

    plotted = 0
    derivative_count = 0
    errors = []

    for i, expr in enumerate(expressions):
        try:
            y = safe_eval(expr, x)
            if not np.any(np.isfinite(y)):
                errors.append(f"'{expr}' undefined")
                continue

            ax.plot(x, y, color=colors[i % len(colors)], lw=2.4,
                    label=expr[:38] + "…" if len(expr) > 38 else expr)
            plotted += 1

            if show_derivatives:
                try:
                    dy = compute_derivative(expr, x)
                    if np.any(np.isfinite(dy)):
                        label = f"d/dx({expr[:30]})" if len(expr) > 30 else f"d/dx({expr})"
                        ax.plot(x, dy, color=deriv_colors[derivative_count % len(deriv_colors)],
                                lw=1.5, linestyle="--", label=label)
                        derivative_count += 1
                except ValueError as ve:
                    errors.append(f"deriv error: {str(ve)[:20]}")

        except (ValueError, TypeError, SyntaxError) as e:
            errors.append(f"'{expr}': {str(e)[:25]}")

    if plotted == 0:
        error_msg = "; ".join(errors[:3]) if errors else "nothing plottable"
        plt.close(_current_fig)
        _current_fig = None
        return error_msg

    ax.axhline(0, color="#444", lw=0.8, zorder=1)
    ax.axvline(0, color="#444", lw=0.8, zorder=1)

    total_plots = plotted + derivative_count
    ax.set_title("Graph" if total_plots == 1 else f"{total_plots} Functions",
                 color="white", fontsize=13, pad=12)
    ax.set_xlabel("x", color="#aaa", fontsize=11)
    ax.set_ylabel("y", color="#aaa", fontsize=11)
    ax.tick_params(colors="#aaa", labelsize=10)
    ax.grid(True, alpha=0.15, linestyle="--", zorder=0)

    for spine in ax.spines.values():
        spine.set_color("#444")

    if total_plots > 1:
        ax.legend(frameon=False, fontsize=10.5, labelcolor="white",
                  loc="upper right", bbox_to_anchor=(1, 1.02))

    plt.tight_layout(pad=1.2)
    plt.show(block=False)
    return None


def save_current_plot():
    global _current_fig

    if _current_fig is None:
        return "no graph to save"

    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("PDF Document", "*.pdf"),
                ("SVG Vector", "*.svg"),
                ("All Files", "*.*")
            ],
            title="Save Graph"
        )

        if not file_path:
            return "save cancelled"

        _current_fig.savefig(file_path, dpi=300, bbox_inches='tight',
                            facecolor=_current_fig.get_facecolor())
        return None

    except PermissionError:
        return "permission denied"
    except OSError as e:
        return f"save failed: {str(e)[:25]}"
    finally:
        root.destroy()


def plot_derivative_only(expr):
    global _current_fig

    try:
        x = np.linspace(-12, 12, 1200)
        dy = compute_derivative(expr, x)

        if not np.any(np.isfinite(dy)):
            return "derivative undefined"

        _current_fig = plt.figure(figsize=(10.5, 7.2), facecolor="#0d1117")
        ax = _current_fig.add_subplot(111, facecolor="#161b22")

        ax.plot(x, dy, color="#58a6ff", lw=2.4, label=f"d/dx({expr})")

        ax.axhline(0, color="#444", lw=0.8, zorder=1)
        ax.axvline(0, color="#444", lw=0.8, zorder=1)
        ax.set_title(f"Derivative of {expr[:40]}", color="white", fontsize=13, pad=12)
        ax.set_xlabel("x", color="#aaa", fontsize=11)
        ax.set_ylabel("y", color="#aaa", fontsize=11)
        ax.tick_params(colors="#aaa", labelsize=10)
        ax.grid(True, alpha=0.15, linestyle="--", zorder=0)

        for spine in ax.spines.values():
            spine.set_color("#444")

        ax.legend(frameon=False, fontsize=10.5, labelcolor="white",
                  loc="upper right", bbox_to_anchor=(1, 1.02))

        plt.tight_layout(pad=1.2)
        plt.show(block=False)
        return None

    except ValueError as ve:
        return f"error: {str(ve)[:30]}"
    except Exception as e:
        return f"plot error: {str(e)[:25]}"


def get_history_expressions(history, max_count=3):
    expressions = []
    for i in range(min(max_count, history.size())):
        line = history.get(history.size() - 1 - i)
        if "→" in line:
            expr = line.split("→")[0].strip()
            if expr and expr not in expressions:
                expressions.append(expr)
    return expressions

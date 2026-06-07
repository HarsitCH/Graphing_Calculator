import tkinter as tk
from engine import safe_eval, set_degree_mode, get_degree_mode
from plotter import plot_expressions, get_history_expressions, save_current_plot, plot_derivative_only


class CalculatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Graphing Calculator")
        self.root.geometry("800x720")
        self.root.configure(bg="#0f0f0f")
        self.root.resizable(True, True)
        self.show_derivatives = False

        self.entry = tk.Entry(
            root,
            font=("Consolas", 22),
            bg="#1a1a1a",
            fg="#e0e0e0",
            insertbackground="#00ccff",
            borderwidth=0,
            relief="flat",
            highlightthickness=2,
            highlightbackground="#333333",
            highlightcolor="#00ccff"
        )
        self.entry.pack(fill="x", padx=20, pady=(20, 10))
        self.entry.focus_set()

        self.mode_frame = tk.Frame(root, bg="#0f0f0f")
        self.mode_frame.pack(fill="x", padx=20, pady=(0, 5))

        self.rad_deg_btn = tk.Button(
            self.mode_frame,
            text="RAD",
            font=("Consolas", 11, "bold"),
            bg="#1a2d1a",
            fg="#66ff66",
            activebackground="#2a3d2a",
            activeforeground="#88ff88",
            bd=0,
            relief="flat",
            command=self.toggle_rad_deg
        )
        self.rad_deg_btn.pack(side="left")

        self.deriv_btn = tk.Button(
            self.mode_frame,
            text="d/dx OFF",
            font=("Consolas", 11, "bold"),
            bg="#2d2d1a",
            fg="#ffff66",
            activebackground="#3d3d2a",
            activeforeground="#ffff88",
            bd=0,
            relief="flat",
            command=self.toggle_derivatives
        )
        self.deriv_btn.pack(side="left", padx=(10, 0))

        self.save_btn = tk.Button(
            self.mode_frame,
            text="SAVE",
            font=("Consolas", 11, "bold"),
            bg="#1a1a2d",
            fg="#8888ff",
            activebackground="#2a2a3d",
            activeforeground="#aaaaff",
            bd=0,
            relief="flat",
            command=self.save_graph
        )
        self.save_btn.pack(side="left", padx=(10, 0))

        main_frame = tk.Frame(root, bg="#0f0f0f")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.calc_frame = tk.Frame(main_frame, bg="#0f0f0f")
        self.calc_frame.grid(row=0, column=0, sticky="n")

        history_frame = tk.Frame(main_frame, bg="#0f0f0f")
        history_frame.grid(row=0, column=1, padx=25, sticky="n")

        tk.Label(
            history_frame,
            text="HISTORY",
            font=("Segoe UI", 14, "bold"),
            fg="#aaaaaa",
            bg="#0f0f0f"
        ).pack(anchor="w", pady=(0, 6))

        self.history = tk.Listbox(
            history_frame,
            width=38,
            height=24,
            bg="#1a1a1a",
            fg="#d0d0d0",
            font=("Consolas", 11),
            selectbackground="#333344",
            selectforeground="white",
            bd=0,
            highlightthickness=0
        )
        self.history.pack()

        self._create_buttons()
        self._setup_keybindings()
        self._update_mode_display()

    def _create_buttons(self):
        buttons = [
            "7", "8", "9", "/", "sin(",
            "4", "5", "6", "*", "cos(",
            "1", "2", "3", "-", "tan(",
            "0", ".", "(", ")", "+",
            "sqrt(", "log(", "ln(", "^", "pi",
            "C", "=", "GRAPH"
        ]

        for i, text in enumerate(buttons):
            r = i // 5
            c = i % 5

            if text == "C":
                cmd = self.clear
                bg, fg = "#2d1a1a", "#ff6666"
            elif text == "=":
                cmd = self.calculate
                bg, fg = "#1a2d1a", "#66ff66"
            elif text == "GRAPH":
                cmd = self.plot
                bg, fg = "#1a2d3d", "#66ccff"
            else:
                cmd = lambda v=text: self.press(v)
                bg, fg = "#222222", "white"

            tk.Button(
                self.calc_frame,
                text=text,
                width=7,
                height=2,
                font=("Consolas", 13),
                bg=bg,
                fg=fg,
                activebackground="#333333",
                activeforeground=fg,
                bd=0,
                relief="flat",
                command=cmd
            ).grid(row=r, column=c, padx=4, pady=4, sticky="nsew")

        for c in range(5):
            self.calc_frame.grid_columnconfigure(c, weight=1)

    def _setup_keybindings(self):
        def key_press(event):
            if event.keysym == "Return":
                self.calculate()
            elif event.keysym == "BackSpace":
                self.backspace()
            elif event.keysym == "Escape":
                self.clear()
            elif event.keysym == "Up":
                self.entry.icursor(0)
            elif event.keysym == "Down":
                self.entry.icursor(tk.END)

        self.root.bind("<Key>", key_press)

    def toggle_rad_deg(self):
        current = get_degree_mode()
        set_degree_mode(not current)
        self._update_mode_display()

    def toggle_derivatives(self):
        self.show_derivatives = not self.show_derivatives
        self.deriv_btn.config(
            text=f"d/dx {'ON' if self.show_derivatives else 'OFF'}",
            bg="#2d3d1a" if self.show_derivatives else "#2d2d1a",
            fg="#88ff88" if self.show_derivatives else "#ffff66"
        )

    def _update_mode_display(self):
        mode = "DEG" if get_degree_mode() else "RAD"
        self.rad_deg_btn.config(
            text=mode,
            bg="#2d3d1a" if get_degree_mode() else "#1a2d1a",
            fg="#88ff88" if get_degree_mode() else "#66ff66"
        )

    def press(self, val):
        self.entry.insert(tk.END, val)

    def clear(self):
        self.entry.delete(0, tk.END)

    def backspace(self):
        s = self.entry.get()
        if s:
            self.entry.delete(len(s) - 1, tk.END)

    def add_to_history(self, expr, result):
        self.history.insert(tk.END, f" {expr: <28} → {result}")
        self.history.see(tk.END)

    def calculate(self):
        try:
            expr = self.entry.get().strip()
            if not expr:
                return
            result = safe_eval(expr)
            if result is not None:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, str(result))
                self.add_to_history(expr, result)
        except ZeroDivisionError:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "÷ by zero")
        except NameError:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "undefined name")
        except Exception as e:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, f"Error → {str(e)[:38]}")

    def plot(self):
        try:
            expressions = []
            curr = self.entry.get().strip()
            if curr:
                expressions.append(curr)

            for expr in get_history_expressions(self.history):
                if expr not in expressions:
                    expressions.append(expr)

            if not expressions:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, "nothing to plot")
                return

            error = plot_expressions(expressions, self.show_derivatives)
            if error:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, error)

        except Exception as e:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, f"plot error → {str(e)[:30]}")

    def save_graph(self):
        error = save_current_plot()
        if error:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, error)

    def run(self):
        self.root.mainloop()

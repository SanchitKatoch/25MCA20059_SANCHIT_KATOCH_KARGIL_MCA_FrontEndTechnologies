# Using generator for step-by-step visualization of backtracking

import time
import threading
import tkinter as tk

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.patches as patches
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


BG = "#0f0f13"
PANEL_BG = "#18181f"
BORDER = "#2a2a3a"
ACCENT = "#c8ff00"
TEXT = "#e0e0e0"
MUTED = "#555566"

SQ_LIGHT = "#1e1e2a"
SQ_DARK = "#13131a"
SQ_QUEEN = "#1a3000"
SQ_CONFLICT = "#2d0a00"
QUEEN_CLR = "#c8ff00"
CONFLICT_CLR = "#ff4422"


def is_safe(board, row, col):
    for r in range(row):
        c = board[r]
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True


def solve_steps(n):
    board = [-1] * n
    def bt(row):
        if row == n:
            yield {"type": "solution", "board": board[:]}
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                yield {"type": "place", "row": row, "col": col, "board": board[:]}
                yield from bt(row + 1)
                board[row] = -1
                yield {"type": "remove", "row": row, "col": col, "board": board[:]}
            else:
                yield {"type": "conflict", "row": row, "col": col, "board": board[:]}
    yield from bt(0)


class BoardCanvas:
    def __init__(self, parent):
        self.fig = Figure(figsize=(5.5, 5.5), facecolor=BG)
        self.ax = self.fig.add_axes([0.1, 0.1, 0.8, 0.8])
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def draw(self, n, board, cur=None, mode="idle"):
        ax = self.ax
        ax.cla()
        ax.set_xlim(0, n)
        ax.set_ylim(0, n)
        ax.set_aspect("equal")
        ax.axis("off")

        for r in range(n):
            for c in range(n):
                queen = (board[r] == c)
                current = (cur == (r, c))
                color = SQ_LIGHT if (r + c) % 2 == 0 else SQ_DARK

                if queen:
                    color = SQ_QUEEN
                elif current and mode == "conflict":
                    color = SQ_CONFLICT

                ax.add_patch(patches.Rectangle((c, n-r-1), 1, 1, facecolor=color))

                if queen:
                    ax.text(c+0.5, n-r-0.5, "♛", ha="center", va="center",
                            fontsize=20, color=QUEEN_CLR)
                elif current and mode == "conflict":
                    ax.text(c+0.5, n-r-0.5, "X", ha="center", va="center",
                            fontsize=14, color=CONFLICT_CLR)

        self.canvas.draw_idle()

    def reset(self, n):
        self.draw(n, [-1]*n)


class StatsChart:
    def __init__(self, parent):
        self.fig = Figure(figsize=(3.5, 2), facecolor=PANEL_BG)
        self.ax = self.fig.add_axes([0.2, 0.3, 0.7, 0.6])
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def refresh(self, n=None, count=None):
        self.ax.cla()

        if n and count is not None:
            # FIX: thin + centered bar
            self.ax.set_xlim(n - 1, n + 1)
            self.ax.bar([n], [count], width=0.4)

            self.ax.set_title(f"N={n}, Solutions={count}", color=TEXT)
            self.ax.set_xlabel("N", color=TEXT)
            self.ax.set_ylabel("Solutions", color=TEXT)

            self.ax.grid(True, linestyle="--", alpha=0.5)

        else:
            self.ax.set_title("Solutions Graph", color=TEXT)

        self.canvas.draw_idle()


class NQueensApp:
    def __init__(self, root):
        self.root = root
        self.n_var = tk.IntVar(value=8)
        self.solutions = []
        self.sol_idx = 0

        root.title("N-Queens Solver")
        root.geometry("900x600")

        self._build_ui()
        self.board.reset(8)

    def _build_ui(self):
        left = tk.Frame(self.root)
        left.pack(side="left", fill="y")

        tk.Label(left, text="N").pack()
        tk.Scale(left, from_=4, to=10, orient="horizontal",
                 variable=self.n_var).pack()

        tk.Button(left, text="Solve", command=self.solve).pack()
        tk.Button(left, text="Animate", command=self.animate).pack()

        tk.Button(left, text="Prev", command=self.prev).pack()
        tk.Button(left, text="Next", command=self.next).pack()

        self.info = tk.Label(left, text="")
        self.info.pack()

        chart_frame = tk.Frame(left)
        chart_frame.pack(fill="both", expand=True)
        self.chart = StatsChart(chart_frame)

        right = tk.Frame(self.root)
        right.pack(side="right", fill="both", expand=True)

        self.board = BoardCanvas(right)

    def solve(self):
        n = self.n_var.get()
        board = [-1]*n
        self.solutions = []

        def bt(row):
            if row == n:
                self.solutions.append(board[:])
                return
            for col in range(n):
                if is_safe(board, row, col):
                    board[row] = col
                    bt(row+1)
                    board[row] = -1

        start = time.time()
        bt(0)
        end = time.time()

        self.sol_idx = 0
        if self.solutions:
            self.board.draw(n, self.solutions[0])

        self.info.config(text=f"Solutions: {len(self.solutions)}, Time: {round(end-start,3)}s")
        self.chart.refresh(n, len(self.solutions))

    def animate(self):
        n = self.n_var.get()
        gen = solve_steps(n)

        def step():
            try:
                s = next(gen)
                self.board.draw(n, s["board"],
                                cur=(s.get("row"), s.get("col")),
                                mode=s["type"])
                self.root.after(100, step)
            except StopIteration:
                pass

        step()

    def prev(self):
        if self.solutions:
            self.sol_idx = (self.sol_idx - 1) % len(self.solutions)
            self.board.draw(self.n_var.get(), self.solutions[self.sol_idx])

    def next(self):
        if self.solutions:
            self.sol_idx = (self.sol_idx + 1) % len(self.solutions)
            self.board.draw(self.n_var.get(), self.solutions[self.sol_idx])


if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensApp(root)
    root.mainloop()

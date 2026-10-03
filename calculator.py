# -*- coding: utf-8 -*-
from tkinter import Tk, Toplevel, Frame, Label, Entry, END, font

# ---------- Theme ----------
BG = "#1C1C1E"          # window background
DISPLAY_BG = "#2C2C2E"  # display box
DISPLAY_FG = "#FFFFFF"
NUM_BG, NUM_HOVER = "#3A3A3C", "#4A4A4D"
OP_BG, OP_HOVER = "#FF9F0A", "#FFB340"
FUNC_BG, FUNC_HOVER = "#A5A5A7", "#C0C0C2"
TEXT_LIGHT, TEXT_DARK = "#FFFFFF", "#000000"
FONT_FAMILY = "Segoe UI"


# ---------- Logic ----------
def get_input(entry, text):
    entry.insert(END, text)


def backspace(entry):
    entry.delete(len(entry.get()) - 1, END)


def clear(entry):
    entry.delete(0, END)


def calc(entry, root):
    expr = entry.get().strip()
    if not expr:
        return
    expr = expr.replace("×", "*").replace("÷", "/").replace("−", "-").replace("^", "**")
    if not set(expr) <= set("0123456789+-*/.() "):
        return
    try:
        result = eval(expr)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        output = str(result)
    except ZeroDivisionError:
        popupmsg(root)
        output = ""
    except Exception:
        output = "Error"
    clear(entry)
    entry.insert(END, output)


def popupmsg(root):
    popup = Toplevel(root)
    popup.title("Alert")
    popup.configure(bg=BG)
    popup.resizable(0, 0)
    popup.geometry("260x130")
    popup.transient(root)
    popup.grab_set()
    Label(popup, text="Cannot divide by 0!\nEnter valid values", bg=BG, fg=TEXT_LIGHT,
          font=(FONT_FAMILY, 11)).pack(pady=(20, 10))
    ok = Label(popup, text="Okay", bg=OP_BG, fg=TEXT_LIGHT, width=10, pady=4,
               font=(FONT_FAMILY, 10, "bold"), cursor="hand2")
    ok.pack()
    ok.bind("<Button-1>", lambda e: popup.destroy())


# ---------- UI ----------
def make_button(parent, text, bg, hover, fg, command, colspan=1):
    """Label-based button: colors work the same on Windows, macOS and Linux."""
    btn = Label(parent, text=text, bg=bg, fg=fg, font=(FONT_FAMILY, 16),
                cursor="hand2", height=2)
    btn.bind("<Enter>", lambda e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    btn.bind("<ButtonPress-1>", lambda e: btn.config(bg=hover))
    btn.bind("<ButtonRelease-1>", lambda e: (btn.config(bg=bg), command()))
    return btn


def cal():
    root = Tk()
    root.title("Calculator")
    root.configure(bg=BG)
    root.resizable(0, 0)

    # Display
    display_frame = Frame(root, bg=DISPLAY_BG)
    display_frame.grid(row=0, column=0, padx=12, pady=(12, 8), sticky="nsew")
    entry = Entry(display_frame, justify="right", font=font.Font(family=FONT_FAMILY, size=26),
                  bg=DISPLAY_BG, fg=DISPLAY_FG, insertbackground=DISPLAY_FG,
                  relief="flat", bd=0, width=14)
    entry.pack(padx=10, pady=18, fill="x")

    # Button grid
    grid = Frame(root, bg=BG)
    grid.grid(row=1, column=0, padx=12, pady=(0, 12))
    for c in range(4):
        grid.columnconfigure(c, weight=1, uniform="col")

    def num(t):
        return dict(bg=NUM_BG, hover=NUM_HOVER, fg=TEXT_LIGHT, command=lambda: get_input(entry, t))

    def op(t):
        return dict(bg=OP_BG, hover=OP_HOVER, fg=TEXT_LIGHT, command=lambda: get_input(entry, t))

    layout = [
        # (text, row, col, colspan, style)
        ("C", 0, 0, 1, dict(bg=FUNC_BG, hover=FUNC_HOVER, fg=TEXT_DARK, command=lambda: clear(entry))),
        ("⌫", 0, 1, 1, dict(bg=FUNC_BG, hover=FUNC_HOVER, fg=TEXT_DARK, command=lambda: backspace(entry))),
        ("^", 0, 2, 1, dict(bg=FUNC_BG, hover=FUNC_HOVER, fg=TEXT_DARK, command=lambda: get_input(entry, "^"))),
        ("÷", 0, 3, 1, op("÷")),
        ("7", 1, 0, 1, num("7")), ("8", 1, 1, 1, num("8")), ("9", 1, 2, 1, num("9")), ("×", 1, 3, 1, op("×")),
        ("4", 2, 0, 1, num("4")), ("5", 2, 1, 1, num("5")), ("6", 2, 2, 1, num("6")), ("−", 2, 3, 1, op("−")),
        ("1", 3, 0, 1, num("1")), ("2", 3, 1, 1, num("2")), ("3", 3, 2, 1, num("3")), ("+", 3, 3, 1, op("+")),
        ("0", 4, 0, 2, num("0")), (".", 4, 2, 1, num(".")),
        ("=", 4, 3, 1, dict(bg=OP_BG, hover=OP_HOVER, fg=TEXT_LIGHT, command=lambda: calc(entry, root))),
    ]
    for text, r, c, span, style in layout:
        b = make_button(grid, text, **style)
        b.grid(row=r, column=c, columnspan=span, padx=3, pady=3, sticky="nsew", ipadx=14)

    # Keyboard support
    root.bind("<Return>", lambda e: calc(entry, root))
    root.bind("<KP_Enter>", lambda e: calc(entry, root))
    root.bind("<Escape>", lambda e: clear(entry))
    entry.focus_set()

    root.mainloop()


if __name__ == "__main__":
    cal()
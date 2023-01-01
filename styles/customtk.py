import tkinter as tk
from styles.colours import Colour


def create_circle(
    c: tk.Canvas,
    x: float,
    y: float,
    radius: float,
    width: float = 0,
    colour: Colour = Colour.DODGER_BLUE,
    tags: str = None,
):
    """helper function for creating a circle on Tkinter canvas"""
    x0 = x - radius
    x1 = x + radius
    y0 = y - radius
    y1 = y + radius
    return c.create_oval(x0, y0, x1, y1, width=width, fill=colour, tags=tags)


class Button(tk.Button):
    def __init__(
        self,
        window,
        text,
        command,
        bg=Colour.DODGER_BLUE,
        fg=Colour.WHITE,
        padx=6,
        pady=6,
        bd=1,
    ):
        super().__init__(
            window,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            padx=padx,
            pady=pady,
            bd=bd,
        )

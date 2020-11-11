# -*- coding: utf-8 -*-

from .modules import tk


class Button(tk.Button):
    def __init__(self, color, pack=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            activebackground=self["bg"],
            activeforeground=color,
            borderwidth=0,
            highlightthickness=0,
            font="Default 20",
            fg=color
        )
        if pack:
            self.pack(side="left", padx=10)

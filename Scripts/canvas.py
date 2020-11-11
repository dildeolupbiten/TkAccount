# -*- coding: utf-8 -*-

from .modules import tk


class Canvas(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame = tk.Frame(master=self.master)
        self.x_scrollbar = tk.Scrollbar(
            master=self.master,
            orient="horizontal",
            command=self.xview
        )
        self.y_scrollbar = tk.Scrollbar(
            master=self.master,
            orient="vertical",
            command=self.yview
        )
        self.configure(
            yscrollcommand=self.y_scrollbar.set,
            xscrollcommand=self.x_scrollbar.set
        )
        self.create_window((0, 0), window=self.frame, anchor="nw")
        self.frame.bind(
            sequence="<Configure>",
            func=lambda event: self.on_frame_configure()
        )
        self.x_scrollbar.pack(side="bottom", fill="x")
        self.y_scrollbar.pack(side="right", fill="y")
        self.pack(fill="both", expand=True)

    def on_frame_configure(self):
        bbox = self.bbox("all")
        x, y, width, height = bbox
        if height < self.winfo_height():
            height = self.winfo_height()
        if width < self.winfo_width():
            width = self.winfo_width()
        self.configure(scrollregion=(x + 2, y + 2, width, height))

# -*- coding: utf-8 -*-

from .messagebox import MsgBox
from .toplevel import FormWindow
from .frame import CategoryFrame
from .utilities import (
    change_category_no, get_frames, read_from_database, write_to_database
)


class Category(FormWindow):
    def __init__(self, icons, *args, **kwargs):
        super().__init__(
            title="Add Category",
            add_command=self.add_category,
            remove_command=self.remove_category,
            apply_command=lambda: self.apply(
                widget=self.canvas.frame,
                icons=icons,
                table="CATEGORIES"
            ),
            *args,
            **kwargs
        )
        self.error = ""
        self.data = read_from_database(table="CATEGORIES")
        if self.data:
            self.load_data(data=self.data)

    def load_data(self, data, widget=None):
        for index, (key, value) in enumerate(data.items()):
            if not widget:
                self.add_category()
                self.canvas.frame.winfo_children()[index].entry.insert(
                    "insert", key
                )
                if value:
                    self.load_data(
                        widget=self.canvas.frame.winfo_children()[index],
                        data=value
                    )
            else:
                widget.add_category()
                widget.winfo_children()[-1].entry.insert("insert", key)
                if value:
                    self.load_data(
                        widget=widget.winfo_children()[-1],
                        data=value
                    )

    def add_category(self):
        CategoryFrame(master=self.canvas.frame, no=self.no)
        self.no += 1

    def remove_category(self):
        for frame in get_frames(widget=self.canvas.frame):
            if frame.var.get() == "1":
                frame.destroy()
                self.no -= 1
        change_category_no(widget=self.canvas.frame)

    def apply(self, widget, icons, table):
        data = self.get_categories(widget=widget, icons=icons)
        if data:
            if not self.error:
                write_to_database(data=data, table=table)
                self.destroy()
                MsgBox(
                    level="info",
                    title="Info",
                    message="Categories were created successfully.",
                    icons=icons,
                    width=360
                )
            elif (
                    self.error
                    ==
                    "There's already a category with \nthis name!"
            ):
                MsgBox(
                    title="Warning",
                    level="warning",
                    icons=icons,
                    message=self.error
                )
            elif self.error == "Fill all the entries!":
                MsgBox(
                    title="Warning",
                    level="warning",
                    icons=icons,
                    message=self.error
                )
        else:
            MsgBox(
                title="Warning",
                level="warning",
                icons=icons,
                message="No categories have been created yet."
            )
        self.error = ""

    def get_categories(self, widget, icons):
        data = {}
        for index, frame in enumerate(get_frames(widget=widget), 1):
            frames = get_frames(widget=frame)
            if frame.entry.get() in data:
                frame.style.configure(
                    frame.entry.cget("style"),
                    fieldbackground="red"
                )
                self.error = "There's already a category with \nthis name!"
            elif not frame.entry.get():
                frame.style.configure(
                    frame.entry.cget("style"),
                    fieldbackground="red"
                )
                self.error = "Fill all the entries!"
            if frames:
                data[frame.entry.get()] = self.get_categories(
                    widget=frame,
                    icons=icons
                )
            else:
                data[frame.entry.get()] = {}
        return data

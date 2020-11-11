# -*- coding: utf-8 -*-

from .button import Button
from .modules import tk, ttk
from .utilities import (
    get_frames, change_category_no, calculate_total_price,
    read_from_database, theme_settings, change_color,
    combobox_selected, get_customer_names
)


class CategoryFrame(tk.Frame):
    def __init__(self, no, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            bd=1,
            relief="sunken"
        )
        self.pack_configure(padx=10, pady=10)
        self.no = no
        self.sub_no = 1
        self.packed = False
        self.title = tk.Label(
            master=self,
            text=f"Category No: {no}",
            font="Default 12 bold"
        )
        self.title.pack()
        self.var = tk.StringVar()
        self.var.set("0")
        self.checkbutton = tk.Checkbutton(
            master=self,
            variable=self.var
        )
        self.checkbutton.pack()
        self.frame = tk.Frame(master=self)
        self.frame.pack()
        self.label = tk.Label(master=self.frame, text="Category Name")
        self.label.pack()
        self.style = ttk.Style()
        self.entry = ttk.Entry(master=self.frame, style=f"{no}.TEntry")
        self.entry.pack()
        self.entry.bind(
            sequence="<KeyRelease>",
            func=lambda event: self.style.configure(
                self.entry.cget("style"),
                fieldbackground="white"
            )
        )
        self.button_frame = tk.Frame(master=self)
        self.button_frame.pack()
        self.add_button = Button(
            master=self.button_frame,
            text="\u2295",
            color="green",
            command=self.add_category
        )
        self.remove_button = Button(
            master=self.button_frame,
            text="\u2296",
            color="red"
        )
        self.remove_button.pack_forget()
        self.remove_button["command"] = self.remove_category
        self.pack(side="left", fill="both", expand=True)

    def add_category(self):
        if not self.packed:
            self.remove_button.pack(side="left", padx=10)
            self.packed = True
        CategoryFrame(master=self, no=f"{self.no}.{self.sub_no}")
        self.sub_no += 1

    def remove_category(self):
        for frame in get_frames(widget=self):
            if frame.var.get() == "1":
                frame.destroy()
                self.sub_no -= 1
        change_category_no(widget=self, no=self.no)
        if not len(get_frames(widget=self)):
            self.packed = False
            self.remove_button.pack_forget()


class ProductFrame(tk.Frame):
    def __init__(self, no, texts, icons, order=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            bd=1,
            relief="sunken"
        )
        self.no = no
        self.style = ttk.Style()
        self.style.theme_settings(
            themename="default",
            settings=theme_settings("TCombobox", "TEntry")
        )
        self.pack_configure(padx=10, pady=10)
        self.widgets = {}
        self.var = tk.StringVar()
        self.var.set("0")
        self.checkbutton = tk.Checkbutton(
            master=self,
            variable=self.var
        )
        self.checkbutton.pack(side="left")
        self.create_widgets(texts=texts, order=order, icons=icons)
        self.pack()

    def create_widgets(self, texts, order, icons):
        frame = tk.Frame(master=self)
        frame.pack(side="left")
        for index, text in enumerate(texts):
            label = tk.Label(master=frame, text=text, font="Default 9 bold")
            label.grid(row=0, column=index)
            if order:
                stmt = text in ["Product Category", "Product Name"]
            else:
                stmt = text == "Product Category"
            if stmt:
                if text == "Product Category":
                    values = read_from_database(
                        table="CATEGORIES",
                        dict_or_list="list"
                    )
                else:
                    values = []
                widget = ttk.Combobox(
                    master=frame,
                    state="readonly",
                    values=values,
                    style=f"{self.no}.{index}.TCombobox"
                )
            elif text in ["Total Price", "Total Gain (%)"]:
                widget = ttk.Entry(
                    master=frame,
                    style=f"{self.no}.{index}.TEntry",
                    state="readonly"
                )
            else:
                widget = ttk.Entry(
                    master=frame,
                    style=f"{self.no}.{index}.TEntry"
                )
                if order and text == "Unit Price":
                    widget["state"] = "readonly"

            if (
                    isinstance(widget, ttk.Entry)
                    and
                    text not in ["Product Name", "Product Category"]
            ):
                widget["width"] = 8
            widget.grid(row=1, column=index)
            widget.bind(
                sequence="<KeyRelease>",
                func=lambda event: change_color(
                    event=event,
                    style=self.style
                )
            )
            self.widgets[text] = widget
        if not order:
            self.widgets["Product Category"].bind(
                sequence="<<ComboboxSelected>>",
                func=lambda event: combobox_selected(
                    event=event,
                    style=self.style,
                )
            )
            widgets = ["Unit Price", "Number Of Products"]
        else:
            for i in [
                    ["Product Category", self.widgets["Product Name"]],
                    ["Product Name", self.widgets["Unit Price"]]
            ]:
                self.widgets[i[0]].bind(
                    sequence="<<ComboboxSelected>>",
                    func=lambda event, item=(*i,): combobox_selected(
                        event=event,
                        style=self.style,
                        item=item
                    )
                )
            widgets = [
                "Unit Price",
                "Number Of Products",
                "Discount (%)",
                "Gain (%)"
            ]
        for widget in widgets:
            self.widgets[widget].bind(
                sequence="<KeyRelease>",
                func=lambda event, name=widget: calculate_total_price(
                    event=event,
                    name=name,
                    widgets=self.widgets,
                    names=widgets,
                    style=self.style,
                    order=order,
                    icons=icons
                )
            )


class CustomerFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(bd=1, relief="sunken")
        self.style = ttk.Style()
        self.style.theme_settings(
            themename="default",
            settings=theme_settings("TCombobox", "TEntry")
        )
        self.title = tk.Label(
            master=self,
            text="Customer Information",
            font="Default 11 bold"
        )
        self.title.pack()
        self.widgets = self.create_widgets(texts=["Name", "Email"])
        self.pack()

    def create_widgets(self, texts):
        widgets = {}
        frame = tk.Frame(master=self)
        frame.pack()
        for index, text in enumerate(texts):
            label = tk.Label(master=frame, text=text, font="Default 9 bold")
            label.grid(row=index, column=0)
            if text == "Name":
                widget = ttk.Combobox(
                    master=frame,
                    values=[],
                    style="TCombobox",
                )
                widget.bind(
                    sequence="<Return>",
                    func=lambda event: get_customer_names(event=event)
                )
                widget.bind(
                    sequence="<<ComboboxSelected>>",
                    func=lambda event: self.combobox_selected(event=event)
                )
            else:
                widget = ttk.Entry(master=frame, style="TEntry")
                widget.bind(
                    sequence="<Configure>",
                    func=lambda event: change_color(
                        event=event,
                        style=self.style
                    )
                )
            widget["width"] = 60
            widget.bind(
                sequence="<KeyRelease>",
                func=lambda event: change_color(
                    event=event,
                    style=self.style
                )
            )
            widget.grid(row=index, column=1, sticky="w")
            widgets[text] = widget
        return widgets

    def combobox_selected(self, event):
        value = event.widget.get().split(", Email: ")
        name = value[0].split("Name: ")[-1]
        email = value[-1]
        event.widget.delete("0", "end")
        event.widget.insert("insert", name)
        self.widgets["Email"].delete("0", "end")
        self.widgets["Email"].insert("insert", email)
        combobox_selected(event=event, style=self.style)

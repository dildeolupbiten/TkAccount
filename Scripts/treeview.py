# -*- coding: utf-8 -*-

from .button import Button
from .messagebox import MsgBox
from .database import Database
from .modules import dt, tk, ttk
from .frame import ProductFrame, CustomerFrame
from .utilities import theme_settings, get_values, edit_columns


class Treeview(tk.Frame):
    def __init__(self, columns, title, icons, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columns = columns
        self.title = title
        self.icons = icons
        self.menu = None
        self.x_scrollbar = tk.Scrollbar(
            master=self,
            orient="horizontal"
        )
        self.y_scrollbar = tk.Scrollbar(
            master=self,
            orient="vertical"
        )
        self.treeview = ttk.Treeview(
            master=self,
            show="headings",
            columns=[f"#{i + 1}" for i in range(len(self.columns))],
            height=10,
            selectmode="extended",
            style="Treeview",
            yscrollcommand=self.y_scrollbar.set,
            xscrollcommand=self.x_scrollbar.set
        )
        self.x_scrollbar.configure(command=self.treeview.xview)
        self.y_scrollbar.configure(command=self.treeview.yview)
        self.x_scrollbar.pack(side="bottom", fill="x")
        self.y_scrollbar.pack(side="right", fill="y")
        self.treeview.pack(side="left", expand=True, fill="both")
        for index, column in enumerate(self.columns):
            self.treeview.column(
                column=f"#{index + 1}",
                minwidth=75,
                width=200,
                anchor="center"
            )
            self._heading(col=index, text=column)
        self.treeview.bind(
            sequence="<Control-a>",
            func=lambda event: self.select_all()
        )
        self.treeview.bind(
            sequence="<Control-A>",
            func=lambda event: self.select_all()
        )
        if len(columns) > 2:
            self.treeview.bind(
                sequence="<Button-1>",
                func=lambda event: self.destroy_menu()
            )
            self.treeview.bind(
                sequence="<Button-3>",
                func=lambda event: self.button3_on_treeview(event=event)
            )
        self.pack(expand=True, fill="both")

    def destroy_menu(self):
        if self.menu:
            self.menu.destroy()
            self.menu = None

    def get_selection(self):
        selected = self.treeview.selection()
        if len(selected) == 1:
            EditWindow(
                columns=self.columns,
                title=self.title,
                icons=self.icons,
                treeview=self.treeview,
                selected=selected
            )

    def button3_on_treeview(self, event):
        self.destroy_menu()
        self.menu = tk.Menu(master=None, tearoff=False)
        self.menu.add_command(
            label="Edit",
            command=self.get_selection
        )
        self.menu.post(event.x_root, event.y_root)

    def _heading(self, col, text):
        self.treeview.heading(
            column=f"#{col + 1}",
            text=text,
            command=lambda: self.sort(col=col, reverse=False)
        )

    def sort(self, col, reverse):
        column = [
            (self.treeview.set(k, col), k)
            for k in self.treeview.get_children("")
        ]
        try:
            column.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            column.sort(reverse=reverse)
        for index, (val, k) in enumerate(column):
            self.treeview.move(k, "", index)
        self.treeview.heading(
            column=col,
            command=lambda: self.sort(col=col, reverse=not reverse)
        )

    def select_all(self):
        for child in self.treeview.get_children():
            self.treeview.selection_add(child)


class EditWindow(tk.Toplevel):
    def __init__(
            self,
            columns,
            title,
            icons,
            treeview,
            selected,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.title(f"Edit {title[:-1]}")
        self.table = title
        self.columns = columns
        self.icons = icons
        self.treeview = treeview
        self.values = self.treeview.item(selected)["values"]
        self.widgets = {}
        self.style = ttk.Style()
        self.style.theme_settings(
            themename="default",
            settings=theme_settings("TCombobox", "TEntry")
        )
        if title in ["Products", "Purchases"]:
            current = 0
            order = False
            self.customers = None
        else:
            current = 2
            order = True
            self.customers = CustomerFrame(master=self)
        self.products = ProductFrame(
            master=self,
            icons=icons,
            texts=columns[current:-1],
            no=1,
            order=order
        )
        self.products.checkbutton.destroy()
        self.apply_button = Button(
            master=self,
            color="green",
            text="\u2713",
            command=lambda: self.apply(selected=selected)
        )
        self.apply_button.pack_forget()
        self.apply_button.pack()
        self.insert_values_to_widgets(current=current)

    def insert_values_to_widgets(self, current):
        if current == 2:
            for i, j in zip(self.values[:current], ["Name", "Email"]):
                widget = self.customers.widgets[j]
                widget.insert("insert", i)
                self.widgets[j] = widget
        for i, j in zip(self.values[current:-1], self.columns[current:-1]):
            widget = self.products.widgets[j]
            if widget["state"].string == "readonly":
                widget["state"] = "normal"
                widget.insert("insert", i)
                widget["state"] = "readonly"
            else:
                widget.insert("insert", i)
            self.widgets[j] = widget
        widget = self.widgets["Product Name"]
        if isinstance(widget, ttk.Combobox):
            self.widgets["Product Name"]["values"] = [
                i[1] for i in Database(table="PRODUCTS").select()
                if i[0] == self.widgets["Product Category"].get()
            ]

    def get_values_from_entries(self):
        error = False
        for k, v in self.widgets.items():
            if not v.get():
                error = True
                if v["state"].string == "readonly":
                    v["state"] = "normal"
                    self.style.configure(
                        v.cget("style"),
                        fieldbackground="red"
                    )
                    v["state"] = "readonly"
                else:
                    self.style.configure(
                        v.cget("style"),
                        fieldbackground="red"
                    )
        if error:
            MsgBox(
                title="Warning",
                level="warning",
                icons=self.icons,
                message="Fill all entries!"
            )
        else:
            return get_values(data=self.widgets.values(), case=False)

    def apply(self, selected):
        new = self.get_values_from_entries()
        old = get_values(data=self.values, case=True)
        new += [dt.now()]
        if new:
            if self.table == "Orders":
                if new[2:4] != old[2:4]:
                    db = Database(table="PRODUCTS")
                    values = [
                        i for i in db.select() if list(i[:2]) == old[2:4]
                    ][0]
                    if values:
                        last_total_price = values[4] + old[4] * old[5]
                        last_number_of_products = int(
                                values[3] + old[5]
                        )
                        last_unit_price = (
                                last_total_price / last_number_of_products
                        )
                        db.update(
                            column="\"Creation Date\"",
                            column_data=values[-1],
                            edit_column="\"Unit Price\"",
                            new_data=last_unit_price
                        )
                        db.update(
                            column="\"Creation Date\"",
                            column_data=values[-1],
                            edit_column="\"Number Of Products\"",
                            new_data=last_number_of_products
                        )
                        db.update(
                            column="\"Creation Date\"",
                            column_data=values[-1],
                            edit_column="\"Total Price\"",
                            new_data=last_total_price
                        )
                    else:
                        db.insert(
                            data=(
                                old[2:6] +
                                [round(old[4] * old[5], 2)] +
                                [dt.now()]
                            )
                        )
                    values = [
                        i for i in db.select() if list(i[:2]) == new[2:4]
                    ][0]
                    if values[3] - new[5] == 0:
                        db.delete(
                            column="\"Creation Date\"",
                            column_data=values[-1]
                        )
                    else:
                        db.update(
                            column="\"Creation Date\"",
                            column_data=values[-1],
                            edit_column="\"Number Of Products\"",
                            new_data=int(values[3] - new[5])
                        )
                        db.update(
                            column="\"Creation Date\"",
                            column_data=values[-1],
                            edit_column="\"Total Price\"",
                            new_data=round(new[4] * (values[3] - new[5]), 2)
                        )
                    db.table = "ORDERS"
                    db.insert(data=new)
                    db.delete(
                        column="\"Creation Date\"",
                        column_data=old[-1]
                    )
                    self.destroy()
                if new[:2] != old[:2]:
                    db = Database(table="ORDERS")
                    db.update(
                        column="\"Creation Date\"",
                        column_data=old[-1],
                        edit_column="\"Customer Name\"",
                        new_data=new[0]
                    )
                    db.update(
                        column="\"Creation Date\"",
                        column_data=old[-1],
                        edit_column="\"Customer Email\"",
                        new_data=new[1]
                    )
                if new[5:] != old[5:]:
                    db = Database(table="PRODUCTS")
                    values = [
                        i for i in db.select()
                        if list(i[:2]) == old[2:4]
                    ][0]
                    if values:
                        number_of_products = values[3]
                        if old[5] > new[5]:
                            number_of_products += (old[5] - new[5])
                        else:
                            number_of_products -= (new[5] - old[5])
                        db.update(
                            column="\"Creation Date\"",
                            column_data=values[-1],
                            edit_column="\"Number Of Products\"",
                            new_data=number_of_products
                        )
                        db.update(
                            column="\"Creation Date\"",
                            column_data=values[-1],
                            edit_column="\"Total Price\"",
                            new_data=round(
                                number_of_products * values[2],
                                2
                            )
                        )
                    else:
                        db.insert(
                            data=(
                                    old[2:6] +
                                    [round(old[4] * old[5], 2)] +
                                    [dt.now()]
                            )
                        )
                    db.table = "ORDERS"
                    for index, i in enumerate(
                            [
                                "\"Number Of Products\"",
                                "\"Discount (%)\"",
                                "\"Gain (%)\"",
                                "\"Total Price\"",
                                "\"Total Gain (%)\""
                            ],
                            5
                    ):
                        db.update(
                            column="\"Creation Date\"",
                            column_data=old[-1],
                            edit_column=i,
                            new_data=new[index]
                        )
                    self.destroy()
            elif self.table in ["Products", "Purchases"]:
                if new[:-1] != old[:-1]:
                    db = Database(table=self.table.upper())
                    for index, i in enumerate(
                            edit_columns(db.columns[:-1])
                    ):
                        db.update(
                            column="\"Creation Date\"",
                            column_data=old[-1],
                            edit_column=f"\"{i}\"",
                            new_data=new[index]
                        )
                    self.destroy()
            values = new[:-1] + [old[-1]]
            values[3] = int(values[3])
            self.treeview.item(selected, values=values)
            MsgBox(
                title="Info",
                level="info",
                icons=self.icons,
                message="Updated the values!"
            )

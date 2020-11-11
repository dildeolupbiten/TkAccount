# -*- coding: utf-8 -*-

from .modules import tk
from .about import About
from .orders import Order
from .product import Product
from .category import Category
from .utilities import check_update
from .toplevel import ViewWindow, PlotView
from .constants import ORDER_COLUMNS, PRODUCT_COLUMNS


class Menu(tk.Menu):
    def __init__(self, icons, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master.configure(menu=self)
        self.menus = self.create_menu_cascade(
            master=self,
            labels=["Add", "View", "Plot", "Help"]
        )
        for i in (
                ["Category", Category],
                ["Product", Product],
                ["Order", Order]
        ):
            self.menus["Add"].add_command(
                label=i[0],
                command=lambda func=i[1]: func(icons=icons)
            )
        for i in (
                ("Products", "PRODUCTS", PRODUCT_COLUMNS),
                ("Orders", "ORDERS", ORDER_COLUMNS),
                ("Purchases", "PURCHASES", PRODUCT_COLUMNS)
        ):
            self.menus["View"].add_command(
                label=i[0],
                command=lambda arg=i: ViewWindow(
                    title=arg[0],
                    table=arg[1],
                    columns=arg[2],
                    icons=icons
                )
            )
        for i in [
                (
                        "Products",
                        ["Product Category", "Product Name"],
                        "Select Product(s)"
                ),
                (
                        "Customers",
                        ["Customer Name", "Customer Mail"],
                        "Select Customer(s)"
                )
        ]:
            self.menus["Plot"].add_command(
                label=i[0],
                command=lambda arg=i: PlotView(
                    icons=icons,
                    title=arg[0],
                    columns=arg[1],
                    label=arg[2]
                )
            )
        for i in [
            ["About", About],
            ["Check for updates", lambda: check_update(icons=icons)]
        ]:
            self.menus["Help"].add_command(
                label=i[0],
                command=i[1]
            )

    def create_menu_cascade(self, master: tk.Menu, labels: list):
        menus = {}
        for label in labels:
            menu = tk.Menu(master=self, tearoff=False)
            master.add_cascade(menu=menu, label=label)
            menus[label] = menu
        return menus

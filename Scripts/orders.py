# -*- coding: utf-8 -*-

from .messagebox import MsgBox
from .frame import ProductFrame
from .toplevel import FormWindow
from .constants import ORDER_COLUMNS
from .utilities import (
    apply, add_product, edit_columns, read_from_database, remove_product
)


class Order(FormWindow):
    def __init__(self, icons, *args, **kwargs):
        super().__init__(
            title="Add Order",
            add_command=lambda: add_product(
                self=self,
                icons=icons,
                product_frame=ProductFrame,
                order=True,
                text=edit_columns(ORDER_COLUMNS)[2:-1]
            ),
            remove_command=lambda: remove_product(self=self),
            apply_command=lambda: apply(
                self=self,
                icons=icons,
                table="ORDERS"
            ),
            customer=True,
            *args,
            **kwargs
        )
        if not read_from_database(table="PRODUCTS"):
            self.destroy()
            MsgBox(
                level="warning",
                title="Warning",
                message="Add products first!",
                icons=icons
            )

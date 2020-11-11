# -*- coding: utf-8 -*-

from .messagebox import MsgBox
from .frame import ProductFrame
from .toplevel import FormWindow
from .constants import PRODUCT_COLUMNS
from .utilities import (
    apply, add_product, edit_columns, read_from_database, remove_product
)


class Product(FormWindow):
    def __init__(self, icons, *args, **kwargs):
        super().__init__(
            title="Add Product",
            add_command=lambda: add_product(
                self=self,
                icons=icons,
                product_frame=ProductFrame,
                text=edit_columns(PRODUCT_COLUMNS)[:-1]
            ),
            remove_command=lambda: remove_product(self=self),
            apply_command=lambda: apply(
                self=self,
                icons=icons,
                table="PRODUCTS"
            ),
            *args,
            **kwargs
        )
        if not read_from_database(table="CATEGORIES"):
            self.destroy()
            MsgBox(
                level="warning",
                title="Warning",
                message="Add categories first!",
                icons=icons
            )

# -*- coding: utf-8 -*-

from .modules import sqlite3
from .constants import (
    CATEGORY_COLUMNS, ORDER_COLUMNS, PRODUCT_COLUMNS
)


class Database:
    def __init__(self, table):
        self.__table = table
        self.connect = sqlite3.connect(database="database.db")
        self.cursor = self.connect.cursor()
        if table == "CATEGORIES":
            self.columns = CATEGORY_COLUMNS
        elif table == "PRODUCTS":
            self.columns = PRODUCT_COLUMNS
        elif table == "PURCHASES":
            self.columns = PRODUCT_COLUMNS
        elif table == "ORDERS":
            self.columns = ORDER_COLUMNS
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.__table}"
            f" ({', '.join(self.columns)})"
        )
        self.connect.commit()

    @property
    def table(self):
        return self.__table

    @table.setter
    def table(self, new):
        self.__table = new
        if new == "CATEGORIES":
            self.columns = CATEGORY_COLUMNS
        elif new in ["PRODUCTS", "PURCHASES"]:
            self.columns = PRODUCT_COLUMNS
        elif new == "ORDERS":
            self.columns = ORDER_COLUMNS

    def insert(self, data):
        self.cursor.execute(
            f"INSERT INTO {self.__table} VALUES "
            f"({', '.join('?' * len(self.columns))})",
            (*data,)
        )
        self.connect.commit()

    def delete(self, column, column_data):
        self.cursor.execute(
            f"DELETE FROM {self.__table} WHERE {column} = ?",
            (column_data, )
        )
        self.connect.commit()

    def update(self, column, column_data, edit_column, new_data):
        self.cursor.execute(
            f"UPDATE {self.__table} "
            f"SET {edit_column} = ?"
            f"WHERE {column} = ?",
            (new_data, column_data)
        )
        self.connect.commit()

    def select(self, order_by=""):
        if order_by:
            query = f"SELECT * FROM {self.__table} ORDER BY {order_by}"
        else:
            query = f"SELECT * FROM {self.__table}"
        return [i for i in self.cursor.execute(query)]

    def drop(self):
        self.cursor.execute(f"DROP TABLE {self.__table}")
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.__table} ({', '.join(self.columns)})"
        )
        self.connect.commit()

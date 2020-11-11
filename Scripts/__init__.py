# -*- coding: utf-8 -*-

from .menu import Menu
from .modules import tk
from .utilities import create_image_files


def main():
    root = tk.Tk()
    root.title("TkAccount")
    root.geometry("800x600")
    Menu(master=root, icons=create_image_files("Icons"))
    root.mainloop()

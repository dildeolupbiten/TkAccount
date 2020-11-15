# -*- coding: utf-8 -*-

import os
import json
import sqlite3
import tkinter as tk

from tkinter import ttk
from random import randint
from subprocess import Popen
from tkinter import PhotoImage
from webbrowser import open_new
from tkcalendar import Calendar
from urllib.error import URLError
from urllib.request import urlopen
from datetime import datetime as dt, timedelta as td
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk
)

#

# -*- coding: utf-8 -*-

from .messagebox import MsgBox
from .canvas import Canvas
from .button import Button
from .treeview import Treeview
from .frame import CustomerFrame
from .modules import (
    dt, tk, ttk, plt, FigureCanvasTkAgg, NavigationToolbar2Tk
)
from .utilities import (
    check_uncheck, condition, create_calendar, edit_columns, find_dates,
    get_comparation_of_customers, get_customer_order_timeline,
    get_cumulation_of_customers, organize_data, plot_bar, plot_timeline,
    read_from_database, reduce_customer_columns, selection_clear,
    theme_settings,
)


class FormWindow(tk.Toplevel):
    def __init__(
            self,
            title,
            add_command,
            remove_command,
            apply_command,
            customer=False,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.title(title)
        self.geometry("800x600")
        self.no = 1
        if customer:
            self.customer_frame = CustomerFrame(master=self)
        self.button_frame = tk.Frame(master=self)
        self.button_frame.pack()
        self.add_button = Button(
            master=self.button_frame,
            text="\u2295",
            color="green",
            command=add_command
        )
        self.remove_button = Button(
            master=self.button_frame,
            text="\u2296",
            color="red",
            command=remove_command
        )
        self.canvas_frame = tk.Frame(master=self)
        self.canvas_frame.pack(expand=True, fill="both")
        self.canvas = Canvas(master=self.canvas_frame)
        self.apply_button = Button(
            master=self,
            text="\u2713",
            color="green",
            command=apply_command
        )
        self.apply_button.pack_forget()
        self.apply_button.pack()


class ViewWindow(tk.Toplevel):
    def __init__(self, title, columns, table, icons, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(title)
        self.columns = edit_columns(columns=columns)
        self.geometry("800x600")
        self.treeview = Treeview(
            master=self,
            columns=self.columns,
            title=title,
            icons=icons
        )
        self.data = read_from_database(table=table)
        if self.data:
            for i, j in enumerate(read_from_database(table=table)):
                self.treeview.treeview.insert(
                    parent="",
                    index=i,
                    values=j
                )


class PlotView(tk.Toplevel):
    def __init__(self, icons, title, label, columns, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order = read_from_database(table="ORDERS")
        if not self.order:
            self.destroy()
            return
        self.title(title)
        self.geometry("1024x600")
        self.style = ttk.Style()
        self.style.theme_settings(
            themename="default",
            settings=theme_settings("TEntry", "TCombobox")
        )
        self.left_frame = tk.Frame(
            master=self,
            bd=1,
            relief="sunken"
        )
        self.left_frame.pack(side="left", expand=True, fill="both")
        self.right_frame = tk.Frame(
            master=self,
            bd=1,
            relief="sunken"
        )
        self.right_frame.pack(side="left", expand=True, fill="both")
        self.treeview_label = tk.Label(
            master=self.left_frame,
            text=label,
            font="Default 11 bold"
        )
        self.treeview_label.pack()
        self.treeview = Treeview(
            master=self.left_frame,
            columns=columns,
            icons=icons,
            title=title
        )
        self.treeview.pack_forget()
        self.treeview.pack()
        self.checkbutton_frame = tk.Frame(master=self.left_frame)
        self.checkbutton_frame.pack()
        self.cumulative_or_comparative = self.create_checkbutton(
            texts=["Cumulative", "Comparative"],
        )
        self.price_or_amount = self.create_checkbutton(
            texts=["Number of products", "Price"],
        )
        if title == "Products":
            self.purchase = read_from_database(
                table="PURCHASES"
            )
            self.insert_to_treeview(
                data=self.purchase
            )
            self.select = "Products"
        elif title == "Customers":
            self.insert_to_treeview(
                data=reduce_customer_columns(self.order)
            )
            self.select = "Customers"
        self.time_widgets = self.create_time_widgets(icons=icons)
        self.plot_button = Button(
            master=self.left_frame,
            color="white",
            image=icons["plot"]["img"],
            pack=False,
            command=lambda: self.get_selections(icons=icons)
        )
        self.plot_button.pack(pady=50)
        self.figure = plt.Figure()
        self.canvas = FigureCanvasTkAgg(
            figure=self.figure,
            master=self.right_frame
        )
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.navbar = NavigationToolbar2Tk(
            canvas=self.canvas,
            window=self.right_frame
        )
        self.bar = None

    def create_checkbutton(self, texts):
        frame = tk.Frame(master=self.checkbutton_frame)
        frame.pack(side="left")
        widgets = {}
        for index, text in enumerate(texts, 1):
            label = tk.Label(
                master=frame,
                text=text,
                font="Default 9 bold"
            )
            label.grid(row=index, column=0, sticky="w")
            var = tk.StringVar()
            var.set("0")
            checkbutton = tk.Checkbutton(master=frame, variable=var)
            checkbutton.grid(row=index, column=1, sticky="w")
            widgets[text] = [var, checkbutton]
        for widget in widgets:
            if widget in ["Comparative", "Cumulative"]:
                widgets[widget][1].configure(
                    command=lambda w=widget: self.create_other_checkbuttons(
                        widgets=widgets,
                        current=w
                    )
                )
            else:
                widgets[widget][1].configure(
                    command=lambda w=widget: check_uncheck(
                        widgets=widgets,
                        current=w
                    )
                )
        return widgets

    def create_other_checkbuttons(self, current, widgets):
        check_uncheck(widgets=widgets, current=current)
        if widgets[current][0].get() == "1" and current == "Comparative":
            self.bar = self.create_checkbutton(
                texts=["Bar", "Timeline"]
            )
        else:
            if self.bar:
                for k, v in self.bar.items():
                    v[1].master.destroy()
                self.bar = None

    def create_time_widgets(self, icons):
        frame = tk.Frame(master=self.left_frame)
        frame.pack()
        widgets = {}
        for index, text in enumerate(["Time Unit", "From", "To"]):
            label = tk.Label(master=frame, text=text, font="Default 9 bold")
            label.grid(row=0, column=index)
            if index == 0:
                widget = ttk.Combobox(
                    master=frame,
                    state="readonly",
                    values=["Day", "Month", "Year"],
                    style="TCombobox"
                )
                widget.bind(
                    sequence="<Button-1>",
                    func=lambda event: widget.event_generate("<Down>")
                )
                widget.bind(
                    sequence="<<ComboboxSelected>>",
                    func=lambda event: selection_clear(
                        event=event,
                        style=self.style
                    )
                )
            else:
                widget = ttk.Entry(master=frame, width=15, state="readonly")
            widget.grid(row=1, column=index)
            widgets[text] = widget
        for i in ["From", "To"]:
            widgets[i].bind(
                sequence="<Button-1>",
                func=lambda event: create_calendar(
                    event=event,
                    widgets=widgets,
                    icons=icons
                )
            )
        return widgets

    def insert_to_treeview(self, data):
        for index, row in enumerate(data):
            self.treeview.treeview.insert(
                parent="",
                index=index,
                values=row[:2]
            )

    def get_time_values(self):
        values = [i.get() for i in self.time_widgets.values()]
        if all(values):
            return values

    def get_selections(self, icons):
        items = [
            self.treeview.treeview.item(selected)["values"]
            for selected in self.treeview.treeview.selection()
        ]
        if not items:
            MsgBox(
                title="Warning",
                level="warning",
                icons=icons,
                message="No item is selected."
            )
            return
        time_values = self.get_time_values()
        if not time_values:
            MsgBox(
                title="Warning",
                level="warning",
                icons=icons,
                message="Specify the time unit and the dates."
            )
            return
        bar = False
        if self.select == "Products":
            if (
                    self.price_or_amount["Number of products"][0].get()
                    ==
                    "1"
            ):
                n = 5
                title = "Number of products sold"
                y_title = "Number of products"
            elif self.price_or_amount["Price"][0].get() == "1":
                n = -3
                title = "Product sold price"
                y_title = "Price (Euro)"
            else:
                MsgBox(
                    title="Warning",
                    level="warning",
                    icons=icons,
                    message="Check one of the checkbuttons of \n"
                            "'Price' or 'Number of products'."
                )
                return
            if (
                    self.cumulative_or_comparative["Cumulative"][0].get()
                    ==
                    "1"
            ):
                mode = "Cumulative"
                sales_items = [
                    [i[-1], i[n]]
                    for i in self.order
                    if list(i[2:4]) in items
                ]
                data = organize_data(
                    data=sales_items,
                    dates=time_values[1:],
                    span=time_values[0]
                )
            elif (
                    self.cumulative_or_comparative["Comparative"][0].get()
                    ==
                    "1"
            ):
                sales_items = {}
                mode = "Comparative"
                for i in self.order:
                    if list(i[2:4]) in items:
                        if tuple(i[2:4]) not in sales_items:
                            sales_items[tuple(i[2:4])] = [[i[-1], i[n]]]
                        else:
                            sales_items[tuple(i[2:4])] += [[i[-1], i[n]]]
                if self.bar["Timeline"][0].get() == "1":
                    data = {}
                    for k, v in sales_items.items():
                        data[k] = organize_data(
                            data=v,
                            dates=time_values[1:],
                            span=time_values[0]
                        )
                elif self.bar["Bar"][0].get() == "1":
                    bar = True
                    data = {}
                    dates = find_dates(
                        dates=time_values[1:],
                        span=time_values[0]
                    )
                    for key, value in sales_items.items():
                        data[key] = 0
                        for i in value:
                            t = dt.strptime(i[0], "%Y-%m-%d %H:%M:%S.%f")
                            for k, v in dates.items():
                                if condition(t=t, k=k, span=time_values[0]):
                                    data[key] += i[1]
                else:
                    MsgBox(
                        title="Warning",
                        level="warning",
                        icons=icons,
                        message="Check one of the checkbuttons of \n"
                                "'Bar' or 'Timeline'."
                    )
                    return
            else:
                MsgBox(
                    title="Warning",
                    level="warning",
                    icons=icons,
                    message="Check one of the checkbuttons of \n"
                            "'Cumulative' or 'Comparative'."
                )
                return
        else:
            dates = find_dates(
                dates=time_values[1:],
                span=time_values[0]
            )
            data = {}
            if self.price_or_amount["Price"][0].get() == "1":
                n = -3
                title = "Product sold price"
                y_title = "Price (Euro)"
            elif (
                    self.price_or_amount["Number of products"][0].get()
                    ==
                    "1"
            ):
                n = 5
                title = "Number of products sold"
                y_title = "Number of products"
            else:
                MsgBox(
                    title="Warning",
                    level="warning",
                    icons=icons,
                    message="Check one of the checkbuttons of \n"
                            "'Price' or 'Number of products'."
                )
                return
            for i in self.order:
                if list(i[:2]) not in items:
                    continue
                t = dt.strptime(i[-1], "%Y-%m-%d %H:%M:%S.%f")
                for k, v in dates.items():
                    if condition(t=t, k=k, span=time_values[0]):
                        if i[:2] not in data:
                            data[i[:2]] = {
                                i[2:4]: i[n]
                            }
                        else:
                            if i[2:4] in data[i[:2]]:
                                data[i[:2]][i[2:4]] += i[n]
                            else:
                                data[i[:2]].update({i[2:4]: i[n]})
            if (
                    self.cumulative_or_comparative["Cumulative"][0].get()
                    ==
                    "1"
            ):
                mode = "Cumulative"
                data = get_cumulation_of_customers(data)
            elif (
                    self.cumulative_or_comparative["Comparative"][0].get()
                    ==
                    "1"
            ):
                mode = "Comparative"
                if self.bar["Timeline"][0].get() == "1":
                    data = get_customer_order_timeline(
                        dates=time_values[1:],
                        items=items,
                        data=self.order,
                        span=time_values[0],
                        n=n
                    )
                elif self.bar["Bar"][0].get() == "1":
                    bar = True
                    data = get_comparation_of_customers(data)
                else:
                    MsgBox(
                        title="Warning",
                        level="warning",
                        icons=icons,
                        message="Check one of the checkbuttons of \n"
                                "'Bar' or 'Timeline'."
                    )
                    return
            else:
                MsgBox(
                    title="Warning",
                    level="warning",
                    icons=icons,
                    message="Check one of the checkbuttons of \n"
                            "'Cumulative' or 'Comparative'."
                )
                return
        self.plot(
            data=data,
            title=title,
            y_title=y_title,
            mode=mode,
            bar=bar
        )

    def plot(self, data, title, y_title, mode, bar=False):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        self.figure.gca().set_ylabel(y_title)
        self.figure.gca().set_title(title)
        self.figure.subplots_adjust(
            left=0.2,
            bottom=0.4,
            right=0.9,
            top=0.9,
            wspace=0.2,
            hspace=0
        )
        if mode == "Cumulative":
            if self.select == "Products":
                for label in ax.xaxis.get_ticklabels():
                    label.set_rotation(45)
                self.figure.gca().set_xlabel("Timeline")
                ax.plot_date(
                    data.keys(),
                    data.values(),
                    color="blue",
                    linewidth=1,
                    fmt="-",
                )
            else:
                plot_bar(self=self, data=data, ax=ax)
        else:
            if self.select == "Products":
                if bar:
                    plot_bar(self=self, data=data, ax=ax)
                else:
                    plot_timeline(self=self, data=data, ax=ax)
            else:
                if bar:
                    plot_bar(self=self, ax=ax, data=data, xlabel="Customers")
                else:
                    plot_timeline(self=self, data=data, ax=ax)
        self.canvas.draw()

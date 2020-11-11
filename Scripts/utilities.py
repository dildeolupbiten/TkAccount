# -*- coding: utf-8 -*-

from .button import Button
from .messagebox import MsgBox
from .database import Database
from .modules import (
    dt, os, td, tk, ttk, json, Popen, urlopen,
    URLError, randint, Calendar, PhotoImage
)


def edit_columns(columns):
    return [
        " ".join(j.replace("\"", "") for j in i.split(" ")[:-1])
        for i in columns
    ]


def get_frames(widget):
    return [
        child for child in widget.winfo_children()
        if hasattr(child, "no")
    ]


def get_values(data, case):
    result = []
    for i in data:
        value = i if case else i.get()
        try:
            result += [float(value)]
        except ValueError:
            result += [value]
    return result


def change_category_no(widget, no=None):
    for index, frame in enumerate(get_frames(widget=widget), 1):
        if not no:
            frame.no = index
        else:
            frame.no = f"{no}.{index}"
        frame.title["text"] = f"Category No: {frame.no}"
        if get_frames(widget=frame):
            change_category_no(widget=frame, no=f"{frame.no}")


def dict_to_list(data, result=None, string=""):
    if result is None:
        result = []
    for key, value in data.items():
        if value:
            dict_to_list(
                data=value,
                result=result,
                string=string + "/" + key
            )
        else:
            result += [string[1:] + "/" + key]
    return result


def convert_to_dict(array, result=None):
    if result is None:
        result = {}
    if array:
        result[array[0]] = {}
        convert_to_dict(array=array[1:], result=result[array[0]])
    return result


def merge_dict(dict1, dict2):
    for key, value in dict1.items():
        if isinstance(value, dict):
            if key in dict2 and isinstance(dict2[key], dict):
                merge_dict(dict1=dict1[key], dict2=dict2[key])
    for key, value in dict2.items():
        if key not in dict1:
            dict1[key] = value
    return dict1


def list_to_dict(category_list):
    category_dict = [
        convert_to_dict(i.split("/")) for i in category_list
    ]
    while len(category_dict) != 1:
        d1 = category_dict[0]
        d2 = category_dict[1]
        category_dict.pop(0)
        category_dict.pop(0)
        category_dict.append(merge_dict(dict1=d1, dict2=d2))
    return category_dict[0]


def theme_settings(*styles):
    return {
        style: {
            "map": {
                "fieldbackground": [("readonly", "white")]
            }
        } for style in styles
    }


def selection_clear(event, style):
    style.map(
        event.widget.cget("style"),
        fieldbackground=[("readonly", "white")]
    )
    event.widget.selection_clear()


def combobox_selected(event, style, item=None):
    selection_clear(event=event, style=style)
    if item:
        data = read_from_database(table="PRODUCTS")
        if item[0] == "Product Category":
            values = [i[1] for i in data if i[0] == event.widget.get()]
            item[1]["values"] = values
        else:
            for i in data:
                if i[1] == event.widget.get():
                    item[1]["state"] = "normal"
                    item[1].delete("0", "end")
                    item[1].insert("insert", i[2])
                    item[1]["state"] = "readonly"
                    break


def control_numeric_widgets(event):
    value = event.widget.get()
    if value:
        try:
            float(value)
        except ValueError:
            event.widget.delete("0", "end")


def total_gain(purchase_price, selling_price):
    return (selling_price - purchase_price) / purchase_price * 100


def calculate_total_price(
        event,
        name,
        widgets,
        names,
        style,
        order,
        icons
):
    change_color(event=event, style=style)
    control_numeric_widgets(event=event)
    if order and name == "Number Of Products":
        control_product_stock(event=event, widgets=widgets, icons=icons)
    widgets["Total Price"]["state"] = "normal"
    if order:
        widgets["Total Gain (%)"]["state"] = "normal"
    numerics = [widgets[name] for name in names]
    if all(i.get() for i in numerics):
        widgets["Total Price"].delete("0", "end")
        if not order:
            result = float(numerics[0].get()) * float(numerics[1].get())
        else:
            result = float(numerics[0].get()) * float(numerics[1].get()) * \
                (1 - float(numerics[2].get()) / 100) * \
                (1 + float(numerics[3].get()) / 100)
            gain = total_gain(
                purchase_price=(
                    float(numerics[0].get()) * float(numerics[1].get())
                ),
                selling_price=result
            )
            widgets["Total Gain (%)"].delete("0", "end")
            widgets["Total Gain (%)"].insert("insert", round(gain, 2))
        widgets["Total Price"].insert("insert", round(result, 2))
    else:
        widgets["Total Price"].delete("0", "end")
        if order:
            widgets["Total Gain (%)"].delete("0", "end")
    widgets["Total Price"]["state"] = "readonly"
    if order:
        widgets["Total Gain (%)"]["state"] = "readonly"


def change_color(event, style):
    if event.widget.get():
        style.configure(
            event.widget.cget("style"),
            fieldbackground="white"
        )


def create_image_files(path):
    return {
        file[:-4]: {
            "img": PhotoImage(
                file=os.path.join(os.getcwd(), path, file)
            )
        } for file in sorted(os.listdir(os.path.join(os.getcwd(), path)))
    }


def read_from_database(table, dict_or_list="dict", order_by=""):
    db = Database(table=table)
    if table == "CATEGORIES":
        data = [i[0] for i in db.select()]
        if data:
            if dict_or_list == "dict":
                return list_to_dict(data)
            else:
                return data
    elif table in ["PRODUCTS", "PURCHASES", "ORDERS"]:
        data = db.select(order_by=order_by)
        if data:
            return data


def write_to_database(data, table):
    db = Database(table=table)
    if table == "CATEGORIES":
        for i in dict_to_list(data):
            db.insert([i])
    elif table in ["PRODUCTS", "PURCHASES", "ORDERS"]:
        if table == "PRODUCTS":
            old = db.select()
            names = [list(j[:2]) for j in old]
            for i in data:
                if i[:2] in names:
                    row = old[names.index(i[:2])]
                    total_price = round(row[4] + i[4], 2)
                    number_of_products = i[3] + row[3]
                    unit_price = round(
                        total_price / number_of_products,
                        2
                    )
                    db.delete(
                        column="\"Total Price\"",
                        column_data=row[4]
                    )
                    db.insert(
                        [
                            *i[:2],
                            unit_price,
                            number_of_products,
                            total_price,
                            i[-1]
                        ]
                    )
                else:
                    db.insert(i)
        else:
            for i in data:
                db.insert(i)


def get_customer_names(event):
    data = read_from_database(table="ORDERS", order_by="\"Customer Name\"")
    if not data:
        return
    customers = [i[:2] for i in data]
    value = event.widget.get().lower()
    found_names = []
    for customer in customers:
        if customer[0].lower().startswith(value):
            name = f"Name: {customer[0]}, Email: {customer[1]}"
            if name not in found_names:
                found_names += [name]
    if found_names:
        event.widget["values"] = found_names
        event.widget.event_generate("<Down>")
    else:
        event.widget["values"] = []


def add_product(self, icons, text, product_frame, order=False):
    product_frame(
        master=self.canvas.frame,
        no=self.no,
        texts=text,
        order=order,
        icons=icons
    )
    self.no += 1


def remove_product(self):
    for frame in self.canvas.frame.winfo_children():
        if frame.var.get() == "1":
            frame.destroy()
            self.no -= 1


def get_data(self, icons):
    error = False
    for frame in self.canvas.frame.winfo_children():
        for index, widget in enumerate(frame.widgets.values()):
            if not widget.get():
                error = True
                if isinstance(widget, ttk.Combobox):
                    frame.style.map(
                        widget.cget("style"),
                        fieldbackground=[("readonly", "red")]
                    )
                else:
                    frame.style.configure(
                        widget.cget("style"),
                        fieldbackground="red"
                    )
    if hasattr(self, "customer_frame"):
        for text, widget in self.customer_frame.widgets.items():
            if not widget.get():
                error = True
                self.customer_frame.style.configure(
                    widget.cget("style"),
                    fieldbackground="red"
                )
    if not error:
        if hasattr(self, "customer_frame"):
            return [
                [
                   widget.get()
                   for widget in self.customer_frame.widgets.values()
                ] + [
                    widget.get() if index < 2 else float(widget.get())
                    for index, widget in enumerate(frame.widgets.values())
                ] + [dt.now()]
                for frame in self.canvas.frame.winfo_children()
            ]
        else:
            return [
                [
                    widget.get() if index < 2 else float(widget.get())
                    for index, widget in enumerate(frame.widgets.values())
                ] + [dt.now()]
                for frame in self.canvas.frame.winfo_children()
            ]
    else:
        MsgBox(
            level="warning",
            title="Warning",
            message="Fill all the entries.",
            icons=icons
        )


def apply(self, icons, table):
    data = get_data(self=self, icons=icons)
    if data:
        if table == "ORDERS":
            change_stock_number(orders=data)
        elif table == "PRODUCTS":
            write_to_database(data=data, table="PURCHASES")
        write_to_database(data=data, table=table)
        self.destroy()
        MsgBox(
            level="info",
            title="Info",
            message=f"{table.title()} were created successfully.",
            icons=icons
        )


def control_product_stock(event, widgets, icons):
    value = event.widget.get()
    data = read_from_database(table="PRODUCTS")
    if data:
        category = widgets["Product Category"].get()
        product_name = widgets["Product Name"].get()
        number_of_products = 0
        for i in data:
            if i[0] == category and i[1] == product_name:
                number_of_products = i[3]
                break
        try:
            if float(value) > number_of_products:
                MsgBox(
                    level="warning",
                    title="Warning",
                    icons=icons,
                    message=f"The stock number for this product is "
                            f"{number_of_products}.",
                    width=380
                )
                event.widget.delete("0", "end")
        except ValueError:
            pass


def change_stock_number(orders):
    db = Database(table="PRODUCTS")
    select = db.select()
    for row in select:
        for order in orders:
            if list(row[:3]) == order[2:4] + [order[4]]:
                if row[3] - order[5] == 0:
                    db.delete(
                        column="\"Creation Date\"",
                        column_data=row[-1]
                    )
                else:
                    db.update(
                        column="\"Creation Date\"",
                        column_data=row[-1],
                        edit_column="\"Number Of Products\"",
                        new_data=row[3] - order[5]
                    )
                    db.update(
                        column="\"Creation Date\"",
                        column_data=row[-1],
                        edit_column="\"Total Price\"",
                        new_data=(row[3] - order[5]) * row[2]
                    )


def create_calendar(event, widgets, icons):
    event.widget.bind(
        sequence="<Button-1>",
        func=lambda e: None
    )
    toplevel = tk.Toplevel()
    toplevel.title("Calendar")
    calendar = Calendar(master=toplevel)
    calendar.pack()
    toplevel.wm_protocol(
        "WM_DELETE_WINDOW",
        lambda: activate_button(
            event=event,
            widgets=widgets,
            icons=icons,
            calendar=calendar
        )
    )
    button = Button(
        master=toplevel,
        color="green",
        pack=False,
        text="\u2295",
        command=lambda: close_calendar(
            event=event,
            widgets=widgets,
            calendar=calendar,
            icons=icons
        )
    )
    button.pack()


def is_valid_time(event, start_time, end_time, icons):
    if start_time >= end_time:
        event.widget["state"] = "readonly"
        MsgBox(
            title="Warning",
            level="warning",
            icons=icons,
            message="'From' date shouldn't be "
                    "greater\n than 'To' date."
        )
        return False
    return True


def close_calendar(event, widgets, calendar, icons):
    event.widget["state"] = "normal"
    event.widget.delete("0", "end")
    start = widgets["From"].get()
    end = widgets["To"].get()
    if start:
        start_time = dt.strptime(start, "%d.%m.%Y")
        end_time = dt.strptime(calendar.get_date(), "%d.%m.%Y")
        if not is_valid_time(
                event=event,
                start_time=start_time,
                end_time=end_time,
                icons=icons
        ):
            return
    elif end:
        start_time = dt.strptime(calendar.get_date(), "%d.%m.%Y")
        end_time = dt.strptime(end, "%d.%m.%Y")
        if not is_valid_time(
                event=event,
                start_time=start_time,
                end_time=end_time,
                icons=icons
        ):
            return
    event.widget.insert("insert", calendar.get_date())
    event.widget["state"] = "readonly"
    activate_button(
        event=event,
        widgets=widgets,
        icons=icons,
        calendar=calendar
    )


def activate_button(event, widgets, icons, calendar):
    event.widget.bind(
        sequence="<Button-1>",
        func=lambda e: create_calendar(
            event=e,
            widgets=widgets,
            icons=icons
        )
    )
    calendar.master.destroy()


def rgb():
    return "#" + "".join(
        hex(i)[2:].zfill(2) for i in (randint(0, 255) for _ in range(3))
    )


def check_uncheck(current, widgets):
    for widget in widgets:
        if widget != current:
            widgets[widget][0].set("0")


def find_dates(dates, span):
    result = {}
    d1 = dt.strptime(dates[0], "%d.%m.%Y")
    d2 = dt.strptime(dates[1], "%d.%m.%Y")
    while d1 < d2:
        result[d1] = 0
        d1 += td(days=1)
    if span == "Day":
        return result
    elif span in ["Month", "Year"]:
        temp = []
        new = {}
        for i in result:
            if span == "Month":
                unit = i.month, i.year
            else:
                unit = i.year
            if unit not in temp:
                temp.append(unit)
                new[i] = 0
        if dates[-1] not in new:
            new[d2] = 0
        return new


def condition(t, k, span):
    if span == "Day":
        return (
            t.year == k.year
            and
            t.month == k.month
            and
            t.day == k.day
        )
    elif span == "Month":
        return t.year == k.year and t.month == k.month
    else:
        return t.year == k.year


def organize_data(data, dates, span):
    dates = find_dates(dates=dates, span=span)
    for i in data:
        t = dt.strptime(i[0], "%Y-%m-%d %H:%M:%S.%f")
        for k, v in dates.items():
            if condition(t=t, k=k, span=span):
                if dates[k]:
                    dates[k] += i[1]
                else:
                    dates[k] = i[1]
    return dates


def reduce_customer_columns(data):
    result = []
    for i in data:
        if list(i[:2]) not in result:
            result.append(list(i[:2]))
    return result


def get_cumulation_of_customers(data):
    result = {}
    for key, value in data.items():
        for k, v in value.items():
            if k not in result:
                result[k] = v
            else:
                result[k] += v
    return result


def get_comparation_of_customers(data):
    result = {}
    for key, value in data.items():
        result[key] = 0
        for k, v in value.items():
            result[key] += v
    return result


def plot_bar(self, data, ax, xlabel="Products"):
    for label in ax.xaxis.get_ticklabels():
        label.set_rotation(90)
    self.figure.gca().set_xlabel(xlabel)
    x = [*range(len(data.keys()))]
    ax.bar(
        x,
        data.values(),
        color=[rgb() for _ in x],
        linewidth=1,
        label=""
    )
    ax.set_xticks(x)
    ax.set_xticklabels([i[1] for i in data.keys()])


def plot_timeline(self, data, ax):
    for label in ax.xaxis.get_ticklabels():
        label.set_rotation(45)
    self.figure.gca().set_xlabel("Timeline")
    for k, v in data.items():
        ax.plot_date(
            v.keys(),
            v.values(),
            color=rgb(),
            linewidth=1,
            label=k,
            fmt="-"
        )
    self.figure.legend(
        loc='lower center',
        ncol=2,
        fancybox=True,
    )


def get_customer_order_timeline(dates, data, span, n, items):
    result = {}
    dates = find_dates(dates=dates, span=span)
    for i in data:
        t = dt.strptime(i[-1], "%Y-%m-%d %H:%M:%S.%f")
        if not list(i[:2]) in items:
            continue
        if i[:2] not in result:
            result[i[:2]] = {k: v for k, v in dates.items()}
        for k, v in dates.items():
            if condition(t=t, k=k, span=span):
                if result[i[:2]][k]:
                    result[i[:2]][k] += i[n]
                else:
                    result[i[:2]][k] = i[n]
    return result


def check_update(icons):
    try:
        new = urlopen(
            "https://raw.githubusercontent.com/dildeolupbiten"
            "/TkAccount/master/README.md"
        ).read().decode()
    except URLError:
        MsgBox(
            title="Warning",
            message="Couldn't connect.",
            level="warning",
            icons=icons
        )
        return
    with open("README.md", "r", encoding="utf-8") as f:
        old = f.read()[:-1]
    if new != old:
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new)
    try:
        scripts = json.load(
            urlopen(
                url=f"https://api.github.com/repos/dildeolupbiten/"
                    f"TkAccount/contents/Scripts?ref=master"
            )
        )
    except URLError:
        MsgBox(
            title="Warning",
            message="Couldn't connect.",
            level="warning",
            icons=icons
        )
        return
    update = False
    for i in scripts:
        try:
            file = urlopen(i["download_url"]).read().decode()
        except URLError:
            MsgBox(
                title="Warning",
                message="Couldn't connect.",
                level="warning",
                icons=icons
            )
            return
        if i["name"] not in os.listdir("Scripts"):
            update = True
            with open(f"Scripts/{i['name']}", "w", encoding="utf-8") as f:
                f.write(file)
        else:
            with open(f"Scripts/{i['name']}", "r", encoding="utf-8") as f:
                if file != f.read():
                    update = True
                    with open(
                            f"Scripts/{i['name']}",
                            "w",
                            encoding="utf-8"
                    ) as g:
                        g.write(file)
    if update:
        MsgBox(
            title="Info",
            message="Program is updated.",
            level="info",
            icons=icons
        )
        if os.name == "posix":
            Popen(["python3", "run.py"])
            os.kill(os.getpid(), __import__("signal").SIGKILL)
        elif os.name == "nt":
            Popen(["python", "run.py"])
            os.system(f"TASKKILL /F /PID {os.getpid()}")
    else:
        MsgBox(
            title="Info",
            message="Program is up-to-date.",
            level="info",
            icons=icons
        )

import tkinter as tk
from tkinter import ttk

def create_expense_window(self):
    self.win = tk.Toplevel(self.root)
    self.win.title("Создание расхода")
    self.win.geometry("750x250")
    self.win.transient(self.root)
    self.win.grab_set()
    self.win.resizable(False, False)

    self.vcmd = self.win.register(self.validate_number)

    self.entrys_info_label = tk.Label(self.win, text="Введите данные расхода:", bg="white")
    self.entrys_info_label.place(rely=0.17, relx=0.05, width=358)

    self.sum_label = tk.Label(self.win, text="Сумма:", bg="white")
    self.sum_label.place(rely=0.27, relx=0.05)

    self.sum_entry = tk.Entry(self.win, validate="key", validatecommand=(self.vcmd, "%P"))
    self.sum_entry.place(rely=0.27, relx=0.118, width=70)

    self.rouble_label = tk.Label(self.win, text="₽", bg="white")
    self.rouble_label.place(rely=0.27, relx=0.215)

    self.category_label = tk.Label(self.win, text="Категория:", bg="white")
    self.category_label.place(rely=0.27, relx=0.25)

    self.available_categoryes = self.load_categoryes()
    
    self.category_combobox = ttk.Combobox(self.win, values=self.available_categoryes, state="readonly")
    self.category_combobox.place(rely=0.27, relx=0.343, width=140)

    self.add_category_button = tk.Button(self.win, text="Добавить категорию", command=self.add_category)
    self.add_category_button.place(rely=0.37, relx=0.35)

    self.delete_category_button = tk.Button(self.win, text="Удалить категорию", command=self.delete_category)
    self.delete_category_button.place(rely=0.49, relx=0.356)

    self.date_label = tk.Label(self.win, text="Дата:", bg="white")
    self.date_label.place(rely=0.37, relx=0.05)

    self.day_combobox = ttk.Combobox(self.win, state="readonly")
    self.day_combobox.place(rely=0.37, relx=0.101, width=40)

    self.available_months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    self.months_combobox = ttk.Combobox(self.win, values=self.available_months, state="readonly")
    self.months_combobox.place(rely=0.37, relx=0.163, width=40)
    self.months_combobox.bind("<<ComboboxSelected>>", self.update_days)

    self.available_years = ["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008",
                            "2009", "2010", "2011", "2012", "2013", "2014", "2014", "2015", "2016",
                            "2006", "2007", "2008", "2017", "2018", "2019", "2020", "2021", "2022",
                            "2023", "2024", "2025", "2026", "2027"]
    self.years_combobox = ttk.Combobox(self.win, values=self.available_years, state="readonly")
    self.years_combobox.place(rely=0.37, relx=0.225, width=50)
    self.years_combobox.bind("<<ComboboxSelected>>", self.update_days)

    self.point_label = tk.Label(self.win, text=".", bg="white", highlightbackground="black", highlightthickness=1)
    self.point_label.place(rely=0.37, relx=0.151)
    self.point_label_2 = tk.Label(self.win, text=".", bg="white", highlightbackground="black", highlightthickness=1)
    self.point_label_2.place(rely=0.37, relx=0.213)

    self.expense_comment_info = tk.Label(self.win, text="Комментарий к расходу:", bg="white")
    self.expense_comment_info.place(rely=0.17, relx=0.55, width=285)

    self.expense_comment = tk.Text(self.win, height=5, width=35, wrap="word")
    self.expense_comment.place(rely=0.27, relx=0.55)
    self.expense_comment.bind("<Key>", self.comment_limits)

    self.confirm_button = tk.Button(self.win, text="Добавить расход", command=self.create_new_expense)
    self.confirm_button.place(rely=0.7, relx=0.42)

    self.set_current_date()
    self.update_days()

def delete_expense_window(self):
    self.dlt = tk.Toplevel(self.root)
    self.dlt.title("Удаление расхода")
    self.dlt.geometry("300x150")
    self.dlt.transient(self.root)
    self.dlt.grab_set()
    self.dlt.resizable(False, False)

    self.enter_expense_label = tk.Label(self.dlt, text="Введите номер расхода:", bg="white")
    self.enter_expense_label.place(rely=0.14, relx=0.28)

    self.enter_expense_entry = tk.Entry(self.dlt)
    self.enter_expense_entry.place(rely=0.32, relx=0.39, width=70)

    self.confirm_delete_button = tk.Button(self.dlt, text="Подтвердить\nудаление расхода", command=self.delete_expense)
    self.confirm_delete_button.place(rely=0.58, relx=0.33)

def expense_info_window(self):
    self.inf = tk.Toplevel(self.root)
    self.inf.title("Узнать детали расхода")
    self.inf.geometry("300x150")
    self.inf.transient(self.root)
    self.inf.grab_set()
    self.inf.resizable(False, False)

    self.enter_expense_label = tk.Label(self.inf, text="Введите номер расхода:", bg="white")
    self.enter_expense_label.place(rely=0.14, relx=0.28)

    self.enter_expense_entry = tk.Entry(self.inf)
    self.enter_expense_entry.place(rely=0.32, relx=0.39, width=70)

    self.confirm_info_button = tk.Button(self.inf, text="Узнать детали\nрасхода", command=self.show_expense_info)
    self.confirm_info_button.place(rely=0.58, relx=0.36)

def general_stats_window(self, get_stats_info):
    stats_info = get_stats_info
    total_expenses = stats_info[0]
    total_sum = stats_info[1]
    max_sum_expense = stats_info[2]
    min_sum_expense = stats_info[3]
    max_sum_category = stats_info[4]
    min_sum_category = stats_info[5]
    max_sum_day = stats_info[6]
    min_sum_day = stats_info[7]
    max_sum_month = stats_info[8]
    min_sum_month = stats_info[9]
    max_sum_year = stats_info[10]
    min_sum_year = stats_info[11]
    
    self.sts = tk.Toplevel(self.root)
    self.sts.title("Общая статистика по вашим тратам")
    self.sts.geometry("350x450")
    self.sts.transient(self.root)
    self.sts.resizable(False, False)

    self.total_expeses_label = tk.Label(self.sts, text=f"Всего, записанных расходов: {total_expenses}", bg="white")
    self.total_expeses_label.place(rely=0.05, relx=0.05)

    self.total_sum_label = tk.Label(self.sts, text=f"Общие траты: {total_sum} ₽", bg="white")
    self.total_sum_label.place(rely=0.13, relx=0.05)

    self.max_sum_expense_label = tk.Label(self.sts, text=f"Наибольшая трата: {max_sum_expense} ₽", bg="white")
    self.max_sum_expense_label.place(rely=0.21, relx=0.05)

    self.min_sum_expense_label = tk.Label(self.sts, text=f"Наименьшая трата: {min_sum_expense} ₽", bg="white")
    self.min_sum_expense_label.place(rely=0.29, relx=0.05)

    self.max_sum_category_label = tk.Label(self.sts, text=f"Самая затратная категория: {max_sum_category}", bg="white")
    self.max_sum_category_label.place(rely=0.37, relx=0.05)

    self.min_sum_category_label = tk.Label(self.sts, text=f"Наименее затратная категория: {min_sum_category}", bg="white")
    self.min_sum_category_label.place(rely=0.45, relx=0.05)

    self.max_sum_day_label = tk.Label(self.sts, text=f"Самый затратный день: {max_sum_day}", bg="white")
    self.max_sum_day_label.place(rely=0.53, relx=0.05)

    self.min_sum_day_label = tk.Label(self.sts, text=f"Наименее затратный день: {min_sum_day}", bg="white")
    self.min_sum_day_label.place(rely=0.61, relx=0.05)

    self.max_sum_month_label = tk.Label(self.sts, text=f"Самый затратный месяц: {max_sum_month}", bg="white")
    self.max_sum_month_label.place(rely=0.69, relx=0.05)

    self.min_sum_month_label = tk.Label(self.sts, text=f"Наименее затратный месяц: {min_sum_month}", bg="white")
    self.min_sum_month_label.place(rely=0.77, relx=0.05)

    self.max_sum_year_label = tk.Label(self.sts, text=f"Самый затратный год: {max_sum_year}", bg="white")
    self.max_sum_year_label.place(rely=0.85, relx=0.05)

    self.min_sum_year_label = tk.Label(self.sts, text=f"Наименее затратный год: {min_sum_year}", bg="white")
    self.min_sum_year_label.place(rely=0.93, relx=0.05)

    self.destroy_sts_button = tk.Button(self.sts, text="Закрыть", command=self.sts.destroy)
    self.destroy_sts_button.place(rely=0.05, relx=0.8)

import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

from authorization_window import AuthorizationWindow
from app_windows import create_expense_window, delete_expense_window, expense_info_window, general_stats_window
from account_operations import logout, delete_account_window, delete_account
from load_expenses_table import load_expenses_table
from technical_functions import update_days, validate_number, check_length, set_current_date, get_current_date_str, comment_limits
from categoryes import load_categoryes, add_category, category_adding_process, delete_category, category_delete_process
from expenses_operations import create_new_expense, delete_expense
from expense_info_functions import show_expense_info, show_expense_info_window
from stats_info import get_stats_info

class RegisterOfMovemenTechnicalEquipmentApp:
    def __init__(self, root, user_login, show_main_app):
        self.ath_window = AuthorizationWindow 
        self.user_login = user_login
        self.show_main_app = show_main_app
        self.root = root
        self.root.title("МОИ РАСХОДЫ")
        self.root.geometry("1500x900")
        self.root.resizable(False, False)

        for widget in self.root.winfo_children():
            widget.destroy()

        self.top_frame = tk.Frame(self.root, bg="white", highlightbackground="black", highlightthickness=2)
        self.top_frame.place(relwidth=1, relheight=0.15)
        self.top_frame.columnconfigure(1, weight=1)

        self.account_label = tk.Label(self.top_frame, bg="lightgray", highlightbackground="gray", highlightthickness=2)
        self.account_label.place(rely=0.1, relx=0.75, relwidth=0.23, relheight=0.56)

        self.account_login_label = tk.Label(self.account_label, text=f"Вы вошли как:\n{self.user_login}",font=("Arial", 12), bg="lightgray",
                anchor="ne", justify="left")
        self.account_login_label.place(relx=0.17)

        self.account_bg_frame = tk.Frame(self.account_label, bg="white", highlightbackground="gray", highlightthickness=2)
        self.account_bg_frame.place(rely=0.02, relwidth=0.170, relheight=0.98)

        self.canvas = tk.Canvas(self.account_bg_frame, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_oval(13, 10, 37, 35, fill="gray", outline="gray", width=2)
        self.canvas.create_arc(2, 39, 49, 70, start=0, extent=180, fill="gray", outline="gray", width=2)

        self.logout_button = tk.Button(self.account_label, text="Выйти из аккаунта", bg="lightgray", command=self.logout)
        self.logout_button.place(relx=0.23, rely=0.62)

        self.delete_account_button = tk.Button(self.account_label, text="Удалить аккаунт", bg="lightgray", command=self.delete_account_window)
        self.delete_account_button.place(relx=0.63, rely=0.62)

        self.title_label = tk.Label(self.top_frame, text="МОИ РАСХОДЫ\n",font=("Arial", 24), bg="white")
        self.title_label.pack(pady=2, ipadx=60, ipady=20)

        self.table_title_label = tk.Label(self.top_frame, text="Ваши расходы:",font=("Arial", 12), bg="white")
        self.table_title_label.place(rely=0.75, relx=0.2)

        self.bottom_frame = tk.Frame(self.root, bg="white", highlightbackground="black", highlightthickness=2)
        self.bottom_frame.place(rely=0.75, relwidth=1, relheight=0.25)
        self.bottom_frame.columnconfigure(1, weight=1)

        self.table_frame = tk.Frame(self.root, bg="#f0f0f0", highlightbackground="black", highlightthickness=1)
        self.table_frame.place(rely=0.15, relx=0.1, relwidth=0.8, relheight=0.6)

        self.tree = None
        self.sсrollbar = None

        self.DB_NAME = "MyExpensesInfo.db"
        self.CATEGORYES_TABLE_NAME = "Категории"
        
        self.load_expenses_table()
        
        self.create_expense_button = tk.Button(text="Создать расход", font=("Arial", 18), command=self.create_expense_window)
        self.create_expense_button.place(relx=0.035, rely=0.82, width=200, height=100)

        self.delete_expense_button = tk.Button(text="Удалить расход", font=("Arial", 18), command=self.delete_expense_window)
        self.delete_expense_button.place(relx=0.235, rely=0.82, width=200, height=100)
        
        self.expense_info_button = tk.Button(text="Детали расходов", font=("Arial", 18), command=self.expense_info_window)
        self.expense_info_button.place(relx=0.432, rely=0.82, width=200, height=100)

        self.general_stats_button = tk.Button(text="Общая\nстатистика", font=("Arial", 18), command=self.general_stats_window)
        self.general_stats_button.place(relx=0.625, rely=0.82, width=200, height=100)

        self.exit_button = tk.Button(text="Выход", font=("Arial", 18), command=self.root.destroy)
        self.exit_button.place(relx=0.835, rely=0.82, width=200, height=100)

        
        self.requests_tree = None
        self.requests_scrollbar = None


        
    def create_expense_window(self):
        return create_expense_window(self)

    def delete_expense_window(self):
        return delete_expense_window(self)

    def expense_info_window(self):
        return expense_info_window(self)

    def general_stats_window(self):
        return general_stats_window(self, self.get_stats_info())



    def logout(self):
        return logout(self)

    def delete_account_window(self):
        return delete_account_window(self)

    def delete_account(self):
        return delete_account(self)



    def load_expenses_table(self):
        return load_expenses_table(self, self.user_login)



    def update_days(self, event=None):
        return update_days(self)

    def validate_number(self, text):
        return validate_number(text)

    def check_length(self, new_text):
        return check_length(self, new_text)

    def set_current_date(self):
        return set_current_date(self)

    def get_current_date_str(self):
        return get_current_date_str(self)

    def comment_limits(self, event):
        return comment_limits(self, event)


    
    def load_categoryes(self):
        return load_categoryes(self)

    def add_category(self):
        return add_category(self)

    def category_adding_process(self):
        return category_adding_process(self)

    def delete_category(self):
        return delete_category(self)

    def category_delete_process(self):
        return category_delete_process(self)



    def create_new_expense(self):
        return create_new_expense(self)

    def delete_expense(self):
        return delete_expense(self)

        

    def show_expense_info(self):
        return show_expense_info(self)

    def show_expense_info_window(self, expense_info):
        return show_expense_info_window(self, expense_info)



    def get_stats_info(self):
        return get_stats_info(self)



if __name__ == "__main__":
    
    DB_NAME = "MyExpensesInfo.db"
    
    # Создание БД и таблицы пользователей, если они не существуют
    if not os.path.exists(DB_NAME):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS "Пользователи" (
                    "Логин"  TEXT NOT NULL UNIQUE,
                    "Пароль" TEXT NOT NULL,
                    "Авторизован" TEXT,
                    PRIMARY KEY("Логин")
                );
            """)
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось создать базу данных или таблицу пользователей: {e}")
            exit()
    
    root = tk.Tk()
    root.withdraw()

    ath_window_instance = None

    def show_main_app(user_login):
        """
        Функция для показа главного приложения и скрытия окна авторизации.
        """
        if ath_window_instance:
            ath_window_instance.root.withdraw()
        
        root.deiconify()
        
        main_app = RegisterOfMovemenTechnicalEquipmentApp(root, user_login, show_main_app) 

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT "Логин" FROM "Пользователи" WHERE "Авторизован" = "Да"')
        login_data = cursor.fetchone()

        if login_data:
            user_login = login_data[0]
            show_main_app(user_login)
        else:
            root.deiconify()
            ath_window_instance = AuthorizationWindow(root, show_main_app)
            
        
        root.mainloop()
            
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка базы данных", f"Не удалось подключиться к базе данных: {e}")
        exit()

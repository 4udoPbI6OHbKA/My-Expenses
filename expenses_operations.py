import tkinter as tk
from tkinter import messagebox
import sqlite3
import textwrap

def create_new_expense(self):
    summa = self.sum_entry.get()
    selected_category =  self.category_combobox.get()
    selected_day = self.day_combobox.get()
    selected_month = self.months_combobox.get()
    selected_year = self.years_combobox.get()
    raw_comment = self.expense_comment.get("1.0", "end-1c").replace("\n", " ")
    comment = textwrap.fill(raw_comment, width=35)

    if not summa:
        messagebox.showwarning("Предупреждение", "Пожалуйста, введите сумму.")
        return
    if not selected_category:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите категорию.")
        return
    if not selected_day or not selected_month or not selected_year:
        messagebox.showwarning("Предупреждение", "Пожалуйста, введите полностью дату произведения расхода.")
        return

    summa = float(summa)
    
    expense_date = str(selected_day) + "." + str(selected_month) + "." + str(selected_year)
    current_date = self.get_current_date_str()

    conn = None
    try:
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        user_expenses_table_name = f"{self.user_login}_расходы"
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS "{user_expenses_table_name}" (
                "Номер расхода" INTEGER PRIMARY KEY AUTOINCREMENT,
                "Сумма" REAL,
                "Категория" TEXT,
                "Дата расхода" TEXT,
                "Дата создания" TEXT,
                "Комментарий" TEXT
            );
        """)
        conn.commit()

        cursor.execute(f"SELECT MAX(\"Номер расхода\") FROM {user_expenses_table_name}")
        max_expense_num = cursor.fetchone()[0]
            
        new_expense_num = 1 if max_expense_num is None else max_expense_num + 1

        cursor.execute(f"""
            INSERT INTO {user_expenses_table_name} ("Номер расхода", "Сумма", "Категория",
            "Дата расхода", "Дата создания", "Комментарий")
            VALUES (?, ?, ?, ?, ?, ?)
        """, (new_expense_num, summa, selected_category, expense_date, current_date, comment))
        conn.commit()

        messagebox.showinfo("Успех", "Добавлен новый расход, в вашу таблицу расходов!")

        self.load_expenses_table()
        self.win.destroy()


    except sqlite3.Error as e:
        messagebox.showerror("Ошибка базы данных", f"Ошибка при работе с базой данных: {e}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка: {e}")
    finally:
        if conn:
            conn.close()

def delete_expense(self):
    entered_expense = self.enter_expense_entry.get()

    if not entered_expense:
        messagebox.showwarning("Предупреждение", "Пожалуйста, введите номер расхода.")
        return

    try:
        entered_expense = int(entered_expense)
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Номер расхода должен быть числом.")
        return

    conn = None
    try:
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        user_expenses_table_name = f"{self.user_login}_расходы"
        cursor.execute(f"SELECT COUNT(*) FROM {user_expenses_table_name} WHERE \"Номер расхода\" = ?", (entered_expense,))
        expense_data = cursor.fetchone()

        if expense_data[0] == 0:
            messagebox.showerror("Ошибка", f"Расход под номером {entered_expense} не найден.")
            return

        cursor.execute(f"DELETE FROM {user_expenses_table_name} WHERE \"Номер расхода\" = ?", (entered_expense,))
        
        cursor.execute(f"""
            UPDATE {user_expenses_table_name} 
            SET "Номер расхода" = "Номер расхода" - 1 
            WHERE "Номер расхода" > ?
        """, (entered_expense,))
        
        conn.commit()

        messagebox.showinfo("Успех", f"Расход №{entered_expense} удален..")
            
        self.load_expenses_table()
        self.dlt.destroy()

    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Ошибка базы данных", f"Ошибка при удалении расхода: {e}")
    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка при удалении расхода: {e}")
    finally:
        if conn:
            conn.close()


            

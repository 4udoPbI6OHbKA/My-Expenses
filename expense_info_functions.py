import tkinter as tk
from tkinter import messagebox
import sqlite3

def show_expense_info(self):
    entered_expense = self.enter_expense_entry.get()

    if not entered_expense:
        messagebox.showwarning("Предупреждение", "Пожалуйста, введите номер расхода.")
        return None

    try:
        entered_expense = int(entered_expense)
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Номер расхода должен быть числом.")
        return None

    conn = None
    try:
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        user_expenses_table_name = f"{self.user_login}_расходы"
        
        cursor.execute(
            f'SELECT "Номер расхода", "Сумма", "Категория", "Дата расхода", "Дата создания", "Комментарий" '
            f'FROM "{user_expenses_table_name}" WHERE "Номер расхода" = ?', 
            (entered_expense,)
        )
        expense_info = cursor.fetchone()

        if expense_info is None:
            messagebox.showerror("Ошибка", f"Расход под номером {entered_expense} не найден.")
            return None

        self.show_expense_info_window(expense_info)
        
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка базы данных", f"Ошибка при выполнении запроса: {e}")
        return None
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка при выполнении запроса: {e}")
        return None
    finally:
        if conn:
            conn.close()


def show_expense_info_window(self, expense_info):
    expense_num = expense_info[0]
    expense_sum = expense_info[1]
    expense_category = expense_info[2]
    expense_make_date = expense_info[3]
    expense_create_date = expense_info[4]
    expense_comment = expense_info[5]
    
    self.inf.destroy()
    self.enf = tk.Toplevel(self.root)
    self.enf.title(f"Информация о расходе под номером {expense_num}")
    self.enf.geometry("350x500")
    self.enf.transient(self.root)
    self.enf.grab_set()
    self.enf.resizable(False, False)

    self.expense_num_label = tk.Label(self.enf, text=f"Номер расхода: {expense_num}", bg="white")
    self.expense_num_label.place(rely=0.05, relx=0.05)

    self.expense_sum_label = tk.Label(self.enf, text=f"Сумма расхода: {expense_sum}", bg="white")
    self.expense_sum_label.place(rely=0.15, relx=0.05)

    self.expense_category_label = tk.Label(self.enf, text=f"Категория расхода: {expense_category}", bg="white")
    self.expense_category_label.place(rely=0.25, relx=0.05)

    self.expense_make_date_label = tk.Label(self.enf, text=f"Дата произведения расхода: {expense_make_date}", bg="white")
    self.expense_make_date_label.place(rely=0.35, relx=0.05)

    self.expense_create_date_label = tk.Label(self.enf, text=f"Дата создания расхода: {expense_create_date}", bg="white")
    self.expense_create_date_label.place(rely=0.45, relx=0.05)

    self.expense_comment_title_label = tk.Label(self.enf, text=f"Комментарий к расходу:", bg="white")
    self.expense_comment_title_label.place(rely=0.55, relx=0.05)

    self.expense_comment_label = tk.Label(self.enf, text=f"{expense_comment}", bg="white", anchor="w", justify="left")
    self.expense_comment_label.place(rely=0.62, relx=0.05)

    self.destroy_enf_button = tk.Button(self.enf, text="Закрыть", command=self.enf.destroy)
    self.destroy_enf_button.place(rely=0.05, relx=0.8)

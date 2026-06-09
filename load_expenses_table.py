import tkinter as tk
from tkinter import ttk
import sqlite3
import os

def load_expenses_table(self, user_login):
    if not user_login:
        return

    user_expenses_table_name = f"{user_login}_расходы"

    for widget in self.table_frame.winfo_children():
        widget.destroy()

    self.tree = None
    self.scrollbar = None

    if not os.path.exists(self.DB_NAME):
        return

    try:
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='{user_expenses_table_name}';")
        if cursor.fetchone()[0] == 0:
            return
 
        column_names_to_display = ["Номер расхода", "Сумма", "Категория", "Дата расхода"]
        
        select_columns_str = ", ".join([f'"{col}"' for col in column_names_to_display])
        
        cursor.execute(f"SELECT {select_columns_str} FROM \"{user_expenses_table_name}\"")
        rows = cursor.fetchall()

        if self.tree is None:
            self.tree = ttk.Treeview(self.table_frame, columns=column_names_to_display, show='headings')

            for col in column_names_to_display:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=150, anchor='center')

            if self.sсrollbar is None:
                self.sсrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
                self.tree.configure(yscrollcommand=self.sсrollbar.set)
                self.sсrollbar.pack(side='right', fill='y')
                self.tree.pack(side='left', fill='both', expand=True)
            else:
                self.tree.pack(side='left', fill='both', expand=True)
        else:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for col in column_names_to_display:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=150, anchor='center')

            if not self.tree.winfo_ismapped():
                self.tree.pack(side='left', fill='both', expand=True)
                if self.sсrollbar:
                    self.sсrollbar.pack(side='right', fill='y')

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        conn.close()

    except sqlite3.Error as e:
        tk.messagebox.showerror("Ошибка базы данных", f"Ошибка при загрузке таблицы расходов: {e}")
    except Exception as e:
        tk.messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка при загрузке таблицы: {e}")

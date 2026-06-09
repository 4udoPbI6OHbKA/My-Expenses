import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def load_categoryes(self):
    loaded_categoryes = []
    try:
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.CATEGORYES_TABLE_NAME}';")
        if cursor.fetchone() is None:
            conn.close()
            return


        cursor.execute(f"SELECT * FROM {self.CATEGORYES_TABLE_NAME}")
        categoryes = cursor.fetchall()
        loaded_categoryes = [category[0].strip("{}") for category in categoryes]

        return loaded_categoryes

        conn.close()

    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных (Запросы): {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при загрузке запросов: {e}")

def add_category(self):
    self.adc = tk.Toplevel(self.win)
    self.adc.title("Добавление категории")
    self.adc.geometry("300x150")
    self.adc.transient(self.win)
    self.adc.grab_set()
    self.adc.resizable(False, False)

    self.add_category_label = tk.Label(self.adc, text="Введите название новой категории:", bg="white")
    self.add_category_label.place(rely=0.15, relx=0.17)

    self.add_category_entry = tk.Entry(self.adc)
    self.add_category_entry.place(rely=0.32, relx=0.1, width=240)

    self.confirm_category_adding_button = tk.Button(self.adc, text="Подтвердить", command=self.category_adding_process)
    self.confirm_category_adding_button.place(rely=0.6, relx=0.36)

def category_adding_process(self):
    new_category = self.add_category_entry.get().strip()

    if not new_category:
        messagebox.showwarning("Предупреждение", "Пожалуйста, введите название новой категории.")
        return

    conn = None
    try:
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.CATEGORYES_TABLE_NAME} (
                "Категория" TEXT UNIQUE
            );
        """)

        try:
            cursor.execute(f"""
                INSERT INTO {self.CATEGORYES_TABLE_NAME} ("Категория")
                VALUES (?)
            """, (new_category,))
            conn.commit()
            
            messagebox.showinfo("Успех", f"Категория '{new_category}' успешно добавлена.")

            self.available_categoryes = self.load_categoryes()
            self.category_combobox.config(values=self.available_categoryes)
            self.adc.destroy()
            
        except sqlite3.IntegrityError:
            messagebox.showwarning("Предупреждение", f"Категория с названием '{new_category}' уже записана, Напишите название новой категории.")

    except sqlite3.Error as e:
        messagebox.showerror("Ошибка базы данных", f"Ошибка при работе с базой данных: {e}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка: {e}")
    finally:
        if conn:
            conn.close()


def delete_category(self):
    self.dlc = tk.Toplevel(self.win)
    self.dlc.title("Удаление категории")
    self.dlc.geometry("300x150")
    self.dlc.transient(self.win)
    self.dlc.grab_set()
    self.dlc.resizable(False, False)

    self.add_category_label = tk.Label(self.dlc, text="Выберете категорию, для удаления:", bg="white")
    self.add_category_label.place(rely=0.15, relx=0.17)

    self.available_categoryes = self.load_categoryes()
    
    self.del_category_combobox = ttk.Combobox(self.dlc, values=self.available_categoryes, state="readonly")
    self.del_category_combobox.place(rely=0.32, relx=0.1, width=240)

    self.confirm_category_delete_button = tk.Button(self.dlc, text="Подтвердить", command=self.category_delete_process)
    self.confirm_category_delete_button.place(rely=0.6, relx=0.36)

def category_delete_process(self):
    category_to_delete = self.del_category_combobox.get()
    selected_category = self.category_combobox.get()
    
    if not category_to_delete:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберете ктегорию для удаления.")
        return

    conn = None
    try:
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        try:
            cursor.execute(f"""
                DELETE FROM {self.CATEGORYES_TABLE_NAME} WHERE
                "Категория" = ?
            """, (category_to_delete,))
            conn.commit()
            
            messagebox.showinfo("Успех", f"Категория '{category_to_delete}' удалена.")

            self.available_categoryes = self.load_categoryes()
            self.category_combobox.config(values=self.available_categoryes)
            if selected_category == category_to_delete:
                self.category_combobox.set("")
            self.dlc.destroy()
            
            
        except sqlite3.IntegrityError:
            messagebox.showwarning("Предупреждение", f"Категория с названием '{category_to_delete}' не найдена.")

    except sqlite3.Error as e:
        messagebox.showerror("Ошибка базы данных", f"Ошибка при работе с базой данных: {e}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка: {e}")
    finally:
        if conn:
            conn.close()
    

    

    

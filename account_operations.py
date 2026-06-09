import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sqlite3

def logout(self):
    answer = messagebox.askyesno("Выход из аккаунта", f"Вы действительно хотите выйти из аккаунта {self.user_login}?")

    if answer:
        if self:
            self.root.withdraw()

        for widget in self.root.winfo_children():
            widget.destroy()

        conn = None
        try:
            conn = sqlite3.connect(self.DB_NAME)
            cursor = conn.cursor()

            cursor.execute("UPDATE Пользователи SET Авторизован = 'Нет' WHERE Логин = ?", (self.user_login,))
            conn.commit()

            self.root.deiconify()
            ath_window = self.ath_window(self.root, self.show_main_app)
            return ath_window

        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Произошла ошибка при выходе из аккаунта: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Непредвиденная ошибка при выходе из аккаунта: {e}")
        finally:
            if conn:
                conn.close()
    
    else:
        return

def delete_account_window(self):
    self.adl = tk.Toplevel(self.root)
    self.adl.title("Удаление аккаунта")
    self.adl.geometry("500x150")
    self.adl.transient(self.root)
    self.adl.grab_set()
    self.adl.resizable(False, False)

    self.val_cmd = self.root.register(self.check_length)

    self.account_delete_info_label_1 = tk.Label(self.adl, text=f"Вы уверены, что хотите удалить аккаунт: {self.user_login}?", bg="white")
    self.account_delete_info_label_1.place(rely=0.1, relx=0.05)

    self.account_delete_info_label_2 = tk.Label(self.adl, text=f"Введите пароль, для подтверждения:", bg="white")
    self.account_delete_info_label_2.place(rely=0.27, relx=0.05)

    self.loged_password_entry = tk.Entry(self.adl, font=("Arial", 11), show="*", validate="key", validatecommand=(self.val_cmd, '%P'))
    self.loged_password_entry.place(rely=0.45, relx=0.1, width=245)

    self.confirm_delete_button = tk.Button(self.adl, text="Подтвердить удаление", command=self.delete_account)
    self.confirm_delete_button.place(rely=0.7, relx=0.2)

    self.cancel_delete_button = tk.Button(self.adl, text="Отмена", command=self.adl.destroy)
    self.cancel_delete_button.place(rely=0.7, relx=0.65)

def delete_account(self):
    loged_password = self.loged_password_entry.get()
    login_to_delete = self.user_login

    if not loged_password:
        messagebox.showwarning("Предупреждение", "Пожалуйста, введите пароль от аккаунта, для удаления.")
        return

    conn = None
    try:
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT Пароль FROM Пользователи WHERE Логин = ?", (login_to_delete,))
        user_data = cursor.fetchone()

        if user_data:
            stored_password = user_data[0]
            if stored_password == loged_password:

                cursor.execute(f"DELETE FROM Пользователи WHERE Логин = ?", (login_to_delete,))
                    
                user_expenses_table_name = f"{login_to_delete}_расходы"
                cursor.execute(f"DROP TABLE IF EXISTS {user_expenses_table_name}")

                conn.commit()
            
                messagebox.showinfo("Успех", f"Аккаунт {login_to_delete} удалён!")

                if self:
                    self.root.withdraw()

                for widget in self.root.winfo_children():
                    widget.destroy()

                self.root.deiconify()
                ath_window = self.ath_window(self.root, self.show_main_app)
                return ath_window
                    
            else:
                messagebox.showerror("Ошибка аутентификации", "Не верный пароль. Введите верный пароль от аккаунта.")
                self.loged_password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Ошибка аутентификации", f"Пользователя с логином '{login_to_delete}' не зарегистрирован. Попробуйте его зарегистрировать или введите другой логин.")

    except sqlite3.Error as e:
        messagebox.showerror("Ошибка базы данных", f"Произошла ошибка при выходе из аккаунта: {e}")
    except Exception as e:
            messagebox.showerror("Ошибка", f"Непредвиденная ошибка при выходе из аккаунта: {e}")
    finally:
        if conn:
            conn.close()

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import re

class AuthorizationWindow:
    def __init__(self, root, show_main_app):
        self.root = root
        self.show_main_app = show_main_app
        self.root.title("Авторизация")
        self.root.geometry("900x500")
        self.root.resizable(False, False)

        self.val_cmd = self.root.register(self.check_length)

        self.DB_NAME = "MyExpensesInfo.db"
        self.user_login = None

        self.central_frame = tk.Frame(self.root, bg="white", highlightbackground="black", highlightthickness=2)
        self.central_frame.place(relwidth=0.8, relheight=0.6, rely=0.15, relx=0.1)

        self.ath_title_label = tk.Label(self.root, text="Авторизация", font=("Arial", 15), bg="white")
        self.ath_title_label.pack(pady=80, ipadx=60, ipady=5)

        self.enter_info_label = tk.Label(self.root, text="Введите данные:", font=("Arial", 11), bg="lightgray")
        self.enter_info_label.place(rely=0.32, relx=0.38)

        self.login_label = tk.Label(self.root, text="Логин:", font=("Arial", 11), bg="lightgray")
        self.login_label.place(rely=0.37, relx=0.32)

        self.login_entry = tk.Entry(self.root, font=("Arial", 11), bg="lightgray", validate="key", validatecommand=(self.val_cmd, '%P'))
        self.login_entry.place(rely=0.371, relx=0.38, width=245)

        self.password_label = tk.Label(self.root, text="Пароль:", font=("Arial", 11), bg="lightgray")
        self.password_label.place(rely=0.42, relx=0.308)

        self.password_entry = tk.Entry(self.root, font=("Arial", 11), bg="lightgray", show="*", validate="key", validatecommand=(self.val_cmd, '%P'))
        self.password_entry.place(rely=0.421, relx=0.38, width=245)

        self.confirm_authorization_button = tk.Button(self.root, text="Войти", font=("Arial", 11), bg="lightgray", command=self.process_authorization)
        self.confirm_authorization_button.place(rely=0.51, relx=0.38, width=200)

        self.or_info_label = tk.Label(self.root, text="или", font=("Arial", 11), bg="lightgray")
        self.or_info_label.place(rely=0.578, relx=0.476)

        self.move_to_registration_button = tk.Button(self.root, text="Зарегестрироваться", font=("Arial", 11), bg="lightgray", command=self.move_to_registration)
        self.move_to_registration_button.place(rely=0.63, relx=0.38, width=200)

        self.exit_button = tk.Button(text="Выход", font=("Arial", 11), bg="lightgray", command=self.root.destroy)
        self.exit_button.place(relx=0.82, rely=0.67)


        self.confirm_registration_button = tk.Button(self.root, text="Создать аккаунт", font=("Arial", 11), bg="lightgray", command=self.process_registration)
        self.move_to_authorization_button = tk.Button(self.root, text="Войти в аккаунт", font=("Arial", 11), bg="lightgray", command=self.move_to_authorization)

        self.confim_password_label = tk.Label(self.root, text="Подтвердить пароль:", font=("Arial", 11), bg="lightgray")
        self.confim_password_entry = tk.Entry(self.root, font=("Arial", 11), bg="lightgray", show="*", validate="key", validatecommand=(self.val_cmd, '%P'))

        self.reg_title_label = tk.Label(self.root, text="Регистрация", font=("Arial", 15), bg="white")


    def move_to_registration(self):
        self.login_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        
        self.ath_title_label.pack_forget()
        self.reg_title_label.pack(pady=80, ipadx=60, ipady=5)
        
        self.confirm_authorization_button.place_forget()
        self.confirm_registration_button.place(rely=0.51, relx=0.38, width=200)

        self.move_to_registration_button.place_forget()
        self.move_to_authorization_button.place(rely=0.63, relx=0.38, width=200)

        self.enter_info_label.place(rely=0.29, relx=0.38)
        self.login_label.place(rely=0.34, relx=0.32)
        self.login_entry.place(rely=0.341, relx=0.38, width=245)
        self.password_label.place(rely=0.39, relx=0.308)
        self.password_entry.place(rely=0.391, relx=0.38, width=245)

        self.confim_password_label.place(rely=0.44, relx=0.205)
        self.confim_password_entry.place(rely=0.441, relx=0.38, width=245)

    def move_to_authorization(self):
        self.login_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confim_password_entry.delete(0, tk.END)
        
        self.reg_title_label.pack_forget()
        self.ath_title_label.pack(pady=80, ipadx=60, ipady=5)
        
        self.confirm_registration_button.place_forget()
        self.confirm_authorization_button.place(rely=0.51, relx=0.38, width=200)

        self.move_to_authorization_button.place_forget()
        self.move_to_registration_button.place(rely=0.63, relx=0.38, width=200)

        self.enter_info_label.place(rely=0.32, relx=0.38)
        self.login_label.place(rely=0.37, relx=0.32)
        self.login_entry.place(rely=0.371, relx=0.38, width=245)
        self.password_label.place(rely=0.42, relx=0.308)
        self.password_entry.place(rely=0.421, relx=0.38, width=245)

        self.confim_password_label.place_forget()
        self.confim_password_entry.place_forget()

    def check_length(self, new_text):
        if len(new_text) > 18:
            return False
        
        if new_text == "":
            return True

        if re.match(r"[a-zA-Z0-9_а-яА-яёЁ]+$", new_text):
            return True
        
        return False

    def process_registration(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confim_password_entry.get()

        if not login or not password or not confirm_password:
            messagebox.showwarning("Предупреждение", "Пожалуйста, заполните все поля.")
            return

        if password != confirm_password:
            messagebox.showerror("Ошибка", "Пароли не совпадают.")
            return

        if len(login) < 3 or len(password) < 3:
            messagebox.showwarning("Предупреждение", "Длины логина и пароля должны быть не менее 3 символов.")
            return

        conn = None
        try:
            conn = sqlite3.connect(self.DB_NAME)
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

            cursor.execute("SELECT COUNT(*) FROM Пользователи WHERE Логин = ?", (login,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Ошибка", f"Пользователь с логином '{login}' уже существует.")
                return

            cursor.execute("INSERT INTO Пользователи (Логин, Пароль, Авторизован) VALUES (?, ?, ?)", (login, password, "Да"))
            conn.commit()
            
            user_expenses_table_name = f"{login}_расходы"
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

            messagebox.showinfo("Успех", "Регистрация прошла успешно!")

            self.user_login = login
            
            self.show_main_app(self.user_login)
            
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Произошла ошибка при работе с базой данных: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Непредвиденная ошибка при регистрации: {e}")
        finally:
            if conn:
                conn.close()


    def process_authorization(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        if not login or not password:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите логин и пароль.")
            return

        conn = None
        try:
            conn = sqlite3.connect(self.DB_NAME)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='Пользователи';")
            if cursor.fetchone()[0] == 0:
                messagebox.showerror("Ошибка авторизации", f"Пользователя с логином '{login}' не зарегистрирован. Попробуйте его зарегистрировать или введите другой логин.")
                return

            cursor.execute("SELECT Пароль FROM Пользователи WHERE Логин = ?", (login,))
            user_data = cursor.fetchone()

            if user_data:
                stored_password = user_data[0]
                if stored_password == password:
                    
                    user_expenses_table_name = f"{login}_расходы"
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

                    cursor.execute("UPDATE Пользователи SET Авторизован = 'Да' WHERE Логин = ?", (login,))
                    conn.commit()
            
                    messagebox.showinfo("Успех", "Авторизация прошла успешно!")

                    self.user_login = login
                    
                    self.show_main_app(self.user_login)
                    
                else:
                    messagebox.showerror("Ошибка авторизации", "Не верный пароль. Попробуйте ввести другой.")
                    self.password_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Ошибка авторизации", f"Пользователя с логином '{login}' не зарегистрирован. Попробуйте его зарегистрировать или введите другой логин.")

        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Произошла ошибка при авторизации: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Непредвиденная ошибка при авторизации: {e}")
        finally:
            if conn:
                conn.close()

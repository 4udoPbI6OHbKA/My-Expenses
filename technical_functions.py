from tkinter import messagebox
from datetime import datetime
import sqlite3
import re

def update_days(self, event=None):
    selected_day = self.day_combobox.get()
    sd = selected_day
    
    selected_month = self.months_combobox.get()
    sm = selected_month
    
    selected_year = self.years_combobox.get()
    sy = selected_year
    

    days_values = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
                  "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                  "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]

    if sm == "01" or sm == "03" or sm == "05" or sm == "07" or sm == "08" or sm == "10" or sm == "12":
        available_days = days_values
        
    elif sm == "02":
        if sy == "2000" or sy == "2004" or sy == "2008" or sy == "2012" or sy == "2016" or sy == "2020" or sy == "2024":
            available_days = days_values[:-2]
            if sd == "30" or sd == "31":
                self.day_combobox.set("")
                
        else:
            available_days = days_values[:-3]
            if sd == "29" or sd == "30" or sd == "31":
                self.day_combobox.set("")
                
    elif sm == "04" or sm == "06" or sm == "09" or sm == "11":
        available_days = days_values[:-1]
        if sd == "31":
            self.day_combobox.set("")
            
    else:
        available_days = []

    self.day_combobox.config(values=available_days)

def validate_number(text):
    if text == "":
        return True

    if text[0] == "0":
        return False

    return text.isdigit()

def check_length(self, new_text):
        if len(new_text) > 18:
            return False
        
        if new_text == "":
            return True

        if re.match(r"[a-zA-Z0-9_а-яА-яёЁ]+$", new_text):
            return True
        
        return False

def set_current_date(self):
    now = datetime.now()
    
    current_day = f"{now.day:02}"
    current_month = f"{now.month:02}"
    current_year = str(now.year)

    self.day_combobox.set(current_day)
    self.months_combobox.set(current_month)
    self.years_combobox.set(current_year)
    
def get_current_date_str(self):
    now = datetime.now()
    return now.strftime("%d.%m.%Y")

def comment_limits(self, event):
    text = self.expense_comment.get("1.0", "end-1c")
    
    if event.keysym in ("BackSpace", "Delete", "Left", "Right", "Up", "Down"):
        return

    if len(text) >= 175:
        return "break"


import sqlite3
from collections import defaultdict
from datetime import datetime

def get_stats_info(self):

    conn = sqlite3.connect(self.DB_NAME)
    cursor = conn.cursor()

    user_expenses_table_name = f"{self.user_login}_расходы"
    cursor.execute(f'SELECT "Сумма", "Категория", "Дата расхода" FROM "{user_expenses_table_name}"')
    rows = cursor.fetchall()
    
    if not rows:
        return [0, 0, 0, 0, None, None, None, None, None, None, None, None]
    
    total_records = len(rows)
    
    all_amounts = []
    
    cat_costs = defaultdict(float)
    day_costs = defaultdict(float)
    month_costs = defaultdict(float)
    year_costs = defaultdict(float)
    
    months_ru = {
        1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 
        5: "Май", 6: "Июнь", 7: "Июль", 8: "Август", 
        9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
    }
    
    for amount, category, date_str in rows:
        amount = float(amount)
        all_amounts.append(amount)
        
        cat_costs[category] += amount
        
        try:
            date_obj = datetime.strptime(date_str, "%d.%m.%Y")
            day_key = date_str
            month_key = (date_obj.year, date_obj.month)
            year_key = date_obj.year
            
            day_costs[day_key] += amount
            month_costs[month_key] += amount
            year_costs[year_key] += amount
        except (ValueError, TypeError):
            continue

    total_spend = sum(all_amounts)
    max_spend = max(all_amounts)
    min_spend = min(all_amounts)
    
    most_exp_cat = max(cat_costs, key=cat_costs.get) if cat_costs else None
    least_exp_cat = min(cat_costs, key=cat_costs.get) if cat_costs else None
    
    most_exp_day = max(day_costs, key=day_costs.get) if day_costs else None
    least_exp_day = min(day_costs, key=day_costs.get) if day_costs else None
    
    most_exp_month_tuple = max(month_costs, key=month_costs.get) if month_costs else None
    least_exp_month_tuple = min(month_costs, key=month_costs.get) if month_costs else None
    
    most_exp_month = months_ru[most_exp_month_tuple[1]] if most_exp_month_tuple else None
    least_exp_month = months_ru[least_exp_month_tuple[1]] if least_exp_month_tuple else None
    
    most_exp_year = max(year_costs, key=year_costs.get) if year_costs else None
    least_exp_year = min(year_costs, key=year_costs.get) if year_costs else None
    
    return [
            total_records, total_spend, max_spend, min_spend,
            most_exp_cat, least_exp_cat, most_exp_day, least_exp_day,
            most_exp_month, least_exp_month, most_exp_year, least_exp_year
            ]

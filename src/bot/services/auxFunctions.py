from datetime import date
from typing import Optional, Tuple
from telegram import Update
from telegram.ext import ContextTypes
from .models import Expense

def parse_date_args(args) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    """Parse command arguments into day, month, year."""
    today = date.today()
    if not args:
        return today.day, today.month, today.year

    # Convert all args to integers
    try:
        numbers = [int(arg) for arg in args]
    except ValueError:
        raise ValueError("All arguments must be numbers")

    if len(numbers) == 1:
        num = numbers[0]
        if 1 <= num <= 12:
            return None, num, today.year
        elif 2020 <= num <= date.today().year():
            return None, None, num
        else:
            raise ValueError(
                "Single argument must be month (1-12) or year (2020-2025)")

    elif len(numbers) == 2:
        month, year = numbers
        if 1 <= month <= 12 and 2020 <= num <= date.today().year():
            return None, month, year
        else:
            raise ValueError("Format: month (1-12) year (2023-2025)")

    elif len(numbers) == 3:
        day, month, year = numbers
        if 1 <= day <= 31 and 1 <= month <= 12 and 2020 <= num <= date.today().year():
            return day, month, year
        else:
            raise ValueError(
                "Format: day (1-31) month (1-12) year (2023-2025)")

    raise ValueError("Invalid number of arguments")
           
def check_budget(category, bot, update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    budget = bot.dataBase.get_budget(category)
    spents = bot.dataBase.get_total_spent(category)

    if (budget > 0):
        if (budget - spents <= 0):
            update.message.reply_text(
                text="🚫 You went over the budget 🚫")
        else:
            update.message.reply_text(
                text=f"Your remaining budget for {category} is {budget - spents}")
            
    return

def get_spent(spent, update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Creates an expense object and checks if the expense format is correct'''
    if ("," in "".join(spent)):
        item = []
        for i in spent:
            if ("," not in i):
                item.append(i)
            else:
                item.append(i.replace(",", ""))
                spent = spent[spent.index(i)+1:]
                break
        spent.insert(0, " ".join(item))
    
    if len(spent) != 3:
        update.message.reply_text(f"🚫 Invalid format 🚫\nTry this format: product, spent, category")
        return None
        
    try:
        int(spent[1])
    except ValueError:  # Check if amount is a number
        update.message.reply_text(f"🚫 Amount must be a number 🚫")
        return None

    return Expense(item=spent[0], amount=int(spent[1]), category=spent[2])
from datetime import date
from typing import Optional, Tuple
from telegram import Update
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

async def get_spending(update: Update):
    try:
        spending = update.message.text.split(" ")

        if ("," in "".join(spending)):
            item = []
            for i in spending:
                if ("," not in i):
                    item.append(i)
                else:
                    item.append(i.replace(",", ""))
                    spending = spending[spending.index(i)+1:]
                    break
            spending.insert(0, " ".join(item))
            
        try:
            amount = int(amount)
        except ValueError:  # Check if amount is a number
            await update.message.reply_text(
                text="🚫 Amount must be a number 🚫")
            return
        
        await update.message.reply_text(text=f"{spending[0]}, {spending[1]}, {spending[2]}")
        
        spending = Expense(item=spending[0], amount=spending[2], category=spending[1])
        
        return spending
    except:
            await update.message.reply_text(text="🚫 Invalid format 🚫\nTry this format: product, spent, category")
            
def check_budget(category, bot, update: Update):
    
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
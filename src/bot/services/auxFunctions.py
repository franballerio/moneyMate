from datetime import date
from typing import Optional, Tuple
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
           
def check_budget(budget, spents, spent_amount) -> int:
    
    if budget == None:
        return 1

    if (budget > 0):
        if (budget - spents - spent_amount <= 0):
            return 0
        else:
            return budget

def get_spent(spent) -> Expense | int:
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
        return 0

    try:
        int(spent[1])
    except ValueError:  # Check if amount is a number
        return 1

    return Expense(item=spent[0], amount=int(spent[1]), category=spent[2])
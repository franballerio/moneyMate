import logging
import pandas as pd
import numpy as np
from datetime import date
from typing import Optional, Tuple
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dbm import mm_db


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
        elif 2020 <= num <= 2025:
            return None, None, num
        else:
            raise ValueError(
                "Single argument must be month (1-12) or year (2020-2025)")

    elif len(numbers) == 2:
        month, year = numbers
        if 1 <= month <= 12 and 2023 <= year <= 2025:
            return None, month, year
        else:
            raise ValueError("Format: month (1-12) year (2023-2025)")

    elif len(numbers) == 3:
        day, month, year = numbers
        if 1 <= day <= 31 and 1 <= month <= 12 and 2023 <= year <= 2025:
            return day, month, year
        else:
            raise ValueError(
                "Format: day (1-31) month (1-12) year (2023-2025)")

    raise ValueError("Invalid number of arguments")


# this helps to know if there are any errors
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class moneyMate:

    def __init__(self):
        # creates the object database manager
        self.db = mm_db()

    async def clear(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.db.clear_expenses()

    async def random_spents(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Parameters for generating random data
        categories = ["groceries", "so", "essentials",
                      "clothes", "entertainment", "transport", "going out"]
        start_date = "2023-01-01"
        end_date = "2025-12-31"
        num_records = 1000

        # Generate random data
        np.random.seed(42)  # For reproducibility
        random_dates = pd.to_datetime(np.random.choice(
            pd.date_range(start_date, end_date), size=num_records))
        random_categories = np.random.choice(categories, size=num_records)
        random_amounts = np.random.randint(100, 80001, size=num_records)
        ids = list(range(1000))

        # Create DataFrame
        df = pd.DataFrame({
            "id": ids,
            "item": "Product",
            "amount": random_amounts,
            "category": random_categories,
            "date": random_dates,
        })

        # Sorting by date for better usability
        df = df.sort_values(by="date").reset_index(drop=True)

        df.to_sql('expenses', self.db.conn, if_exists='replace', index=False)

        await update.message.reply_text(text="Random spents generated")

    async def add_spending(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        spending = context.args

        if not context.args:  # Check if args are empty
            await update.message.reply_text(
                text="🚫 No arguments provided 🚫\nTry this format: /add product, spent, category")
            return

        spending = [i.replace(",", "") for i in context.args]
        if len(spending) != 3:  # Check if the format is valid
            await update.message.reply_text(
                text="🚫 Invalid format 🚫\nTry this format: /add product, spent, category")
            return

        item, amount, category = spending
        try:
            amount = int(amount)
        except ValueError:  # Check if amount is a number
            await update.message.reply_text(
                text="🚫 Amount must be a number 🚫")
            return

        self.db.add_expense(item, int(amount), category)

        await update.message.reply_text(
            text=f"💸  Spent  💸\n\n \t\t📅  {date.today()}\n \t\t📦  {item.capitalize()}\n \t\t💰  ${amount:,.2f}\n \t\t📝  {category.capitalize()}\n\n ✅  Added successfully  ✅")

        budget = self.db.get_budget(category)
        spents = self.db.get_total_spent(category)

        if (budget > 0):
            if (budget - spents <= 0):
                await update.message.reply_text(
                    text="🚫 You went over the budget 🚫")
            else:
                await context.bot.send_message(
                    text=f"Your remaining budget for {category} is {budget - spents}")
        return

    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            text="Sorry, I didn't understand that command.")
        return

    async def balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Calculate balance for given time period.
        Supports querying by: month, year, specific date, or month-year combination.
        """
        months = {
            str(i): month for i, month in enumerate([
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ], 1)
        }

        try:
            day, month, year = parse_date_args(context.args)

            if day:
                spent = self.db.get_sp_day(year, month, day)
            elif month:
                spent = self.db.get_sp_month(year, month)
            elif year:
                spent = self.db.get_sp_year(year)
            else:
                spent = self.db.get_sp()

            spent = pd.DataFrame(
                spent, columns=['id', 'item', 'amount', 'category', 'date'])

            command = update.message.text.split()[0]

            if command == '/spent':
                await update.message.reply_text(
                    text=f"On {day, month, year} you spent in:\n{spent}")
                return
            if command == '/total':
                await update.message.reply_text(f"You spent ${spent['amount'].sum():,.2f} on {day, month, year}")
                return

        except ValueError as e:
            await update.message.reply_text(str(e))
            return
        except Exception as e:
            await update.message.reply_text("An error occurred while calculating your balance.")
            return

    async def delete_spending(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.db.del_last()
        await update.message.reply_text("Last expense deleted")
        return

    async def cat_budget(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        '/budget [category] [budget]'

        message = context.args

        if (len(message) == 2 and (type(int(message[1])) == int) and (type(message[0]) == str)):
            category, budget = message

            if (int(budget) >= 0):
                self.db.set_budget(category, int(budget))

                await update.message.reply_text(f"Budget correctly allocated  📊\n\nOn this month you only can spend ${budget} in {category}")
            else:
                await update.message.reply_text("Budget can't be less than 0")
        else:
            await update.message.reply_text("Format not valid for a budget, try /budget [category] [budget]")

    async def categories(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        categories = self.db.get_categories()

        await update.message.reply_text(text=f"{categories.__str__}")
        return

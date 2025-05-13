import logging
import pandas as pd
import numpy as np
from datetime import date
from telegram import Update
from telegram.ext import ContextTypes
from services.databaseManager import Database_Manager
import services.auxFunctions as aux
from services.models import Expense


logger = logging.getLogger(__name__)

class MoneyMate():

    def __init__(self, db_manager):
        # creates the object database manager
        self.dataBase: Database_Manager = db_manager

    async def clear(self):
        self.dataBase.clear_expenses()

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

        df.to_sql('expenses', self.dataBase.conn, if_exists='replace', index=False)

        await update.message.reply_text(text="Random spents generated")

    async def add_spending(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        spent: Expense = aux.get_spending(update)
        
        await update.message.reply_text(
            text=f"💸  Spent  💸\n\n \t\t📅  {date.today()}\n \t\t📦  {spent.item.capitalize()}\n \t\t💰  ${spent.amount:,.2f}\n \t\t📝  {spent.category.capitalize()}\n\n ✅  Added successfully  ✅")

        self.dataBase.add_expense(spent.item, spent.amount, spent.category)
        
        aux.check_budget(spent.category, self, update)
        
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
            day, month, year = aux.parse_date_args(context.args)

            if day:
                spent = self.dataBase.get_sp_day(year, month, day)
            elif month:
                spent = self.dataBase.get_sp_month(year, month)
            elif year:
                spent = self.dataBase.get_sp_year(year)
            else:
                spent = self.dataBase.get_sp()

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
        self.dataBase.del_last()
        await update.message.reply_text("Last expense deleted")
        return

    async def category_budget(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        '/budget [category] [budget]'

        message = context.args

        if (len(message) == 2 and (type(int(message[1])) == int) and (type(message[0]) == str)):
            category, budget = message

            if (int(budget) >= 0):
                self.dataBase.set_budget(category, int(budget))

                await update.message.reply_text(f"Budget correctly allocated  📊\n\nOn this month you only can spend ${budget} in {category}")
            else:
                await update.message.reply_text("Budget can't be less than 0")
        else:
            await update.message.reply_text("Format not valid for a budget, try /budget [category] [budget]")

    async def categories(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        categories = self.dataBase.get_categories()

        await update.message.reply_text(text=f"{categories.__str__}")
        return

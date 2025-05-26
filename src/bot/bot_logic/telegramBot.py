import logging
import pandas as pd
import numpy as np
from datetime import date
from telegram import Update
from telegram.ext import ContextTypes
from services.databaseManager import Database_Manager
from services.auxFunctions import check_budget
from services.auxFunctions import get_spent
from services.auxFunctions import parse_date_args
from services.auxFunctions import format_df_itemized_to_monospaced_table
from services.googleSheets import WorkSheet




logger = logging.getLogger(__name__)

class MoneyMate():

    def __init__(self, db_manager):
        # creates the object database manager
        self.dataBase: Database_Manager = db_manager
        self.worksheet = WorkSheet()

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
        
        spent = update.message.text.split(" ")
        # format spent like this [spent, amount, category] 
        spent = get_spent(spent)
        
        if spent == 0:
            await update.message.reply_text(f"🚫 Invalid format 🚫\nTry this format:\nproduct spent category\nyour product, spent, category")
            return None
        elif spent == 1:
            await update.message.reply_text(f"🚫 Invalid format 🚫\nAmount must be a number")
            return None

        budget = self.dataBase.get_budget(spent.category) # get the budget
        spents = self.dataBase.get_total_spents(spent.category) # get all the spents
        
        budget = check_budget(budget, spents, spent.amount)
        # it returns an error code or the category budget (if budget exists)
        
        if budget == 0:
            await update.message.reply_text(text="🚫 You went over the budget 🚫")
            return
            
        self.dataBase.add_expense(spent.item, spent.amount, spent.category)
        
        self.worksheet.sheet_add(spent)
        
        await update.message.reply_text(
            text=f"💸  Spent  💸\n\n \t\t📅  {date.today()}\n \t\t📦  {spent.item.capitalize()}\n \t\t💰  ${spent.amount:,.2f}\n \t\t📝  {spent.category.capitalize()}\n\n ✅  Added successfully  ✅")
        
        if budget == 1:
                await update.message.reply_text(text="There isn't a budget set for this category")  
        else:
            await update.message.reply_text(
                text=f"Your remaining budget for {spent.category} is ${budget - spents - spent.amount}")
            
        return

    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            text="Sorry, I didn't understand that command.")
        return

    async def spent(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            day, month, year = parse_date_args(tuple(context.args)) # returns day, month, year

            if day and month and year:
                spent = self.dataBase.get_expenses_by_day_month_year(year, month, day)
                title = f"Spent on {day}/{month}/{year}"
            else:
                spent = self.dataBase.get_expenses_today()
                title = "Spent today"

            spent = pd.DataFrame(spent, columns=['id', 'item', 'amount', 'category', 'date'])
            
            spents = format_df_itemized_to_monospaced_table(spent, title)

            await update.message.reply_text(
                text=spents)
            return

        except ValueError as e:
            await update.message.reply_text(str(e))
            return
        except Exception as e:
            await update.message.reply_text(str(e))
            #await update.message.reply_text("An error occurred while calculating your balance.")
            return

    async def delete_spending(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.dataBase.delete_last_expense()
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
        categories = self.dataBase.get_categories(self.dataBase)

        await update.message.reply_text(text=f"{categories.__str__}")
        return

    async def budgets(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        budgets_list = self.dataBase.get_budgets()

        await update.message.reply_text(text=f"{budgets_list}")
        return
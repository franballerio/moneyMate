import logging
from datetime import date

import pandas as pd
import services.auxFunctions as aux
from telegram import Update
from telegram.ext import ContextTypes

# from services.googleSheets import WorkSheet

logger = logging.getLogger(__name__)
months = {
    str(i): month
    for i, month in enumerate(
        [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
        1,
    )
}


class MoneyMate:
    def __init__(self, db_manager):
        # TODO: replace model by repository
        self.model = db_manager
        # self.worksheet = WorkSheet()

    async def clear(self):
        self.model.clear_all_expenses()

    async def add_spending(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        if text.startswith("/"):
            text = text.split(" ", 1)[1] if " " in text else ""
        data = text.split(",")
        # get spent like this Spent(item, amount, category), or error number
        spent = aux.get_spent(data)

        # error handler
        if spent == 0:
            await update.message.reply_text(
                "🚫 Invalid format 🚫\nTry this format:\nproduct spent category\nyour product, spent, category"
            )
            return None
        elif spent == 1:
            await update.message.reply_text(
                "🚫 Invalid format 🚫\nAmount must be a number"
            )
            return None

        budget = self.model.get_budget(spent.category)
        spents = self.model.get_total_spents(spent.category)

        remaining = aux.check_budget(budget, spents, spent.amount)

        if remaining == 0:
            await update.message.reply_text(text="🚫 You went over the budget 🚫")
            return

        self.model.add_expense(spent.item, spent.amount, spent.category)

        await update.message.reply_text(
            text=f"💸  Spent  💸\n\n \t\t📅  {date.today()}\n \t\t📦  {spent.item.capitalize()}\n \t\t💰  ${spent.amount:,.2f}\n \t\t📝  {spent.category.capitalize()}\n\n ✅  Added successfully  ✅"
        )

        if remaining is None:
            await update.message.reply_text(
                text="There isn't a budget set for this category"
            )
        else:
            await update.message.reply_text(
                text=f"Your remaining budget for {spent.category} is ${remaining:,.2f}"
            )

        return

    async def spent(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Calculate balance for given time period.
        Supports querying by: month, year, specific date, or month-year combination.
        """
        try:
            day, month, year = aux.parse_date_args(
                tuple(context.args)
            )  # returns day, month, year

            if day and month and year:
                spent = self.model.get_expenses_by_day_month_year(year, month, day)
                title = f"Spent on {day}/{month}/{year}"
            else:
                spent = self.model.get_expenses_today()
                title = "Spent today"

            spent = pd.DataFrame(
                spent, columns=["id", "item", "amount", "category", "date", "created_by", "version", "deleted_at", "created_at", "updated_at"]
            )

            spents = pd.DataFrame.to_json(spent)

            await update.message.reply_text(text=spents)
            return

        except ValueError as e:
            await update.message.reply_text(str(e))
            return
        except Exception as e:
            await update.message.reply_text(str(e))
            # await update.message.reply_text("An error occurred while calculating your balance.")
            return

    async def delete_spending(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.model.delete_last_expense()
        await update.message.reply_text("Last expense deleted")
        return

    async def category_budget(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        "/budget [category] [budget]"

        message = context.args

        if len(message) == 2:
            try:
                amount = int(message[1])
            except ValueError:
                await update.message.reply_text("Budget must be a number")
                return

            category = message[0]

            if amount >= 0:
                self.model.set_budget(category, amount)

                await update.message.reply_text(
                    f"Budget correctly allocated  📊\n\nOn this month you only can spend ${amount} in {category}"
                )
            else:
                await update.message.reply_text("Budget can't be less than 0")
        else:
            await update.message.reply_text(
                "Format not valid for a budget, try /budget [category] [budget]"
            )

    async def categories(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        categories = self.model.get_categories()
        await update.message.reply_text(text=str(categories))
        return

    async def budgets(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        budgets_list = self.model.get_budgets()

        await update.message.reply_text(text=f"{budgets_list}")
        return

    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(text="Sorry, I didn't understand that command.")
        return
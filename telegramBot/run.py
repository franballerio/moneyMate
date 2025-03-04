import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
# this helps to know what the bot is doing, and if there are any errors
from bot import moneyMate


def main():

    mm = moneyMate()

    # create the bot application (object)
    application = ApplicationBuilder().token(
        '7735203801:AAGwegnbEhqjLWGI-3QgmLz3iM53TvPShaU').build()

    create_df = CommandHandler('simulate', mm.random_spents)
    application.add_handler(create_df)

    clear_df = CommandHandler('restart', mm.clear)
    application.add_handler(clear_df)

    spendings_handler = CommandHandler('add', mm.add_spending)
    application.add_handler(spendings_handler)

    spent = CommandHandler('spent', mm.balance)
    application.add_handler(spent)

    balance = CommandHandler('total', mm.balance)
    application.add_handler(balance)

    delete_handler = CommandHandler('undo', mm.delete_spending)
    application.add_handler(delete_handler)

    budget_handler = CommandHandler('budget', mm.cat_budget)
    application.add_handler(budget_handler)

    categ_handler = CommandHandler('categories', mm.categories)
    application.add_handler(categ_handler)

    # this should be at the end of the file, it tells the bot what to do when an unknown command is sent
    # so this is triggered when the user sends a command that the bot doesn't know
    unknown_handler = MessageHandler(
        filters.TEXT & ~filters.COMMAND, mm.unknown)
    application.add_handler(unknown_handler)

    unknown_handler = MessageHandler(filters.COMMAND, mm.unknown)
    application.add_handler(unknown_handler)

    # runs the bot until ctrl+c is pressed
    application.run_polling()


if __name__ == "__main__":
    main()

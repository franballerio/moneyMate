from telegram.ext import CommandHandler, MessageHandler, filters
# this helps to know what the bot is doing, and if there are any errors

def registerHandlers(application, money_mate):

    create_df = CommandHandler('simulate', money_mate.random_spents)
    clear_df = CommandHandler('restart', money_mate.clear)
    spendings_handler = CommandHandler('add', money_mate.add_spending)
    spent = CommandHandler('spent', money_mate.balance)
    balance = CommandHandler('total', money_mate.balance)
    delete_handler = CommandHandler('undo', money_mate.delete_spending)
    budget_handler = CommandHandler('budget', money_mate.category_budget)
    budgets_handler = CommandHandler('budgets', money_mate.budgets)
    categ_handler = CommandHandler('categories', money_mate.categories)
    # this should be at the end of the file, it tells the bot what to do when an unknown comoney_mateand is sent
    # so this is triggered when the user sends a comoney_mateand that the bot doesn't know
    add_spending_handler = MessageHandler(filters.TEXT, money_mate.add_spending)
    unknown_command_handler = MessageHandler(filters.COMMAND, money_mate.unknown)
    
    application.add_handler(create_df)
    application.add_handler(clear_df)
    application.add_handler(spendings_handler)
    application.add_handler(spent)
    application.add_handler(balance)
    application.add_handler(delete_handler)
    application.add_handler(budget_handler)
    application.add_handler(budgets_handler)
    application.add_handler(categ_handler)
    application.add_handler(unknown_command_handler)
    application.add_handler(add_spending_handler)


import logging
from telegram.ext import ApplicationBuilder
from bot_logic.telegramBot import MoneyMate
from services.databaseManager import Database_Manager
from handlers import registerHandlers
from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv("telegram_bot_api")
db_name = os.getenv("database_name")


# Configure logging (good practice to have it in your main entry point)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler()] # To console
)
logger = logging.getLogger(__name__)

def main():
    
    db_manager = Database_Manager(db_name=db_name)
    
    money_mate = MoneyMate(db_manager)
    
        # create the bot application (object)
    application = ApplicationBuilder().token(
        bot_token).build()
    
    registerHandlers(application, money_mate)
    
    logger.info("Starting bot polling...")
    # runs the bot until ctrl+c is pressed
    application.run_polling()

if __name__ == "__main__":
    main()
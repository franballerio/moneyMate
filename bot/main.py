import logging
import os

from bot_logic.telegramBot import MoneyMate
from dotenv import load_dotenv
from handlers import registerHandlers
from services.databaseManager import Database_Manager
from telegram.ext import ApplicationBuilder

load_dotenv()
bot_token = os.getenv("TELEGRAM_TOKEN") or ""
db_name = os.getenv("DB_NAME")

# Configure logging (good practice to have it in your main entry point)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()],  # To console
)
logger = logging.getLogger(__name__)


def main():
    db_url = os.getenv("DATABASE_URL")
    model = Database_Manager(database_url=db_url)
    money_mate = MoneyMate(model)

    # create the bot application (object)
    application = ApplicationBuilder().token(bot_token).build()
    registerHandlers(application, money_mate)

    logger.info("Startinging bot...")
    # runs the bot until ctrl+c is pressed
    application.run_polling()


if __name__ == "__main__":
    main()

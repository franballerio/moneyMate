import psycopg2
from psycopg2 import sql
from datetime import date
import logging
import os
import os.path

logger = logging.getLogger(__name__)


class Database_Manager:
    def __init__(self, database_url=None):
        if database_url is None:
            database_url = os.environ.get(
                "DATABASE_URL",
                "postgresql://user:password@localhost:5432/moneymate"
            )
        
        logger.info(f"Initializing PostgreSQL connection")
        try:
            self.conn = psycopg2.connect(database_url)
            self.cursor = self.conn.cursor()
            logger.info(f"Successfully connected to PostgreSQL")
            self.create_tables()
        except psycopg2.Error as e:
            logger.error(f"Error connecting to PostgreSQL: {e}")
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()
            raise

    def create_tables(self):
        logger.info("Attempting to create tables...")
        try:
            logger.info("Executing: CREATE TABLE IF NOT EXISTS expenses (...)")
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    id SERIAL PRIMARY KEY,
                    item TEXT NOT NULL,
                    amount NUMERIC(12, 2) NOT NULL,
                    category TEXT NOT NULL,
                    date DATE NOT NULL,
                    created_by VARCHAR(10) DEFAULT 'bot',
                    version INTEGER DEFAULT 1,
                    deleted_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
            logger.info("CREATE TABLE IF NOT EXISTS expenses - command executed.")

            logger.info("Executing: CREATE TABLE IF NOT EXISTS budgets (...)")
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS budgets (
                    id VARCHAR(100) PRIMARY KEY,
                    category TEXT UNIQUE NOT NULL,
                    limit_amount NUMERIC(12, 2) NOT NULL,
                    period VARCHAR(20) DEFAULT 'monthly',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
            logger.info("CREATE TABLE IF NOT EXISTS budgets - command executed.")

            logger.info("Committing table creation transaction...")
            self.conn.commit()
            logger.info("Table creation transaction committed successfully.")
        except psycopg2.Error as e:
            logger.error(f"PostgreSQL error during table creation: {e}")
            logger.info("Attempting to rollback transaction due to error...")
            try:
                if self.conn:
                    self.conn.rollback()
                    logger.info("Transaction rollback successful.")
            except psycopg2.Error as rb_e:
                logger.error(f"PostgreSQL error during rollback: {rb_e}")
            raise

    def add_expense(self, item, amount, category):
        try:
            self.cursor.execute(
                "INSERT INTO expenses (item, amount, category, date, created_by) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (item, amount, category, date.today(), "bot")
            )
            result = self.cursor.fetchone()
            self.conn.commit()
            logger.info(f"Added expense: {item}, {amount}, {category}")
            return True
        except psycopg2.Error as e:
            logger.error(f"Error adding expense: {e}")
            self.conn.rollback()
            return False

    def set_budget(self, category, amount):
        try:
            budget_id = f"{category}_monthly"
            self.cursor.execute(
                """INSERT INTO budgets (id, category, limit_amount, period) 
                   VALUES (%s, %s, %s, 'monthly')
                   ON CONFLICT (id) DO UPDATE SET limit_amount = %s, updated_at = CURRENT_TIMESTAMP""",
                (budget_id, category, amount, amount)
            )
            self.conn.commit()
            logger.info(f"Set budget for {category}: {amount}")
            return True
        except psycopg2.Error as e:
            logger.error(f"Error setting budget for {category}: {e}")
            self.conn.rollback()
            return False

    def get_budgets(self):
        try:
            self.cursor.execute("SELECT * FROM budgets")
            result = self.cursor.fetchall()
            return result if result else []
        except psycopg2.Error as e:
            logger.error(f"Error getting budgets: {e}")
            return []

    def get_budget(self, category):
        try:
            self.cursor.execute(
                "SELECT limit_amount FROM budgets WHERE category = %s", (category,))
            result = self.cursor.fetchone()
            logger.info(f"get_budget for '{category}': Result is {result}")
            return float(result[0]) if result else None
        except psycopg2.Error as e:
            logger.error(f"Error getting budget for {category}: {e}")
            return None

    def get_total_spents(self, category):
        try:
            self.cursor.execute(
                "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE category = %s AND deleted_at IS NULL",
                (category,))
            result = self.cursor.fetchone()
            return float(result[0]) if result and result[0] is not None else 0
        except psycopg2.Error as e:
            logger.error(f"Error getting total spent for {category}: {e}")
            return 0

    def get_all_expenses(self):
        try:
            self.cursor.execute("SELECT * FROM expenses WHERE deleted_at IS NULL ORDER BY date DESC")
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            logger.error(f"Error getting all expenses: {e}")
            return []

    def get_category_expenses(self, category):
        try:
            self.cursor.execute(
                "SELECT * FROM expenses WHERE category = %s AND deleted_at IS NULL ORDER BY date DESC",
                (category,))
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            logger.error(f"Error getting expenses for category {category}: {e}")
            return []

    def get_categories(self):
        try:
            self.cursor.execute(
                "SELECT DISTINCT category FROM expenses WHERE deleted_at IS NULL")
            return [row[0] for row in self.cursor.fetchall()]
        except psycopg2.Error as e:
            logger.error(f"Error getting categories from expenses: {e}")
            return []

    def get_expenses_today(self):
        today = date.today()
        try:
            self.cursor.execute(
                "SELECT * FROM expenses WHERE date = %s AND deleted_at IS NULL",
                (today,))
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            logger.error(f"Error getting expenses for today: {e}")
            return []

    def get_expenses_by_year(self, year):
        try:
            self.cursor.execute(
                "SELECT * FROM expenses WHERE EXTRACT(YEAR FROM date) = %s AND deleted_at IS NULL",
                (str(year),)
            )
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            logger.error(f"Error getting expenses for year {year}: {e}")
            return []

    def get_expenses_by_month_year(self, year, month):
        try:
            self.cursor.execute(
                "SELECT * FROM expenses WHERE EXTRACT(YEAR FROM date) = %s AND EXTRACT(MONTH FROM date) = %s AND deleted_at IS NULL",
                (str(year), str(month).zfill(2))
            )
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            logger.error(f"Error getting expenses for {year}/{month}: {e}")
            return []

    def get_expenses_by_day_month_year(self, year, month, day):
        from datetime import date as date_class
        date_obj = date_class(int(year), int(month), int(day))
        try:
            self.cursor.execute(
                "SELECT * FROM expenses WHERE date = %s AND deleted_at IS NULL",
                (date_obj,)
            )
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            logger.error(f"Error getting expenses for {date_obj}: {e}")
            return []

    def delete_last_expense(self):
        try:
            self.cursor.execute(
                "SELECT id FROM expenses WHERE deleted_at IS NULL ORDER BY id DESC LIMIT 1"
            )
            last_expense = self.cursor.fetchone()
            if last_expense:
                self.cursor.execute(
                    "UPDATE expenses SET deleted_at = CURRENT_TIMESTAMP WHERE id = %s",
                    (last_expense[0],)
                )
                self.conn.commit()
                logger.info(f"Soft-deleted expense with id: {last_expense[0]}")
                return True
            else:
                logger.info("No expenses to delete.")
                return False
        except psycopg2.Error as e:
            logger.error(f"Error deleting last expense: {e}")
            self.conn.rollback()
            return False

    def clear_all_expenses(self):
        logger.warning("Attempting to clear all expenses")
        try:
            self.cursor.execute("DELETE FROM expenses")
            self.conn.commit()
            logger.info("All expenses cleared.")
            return True
        except psycopg2.Error as e:
            logger.error(f"Error clearing all expenses: {e}")
            self.conn.rollback()
            return False

    def clear_all_budgets(self):
        logger.warning("Attempting to clear all budgets")
        try:
            self.cursor.execute("DELETE FROM budgets")
            self.conn.commit()
            logger.info("All budgets cleared.")
            return True
        except psycopg2.Error as e:
            logger.error(f"Error clearing all budgets: {e}")
            self.conn.rollback()
            return False

    def close(self):
        if self.conn:
            logger.info("Closing PostgreSQL connection")
            self.cursor.close()
            self.conn.close()
            self.conn = None
        else:
            logger.info("Database connection already closed or was never opened.")
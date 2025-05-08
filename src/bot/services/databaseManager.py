import sqlite3
from datetime import date
import logging
import os

logger = logging.getLogger(__name__)

class Database_Manager:
    def __init__(self, db_name):
        logger.info(f"Initializing database connection to {db_name}")
        self.db_name = db_name

        # Ensure the directory for the database file exists
        db_dir = os.path.dirname(self.db_name)
        if db_dir and not os.path.exists(db_dir): # Check if db_dir is not empty and if it exists
            try:
                os.makedirs(db_dir, exist_ok=True) # Create the directory if it doesn't exist
                logger.info(f"Created database directory: {db_dir}")
            except OSError as e:
                logger.error(f"Error creating database directory {db_dir}: {e}")
                # Depending on how critical this is, you might want to raise the error
                # or handle it in a way that allows the app to continue (e.g., fallback to in-memory DB)
                raise # Re-raise the exception if directory creation is critical

        # Connect to the database. This will create the file if it doesn't exist in the specified path.
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self._create_tables()
        except sqlite3.Error as e:
            logger.error(f"Error connecting to or initializing database {self.db_name}: {e}")
            raise # Re-raise the exception as this is critical

    def _create_tables(self):
        # Create expenses table if it doesn't exist
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                item TEXT,
                amount REAL,
                category TEXT,
                date TIMESTAMP
            )''')

        # Create table for budgets
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                category TEXT PRIMARY KEY,
                amount REAL
            )''')

        self.conn.commit()

    def add_expense(self, item, amount, category):
        self.cursor.execute("INSERT INTO expenses (item, amount, category, date) VALUES (?, ?, ?, ?)",
                            (item, amount, category, date.today()))
        self.conn.commit()
        return True

    def set_budget(self, category, amount):
        self.cursor.execute("INSERT OR REPLACE INTO budgets (category, amount) VALUES (?, ?)",
                            (category, amount))
        self.conn.commit()
        return True

    def get_budget(self, category):
        self.cursor.execute(
            "SELECT amount FROM budgets WHERE category = ?", (category,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def get_total_spent(self, category):
        self.cursor.execute(
            "SELECT SUM(amount) FROM expenses WHERE category = ?", (category,))
        result = self.cursor.fetchone()
        return result[0] if result and result[0] else 0

    def get_all_expenses(self):
        self.cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
        return self.cursor.fetchall()

    def get_category_expenses(self, category):
        self.cursor.execute(
            "SELECT * FROM expenses WHERE category = ? ORDER BY date DESC", (category,))
        return self.cursor.fetchall()

    def get_categories(self):
        self.cursor.execute(
            "SELECT category FROM expenses")
        return self.cursor.fetchall()

    def get_sp(self):
        day = str(date.today().day).zfill(2)
        month = str(date.today().month).zfill(2)

        self.cursor.execute(
            "SELECT * FROM expenses WHERE strftime('%Y-%m-%d', date) = ?", (f"{date.today().year}-{month}-{day}",))
        return self.cursor.fetchall()

    # Query by year
    def get_sp_year(self, year):
        self.cursor.execute(
            "SELECT * FROM expenses WHERE strftime('%Y', date) = ?",
            (str(year),)
        )
        return self.cursor.fetchall()

    # Query by month and year
    def get_sp_month(self, year, month):
        # Month should be 01-12 format
        month_str = str(month).zfill(2)
        self.cursor.execute(
            "SELECT * FROM expenses WHERE strftime('%Y-%m', date) = ?",
            (f"{year}-{month_str}",)
        )
        return self.cursor.fetchall()

    # Query by specific day
    def get_sp_day(self, year, month, day):
        # Format with leading zeros
        month_str = str(month).zfill(2)
        day_str = str(day).zfill(2)
        self.cursor.execute(
            "SELECT * FROM expenses WHERE strftime('%Y-%m-%d', date) = ?", (
                f"{year}-{month_str}-{day_str}",)
        )
        return self.cursor.fetchall()

    def del_last(self):
        self.cursor.execute(
            "DELETE FROM expenses WHERE id = (SELECT id FROM expenses ORDER BY id DESC LIMIT 1)"
        )

    def clear_expenses(self):
        # Drop expenses table
        self.cursor.execute("DROP TABLE IF EXISTS expenses")
        self.conn.commit()

        # Recreate the table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                item TEXT,
                amount REAL,
                category TEXT,
                date TIMESTAMP
            )''')
        self.conn.commit()

    def close(self):
        self.conn.close()

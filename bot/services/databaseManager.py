import sqlite3
from datetime import date
import logging
import os

# It's good practice to get the logger for the current module
logger = logging.getLogger(__name__)

class Database_Manager:
    def __init__(self, db_name):
        # Log the initial relative path
        logger.info(f"Initializing database connection with relative path: {db_name}")
        # Resolve the relative path to an absolute path for clarity and robustness
        self.db_name = os.path.abspath(db_name)
        logger.info(f"Absolute database path resolved to: {self.db_name}")

        # Ensure the directory for the database file exists
        db_dir = os.path.dirname(self.db_name)
        if db_dir and not os.path.exists(db_dir): # Check if db_dir is not empty and if it exists
            logger.info(f"Database directory '{db_dir}' does not exist. Attempting to create.")
            try:
                os.makedirs(db_dir, exist_ok=True) # Create the directory if it doesn't exist
                logger.info(f"Successfully created database directory: {db_dir}")
            except OSError as e:
                logger.error(f"Error creating database directory {db_dir}: {e}")
                raise # Re-raise the exception if directory creation is critical

        # Connect to the database. This will create the file if it doesn't exist in the specified path.
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            logger.info(f"Successfully connected to database: {self.db_name}")
            self.create_tables() # Call to create tables
        except sqlite3.Error as e:
            logger.error(f"Error connecting to or initializing database {self.db_name}: {e}")
            # Clean up connection if it was partially opened before re-raising
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()
            raise # Re-raise the exception as this is critical

    def create_tables(self):
        logger.info("Attempting to create tables...")
        try:
            # Create expenses table if it doesn't exist
            logger.info("Executing: CREATE TABLE IF NOT EXISTS expenses (...)")
            self.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    item TEXT,
                    amount REAL,
                    category TEXT,
                    date TIMESTAMP
                )''')
            logger.info("CREATE TABLE IF NOT EXISTS expenses - command executed.")

            # Create table for budgets
            logger.info("Executing: CREATE TABLE IF NOT EXISTS budgets (...)")
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS budgets (
                    category TEXT PRIMARY KEY,
                    amount REAL
                )''')
            logger.info("CREATE TABLE IF NOT EXISTS budgets - command executed.")

            logger.info("Committing table creation transaction...")
            self.conn.commit()
            logger.info("Table creation transaction committed successfully.")
        except sqlite3.Error as e:
            logger.error(f"SQLite error during table creation: {e}")
            logger.info("Attempting to rollback transaction due to error...")
            try:
                if self.conn: # Check if connection object exists
                    self.conn.rollback()
                    logger.info("Transaction rollback successful.")
            except sqlite3.Error as rb_e:
                logger.error(f"SQLite error during rollback: {rb_e}")
            raise # Re-raise the original error to signal failure

    def add_expense(self, item, amount, category):
        try:
            self.cursor.execute("INSERT INTO expenses (item, amount, category, date) VALUES (?, ?, ?, ?)",
                                (item, amount, category, date.today()))
            self.conn.commit()
            logger.info(f"Added expense: {item}, {amount}, {category}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error adding expense: {e}")
            return False

    def set_budget(self, category, amount):
        try:
            self.cursor.execute("INSERT OR REPLACE INTO budgets (category, amount) VALUES (?, ?)",
                                (category, amount))
            self.conn.commit()
            logger.info(f"Set budget for {category}: {amount}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error setting budget for {category}: {e}")
            return False

    def get_budgets(self):
        try:
            self.cursor.execute(
                "SELECT * FROM budgets")
            result = self.cursor.fetchone()
            return result if result else None
        except sqlite3.Error as e:
            logger.error(f"Error getting budgets: {e}")
            return None
        
    def get_budget(self, category):
        try:
            self.cursor.execute(
                "SELECT amount FROM budgets WHERE category = ?", (category,))
            result = self.cursor.fetchone()
            logger.info(f"get_budget for '{category}': Result is {result}")
            return result[0] if result else None
        except sqlite3.Error as e:
            logger.error(f"Error getting budget for {category}: {e}")
            return None

    def get_total_spents(self, category): # Renamed from get_total_spents for clarity
        try:
            self.cursor.execute(
                "SELECT SUM(amount) FROM expenses WHERE category = ?", (category,))
            result = self.cursor.fetchone()
            return result[0] if result and result[0] is not None else 0
        except sqlite3.Error as e:
            logger.error(f"Error getting total spent for {category}: {e}")
            return 0


    def get_all_expenses(self):
        try:
            self.cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error getting all expenses: {e}")
            return []

    def get_category_expenses(self, category):
        try:
            self.cursor.execute(
                "SELECT * FROM expenses WHERE category = ? ORDER BY date DESC", (category,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error getting expenses for category {category}: {e}")
            return []

    def get_categories(self):
        try:
            # This gets categories present in expenses, might want distinct categories from budgets too
            self.cursor.execute(
                "SELECT DISTINCT category FROM expenses") # Added DISTINCT
            return [row[0] for row in self.cursor.fetchall()] # Return a list of strings
        except sqlite3.Error as e:
            logger.error(f"Error getting categories from expenses: {e}")
            return []

    # Renamed from get_sp for clarity
    def get_expenses_today(self):
        today_str = date.today().isoformat() # YYYY-MM-DD
        try:
            # Ensure date in table is stored as YYYY-MM-DD string or compatible for this comparison
            # If 'date' column is TIMESTAMP and stores full datetime, use strftime on the column
            self.cursor.execute(
                "SELECT * FROM expenses WHERE date(date) = ?", (today_str,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error getting expenses for today ({today_str}): {e}")
            return []

    def get_expenses_by_year(self, year):
        try:
            self.cursor.execute(
                "SELECT * FROM expenses WHERE strftime('%Y', date) = ?",
                (str(year),)
            )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error getting expenses for year {year}: {e}")
            return []

    def get_expenses_by_month_year(self, year, month):
        month_str = str(month).zfill(2)
        year_month_str = f"{year}-{month_str}"
        try:
            self.cursor.execute(
                "SELECT * FROM expenses WHERE strftime('%Y-%m', date) = ?",
                (year_month_str,)
            )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error getting expenses for {year_month_str}: {e}")
            return []

    def get_expenses_by_day_month_year(self, year, month, day):
        month_str = str(month).zfill(2)
        day_str = str(day).zfill(2)
        date_str = f"{year}-{month_str}-{day_str}"
        try:
            self.cursor.execute(
                "SELECT * FROM expenses WHERE date(date) = ?", # Using date() function for comparison
                (date_str,)
            )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error getting expenses for {date_str}: {e}")
            return []

    def delete_last_expense(self): # Renamed from del_last
        try:
            # Check if there are any expenses first
            self.cursor.execute("SELECT id FROM expenses ORDER BY id DESC LIMIT 1")
            last_expense = self.cursor.fetchone()
            if last_expense:
                self.cursor.execute("DELETE FROM expenses WHERE id = ?", (last_expense[0],))
                self.conn.commit()
                logger.info(f"Deleted last expense with id: {last_expense[0]}")
                return True
            else:
                logger.info("No expenses to delete.")
                return False
        except sqlite3.Error as e:
            logger.error(f"Error deleting last expense: {e}")
            return False

    def clear_all_expenses(self): # Renamed from clear_expenses
        logger.warning("Attempting to clear all expenses by dropping and recreating the 'expenses' table.")
        try:
            self.cursor.execute("DROP TABLE IF EXISTS expenses")
            logger.info("'expenses' table dropped.")
            # Recreate the table
            self.cursor.execute('''
                CREATE TABLE expenses (
                    id INTEGER PRIMARY KEY,
                    item TEXT,
                    amount REAL,
                    category TEXT,
                    date TIMESTAMP
                )''')
            self.conn.commit()
            logger.info("'expenses' table recreated successfully after clearing.")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error clearing all expenses: {e}")
            return False
            
    def clear_all_budgets(self):
        logger.warning("Attempting to clear all budgets by dropping and recreating the 'budgets' table.")
        try:
            self.cursor.execute("DROP TABLE IF EXISTS budgets")
            logger.info("'budgets' table dropped.")
            # Recreate the table
            self.cursor.execute('''
                CREATE TABLE budgets (
                    category TEXT PRIMARY KEY,
                    amount REAL
                )''')
            self.conn.commit()
            logger.info("'budgets' table recreated successfully after clearing.")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error clearing all budgets: {e}")
            return False

    def close(self):
        if self.conn:
            logger.info(f"Closing database connection to {self.db_name}")
            self.conn.close()
            self.conn = None # Set to None to prevent further use
        else:
            logger.info("Database connection already closed or was never opened.")


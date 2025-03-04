import sqlite3
from datetime import date


class mm_db:
    def __init__(self, db_name='expenses.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        # Create expenses table if it doesn't exist
        self.cursor.execute('''
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
            "DELETE FROM expenses WHERE id = (SELECT id FROM your_table ORDER BY id DESC LIMIT 1)"
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

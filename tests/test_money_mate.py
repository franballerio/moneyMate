import unittest
from unittest.mock import AsyncMock, MagicMock, patch

# To make imports work, assuming 'tests' is a sibling directory to 'src'
# and your project structure is src/bot/...
# If you run tests from the root directory of the project (e.g. 'moneyMate-feature-expense-object'),
# you might need to adjust PYTHONPATH or use relative imports if tests is a package.
# For simplicity, this adds 'src' to sys.path.
import sys
import os

# Get the absolute path to the 'src' directory
# This assumes the test file is in a directory like 'tests/'
# and 'src/' is a sibling to 'tests/' or at a known relative path.
# Adjust this path if your directory structure is different.
# For example, if tests/ is inside src/, this needs to change.
# If franballerio/moneymate/moneyMate-feature-expense-object is the root:
project_root = os.path.abspath('/home/franb/projects/moneyMate/')
src_path = os.path.join(project_root, 'src/bot')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Now import the modules to be tested
# Ensure your file is named telegramBot.py and not telgramBot.py for these imports
# If it's telgramBot.py, change the import accordingly.
try:
    from bot.services.models import Expense
    from bot.services.auxFunctions import get_spending # This will test the corrected version
    from bot.bot_logic.telegramBot import add_spending, show_spending # Corrected to telgramBot.py as per user path
except ImportError as e:
    print(f"Failed to import modules: {e}")
    print(f"Current sys.path: {sys.path}")
    print("Please ensure that the 'src' directory is in your PYTHONPATH or the path is correctly set.")
    # You might need to run `export PYTHONPATH=$PYTHONPATH:/path/to/your/src`
    # or configure your IDE's test runner.
    raise

class TestExpenseModel(unittest.TestCase):
    """Tests for the Expense data class in models.py"""

    def test_expense_creation(self):
        """Test successful creation of an Expense object."""
        expense = Expense(item="Coffee", amount=3, category="Food")
        self.assertEqual(expense.item, "Coffee")
        self.assertEqual(expense.amount, 3)
        self.assertEqual(expense.category, "Food")

    def test_expense_attributes(self):
        """Test attributes of an Expense object."""
        expense = Expense(item="Groceries", amount=50, category="Food")
        self.assertIsInstance(expense.item, str)
        self.assertIsInstance(expense.amount, int)
        self.assertIsInstance(expense.category, str)


class TestGetSpendingFunction(unittest.TestCase):
    """Tests for the get_spending function in auxFunctions.py (using the corrected version)."""

    def test_get_spending_comma_separated(self):
        """Test with comma-separated input: 'item, amount, category'"""
        result = get_spending("Lunch, 15, Food")
        self.assertIsInstance(result, Expense)
        self.assertEqual(result.item, "Lunch")
        self.assertEqual(result.amount, 15)
        self.assertEqual(result.category, "Food")

    def test_get_spending_comma_separated_with_spaces(self):
        """Test with comma-separated input and extra spaces: ' item , amount , category '"""
        result = get_spending("  Movie Tickets , 25 , Entertainment  ")
        self.assertIsInstance(result, Expense)
        self.assertEqual(result.item, "Movie Tickets")
        self.assertEqual(result.amount, 25)
        self.assertEqual(result.category, "Entertainment")

    def test_get_spending_space_separated(self):
        """Test with space-separated input: 'item amount category'"""
        result = get_spending("Gym Membership 50 Health")
        self.assertIsInstance(result, Expense)
        self.assertEqual(result.item, "Gym Membership") # Item is "Gym Membership"
        self.assertEqual(result.amount, 50)
        self.assertEqual(result.category, "Health")
        
    def test_get_spending_space_separated_single_item_word(self):
        """Test with space-separated input: 'item amount category'"""
        result = get_spending("Book 20 Education")
        self.assertIsInstance(result, Expense)
        self.assertEqual(result.item, "Book") 
        self.assertEqual(result.amount, 20)
        self.assertEqual(result.category, "Education")

    def test_get_spending_amount_with_decimals_truncates(self):
        """Test that decimal amounts are truncated to integers."""
        result = get_spending("Coffee, 2.75, Food")
        self.assertIsInstance(result, Expense)
        self.assertEqual(result.item, "Coffee")
        self.assertEqual(result.amount, 2) # 2.75 truncates to 2
        self.assertEqual(result.category, "Food")

    def test_get_spending_invalid_format_not_enough_parts_comma(self):
        """Test invalid format: not enough parts (comma-separated)."""
        result = get_spending("Snacks, 5")
        self.assertEqual(result, "Invalid format: Please use 'item, amount, category' or 'item amount category'.") # Corrected version error

    def test_get_spending_invalid_format_not_enough_parts_space(self):
        """Test invalid format: not enough parts (space-separated)."""
        result = get_spending("Snacks 5")
        self.assertEqual(result, "Invalid format: Not enough details. Use: item, amount, category OR item amount category")

    def test_get_spending_invalid_amount_non_numeric(self):
        """Test invalid format: non-numeric amount."""
        result = get_spending("Gift, abc, Other")
        self.assertEqual(result, "Invalid format: Amount must be a valid number (e.g., 100 or 2.50).")

    def test_get_spending_empty_item_comma(self):
        """Test invalid format: empty item name (comma-separated)."""
        result = get_spending(", 10, Food")
        self.assertEqual(result, "Invalid format: Item name cannot be empty.")

    def test_get_spending_empty_item_space(self):
        """Test invalid format: empty item name (space-separated - this case is tricky, depends on parsing)."""
        # The corrected parser would likely fail with "Not enough details" if item is truly empty before amount/category
        result = get_spending("10 Food") # This implies item is empty
        self.assertEqual(result, "Invalid format: Not enough details. Use: item, amount, category OR item amount category")


    def test_get_spending_empty_category_comma(self):
        """Test invalid format: empty category name (comma-separated)."""
        result = get_spending("Book, 20, ")
        self.assertEqual(result, "Invalid format: Category cannot be empty.")
        
    def test_get_spending_negative_amount(self):
        """Test invalid format: negative amount."""
        result = get_spending("Refund, -10, Other")
        self.assertEqual(result, "Invalid format: Amount must be a positive number.")

    def test_get_spending_zero_amount(self):
        """Test invalid format: zero amount."""
        result = get_spending("Freebie, 0, Other")
        self.assertEqual(result, "Invalid format: Amount must be a positive number.")


class TestTelegramBotLogic(unittest.IsolatedAsyncioTestCase):
    """Tests for the Telegram bot logic functions (add_spending, show_spending)."""

    async def test_add_spending_success(self):
        """Test successful addition of an expense via add_spending."""
        update = MagicMock()
        update.message = AsyncMock()
        # Simulate user message: "/add Groceries, 50, Food"
        # The add_spending function expects the message *after* "/add "
        update.message.text = "/add Groceries, 50, Food"
        
        context = MagicMock()
        context.user_data = {} # Simulate user_data storage

        # Patch get_spending to control its output for this test
        # This assumes get_spending is imported in telgramBot.py as `from ..services.auxFunctions import get_spending`
        # or similar. Adjust the patch target if the import is different.
        with patch('bot.bot_logic.telgramBot.get_spending') as mock_get_spending:
            mock_get_spending.return_value = Expense(item="Groceries", amount=50, category="Food")
            
            await add_spending(update, context)

            # Verify get_spending was called with the correct part of the message
            mock_get_spending.assert_called_once_with("Groceries, 50, Food")
            
            # Verify reply
            update.message.reply_text.assert_called_once_with("Spending added: Groceries, $50.00, Food")
            
            # Verify user_data
            self.assertIn('spendings', context.user_data)
            self.assertEqual(len(context.user_data['spendings']), 1)
            added_expense = context.user_data['spendings'][0]
            self.assertEqual(added_expense.item, "Groceries")
            self.assertEqual(added_expense.amount, 50)
            self.assertEqual(added_expense.category, "Food")

    async def test_add_spending_invalid_format(self):
        """Test add_spending when get_spending returns an error message."""
        update = MagicMock()
        update.message = AsyncMock()
        update.message.text = "/add Invalid data" # Content for get_spending
        
        context = MagicMock()
        context.user_data = {}

        with patch('bot.bot_logic.telgramBot.get_spending') as mock_get_spending:
            mock_get_spending.return_value = "Invalid format: Test error" # Simulate error from get_spending
            
            await add_spending(update, context)
            
            mock_get_spending.assert_called_once_with("Invalid data")
            update.message.reply_text.assert_called_once_with("Invalid format: Test error")
            self.assertNotIn('spendings', context.user_data) # No spending should be added

    async def test_add_spending_no_text_after_command(self):
        """Test add_spending when there's no text after /add command."""
        update = MagicMock()
        update.message = AsyncMock()
        update.message.text = "/add " # No actual expense data
        
        context = MagicMock()
        context.user_data = {}

        # We don't even need to mock get_spending here, as add_spending should handle this edge case.
        await add_spending(update, context)
        
        # Check that reply_text was called with the help message
        expected_message = "Please use the format: /add item, amount, category or /add item amount category"
        update.message.reply_text.assert_called_once_with(expected_message)
        self.assertNotIn('spendings', context.user_data)


    async def test_show_spending_no_expenses(self):
        """Test show_spending when there are no expenses."""
        update = MagicMock()
        update.message = AsyncMock()
        
        context = MagicMock()
        context.user_data = {} # No 'spendings' key or empty list

        await show_spending(update, context)
        update.message.reply_text.assert_called_once_with("No spendings added yet.")

    async def test_show_spending_with_expenses(self):
        """Test show_spending with multiple expenses."""
        update = MagicMock()
        update.message = AsyncMock()
        
        context = MagicMock()
        context.user_data = {
            'spendings': [
                Expense(item="Coffee", amount=3, category="Food"),
                Expense(item="Book", amount=20, category="Education"),
                Expense(item="Bus fare", amount=1, category="Transport")
            ]
        }

        expected_reply = "Your spendings:\n" \
                         "1. Coffee, $3.00, Food\n" \
                         "2. Book, $20.00, Education\n" \
                         "3. Bus fare, $1.00, Transport"
        
        await show_spending(update, context)
        update.message.reply_text.assert_called_once_with(expected_reply)

    async def test_show_spending_with_float_like_amount_formatting(self):
        """Test show_spending ensures amount is formatted like float (e.g., 50 -> $50.00)."""
        update = MagicMock()
        update.message = AsyncMock()
        
        context = MagicMock()
        context.user_data = {
            'spendings': [
                Expense(item="Lunch", amount=12, category="Food") 
            ]
        }
        # The amount is stored as int, but displayed with .00
        expected_reply = "Your spendings:\n1. Lunch, $12.00, Food"
        
        await show_spending(update, context)
        update.message.reply_text.assert_called_once_with(expected_reply)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    # Using exit=False for environments where exiting might close the test runner UI
    # For command line, unittest.main() is fine.

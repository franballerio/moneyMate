import pandas as pd

from datetime import date
from typing import Optional, Tuple
from .expense import Expense

def parse_date_args(args) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    """Parse command arguments into day, month, year."""
    today = date.today()
    if not args:
        return None, None, None

    # Convert all args to integers
    try:
        numbers = [int(arg) for arg in args]
    except ValueError:
        raise ValueError("All arguments must be numbers")

    if len(numbers) == 1:
        num = numbers[0]
        if 1 <= num <= 12:
            return None, num, date.today().year
        elif 2020 <= num <= date.today().year:
            return None, None, num
        else:
            raise ValueError(
                "Single argument must be month (1-12) or year (2020-2025)")

    elif len(numbers) == 2:
        month, year = numbers
        if 1 <= month <= 12 and 2020 <= year <= date.today().year:
            return None, month, year
        else:
            raise ValueError("Format: month (1-12) year (2023-2025)")

    elif len(numbers) == 3:
        day, month, year = numbers
        if 1 <= day <= 31 and 1 <= month <= 12 and 2020 <= year <= date.today().year:
            return day, month, year
        else:
            raise ValueError(
                "Format: day (1-31) month (1-12) year (2023-2025)")

    raise ValueError("Invalid number of arguments")
           
def check_budget(budget, spents, spent_amount) -> int:
    
    if budget == None:
        return 1

    if (budget > 0):
        if (budget - spents - spent_amount <= 0):
            return 0
        else:
            return budget

def get_spent(spent) -> Expense | int:
    '''Creates an expense object and checks if the expense format is correct'''
    if ("," in "".join(spent)):
        item = []
        for i in spent:
            if ("," not in i):
                item.append(i)
            else:
                item.append(i.replace(",", ""))
                spent = spent[spent.index(i)+1:]
                break
        spent.insert(0, " ".join(item))
    
    if len(spent) != 3:
        return 0

    try:
        int(spent[1])
    except ValueError:  # Check if amount is a number
        return 1

    return Expense(item=spent[0], amount=int(spent[1]), category=spent[2])

def format_df_itemized_to_monospaced_table(df, report_title_str):
    """
    Formats a Pandas DataFrame of expenses into a monospaced text table for Telegram,
    listing individual items.

    Args:
        df (pd.DataFrame): A DataFrame with at least columns ['item', 'amount', 'category'].
                           'amount' should be numeric. Other columns like 'date' are ignored for display
                           but should be used for filtering the df beforehand.
        report_title_str (str): The title string for the table (e.g., "Spent Today (YYYY-MM-DD)").

    Returns:
        str: A string formatted as a monospaced table listing individual items.
    """
    if df.empty:
        return f"\nNo items to display for the period: {report_title_str}\n"

    # --- 1. Prepare data for display ---
    # Ensure 'amount' is numeric
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
    
    # Select and prepare display columns
    display_df = df[['item', 'category', 'amount']].copy()
    display_df['amount_str'] = display_df['amount'].apply(lambda x: f"${x:.2f}")

    total_overall_amount = display_df['amount'].sum()

    # --- 2. Define headers ---
    header = {"item": "Item", "category": "Category", "amount": "Amount"}
    cols_order = ['item', 'category', 'amount'] # Define column order

    # --- 3. Calculate column widths ---
    col_widths = {col: len(header[col]) for col in cols_order}

    # Update widths based on data
    for _, row in display_df.iterrows():
        if len(str(row["item"])) > col_widths["item"]:
            col_widths["item"] = len(str(row["item"]))
        if len(str(row["category"])) > col_widths["category"]:
            col_widths["category"] = len(str(row["category"]))
        if len(row["amount_str"]) > col_widths["amount"]:
            col_widths["amount"] = len(row["amount_str"])
            
    # Consider the "Total:" label width for the combined width of item and category columns
    # For the total line, "Total:" will span the first N-1 columns conceptually.
    # Here, we'll have "Total:" in the item column, and blank in category.
    total_label = "Total:"
    if len(total_label) > col_widths["item"]: # Ensure 'item' col can hold "Total:"
        col_widths["item"] = len(total_label)
    
    # Ensure amount column can hold the formatted total amount
    formatted_total_overall_amount_str = f"${total_overall_amount:.2f}"
    if len(formatted_total_overall_amount_str) > col_widths["amount"]:
        col_widths["amount"] = len(formatted_total_overall_amount_str)

    # --- 4. Build the table string ---
    table_string_lines = []

    # Title
    table_string_lines.append(report_title_str)
    # Separator length calculation: sum of col_widths + (num_cols - 1) * " | " (3 chars each)
    separator_len = sum(col_widths.values()) + (len(cols_order) - 1) * 3
    table_string_lines.append("-" * separator_len)

    # Header row
    header_parts = [header[col].ljust(col_widths[col]) for col in cols_order]
    # Right-justify the 'Amount' header
    header_parts[-1] = header['amount'].rjust(col_widths['amount'])
    table_string_lines.append(" | ".join(header_parts))


    # Separator line
    table_string_lines.append("-" * separator_len)

    # Data rows
    for _, row in display_df.iterrows():
        item_str = str(row["item"]).ljust(col_widths["item"])
        category_str = str(row["category"]).ljust(col_widths["category"])
        amount_str_val = row["amount_str"].rjust(col_widths["amount"])
        
        table_string_lines.append(f"{item_str} | {category_str} | {amount_str_val}")

    # Separator line before total
    table_string_lines.append("-" * separator_len)

    # Total row
    # "Total:" spans the first column, other descriptive columns are blank
    total_label_padded = total_label.ljust(col_widths["item"])
    blank_category_padding = " ".ljust(col_widths["category"]) # For alignment
    
    total_row_str = (f"{total_label_padded} | "
                     f"{blank_category_padding} | "
                     f"{formatted_total_overall_amount_str.rjust(col_widths['amount'])}")
    table_string_lines.append(total_row_str)

    # --- 5. Join lines and wrap in monospace formatting ---
    return "\n" + "\n".join(table_string_lines) + "\n"

def format_df_aggregated_to_monospaced_table(df, report_title_str):
    """
    Formats a Pandas DataFrame of expenses into a monospaced text table for Telegram,
    aggregating expenses by category. (Simplified version of previous answer for context)
    """
    if df.empty:
        return f"\nNo expenses recorded for the period: {report_title_str}\n"
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
    aggregated_expenses = df.groupby('category')['amount'].sum().reset_index()
    total_overall_amount = df['amount'].sum()

    table_data_rows = [{"category": row["category"], "amount_val": row["amount"]} for _, row in aggregated_expenses.iterrows()]
    header = {"category": "Category", "amount": "Amount"}
    col_widths = {"category": len(header["category"]), "amount": len(header["amount"])}

    for data_row_dict in table_data_rows:
        category_str = str(data_row_dict["category"])
        amount_str = f"${data_row_dict['amount_val']:.2f}"
        if len(category_str) > col_widths["category"]: col_widths["category"] = len(category_str)
        if len(amount_str) > col_widths["amount"]: col_widths["amount"] = len(amount_str)
    total_label = "Total:"
    if len(total_label) > col_widths["category"]: col_widths["category"] = len(total_label)
    formatted_total_overall_amount_str = f"${total_overall_amount:.2f}"
    if len(formatted_total_overall_amount_str) > col_widths["amount"]: col_widths["amount"] = len(formatted_total_overall_amount_str)

    table_string_lines = [report_title_str]
    separator_len = col_widths["category"] + col_widths["amount"] + 3
    table_string_lines.append("-" * separator_len)
    table_string_lines.append(f"{header['category'].ljust(col_widths['category'])} | {header['amount'].rjust(col_widths['amount'])}")
    table_string_lines.append("-" * separator_len)
    for data_row_dict in table_data_rows:
        category_str = str(data_row_dict["category"])
        amount_str = f"${data_row_dict['amount_val']:.2f}"
        table_string_lines.append(f"{category_str.ljust(col_widths['category'])} | {amount_str.rjust(col_widths['amount'])}")
    table_string_lines.append("-" * separator_len)
    table_string_lines.append(f"{total_label.ljust(col_widths['category'])} | {formatted_total_overall_amount_str.rjust(col_widths['amount'])}")
    return "\n" + "\n".join(table_string_lines) + "\n"


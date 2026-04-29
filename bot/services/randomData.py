import pandas as pd
import numpy as np

def random_spents():
        # Parameters for generating random data
        categories = ["groceries", "so", "essentials",
                      "clothes", "entertainment", "transport", "going out"]
        start_date = "2023-01-01"
        end_date = "2025-12-31"
        num_records = 1000

        # Generate random data
        np.random.seed(42)  # For reproducibility
        random_dates = pd.to_datetime(np.random.choice(
            pd.date_range(start_date, end_date), size=num_records))
        random_categories = np.random.choice(categories, size=num_records)
        random_amounts = np.random.randint(100, 80001, size=num_records)
        ids = list(range(1000))

        # Create DataFrame
        df = pd.DataFrame({
            "id": ids,
            "item": "Product",
            "amount": random_amounts,
            "category": random_categories,
            "date": random_dates,
        })

        # Sorting by date for better usability
        df = df.sort_values(by="date").reset_index(drop=True)
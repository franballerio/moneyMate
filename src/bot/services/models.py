from dataclasses import dataclass

@dataclass
class Expense:
    item: str
    category: str
    amount: int


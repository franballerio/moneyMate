from dataclasses import dataclass

@dataclass
class Expense:
    item: str
    amount: int
    category: str


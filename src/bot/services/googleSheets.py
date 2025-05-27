import gspread

from .expense import Expense
from datetime import date
from dataclasses import dataclass

@dataclass
class WorkSheet():
    __gc = gspread.service_account("/home/franb/projects/moneyMate/.config/gspread/service_account.json")
    __workSheet = __gc.open("All time spendings")
    __size = 0
    
    def sheet_add(self, expense: Expense):
        spent = [date.today().strftime("%d/%m/%Y %H:%M"), expense.item, expense.amount, expense.category]
        
        self.__workSheet.get_worksheet(0).append_row(spent)
        self.__size =+ 1
        return
    
    def sheet_del(self):        
        self.__workSheet.get_worksheet(0).delete_rows(self.__size)
        return
    
    def sheet_clear(self):
        self.__workSheet.get_worksheet(0).clear()
        return
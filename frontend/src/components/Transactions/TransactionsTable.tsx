import React, { useState } from 'react';
import type { Expense } from '../../services/api';

interface TransactionsTableProps {
  expenses: Expense[];
  loading: boolean;
  total: number;
  onPageChange: (page: number) => void;
  currentPage: number;
  limit: number;
}

const TransactionsTable: React.FC<TransactionsTableProps> = ({
  expenses,
  loading,
  total,
  onPageChange,
  currentPage,
  limit,
}) => {
  const [sortBy, setSortBy] = useState<'date' | 'amount'>('date');
  const [filterCategory, setFilterCategory] = useState('');

  const sortedExpenses = [...expenses].sort((a, b) => {
    if (sortBy === 'date') {
      return new Date(b.date).getTime() - new Date(a.date).getTime();
    } else {
      return b.amount - a.amount;
    }
  });

  const filteredExpenses = filterCategory
    ? sortedExpenses.filter((e) => e.category.toLowerCase() === filterCategory.toLowerCase())
    : sortedExpenses;

  const totalPages = Math.ceil(total / limit);

  const categories = Array.from(new Set(expenses.map((e) => e.category)));

  return (
    <div className="bg-white rounded-lg shadow-sm">
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center justify-between gap-4">
          <h2 className="text-lg font-semibold text-gray-800">Recent Transactions</h2>
          <div className="flex gap-2">
            <select
              value={filterCategory}
              onChange={(e) => setFilterCategory(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
            >
              <option value="">All Categories</option>
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as 'date' | 'amount')}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
            >
              <option value="date">Sort by Date</option>
              <option value="amount">Sort by Amount</option>
            </select>
          </div>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50">
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Item</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Category</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Amount</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Date</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Source</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Action</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={6} className="px-6 py-4 text-center text-gray-500">
                  Loading...
                </td>
              </tr>
            ) : filteredExpenses.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-6 py-4 text-center text-gray-500">
                  No transactions found
                </td>
              </tr>
            ) : (
              filteredExpenses.map((expense) => (
                <tr key={expense.id} className="border-b border-gray-200 hover:bg-gray-50 transition">
                  <td className="px-6 py-4 text-sm text-gray-800 font-medium">{expense.item}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {expense.category}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm font-semibold text-gray-800">${expense.amount.toFixed(2)}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{new Date(expense.date).toLocaleDateString()}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {expense.created_by === 'bot' ? '🤖 Bot' : '💻 Web'}
                  </td>
                  <td className="px-6 py-4 text-sm">
                    <button className="text-red-500 hover:text-red-700 font-medium">Delete</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
        <p className="text-sm text-gray-600">
          Showing <span className="font-semibold">{filteredExpenses.length}</span> of{' '}
          <span className="font-semibold">{total}</span> transactions
        </p>
        <div className="flex gap-2">
          <button
            disabled={currentPage === 1}
            onClick={() => onPageChange(currentPage - 1)}
            className="px-3 py-1 text-sm font-medium text-gray-700 bg-gray-100 rounded hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            Previous
          </button>
          <div className="flex items-center gap-1">
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
              <button
                key={page}
                onClick={() => onPageChange(page)}
                className={`px-3 py-1 text-sm font-medium rounded transition ${
                  currentPage === page
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-700 bg-gray-100 hover:bg-gray-200'
                }`}
              >
                {page}
              </button>
            ))}
          </div>
          <button
            disabled={currentPage === totalPages}
            onClick={() => onPageChange(currentPage + 1)}
            className="px-3 py-1 text-sm font-medium text-gray-700 bg-gray-100 rounded hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};

export default TransactionsTable;

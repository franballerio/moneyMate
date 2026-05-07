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

const Categories: React.FC<{ category: string }> = ({ category }) => (
  <span className="inline-flex items-center px-2.5 py-1 rounded-pill text-[11px] font-medium tracking-wide uppercase bg-surface-black/5 text-ink-muted-80 border border-hairline/50">
    {category}
  </span>
);

const SortIcon: React.FC = () => (
  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="opacity-40">
    <path d="M11 5h10M11 9h7M11 13h4" />
  </svg>
);

const BotIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="11" width="18" height="10" rx="2" />
    <circle cx="12" cy="5" r="2" />
    <path d="M12 7v4" />
    <line x1="8" y1="16" x2="8" y2="16" />
    <line x1="16" y1="16" x2="16" y2="16" />
  </svg>
);

const WebIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10" />
    <line x1="2" y1="12" x2="22" y2="12" />
    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
  </svg>
);

const TrashIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="3 6 5 6 21 6" />
    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
  </svg>
);

const ChevronLeft: React.FC = () => (
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="15 18 9 12 15 6" />
  </svg>
);

const ChevronRight: React.FC = () => (
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="9 18 15 12 9 6" />
  </svg>
);

const PlusIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <line x1="12" y1="5" x2="12" y2="19" />
    <line x1="5" y1="12" x2="19" y2="12" />
  </svg>
);

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

  const totalPages = Math.ceil(total / limit) || 1;
  const categories = Array.from(new Set(expenses.map((e) => e.category)));

  return (
    <div className="bg-canvas border border-hairline rounded-[18px] overflow-hidden">
      <div className="px-6 py-4 border-b border-hairline flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <h2 className="text-body-strong text-ink">Recent Transactions</h2>
        <div className="flex flex-wrap gap-3">
          <select
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="h-8 px-3 rounded-pill bg-surface-pearl border border-hairline text-caption text-ink focus:outline-none focus:ring-2 focus:ring-primary/20 appearance-none pr-8"
            style={{ backgroundImage: 'url("data:image/svg+xml,%3Csvg width=\'10\' height=\'6\' viewBox=\'0 0 10 6\' fill=\'none\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cpath d=\'M1 1L5 5L9 1\' stroke=\'%237a7a7a\' stroke-width=\'1.5\' stroke-linecap=\'round\' stroke-linejoin=\'round\'/%3E%3C/svg%3E")', backgroundRepeat: 'no-repeat', backgroundPosition: 'right 12px center' }}
          >
            <option value="">All Categories</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
          <div className="flex gap-2">
            <button
              onClick={() => setSortBy('date')}
              className={`h-8 px-3 rounded-pill text-caption transition-colors flex items-center gap-1.5 ${
                sortBy === 'date' ? 'bg-primary/10 text-primary' : 'bg-surface-pearl border border-hairline text-ink-muted-80 hover:text-ink'
              }`}
            >
              <SortIcon />
              Date
            </button>
            <button
              onClick={() => setSortBy('amount')}
              className={`h-8 px-3 rounded-pill text-caption transition-colors flex items-center gap-1.5 ${
                sortBy === 'amount' ? 'bg-primary/10 text-primary' : 'bg-surface-pearl border border-hairline text-ink-muted-80 hover:text-ink'
              }`}
            >
              <SortIcon />
              Amount
            </button>
          </div>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-hairline">
              <th className="px-6 py-3 text-caption font-semibold text-ink-muted-48">Item</th>
              <th className="px-6 py-3 text-caption font-semibold text-ink-muted-48">Category</th>
              <th className="px-6 py-3 text-caption font-semibold text-ink-muted-48">Amount</th>
              <th className="px-6 py-3 text-caption font-semibold text-ink-muted-48">Date</th>
              <th className="px-6 py-3 text-caption font-semibold text-ink-muted-48">Source</th>
              <th className="px-6 py-3 text-caption font-semibold text-ink-muted-48">Action</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={6} className="px-6 py-12 text-center text-caption text-ink-muted-48">
                  Loading transactions...
                </td>
              </tr>
            ) : filteredExpenses.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-6 py-16 text-center">
                  <div className="flex flex-col items-center gap-2">
                    <div className="w-10 h-10 rounded-full bg-surface-pearl flex items-center justify-center text-ink-muted-48">
                      <PlusIcon />
                    </div>
                    <p className="text-caption text-ink-muted-48">No transactions found</p>
                  </div>
                </td>
              </tr>
            ) : (
              filteredExpenses.map((expense) => (
                <tr key={expense.id} className="border-b border-hairline last:border-none hover:bg-surface-pearl/30 transition-colors duration-150">
                  <td className="px-6 py-4 text-body text-ink">{expense.item}</td>
                  <td className="px-6 py-4">
                    <Categories category={expense.category} />
                  </td>
                  <td className="px-6 py-4 text-body-strong text-ink">
                    ${Number(expense.amount || 0).toFixed(2)}
                  </td>
                  <td className="px-6 py-4 text-caption text-ink-muted-80">
                    {new Date(expense.date).toLocaleDateString('en-US', {
                      month: 'short',
                      day: 'numeric',
                      year: 'numeric',
                    })}
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center gap-1.5 text-caption text-ink-muted-80">
                      {expense.created_by === 'bot' ? (
                        <><BotIcon /> Bot</>
                      ) : (
                        <><WebIcon /> Web</>
                      )}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <button className="text-caption text-ink-muted-48 hover:text-red-500 transition-colors focus:outline-none flex items-center gap-1.5">
                      <TrashIcon />
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="px-6 py-4 border-t border-hairline flex flex-col sm:flex-row items-center justify-between gap-4">
        <p className="text-caption text-ink-muted-48">
          Showing <span className="text-ink font-medium">{filteredExpenses.length}</span> of{' '}
          <span className="text-ink font-medium">{total}</span> transactions
        </p>
        <div className="flex gap-2">
          <button
            disabled={currentPage === 1}
            onClick={() => onPageChange(currentPage - 1)}
            className="h-8 px-3 text-caption font-medium rounded-pill border border-hairline bg-canvas hover:bg-surface-pearl disabled:opacity-40 disabled:cursor-not-allowed transition-colors text-ink flex items-center gap-1"
          >
            <ChevronLeft />
            Previous
          </button>

          <div className="hidden sm:flex items-center gap-1">
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
              <button
                key={page}
                onClick={() => onPageChange(page)}
                className={`w-8 h-8 flex items-center justify-center text-caption font-medium rounded-full transition-colors ${
                  currentPage === page
                    ? 'bg-ink text-canvas'
                    : 'text-ink hover:bg-surface-pearl'
                }`}
              >
                {page}
              </button>
            ))}
          </div>

          <button
            disabled={currentPage === totalPages}
            onClick={() => onPageChange(currentPage + 1)}
            className="h-8 px-3 text-caption font-medium rounded-pill border border-hairline bg-canvas hover:bg-surface-pearl disabled:opacity-40 disabled:cursor-not-allowed transition-colors text-ink flex items-center gap-1"
          >
            Next
            <ChevronRight />
          </button>
        </div>
      </div>
    </div>
  );
};

export default TransactionsTable;

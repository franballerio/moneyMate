import React from 'react';
import type { Budget } from '../../services/api';

interface BudgetProgressProps {
  budgets: Budget[];
  loading: boolean;
}

const BudgetProgress: React.FC<BudgetProgressProps> = ({ budgets, loading }) => {
  if (loading) {
    return <div className="text-center text-gray-500">Loading budgets...</div>;
  }

  if (budgets.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8">
        No budgets set. Create one to get started!
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {budgets.map((budget) => {
        const percentage = (budget.spent / budget.limit_amount) * 100;
        const isOverBudget = percentage > 100;

        return (
          <div key={budget.id} className="bg-white p-4 rounded-lg shadow-sm hover:shadow-md transition">
            <div className="flex items-center justify-between mb-2">
              <div>
                <p className="font-semibold text-gray-800 capitalize">{budget.category}</p>
                <p className="text-xs text-gray-500">{budget.period}</p>
              </div>
              <p className={`text-sm font-bold ${isOverBudget ? 'text-red-600' : 'text-green-600'}`}>
                ${budget.spent.toFixed(2)} / ${budget.limit_amount.toFixed(2)}
              </p>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`h-2 rounded-full transition ${
                  isOverBudget ? 'bg-red-500' : percentage > 75 ? 'bg-orange-500' : 'bg-green-500'
                }`}
                style={{ width: `${Math.min(percentage, 100)}%` }}
              ></div>
            </div>
            {isOverBudget && (
              <p className="text-xs text-red-600 mt-2">⚠️ Over budget by ${(budget.spent - budget.limit_amount).toFixed(2)}</p>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default BudgetProgress;

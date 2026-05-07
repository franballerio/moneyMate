import React from 'react';
import type { Budget } from '../../services/api';

interface BudgetProgressProps {
  budgets: Budget[];
  loading: boolean;
}

const BudgetProgress: React.FC<BudgetProgressProps> = ({ budgets, loading }) => {
  if (loading) {
    return (
      <div className="bg-canvas border border-hairline rounded-[18px] p-[24px] flex items-center justify-center min-h-[200px]">
        <p className="text-caption text-ink-muted-48">Loading budgets...</p>
      </div>
    );
  }

  if (budgets.length === 0) {
    return (
      <div className="bg-canvas border border-hairline rounded-[18px] p-[24px] flex flex-col items-center justify-center text-center min-h-[200px] gap-3">
        <div className="w-10 h-10 rounded-full bg-surface-pearl flex items-center justify-center text-ink-muted-48">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <rect x="2" y="4" width="20" height="16" rx="2" />
            <line x1="2" y1="10" x2="22" y2="10" />
          </svg>
        </div>
        <p className="text-caption text-ink-muted-48">No budgets set. Create one to get started.</p>
      </div>
    );
  }

  return (
    <div className="bg-canvas border border-hairline rounded-[18px] p-[24px]">
      <h3 className="text-body-strong text-ink mb-5">Budget Status</h3>
      <div className="space-y-5">
        {budgets.map((budget) => {
          const spent = budget.spent ?? 0;
          const percentage = (spent / budget.limit_amount) * 100;
          const isOverBudget = percentage > 100;

          return (
            <div key={budget.id}>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className="text-body text-ink capitalize">{budget.category}</span>
                  <span className="text-fine-print text-ink-muted-48">{budget.period}</span>
                </div>
                <div className="text-right">
                  <span className={`text-body-strong ${isOverBudget ? 'text-red-500' : 'text-ink'}`}>
                    ${Number(spent).toFixed(2)}
                  </span>
                  <span className="text-fine-print text-ink-muted-48 ml-1">
                    / ${Number(budget.limit_amount || 0).toFixed(2)}
                  </span>
                </div>
              </div>

              <div className="w-full bg-surface-pearl border border-divider-soft rounded-pill h-[6px] overflow-hidden">
                <div
                  className={`h-full rounded-pill transition-all duration-700 ease-out ${
                    isOverBudget ? 'bg-red-500' : percentage > 80 ? 'bg-orange-500' : 'bg-primary'
                  }`}
                  style={{ width: `${Math.min(percentage, 100)}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default BudgetProgress;

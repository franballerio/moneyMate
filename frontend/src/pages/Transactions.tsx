import React, { useState } from 'react';
import Layout from '../components/Layout';
import TransactionsTable from '../components/Transactions/TransactionsTable';
import { useExpenses } from '../services/api';

const Transactions: React.FC = () => {
  const [page, setPage] = useState(1);
  const limit = 20;
  const { expenses, loading, total } = useExpenses(page, limit);

  return (
    <Layout>
      <div className="flex flex-col gap-[32px]">
        <header className="flex flex-col sm:flex-row sm:items-end justify-between gap-6">
          <div>
            <h1 className="text-hero-display text-ink tracking-tight mb-2">Transactions</h1>
            <p className="text-body text-ink-muted-80 max-w-[600px]">
              View and manage all your expenses in one place.
            </p>
          </div>

          <button className="btn-primary h-[44px] flex items-center gap-2">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
            Add Expense
          </button>
        </header>

        <section>
          <TransactionsTable
            expenses={expenses}
            loading={loading}
            total={total}
            onPageChange={setPage}
            currentPage={page}
            limit={limit}
          />
        </section>
      </div>
    </Layout>
  );
};

export default Transactions;

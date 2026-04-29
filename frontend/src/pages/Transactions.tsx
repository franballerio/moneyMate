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
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">Transactions</h1>
            <p className="text-gray-600 mt-1">View and manage all your expenses</p>
          </div>
          <button className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium">
            ➕ Add Expense
          </button>
        </div>

        <TransactionsTable
          expenses={expenses}
          loading={loading}
          total={total}
          onPageChange={setPage}
          currentPage={page}
          limit={limit}
        />
      </div>
    </Layout>
  );
};

export default Transactions;

import React from 'react';
import Layout from '../components/Layout';

const Budgets: React.FC = () => {
  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">Budgets</h1>
            <p className="text-gray-600 mt-1">Set and manage your spending limits</p>
          </div>
          <button className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium">
            ➕ Create Budget
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-8 text-center">
          <p className="text-gray-500 text-lg">Budget management coming soon...</p>
        </div>
      </div>
    </Layout>
  );
};

export default Budgets;

import React from 'react';
import Layout from '../components/Layout';

const Analytics: React.FC = () => {
  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Analytics</h1>
          <p className="text-gray-600 mt-1">Detailed spending insights and reports</p>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-8 text-center">
          <p className="text-gray-500 text-lg">Advanced analytics coming soon...</p>
        </div>
      </div>
    </Layout>
  );
};

export default Analytics;

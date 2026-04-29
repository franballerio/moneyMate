import React from 'react';
import Layout from '../components/Layout';
import MetricCard from '../components/Dashboard/MetricCard';
import BudgetProgress from '../components/Dashboard/BudgetProgress';
import TrendChart from '../components/Charts/TrendChart';
import CategoryChart from '../components/Charts/CategoryChart';
import {
  useMetricsSummary,
  useCategoryMetrics,
  useTrends,
  useBudgets,
} from '../services/api';

const Dashboard: React.FC = () => {
  const { metrics, loading: metricsLoading } = useMetricsSummary();
  const { categories, loading: categoriesLoading } = useCategoryMetrics();
  const { trends, loading: trendsLoading } = useTrends();
  const { budgets, loading: budgetsLoading } = useBudgets();

  return (
    <Layout>
      <div className="space-y-6">
        {/* Metrics Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <MetricCard
            title="Today's Spending"
            value={metrics ? `$${metrics.daily.toFixed(2)}` : '$0.00'}
            icon="📅"
            color="blue"
            trend={metricsLoading ? 'Loading...' : 'Last 24 hours'}
          />
          <MetricCard
            title="This Month"
            value={metrics ? `$${metrics.monthly.toFixed(2)}` : '$0.00'}
            icon="📊"
            color="green"
            trend={metricsLoading ? 'Loading...' : 'Month to date'}
          />
          <MetricCard
            title="All Time"
            value={metrics ? `$${metrics.all_time.toFixed(2)}` : '$0.00'}
            icon="💰"
            color="orange"
            trend={metricsLoading ? 'Loading...' : 'Total spending'}
          />
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <TrendChart data={trends} loading={trendsLoading} />
          <CategoryChart data={categories} loading={categoriesLoading} />
        </div>

        {/* Budget Progress */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-lg font-semibold mb-4 text-gray-800">Budget Status</h2>
          <BudgetProgress budgets={budgets} loading={budgetsLoading} />
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;

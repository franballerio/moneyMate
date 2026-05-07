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

const CalendarIcon: React.FC = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
    <line x1="16" y1="2" x2="16" y2="6" />
    <line x1="8" y1="2" x2="8" y2="6" />
    <line x1="3" y1="10" x2="21" y2="10" />
  </svg>
);

const TrendingUpIcon: React.FC = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
    <polyline points="17 6 23 6 23 12" />
  </svg>
);

const DollarIcon: React.FC = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
    <line x1="12" y1="1" x2="12" y2="23" />
    <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
  </svg>
);

const Dashboard: React.FC = () => {
  const { metrics, loading: metricsLoading } = useMetricsSummary();
  const { categories, loading: categoriesLoading } = useCategoryMetrics();
  const { trends, loading: trendsLoading } = useTrends();
  const { budgets, loading: budgetsLoading } = useBudgets();

  return (
    <Layout>
      <div className="flex flex-col gap-[32px]">
        <header className="mb-2">
          <h1 className="text-hero-display text-ink tracking-tight mb-2">Overview</h1>
          <p className="text-body text-ink-muted-80 max-w-[600px]">
            Here's a snapshot of your recent spending. Keep track of where your money goes
            and stay on top of your financial goals.
          </p>
        </header>

        <section className="grid grid-cols-1 md:grid-cols-3 gap-[24px]">
          <MetricCard
            title="Today's Spending"
            value={metrics ? `$${Number(metrics.daily || 0).toFixed(2)}` : '$0.00'}
            icon={<CalendarIcon />}
            trend={metricsLoading ? 'Loading...' : 'Last 24 hours'}
          />
          <MetricCard
            title="This Month"
            value={metrics ? `$${Number(metrics.monthly || 0).toFixed(2)}` : '$0.00'}
            icon={<TrendingUpIcon />}
            trend={metricsLoading ? 'Loading...' : 'Month to date'}
          />
          <MetricCard
            title="All Time"
            value={metrics ? `$${Number(metrics.all_time || 0).toFixed(2)}` : '$0.00'}
            icon={<DollarIcon />}
            trend={metricsLoading ? 'Loading...' : 'Total spending'}
          />
        </section>

        <section className="grid grid-cols-1 lg:grid-cols-[1.5fr_1fr] gap-[24px]">
          <TrendChart data={trends} loading={trendsLoading} />

          <div className="flex flex-col gap-[24px]">
            <CategoryChart data={categories} loading={categoriesLoading} />
            <BudgetProgress budgets={budgets} loading={budgetsLoading} />
          </div>
        </section>
      </div>
    </Layout>
  );
};

export default Dashboard;

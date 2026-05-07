import React from 'react';
import Layout from '../components/Layout';

const Analytics: React.FC = () => {
  return (
    <Layout>
      <div className="flex flex-col gap-[32px]">
        <header className="flex flex-col sm:flex-row sm:items-end justify-between gap-6">
          <div>
            <h1 className="text-hero-display text-ink tracking-tight mb-2">Analytics</h1>
            <p className="text-body text-ink-muted-80 max-w-[600px]">
              Detailed spending insights, reports, and financial projections.
            </p>
          </div>
        </header>

        <section className="bg-canvas border border-hairline rounded-[18px] p-[64px] flex flex-col items-center justify-center text-center gap-5 min-h-[400px]">
          <div className="w-16 h-16 rounded-full bg-surface-pearl flex items-center justify-center text-ink-muted-48">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21.21 15.89A10 10 0 1 1 8 2.83" />
              <path d="M22 12A10 10 0 0 0 12 2v10z" />
            </svg>
          </div>
          <div>
            <h2 className="text-display-md text-ink mb-2">Advanced analytics coming soon</h2>
            <p className="text-body text-ink-muted-80 max-w-[400px]">
              Dive deeper into your data with customized reports, trends over time, and predictive insights. Check back soon.
            </p>
          </div>
        </section>
      </div>
    </Layout>
  );
};

export default Analytics;

import React from 'react';
import Layout from '../components/Layout';

const Budgets: React.FC = () => {
  return (
    <Layout>
      <div className="flex flex-col gap-[32px]">
        <header className="flex flex-col sm:flex-row sm:items-end justify-between gap-6">
          <div>
            <h1 className="text-hero-display text-ink tracking-tight mb-2">Budgets</h1>
            <p className="text-body text-ink-muted-80 max-w-[600px]">
              Set and manage your spending limits for different categories.
            </p>
          </div>

          <button className="h-[44px] px-[24px] bg-primary text-on-primary rounded-pill text-[15px] font-semibold tracking-[-0.016em] hover:scale-[0.98] active:scale-[0.95] transition-transform duration-200 self-start sm:self-auto flex items-center gap-2">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
            Create Budget
          </button>
        </header>

        <section className="bg-canvas border border-hairline rounded-[18px] p-[64px] flex flex-col items-center justify-center text-center gap-5 min-h-[400px]">
          <div className="w-16 h-16 rounded-full bg-surface-pearl flex items-center justify-center text-ink-muted-48">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <rect x="2" y="4" width="20" height="16" rx="2" />
              <line x1="2" y1="10" x2="22" y2="10" />
            </svg>
          </div>
          <div>
            <h2 className="text-display-md text-ink mb-2">Budget management coming soon</h2>
            <p className="text-body text-ink-muted-80 max-w-[400px]">
              We're building powerful new tools to help you track spending limits across all your categories. Check back soon.
            </p>
          </div>
        </section>
      </div>
    </Layout>
  );
};

export default Budgets;

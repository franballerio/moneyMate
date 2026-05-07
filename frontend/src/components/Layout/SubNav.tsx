import React from 'react';
import { useLocation, Link } from 'react-router-dom';

const pageMeta: Record<string, { title: string; subtitle: string }> = {
  '/': { title: 'Dashboard', subtitle: 'Overview' },
  '/transactions': { title: 'Transactions', subtitle: 'All expenses' },
  '/budgets': { title: 'Budgets', subtitle: 'Spending limits' },
  '/analytics': { title: 'Analytics', subtitle: 'Insights & reports' },
  '/settings': { title: 'Settings', subtitle: 'Preferences' },
};

const SubNav: React.FC = () => {
  const location = useLocation();
  const meta = pageMeta[location.pathname] || pageMeta['/'];

  return (
    <div className="sticky top-[44px] z-40 w-full h-[52px] bg-canvas-parchment/80 backdrop-blur-[20px] backdrop-saturate-[180%] border-b border-hairline">
      <div className="flex items-center justify-between h-full px-5 max-w-[980px] mx-auto">
        <div className="flex items-center gap-3">
          <h2 className="text-tagline text-ink">{meta.title}</h2>
          <span className="hidden sm:inline text-caption text-ink-muted-48 mt-0.5">— {meta.subtitle}</span>
        </div>

        <div className="flex items-center gap-4">
          {location.pathname !== '/transactions' && (
            <Link to="/transactions" className="hidden md:block text-button-utility text-ink-muted-48 hover:text-primary transition-colors">
              View All
            </Link>
          )}
          <button className="bg-primary text-on-primary rounded-pill px-[18px] h-[32px] text-[13px] font-text font-medium tracking-[-0.01em] hover:scale-95 active:scale-95 transition-transform duration-200 flex items-center gap-1.5">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
            Add Expense
          </button>
        </div>
      </div>
    </div>
  );
};

export default SubNav;

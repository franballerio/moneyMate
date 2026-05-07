import React from 'react';
import Layout from '../components/Layout';

const Settings: React.FC = () => {
  return (
    <Layout>
      <div className="flex flex-col gap-[32px]">
        <header className="flex flex-col sm:flex-row sm:items-end justify-between gap-6">
          <div>
            <h1 className="text-hero-display text-ink tracking-tight mb-2">Settings</h1>
            <p className="text-body text-ink-muted-80 max-w-[600px]">
              Manage your account preferences, integrations, and application settings.
            </p>
          </div>
        </header>

        <section className="bg-canvas border border-hairline rounded-[18px] p-[64px] flex flex-col items-center justify-center text-center gap-5 min-h-[400px]">
          <div className="w-16 h-16 rounded-full bg-surface-pearl flex items-center justify-center text-ink-muted-48">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="3" />
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
            </svg>
          </div>
          <div>
            <h2 className="text-display-md text-ink mb-2">Settings management coming soon</h2>
            <p className="text-body text-ink-muted-80 max-w-[400px]">
              We are working on bringing you fine-grained control over your MoneyMate experience, including Telegram integration and notifications.
            </p>
          </div>
        </section>
      </div>
    </Layout>
  );
};

export default Settings;

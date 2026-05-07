import React from 'react';
import { Link } from 'react-router-dom';

const linkSections = [
  {
    heading: 'Product',
    links: [
      { to: '/', label: 'Dashboard' },
      { to: '/transactions', label: 'Transactions' },
      { to: '/budgets', label: 'Budgets' },
      { to: '/analytics', label: 'Analytics' },
    ],
  },
  {
    heading: 'Support',
    links: [
      { to: '/settings', label: 'Settings' },
      { to: '#', label: 'Contact' },
      { to: '#', label: 'FAQ' },
      { to: '#', label: 'Privacy' },
    ],
  },
  {
    heading: 'Company',
    links: [
      { to: '#', label: 'About' },
      { to: '#', label: 'Blog' },
      { to: '#', label: 'Press' },
      { to: '#', label: 'Careers' },
    ],
  },
  {
    heading: 'Legal',
    links: [
      { to: '#', label: 'Terms of Use' },
      { to: '#', label: 'Privacy Policy' },
      { to: '#', label: 'Cookie Policy' },
      { to: '#', label: 'Trademarks' },
    ],
  },
];

const Footer: React.FC = () => {
  return (
    <footer className="bg-canvas-parchment border-t border-hairline mt-xxl">
      <div className="max-w-[980px] mx-auto px-5 py-[64px]">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {linkSections.map((section) => (
            <div key={section.heading}>
              <h4 className="text-caption-strong text-ink mb-4">{section.heading}</h4>
              <ul className="space-y-1.5">
                {section.links.map((link) => (
                  <li key={link.label}>
                    <Link
                      to={link.to}
                      className="text-dense-link text-ink-muted-80 hover:text-primary transition-colors"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-12 pt-6 border-t border-hairline flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-fine-print text-ink-muted-48">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 2L2 7l10 5 10-5-10-5z" />
              <path d="M2 17l10 5 10-5" />
              <path d="M2 12l10 5 10-5" />
            </svg>
            <span>MoneyMate</span>
          </div>
          <p className="text-fine-print text-ink-muted-48 text-center sm:text-left">
            Copyright &copy; {new Date().getFullYear()} MoneyMate. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

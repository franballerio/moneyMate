import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Sidebar: React.FC = () => {
  const location = useLocation();

  const navItems = [
    { label: 'Dashboard', path: '/', icon: '📊' },
    { label: 'Transactions', path: '/transactions', icon: '💳' },
    { label: 'Budgets', path: '/budgets', icon: '💰' },
    { label: 'Analytics', path: '/analytics', icon: '📈' },
    { label: 'Settings', path: '/settings', icon: '⚙️' },
  ];

  return (
    <aside className="w-64 bg-gradient-to-b from-blue-600 to-blue-800 text-white shadow-lg h-screen fixed left-0 top-0 overflow-y-auto">
      <div className="p-6">
        <div className="text-3xl font-bold">💸 MoneyMate</div>
        <p className="text-blue-100 text-sm mt-1">Smart Finance Manager</p>
      </div>

      <nav className="mt-8 px-4 space-y-2">
        {navItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`flex items-center gap-3 px-4 py-3 rounded-lg transition ${
              location.pathname === item.path
                ? 'bg-blue-500 font-semibold'
                : 'hover:bg-blue-700'
            }`}
          >
            <span className="text-xl">{item.icon}</span>
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>

      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-blue-700">
        <div className="bg-blue-900 rounded-lg p-3">
          <p className="text-xs text-blue-200">Logged in as</p>
          <p className="text-sm font-semibold truncate">user@example.com</p>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;

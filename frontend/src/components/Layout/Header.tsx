import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="fixed top-0 left-64 right-0 bg-white shadow-sm h-16 flex items-center justify-between px-8 z-10">
      <div className="flex-1">
        <h1 className="text-2xl font-bold text-gray-800">Personal Finance Dashboard</h1>
      </div>

      <div className="flex items-center gap-4">
        <button className="p-2 hover:bg-gray-100 rounded-full relative">
          <span className="text-xl">🔔</span>
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>

        <button className="p-2 hover:bg-gray-100 rounded-full">
          <span className="text-xl">👤</span>
        </button>

        <button className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition">
          Logout
        </button>
      </div>
    </header>
  );
};

export default Header;

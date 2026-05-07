import React from 'react';
import type { ReactNode } from 'react';
import Header from './Header';
import SubNav from './SubNav';
import Footer from './Footer';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-canvas-parchment flex flex-col text-ink font-text">
      <Header />
      <SubNav />
      <main className="flex-1 w-full mx-auto px-5 max-w-[980px] py-section">
        {children}
      </main>
      <Footer />
    </div>
  );
};

export default Layout;

import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Shield, FileText, Eye, Settings, Play } from 'lucide-react';

const Layout = ({ children }) => {
  const location = useLocation();

  const navigation = [
    { name: 'Dashboard', href: '/', icon: Shield },
    { name: 'Evaluate', href: '/evaluate', icon: FileText },
    { name: 'Audit Trail', href: '/audit', icon: Eye },
    { name: 'Policies', href: '/policies', icon: Settings },
    { name: 'Demo', href: '/demo', icon: Play },
  ];

  return (
    <div className="min-h-screen actum-main-bg">
      {/* Header */}
      <header className="actum-content-bg shadow-sm actum-border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-xl font-bold actum-text-primary">
                  <span className="hpe-text-brand">Actum</span> AI Compliance Engine
                </h1>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <nav className="w-64 actum-sidebar-bg shadow-sm min-h-screen">
          <div className="p-4">
            <nav className="space-y-2">
              {navigation.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors duration-200 ${
                      isActive
                        ? 'bg-gray-200 text-hpe-brand border-r-2 border-hpe-brand'
                        : 'actum-text-secondary hover:bg-hpe-bg-light-background-contrast hover:actum-text-primary'
                    }`}
                  >
                    <Icon className="mr-3 h-5 w-5" />
                    {item.name}
                  </Link>
                );
              })}
            </nav>
          </div>
        </nav>

        {/* Main content */}
        <main className="flex-1 p-8 actum-content-bg">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;

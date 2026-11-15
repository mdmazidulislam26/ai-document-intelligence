import React from 'react';
import Link from 'next/link';
import { Layers, Search, FileCheck } from 'lucide-react';

export const Navbar = () => {
  return (
    <header className="bg-slate-900 text-white border-b border-slate-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5 font-bold text-lg tracking-tight">
          <Layers className="w-6 h-6 text-indigo-400" />
          <span>DocIntel <span className="text-indigo-400 font-normal text-sm">System</span></span>
        </Link>
        <nav className="flex items-center gap-6 text-sm font-medium">
          <Link href="/" className="flex items-center gap-1.5 text-slate-300 hover:text-white transition">
            <FileCheck className="w-4 h-4" />
            <span>Dashboard</span>
          </Link>
          <Link href="/search" className="flex items-center gap-1.5 text-slate-300 hover:text-white transition">
            <Search className="w-4 h-4" />
            <span>Hybrid Search</span>
          </Link>
        </nav>
      </div>
    </header>
  );
};

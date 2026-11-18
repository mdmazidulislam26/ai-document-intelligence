'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Layers, Search, FileCheck, KeyRound } from 'lucide-react';
import { getStoredApiKey, setStoredApiKey } from '@/lib/api';

export const Navbar = () => {
  const [apiKeyInput, setApiKeyInput] = useState('');
  const [savedNotice, setSavedNotice] = useState(false);

  useEffect(() => {
    setApiKeyInput(getStoredApiKey());
  }, []);

  const handleKeySave = (e: React.FormEvent) => {
    e.preventDefault();
    setStoredApiKey(apiKeyInput);
    setSavedNotice(true);
    setTimeout(() => setSavedNotice(false), 2000);
  };

  return (
    <header className="bg-slate-900 text-white border-b border-slate-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between gap-4">
        <Link href="/" className="flex items-center gap-2.5 font-bold text-lg tracking-tight shrink-0">
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

          <form onSubmit={handleKeySave} className="hidden md:flex items-center gap-1.5 bg-slate-800 px-2.5 py-1 rounded-lg border border-slate-700">
            <KeyRound className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
            <input
              type="password"
              value={apiKeyInput}
              onChange={(e) => setApiKeyInput(e.target.value)}
              placeholder="API Key"
              aria-label="API Key"
              className="bg-transparent text-xs text-slate-200 placeholder-slate-500 outline-none w-36"
            />
            <button
              type="submit"
              className="text-[11px] font-semibold px-2 py-0.5 rounded bg-indigo-600 hover:bg-indigo-500 text-white"
            >
              {savedNotice ? 'Saved' : 'Set'}
            </button>
          </form>
        </nav>
      </div>
    </header>
  );
};

'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import axios from 'axios';
import { Search as SearchIcon, ArrowUpRight, Sparkles } from 'lucide-react';
import { StatusBadge } from '@/components/StatusBadge';

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [searchType, setSearchType] = useState('hybrid');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    const apiUrl = '';
    try {
      const res = await axios.get(`${apiUrl}/api/search`, {
        params: { q: query, type: searchType, limit: 15 },
      });
      setResults(res.data);
    } catch (err) {
      console.error('Search failed:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Hybrid Document Search</h1>
        <p className="text-sm text-slate-500 mt-1">
          Search invoices using keyword text matching or vector semantic embeddings.
        </p>
      </div>

      <form onSubmit={handleSearch} className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-4">
        <div className="flex gap-3">
          <div className="relative flex-1">
            <SearchIcon className="w-4 h-4 text-slate-400 absolute left-3 top-3.5" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by vendor, item, invoice number, or concept (e.g. 'Software license payment')..."
              className="w-full pl-9 pr-4 py-2.5 text-sm border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold rounded-lg shadow-sm transition"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>

        <div className="flex items-center gap-6 text-xs text-slate-600">
          <span className="font-semibold text-slate-700">Search Mode:</span>
          {['hybrid', 'semantic', 'keyword'].map((mode) => (
            <label key={mode} className="inline-flex items-center gap-1.5 cursor-pointer capitalize">
              <input
                type="radio"
                name="searchType"
                value={mode}
                checked={searchType === mode}
                onChange={() => setSearchType(mode)}
                className="text-indigo-600 focus:ring-indigo-500"
              />
              {mode}
            </label>
          ))}
        </div>
      </form>

      {/* Results List */}
      <div className="space-y-3">
        {results.map((item) => (
          <div
            key={item.document_id}
            className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between hover:border-indigo-300 transition"
          >
            <div>
              <div className="flex items-center gap-3">
                <h3 className="font-semibold text-slate-900 text-base">{item.supplier_name || 'Unknown Supplier'}</h3>
                <StatusBadge status={item.status} />
                {item.similarity_score !== null && (
                  <span className="inline-flex items-center gap-1 text-xs text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full font-medium">
                    <Sparkles className="w-3 h-3" /> Score: {item.similarity_score}
                  </span>
                )}
              </div>
              <div className="text-xs text-slate-500 mt-1 flex items-center gap-4">
                <span>File: {item.filename}</span>
                <span>Invoice: {item.invoice_number || 'N/A'}</span>
                <span>Total: {item.total_amount ? `$${item.total_amount.toFixed(2)}` : 'N/A'}</span>
              </div>
            </div>

            <Link
              href={`/documents/${item.document_id}`}
              className="inline-flex items-center gap-1 text-xs font-semibold text-indigo-600 hover:text-indigo-800"
            >
              View Document <ArrowUpRight className="w-4 h-4" />
            </Link>
          </div>
        ))}
        {results.length === 0 && !loading && query && (
          <div className="p-8 text-center text-slate-400 bg-white rounded-xl border">No matching records found.</div>
        )}
      </div>
    </div>
  );
}

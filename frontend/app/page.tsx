'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { FileUploader } from '@/components/FileUploader';
import { StatusBadge } from '@/components/StatusBadge';
import { ArrowUpRight, RefreshCw } from 'lucide-react';
import { apiClient } from '@/lib/api';
import { formatMoney } from '@/lib/money';

interface DocumentRecord {
  id: number;
  filename: string;
  file_type: string;
  status: string;
  created_at: string;
  extracted_invoice?: {
    supplier_name: string | null;
    invoice_number: string | null;
    total_amount: string | number | null;
    currency: string | null;
  };
}

export default function DashboardPage() {
  const [documents, setDocuments] = useState<DocumentRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [authError, setAuthError] = useState<string | null>(null);

  const fetchDocuments = async () => {
    try {
      const res = await apiClient.get('/api/documents?limit=50');
      setDocuments(res.data);
      setAuthError(null);
    } catch (err: any) {
      if (err.response?.status === 401) {
        setAuthError('Authentication required. Enter your API Key in the top navigation bar.');
      } else {
        console.error('Failed to fetch documents:', err);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
    const interval = setInterval(fetchDocuments, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">Document Intelligence Workspace</h1>
        <p className="text-sm text-slate-500 mt-1">Upload and monitor incoming invoices, receipts, and spreadsheets.</p>
      </div>

      {authError && (
        <div className="p-4 bg-amber-50 border border-amber-200 text-amber-900 rounded-xl text-sm">
          {authError}
        </div>
      )}

      <FileUploader onUploadSuccess={fetchDocuments} />

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between">
          <h2 className="text-base font-semibold text-slate-800">Recent Documents</h2>
          <button
            onClick={fetchDocuments}
            className="flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-indigo-600 transition"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            Refresh
          </button>
        </div>

        {loading ? (
          <div className="p-8 text-center text-slate-400">Loading documents...</div>
        ) : documents.length === 0 ? (
          <div className="p-12 text-center text-slate-400">No documents processed yet. Upload one above!</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-600">
              <thead className="bg-slate-50 text-xs uppercase font-medium text-slate-500 border-b border-slate-200">
                <tr>
                  <th className="px-6 py-3">Document ID / File</th>
                  <th className="px-6 py-3">Supplier Name</th>
                  <th className="px-6 py-3">Invoice Number</th>
                  <th className="px-6 py-3">Total Amount</th>
                  <th className="px-6 py-3">Status</th>
                  <th className="px-6 py-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {documents.map((doc) => (
                  <tr key={doc.id} className="hover:bg-slate-50 transition">
                    <td className="px-6 py-4">
                      <div className="font-medium text-slate-900">{doc.filename}</div>
                      <div className="text-xs text-slate-400">Doc #{doc.id} • {doc.file_type.toUpperCase()}</div>
                    </td>
                    <td className="px-6 py-4 font-medium text-slate-800">
                      {doc.extracted_invoice?.supplier_name || <span className="text-slate-400 italic">Not detected</span>}
                    </td>
                    <td className="px-6 py-4">
                      {doc.extracted_invoice?.invoice_number || <span className="text-slate-400 italic">N/A</span>}
                    </td>
                    <td className="px-6 py-4 font-semibold text-slate-900 font-mono">
                      {doc.extracted_invoice?.total_amount != null
                        ? `${formatMoney(doc.extracted_invoice.total_amount)} ${doc.extracted_invoice.currency || 'USD'}`
                        : <span className="text-slate-400 italic">N/A</span>}
                    </td>
                    <td className="px-6 py-4">
                      <StatusBadge status={doc.status} />
                    </td>
                    <td className="px-6 py-4 text-right">
                      <Link
                        href={`/documents/${doc.id}`}
                        className="inline-flex items-center gap-1 text-xs font-semibold text-indigo-600 hover:text-indigo-800"
                      >
                        Review & Edit
                        <ArrowUpRight className="w-4 h-4" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

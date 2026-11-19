'use client';

import React, { useEffect, useState } from 'react';
import { apiClient } from '@/lib/api';
import { FileCheck, AlertCircle, AlertTriangle, Loader2, RefreshCw } from 'lucide-react';

interface ReferenceDocOption {
  id: number;
  filename: string;
  file_type: string;
  status: string;
}

interface CrossVerifyRecord {
  id: number;
  document_id: number;
  reference_document_id: number;
  verification_mode: string;
  overall_status: string;
  discrepancy_count: number;
  comparison_details: {
    primary_filename?: string;
    reference_filename?: string;
    matched_invoice_number?: string | null;
    status_reason?: string;
    fields?: Record<string, { document: string | null; reference: string | null; matched: boolean }>;
    line_items_comparison?: {
      document_count: number;
      reference_count: number;
      document_items_sum: string;
      reference_items_sum: string;
      matched: boolean;
    } | null;
  };
  created_at: string;
}

interface Props {
  documentId: string | string[];
  onVerified: () => void;
}

export const CrossVerificationPanel: React.FC<Props> = ({ documentId, onVerified }) => {
  const [candidates, setCandidates] = useState<ReferenceDocOption[]>([]);
  const [selectedRefId, setSelectedRefId] = useState<string>('');
  const [history, setHistory] = useState<CrossVerifyRecord[]>([]);
  const [latestResult, setLatestResult] = useState<CrossVerifyRecord | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const loadData = async () => {
    try {
      const [docsRes, histRes] = await Promise.all([
        apiClient.get('/api/documents?limit=100'),
        apiClient.get(`/api/documents/${documentId}/cross-verify/history`),
      ]);
      const currentId = Number(documentId);
      const eligible = (docsRes.data || []).filter(
        (d: ReferenceDocOption) => d.id !== currentId && d.status !== 'failed'
      );
      setCandidates(eligible);
      if (eligible.length > 0 && !selectedRefId) {
        setSelectedRefId(String(eligible[0].id));
      }
      const histList: CrossVerifyRecord[] = histRes.data || [];
      setHistory(histList);
      if (histList.length > 0 && !latestResult) {
        setLatestResult(histList[0]);
      }
    } catch (err) {
      console.error('Failed to load cross-verification data:', err);
    }
  };

  useEffect(() => {
    if (documentId) {
      loadData();
    }
  }, [documentId]);

  const handleRunCrossVerify = async () => {
    if (!selectedRefId) return;
    setIsRunning(true);
    setErrorMsg(null);
    try {
      const res = await apiClient.post(`/api/documents/${documentId}/cross-verify`, {
        reference_document_id: Number(selectedRefId),
      });
      setLatestResult(res.data);
      await loadData();
      onVerified();
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || 'Cross-verification failed.');
    } finally {
      setIsRunning(false);
    }
  };

  const renderStatusPill = (status: string) => {
    if (status === 'matched') {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
          <FileCheck className="w-3.5 h-3.5" /> Matched
        </span>
      );
    }
    if (status === 'mismatched') {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-100 text-rose-800 border border-rose-200">
          <AlertCircle className="w-3.5 h-3.5" /> Mismatched
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-200">
        <AlertTriangle className="w-3.5 h-3.5" /> {status.replace(/_/g, ' ')}
      </span>
    );
  };

  const fieldKeys = latestResult?.comparison_details?.fields
    ? Object.keys(latestResult.comparison_details.fields)
    : [];

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 md:p-8 space-y-5">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900">Cross-Document Verification</h2>
          <p className="text-xs text-slate-500">
            Compare this invoice against another PDF, image, Excel (.xlsx/.xls), or CSV reference document.
          </p>
        </div>
        <button
          type="button"
          onClick={loadData}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-indigo-600"
        >
          <RefreshCw className="w-3.5 h-3.5" /> Refresh List
        </button>
      </div>

      <div className="flex flex-col sm:flex-row gap-3">
        <select
          value={selectedRefId}
          onChange={(e) => setSelectedRefId(e.target.value)}
          disabled={candidates.length === 0 || isRunning}
          className="flex-1 text-sm px-3 py-2 border rounded-lg bg-white focus:ring-2 focus:ring-indigo-500 outline-none"
        >
          {candidates.length === 0 ? (
            <option value="">No other eligible documents uploaded yet</option>
          ) : (
            candidates.map((doc) => (
              <option key={doc.id} value={String(doc.id)}>
                Doc #{doc.id} — {doc.filename} ({doc.file_type.toUpperCase()} • {doc.status})
              </option>
            ))
          )}
        </select>

        <button
          type="button"
          onClick={handleRunCrossVerify}
          disabled={!selectedRefId || isRunning}
          className="inline-flex items-center justify-center gap-2 px-4 py-2 bg-slate-900 hover:bg-slate-800 disabled:bg-slate-300 text-white rounded-lg text-sm font-semibold transition"
        >
          {isRunning ? <Loader2 className="w-4 h-4 animate-spin" /> : <FileCheck className="w-4 h-4" />}
          {isRunning ? 'Verifying...' : 'Run Cross-Verification'}
        </button>
      </div>

      {errorMsg && (
        <div className="p-3 bg-rose-50 border border-rose-200 text-rose-800 rounded-lg text-sm">
          {errorMsg}
        </div>
      )}

      {latestResult && (
        <div className="border border-slate-200 rounded-lg p-4 bg-slate-50 space-y-3">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-2 text-sm font-semibold text-slate-800">
              <span>Latest Result:</span>
              {renderStatusPill(latestResult.overall_status)}
              <span className="text-xs font-normal text-slate-500">
                Mode: {latestResult.verification_mode.replace(/_/g, ' ')} • Reference: #
                {latestResult.reference_document_id}{' '}
                {latestResult.comparison_details?.reference_filename
                  ? `(${latestResult.comparison_details.reference_filename})`
                  : ''}
              </span>
            </div>
            <span className="text-xs font-medium text-slate-600">
              Discrepancies: {latestResult.discrepancy_count}
            </span>
          </div>

          {fieldKeys.length > 0 && (
            <div className="overflow-x-auto bg-white border rounded-lg">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-600 border-b">
                  <tr>
                    <th className="p-2.5">Field</th>
                    <th className="p-2.5">This Document</th>
                    <th className="p-2.5">Reference</th>
                    <th className="p-2.5">Match</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {fieldKeys.map((field) => {
                    const row = latestResult.comparison_details.fields![field];
                    return (
                      <tr key={field}>
                        <td className="p-2.5 font-semibold text-slate-700">{field}</td>
                        <td className="p-2.5 font-mono">{row.document ?? 'null'}</td>
                        <td className="p-2.5 font-mono">{row.reference ?? 'null'}</td>
                        <td className="p-2.5">
                          <span
                            className={
                              row.matched
                                ? 'text-emerald-700 font-semibold'
                                : 'text-rose-700 font-semibold'
                            }
                          >
                            {row.matched ? 'Yes' : 'Mismatch'}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}

          {latestResult.comparison_details?.line_items_comparison && (
            <div className="text-xs text-slate-700 bg-white border rounded-lg p-3">
              <span className="font-semibold">Line Items Check: </span>
              This doc: {latestResult.comparison_details.line_items_comparison.document_count} item(s) (sum{' '}
              {latestResult.comparison_details.line_items_comparison.document_items_sum}) vs Reference:{' '}
              {latestResult.comparison_details.line_items_comparison.reference_count} item(s) (sum{' '}
              {latestResult.comparison_details.line_items_comparison.reference_items_sum}) —{' '}
              <span
                className={
                  latestResult.comparison_details.line_items_comparison.matched
                    ? 'text-emerald-700 font-semibold'
                    : 'text-rose-700 font-semibold'
                }
              >
                {latestResult.comparison_details.line_items_comparison.matched ? 'Matched' : 'Mismatch'}
              </span>
            </div>
          )}
        </div>
      )}

      {history.length > 0 && (
        <div className="pt-2">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
            Verification History ({history.length})
          </h3>
          <div className="divide-y border rounded-lg text-xs">
            {history.map((h) => (
              <div key={h.id} className="p-2.5 flex flex-wrap items-center justify-between gap-2 bg-white">
                <div>
                  <span className="font-semibold text-slate-800">
                    Ref #{h.reference_document_id}{' '}
                    {h.comparison_details?.reference_filename
                      ? `(${h.comparison_details.reference_filename})`
                      : ''}
                  </span>{' '}
                  <span className="text-slate-500">• {h.verification_mode.replace(/_/g, ' ')}</span>
                </div>
                <div className="flex items-center gap-3">
                  {renderStatusPill(h.overall_status)}
                  <span className="text-slate-400">
                    {new Date(h.created_at).toLocaleString()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

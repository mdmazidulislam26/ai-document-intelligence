'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { StatusBadge } from '@/components/StatusBadge';
import { ValidationAlerts } from '@/components/ValidationAlerts';
import { ArrowLeft, Save, RotateCcw, CheckCircle } from 'lucide-react';
import { apiClient } from '@/lib/api';
import { formatMoney, multiplyMoney } from '@/lib/money';

export default function DocumentDetailPage() {
  const params = useParams();
  const router = useRouter();
  const documentId = params.id;

  const [document, setDocument] = useState<any>(null);
  const [formData, setFormData] = useState<any>({});
  const [isSaving, setIsSaving] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const fetchDocument = async () => {
    try {
      const res = await apiClient.get(`/api/documents/${documentId}`);
      setDocument(res.data);
      if (res.data.extracted_invoice) {
        const inv = res.data.extracted_invoice;
        const formattedItems = (inv.line_items || []).map((item: any) => ({
          ...item,
          quantity: item.quantity != null ? String(item.quantity) : '1',
          unit_price: formatMoney(item.unit_price),
          total: formatMoney(item.total),
        }));

        // Preserve null/unknown currency as empty string (never default to USD)
        setFormData({
          invoice_number: inv.invoice_number || '',
          invoice_date: inv.invoice_date || '',
          supplier_name: inv.supplier_name || '',
          customer_name: inv.customer_name || '',
          subtotal: formatMoney(inv.subtotal),
          tax: formatMoney(inv.tax),
          total_amount: formatMoney(inv.total_amount),
          currency: inv.currency || '',
          line_items: formattedItems,
        });
      }
    } catch (err) {
      console.error('Failed to fetch document detail:', err);
    }
  };

  useEffect(() => {
    if (documentId) fetchDocument();
  }, [documentId]);

  const handleInputChange = (field: string, value: any) => {
    setFormData((prev: any) => ({ ...prev, [field]: value }));
  };

  const handleBlurFormat = (field: string) => {
    setFormData((prev: any) => ({
      ...prev,
      [field]: formatMoney(prev[field]),
    }));
  };

  const handleLineItemChange = (index: number, field: string, value: any) => {
    const updated = [...formData.line_items];
    updated[index][field] = value;
    if (field === 'quantity' || field === 'unit_price') {
      const q = field === 'quantity' ? value : updated[index].quantity;
      const p = field === 'unit_price' ? value : updated[index].unit_price;
      updated[index]['total'] = multiplyMoney(q, p);
    }
    setFormData((prev: any) => ({ ...prev, line_items: updated }));
  };

  const handleSaveCorrections = async () => {
    setIsSaving(true);
    setSuccessMessage(null);
    try {
      const cleanedItems = (formData.line_items || []).map((it: any) => ({
        description: it.description,
        quantity: it.quantity !== '' && it.quantity != null ? String(it.quantity) : '0',
        unit_price: it.unit_price !== '' && it.unit_price != null ? formatMoney(it.unit_price) : '0.00',
        total: it.total !== '' && it.total != null ? formatMoney(it.total) : '0.00',
      }));

      const normalizedCurrency =
        formData.currency && String(formData.currency).trim()
          ? String(formData.currency).trim().toUpperCase()
          : null;

      const payload = {
        invoice_number: formData.invoice_number || null,
        invoice_date: formData.invoice_date || null,
        supplier_name: formData.supplier_name || null,
        customer_name: formData.customer_name || null,
        subtotal: formData.subtotal !== '' ? formatMoney(formData.subtotal) : null,
        tax: formData.tax !== '' ? formatMoney(formData.tax) : null,
        total_amount: formData.total_amount !== '' ? formatMoney(formData.total_amount) : null,
        currency: normalizedCurrency,
        line_items: cleanedItems,
      };

      const res = await apiClient.put(`/api/documents/${documentId}/correct`, payload);
      setDocument(res.data);
      setSuccessMessage('Corrections saved and re-validated successfully!');
      fetchDocument();
    } catch (err: any) {
      alert('Error saving corrections: ' + (err.response?.data?.detail || err.message));
    } finally {
      setIsSaving(false);
    }
  };

  const handleReprocess = async () => {
    try {
      await apiClient.post(`/api/documents/${documentId}/reprocess`);
      alert('Document requeued for reprocessing.');
      setTimeout(fetchDocument, 2000);
    } catch (err: any) {
      alert('Reprocess error: ' + (err.response?.data?.detail || err.message));
    }
  };

  if (!document) return <div className="p-12 text-center text-slate-500">Loading document details...</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <button
          onClick={() => router.push('/')}
          className="inline-flex items-center gap-2 text-sm text-slate-600 hover:text-slate-900 font-medium"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Dashboard
        </button>
        <div className="flex items-center gap-3">
          <button
            onClick={handleReprocess}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 border border-slate-300 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-100"
          >
            <RotateCcw className="w-3.5 h-3.5" /> Reprocess Document
          </button>
          <StatusBadge status={document.status} />
        </div>
      </div>

      <ValidationAlerts logs={document.validation_logs} />

      {successMessage && (
        <div className="flex items-center gap-2 p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-lg text-sm">
          <CheckCircle className="w-4 h-4 text-emerald-600" />
          <span>{successMessage}</span>
        </div>
      )}

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 md:p-8 space-y-6">
        <div className="border-b border-slate-100 pb-4">
          <h2 className="text-lg font-bold text-slate-900">Extracted Invoice Details</h2>
          <p className="text-xs text-slate-500">Formatted in exact financial 2-decimal precision (e.g. 150.00).</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Supplier Name</label>
            <input
              type="text"
              value={formData.supplier_name || ''}
              onChange={(e) => handleInputChange('supplier_name', e.target.value)}
              className="w-full text-sm px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Customer Name</label>
            <input
              type="text"
              value={formData.customer_name || ''}
              onChange={(e) => handleInputChange('customer_name', e.target.value)}
              className="w-full text-sm px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Invoice Number</label>
            <input
              type="text"
              value={formData.invoice_number || ''}
              onChange={(e) => handleInputChange('invoice_number', e.target.value)}
              className="w-full text-sm px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Invoice Date</label>
            <input
              type="date"
              value={formData.invoice_date || ''}
              onChange={(e) => handleInputChange('invoice_date', e.target.value)}
              className="w-full text-sm px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Subtotal Amount</label>
            <input
              type="number"
              step="0.01"
              value={formData.subtotal ?? ''}
              onChange={(e) => handleInputChange('subtotal', e.target.value)}
              onBlur={() => handleBlurFormat('subtotal')}
              className="w-full text-sm px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none font-mono"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Tax Amount</label>
            <input
              type="number"
              step="0.01"
              value={formData.tax ?? ''}
              onChange={(e) => handleInputChange('tax', e.target.value)}
              onBlur={() => handleBlurFormat('tax')}
              className="w-full text-sm px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none font-mono"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Total Amount</label>
            <input
              type="number"
              step="0.01"
              value={formData.total_amount ?? ''}
              onChange={(e) => handleInputChange('total_amount', e.target.value)}
              onBlur={() => handleBlurFormat('total_amount')}
              className="w-full text-sm px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none font-mono font-semibold"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Currency</label>
            <input
              type="text"
              value={formData.currency ?? ''}
              placeholder="Unknown (leave blank if missing)"
              onChange={(e) => handleInputChange('currency', e.target.value)}
              className="w-full text-sm px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none font-mono"
            />
          </div>
        </div>

        <div className="pt-4">
          <h3 className="text-sm font-bold text-slate-800 mb-3">Line Items</h3>
          <div className="border rounded-lg overflow-hidden">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 font-semibold text-slate-600 border-b">
                <tr>
                  <th className="p-3">Description</th>
                  <th className="p-3 w-24">Qty</th>
                  <th className="p-3 w-32">Unit Price</th>
                  <th className="p-3 w-32">Total</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {formData.line_items?.map((item: any, idx: number) => (
                  <tr key={idx}>
                    <td className="p-2">
                      <input
                        type="text"
                        value={item.description || ''}
                        onChange={(e) => handleLineItemChange(idx, 'description', e.target.value)}
                        className="w-full p-1.5 border rounded outline-none text-xs"
                      />
                    </td>
                    <td className="p-2">
                      <input
                        type="number"
                        value={item.quantity ?? ''}
                        onChange={(e) => handleLineItemChange(idx, 'quantity', e.target.value)}
                        className="w-full p-1.5 border rounded outline-none text-xs font-mono"
                      />
                    </td>
                    <td className="p-2">
                      <input
                        type="number"
                        step="0.01"
                        value={item.unit_price ?? ''}
                        onChange={(e) => handleLineItemChange(idx, 'unit_price', e.target.value)}
                        className="w-full p-1.5 border rounded outline-none text-xs font-mono"
                      />
                    </td>
                    <td className="p-2 font-mono font-semibold text-slate-800">
                      {formatMoney(item.total)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="pt-4 flex justify-end">
          <button
            onClick={handleSaveCorrections}
            disabled={isSaving}
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-semibold shadow-sm transition"
          >
            <Save className="w-4 h-4" />
            {isSaving ? 'Re-validating...' : 'Save & Re-validate'}
          </button>
        </div>
      </div>
    </div>
  );
}

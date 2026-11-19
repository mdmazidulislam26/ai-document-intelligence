'use client';

import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, Loader2, CheckCircle2, AlertCircle } from 'lucide-react';
import { apiClient } from '@/lib/api';

export const FileUploader: React.FC<{ onUploadSuccess: () => void }> = ({ onUploadSuccess }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);
  const [isError, setIsError] = useState(false);

  const onDrop = async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;
    setIsUploading(true);
    setUploadMessage(null);
    setIsError(false);

    const formData = new FormData();
    acceptedFiles.forEach((file) => {
      formData.append('files', file);
    });

    try {
      await apiClient.post('/api/documents/upload', formData);
      setIsError(false);
      setUploadMessage(`Successfully queued ${acceptedFiles.length} file(s) for processing.`);
      onUploadSuccess();
    } catch (err: any) {
      setIsError(true);
      const detail = err.response?.data?.detail;
      const formattedDetail =
        typeof detail === 'string'
          ? detail
          : Array.isArray(detail)
            ? detail.map((d: any) => d?.msg || JSON.stringify(d)).join(', ')
            : err.message || 'Upload failed. Please verify API key and backend connection.';
      setUploadMessage(formattedDetail);
    } finally {
      setIsUploading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.jpg', '.jpeg', '.png', '.tiff', '.tif'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
      'text/csv': ['.csv'],
    },
    disabled: isUploading,
  });

  return (
    <div className="w-full bg-white rounded-xl border border-dashed border-gray-300 p-8 text-center hover:border-indigo-500 transition-colors cursor-pointer shadow-sm">
      <div {...getRootProps()} className="flex flex-col items-center justify-center">
        <input {...getInputProps()} />
        <div className="w-14 h-14 bg-indigo-50 rounded-full flex items-center justify-center mb-4 text-indigo-600">
          {isUploading ? (
            <Loader2 className="w-7 h-7 animate-spin" />
          ) : (
            <UploadCloud className="w-7 h-7" />
          )}
        </div>
        <p className="text-base font-medium text-gray-800">
          {isDragActive ? 'Drop the files here...' : 'Drag and drop invoices, PDFs, scans, Excel or CSV'}
        </p>
        <p className="text-xs text-gray-500 mt-1">
          Supports multi-page PDFs (up to 1000 pages), JPG, PNG, TIFF, XLSX, XLS, CSV (Max 50MB)
        </p>
        {uploadMessage && (
          <div
            className={`mt-4 flex items-center gap-2 text-sm px-4 py-2 rounded-lg ${
              isError ? 'text-rose-700 bg-rose-50' : 'text-indigo-700 bg-indigo-50'
            }`}
          >
            {isError ? (
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            ) : (
              <CheckCircle2 className="w-4 h-4 text-indigo-600 shrink-0" />
            )}
            <span>{uploadMessage}</span>
          </div>
        )}
      </div>
    </div>
  );
};

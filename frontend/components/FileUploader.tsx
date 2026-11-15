'use client';

import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { UploadCloud, FileText, Loader2, CheckCircle2 } from 'lucide-react';

export const FileUploader: React.FC<{ onUploadSuccess: () => void }> = ({ onUploadSuccess }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);

  const onDrop = async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;
    setIsUploading(true);
    setUploadMessage(null);

    const formData = new FormData();
    acceptedFiles.forEach((file) => {
      formData.append('files', file);
    });

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      await axios.post(`${apiUrl}/api/documents/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setUploadMessage(`Successfully queued ${acceptedFiles.length} file(s) for processing.`);
      onUploadSuccess();
    } catch (err: any) {
      setUploadMessage(err.response?.data?.detail || 'Upload failed. Please check backend connection.');
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
          <div className="mt-4 flex items-center gap-2 text-sm text-indigo-700 bg-indigo-50 px-4 py-2 rounded-lg">
            <CheckCircle2 className="w-4 h-4 text-indigo-600" />
            <span>{uploadMessage}</span>
          </div>
        )}
      </div>
    </div>
  );
};

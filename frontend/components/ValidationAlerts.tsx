import React from 'react';
import { AlertCircle, AlertTriangle } from 'lucide-react';

interface LogItem {
  rule_name: str;
  error_description: string;
  severity: string;
}

export const ValidationAlerts: React.FC<{ logs: LogItem[] }> = ({ logs }) => {
  if (!logs || logs.length === 0) return null;

  return (
    <div className="space-y-2 mb-6">
      <h3 className="text-sm font-bold uppercase tracking-wider text-rose-700">Validation Flags Detected</h3>
      {logs.map((log, idx) => (
        <div
          key={idx}
          className={`flex items-start gap-3 p-3.5 rounded-lg border text-sm ${
            log.severity === 'CRITICAL' || log.severity === 'ERROR'
              ? 'bg-rose-50 border-rose-200 text-rose-900'
              : 'bg-amber-50 border-amber-200 text-amber-900'
          }`}
        >
          {log.severity === 'CRITICAL' || log.severity === 'ERROR' ? (
            <AlertCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
          ) : (
            <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
          )}
          <div>
            <span className="font-semibold">{log.rule_name}: </span>
            <span>{log.error_description}</span>
          </div>
        </div>
      ))}
    </div>
  );
};

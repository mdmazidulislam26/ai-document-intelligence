import './globals.css';
import { Navbar } from '@/components/Navbar';

export const metadata = {
  title: 'AI Document Intelligence System',
  description: 'Enterprise Automated Financial Document Extraction and Verification',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-50 text-slate-900 min-h-screen flex flex-col font-sans">
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto p-6 md:p-8">
          {children}
        </main>
      </body>
    </html>
  );
}

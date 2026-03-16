import './globals.css';
import ClientToaster from '@/components/ClientToaster';

export const metadata = {
  title: 'AI Assignment Generator',
  description: 'Generate professional academic assignments with AI-powered research, writing, and formatting.',
  icons: { icon: '/favicon.ico' },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="scroll-smooth" suppressHydrationWarning>
      <body className="min-h-screen bg-[#0a0a0f] text-white overflow-x-hidden" suppressHydrationWarning>
        <ClientToaster />
        {children}
      </body>
    </html>
  );
}

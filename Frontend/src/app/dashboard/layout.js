/**
 * @fileoverview Dashboard layout — protected route wrapper with Navbar.
 */
import Navbar from '@/components/Navbar';
import ProtectedRoute from '@/components/ProtectedRoute';

export const metadata = {
  title: 'Dashboard — AI Assignment Generator',
};

export default function DashboardLayout({ children }) {
  return (
    <ProtectedRoute>
      <Navbar />
      <main className="pt-20 pb-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        {children}
      </main>
    </ProtectedRoute>
  );
}

'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useSeekerAuth } from '@/hooks/useAuth';
import { seekerService } from '@/services/seeker-service';
import { FileText, Briefcase, Building2, Calendar, XCircle } from 'lucide-react';

export default function ApplicationsPage() {
  // Use the custom authentication hook for seeker-specific protection
  const { user, isLoading: authLoading, logout } = useSeekerAuth();
  const [applications, setApplications] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Load applications once authentication is confirmed
  useEffect(() => {
    if (!authLoading && user) {
      loadApplications();
    }
  }, [authLoading, user]);

  const loadApplications = async () => {
    try {
      const data = await seekerService.getApplications();
      setApplications(data.applications || []);
    } catch (error) {
      console.error('Failed to load applications:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleWithdraw = async (jobId: string) => {
    if (!confirm('Are you sure you want to withdraw this application?')) return;

    try {
      await seekerService.withdrawApplication(jobId);
      await loadApplications();
    } catch (error) {
      console.error('Failed to withdraw application:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-emerald-50 to-white">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <Link href="/seeker/dashboard" className="text-2xl font-bold text-emerald-600 hover:text-emerald-700 transition-colors">
              WorkAtlas
            </Link>
            <nav className="flex items-center gap-6">
              <Link 
                href="/seeker/dashboard" 
                className="text-gray-700 hover:text-emerald-600 transition-colors font-medium"
              >
                Dashboard
              </Link>
              <Link 
                href="/seeker/recommendations" 
                className="text-gray-700 hover:text-emerald-600 transition-colors font-medium"
              >
                AI Recommendations
              </Link>
              <Link 
                href="/seeker/jobs" 
                className="text-gray-700 hover:text-emerald-600 transition-colors font-medium"
              >
                Search Jobs
              </Link>
              <Link 
                href="/seeker/profile" 
                className="text-gray-700 hover:text-emerald-600 transition-colors font-medium"
              >
                Profile
              </Link>
              <button 
                onClick={logout} 
                className="text-gray-700 hover:text-red-600 transition-colors font-medium"
              >
                Logout
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Page Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-emerald-100 rounded-lg">
              <FileText className="h-6 w-6 text-emerald-600" />
            </div>
            <h1 className="text-4xl font-bold text-gray-900">My Applications</h1>
          </div>
          <p className="text-gray-600 ml-14">Track your job applications and their status</p>
        </div>

        {loading ? (
          <div className="text-center py-16">
            <div className="inline-flex items-center justify-center w-16 h-16 mb-4 bg-emerald-100 rounded-full">
              <div className="w-8 h-8 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin"></div>
            </div>
            <p className="text-xl text-gray-600">Loading your applications...</p>
          </div>
        ) : applications.length === 0 ? (
          <div className="text-center py-16 bg-white rounded-2xl shadow-lg border border-gray-100">
            <div className="inline-flex items-center justify-center w-20 h-20 mb-6 bg-emerald-50 rounded-full">
              <FileText className="h-10 w-10 text-emerald-600" />
            </div>
            <h3 className="text-2xl font-semibold text-gray-900 mb-2">No Applications Yet</h3>
            <p className="text-gray-600 mb-6">Start your job search and apply to positions that match your skills</p>
            <Link
              href="/seeker/jobs"
              className="inline-flex items-center gap-2 px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors font-medium"
            >
              <Briefcase className="h-5 w-5" />
              Search Jobs
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {applications.map((app, index) => (
              <div 
                key={index} 
                className="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow border border-gray-100 p-6"
              >
                <div className="flex justify-between items-start">
                  <div className="flex items-start gap-4 flex-1">
                    <div className="p-3 bg-emerald-50 rounded-lg">
                      <Briefcase className="h-6 w-6 text-emerald-600" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold text-gray-900 mb-1">{app.job_title || 'Unknown Job'}</h3>
                      <div className="flex items-center gap-2 text-gray-600 mb-3">
                        <Building2 className="h-4 w-4" />
                        <span>{app.company_name || 'Unknown Company'}</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm text-gray-500">
                        <Calendar className="h-4 w-4" />
                        <span>Applied: {new Date(app.date_applied).toLocaleDateString()}</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className={`px-4 py-2 rounded-full text-sm font-medium ${
                      app.application_status === 'Submitted' ? 'bg-emerald-100 text-emerald-800' :
                      app.application_status === 'Under Review' ? 'bg-blue-100 text-blue-800' :
                      app.application_status === 'Interviewed' ? 'bg-purple-100 text-purple-800' :
                      app.application_status === 'Offered' ? 'bg-green-100 text-green-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {app.application_status}
                    </span>
                    {app.application_status === 'Submitted' && (
                      <button
                        onClick={() => handleWithdraw(app.job_id)}
                        className="inline-flex items-center gap-2 px-4 py-2 text-red-600 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors font-medium"
                      >
                        <XCircle className="h-4 w-4" />
                        Withdraw
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}


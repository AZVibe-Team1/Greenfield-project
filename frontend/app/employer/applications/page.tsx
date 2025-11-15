'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useEmployerAuth } from '@/hooks/useAuth';
import { employerService } from '@/services/employer-service';
import { Briefcase, Users, Calendar, Clock, FileText, ChevronRight } from 'lucide-react';

export default function EmployerApplicationsPage() {
  // Use the custom authentication hook for employer-specific protection
  const { user, isLoading: authLoading, logout } = useEmployerAuth();
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
      const data = await employerService.getApplications();
      setApplications(data.applications || []);
    } catch (error) {
      console.error('Failed to load applications:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <Link href="/employer/dashboard" className="text-2xl font-bold text-blue-600 hover:text-blue-700 transition-colors">
              Job Portal
            </Link>
            <nav className="flex items-center gap-6">
              <Link 
                href="/employer/dashboard" 
                className="text-gray-700 hover:text-blue-600 transition-colors font-medium"
              >
                Dashboard
              </Link>
              <Link 
                href="/employer/jobs" 
                className="text-gray-700 hover:text-blue-600 transition-colors font-medium"
              >
                My Jobs
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
            <div className="p-2 bg-blue-100 rounded-lg">
              <Users className="h-6 w-6 text-blue-600" />
            </div>
            <h1 className="text-4xl font-bold text-gray-900">Applications Received</h1>
          </div>
          <p className="text-gray-600 ml-14">Review and manage candidate applications for your job postings</p>
        </div>

        {loading ? (
          <div className="text-center py-16">
            <div className="inline-flex items-center justify-center w-16 h-16 mb-4 bg-blue-100 rounded-full">
              <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
            </div>
            <p className="text-xl text-gray-600">Loading applications...</p>
          </div>
        ) : applications.length === 0 ? (
          <div className="text-center py-16 bg-white rounded-2xl shadow-lg border border-gray-100">
            <div className="inline-flex items-center justify-center w-20 h-20 mb-6 bg-blue-50 rounded-full">
              <FileText className="h-10 w-10 text-blue-600" />
            </div>
            <h3 className="text-2xl font-semibold text-gray-900 mb-2">No Applications Yet</h3>
            <p className="text-gray-600 mb-6">You haven't received any applications for your job postings</p>
            <Link
              href="/employer/jobs"
              className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              <Briefcase className="h-5 w-5" />
              View My Job Postings
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {applications.map((app, index) => (
              <div 
                key={index} 
                className="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow border border-gray-100 p-6"
              >
                <div className="flex justify-between items-start mb-4">
                  <div className="flex items-start gap-4 flex-1">
                    <div className="p-3 bg-blue-50 rounded-lg">
                      <Users className="h-6 w-6 text-blue-600" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold text-gray-900 mb-1">
                        Applicant ID: {app.applicant_id}
                      </h3>
                      <div className="flex items-center gap-2 text-gray-600 mb-3">
                        <Briefcase className="h-4 w-4" />
                        <span>Job ID: {app.job_id}</span>
                      </div>
                      
                      <div className="flex flex-wrap gap-4 text-sm">
                        <div className="flex items-center gap-2 text-gray-500">
                          <Calendar className="h-4 w-4" />
                          <span>Received: {new Date(app.initial_daterec).toLocaleDateString()}</span>
                        </div>
                        {app.current_status_date && (
                          <div className="flex items-center gap-2 text-gray-500">
                            <Clock className="h-4 w-4" />
                            <span>Updated: {new Date(app.current_status_date).toLocaleDateString()}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3">
                    <span className={`px-4 py-2 rounded-full text-sm font-medium ${
                      app.current_status === 'Received' ? 'bg-blue-100 text-blue-800' :
                      app.current_status === 'Reviewed' ? 'bg-purple-100 text-purple-800' :
                      app.current_status === 'Interviewed' ? 'bg-yellow-100 text-yellow-800' :
                      app.current_status === 'Offered' ? 'bg-green-100 text-green-800' :
                      app.current_status === 'Hired' ? 'bg-emerald-100 text-emerald-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {app.current_status}
                    </span>
                    <button className="p-2 hover:bg-gray-50 rounded-lg transition-colors">
                      <ChevronRight className="h-5 w-5 text-gray-400" />
                    </button>
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


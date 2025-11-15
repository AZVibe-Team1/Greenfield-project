'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useEmployerAuth } from '@/hooks/useAuth';
import { employerService } from '@/services/employer-service';
import { Job } from '@/types';
import { 
  Briefcase, 
  Plus, 
  Edit2, 
  Trash2, 
  Calendar, 
  DollarSign, 
  GraduationCap,
  CheckCircle,
  XCircle,
  Users,
  Sparkles
} from 'lucide-react';

export default function EmployerJobsPage() {
  // Use the custom authentication hook for employer-specific protection
  const { user, isLoading: authLoading, logout } = useEmployerAuth();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);

  // Load jobs once authentication is confirmed
  useEffect(() => {
    if (!authLoading && user) {
      loadJobs();
    }
  }, [authLoading, user]);

  const loadJobs = async () => {
    try {
      const data = await employerService.getJobs();
      setJobs(data);
    } catch (error) {
      console.error('Failed to load jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (jobId: string) => {
    if (!confirm('Are you sure you want to delete this job posting?')) return;

    try {
      await employerService.deleteJob(jobId);
      await loadJobs();
    } catch (error) {
      console.error('Failed to delete job:', error);
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
                href="/employer/applications" 
                className="text-gray-700 hover:text-blue-600 transition-colors font-medium"
              >
                Applications
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
        <div className="flex flex-col md:flex-row md:justify-between md:items-center mb-8 gap-4">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Briefcase className="h-6 w-6 text-blue-600" />
              </div>
              <h1 className="text-4xl font-bold text-gray-900">My Job Postings</h1>
            </div>
            <p className="text-gray-600 ml-14">Manage your active and past job listings</p>
          </div>
          <Link
            href="/employer/jobs/new"
            className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium shadow-md hover:shadow-lg"
          >
            <Plus className="h-5 w-5" />
            Post New Job
          </Link>
        </div>

        {loading ? (
          <div className="text-center py-16">
            <div className="inline-flex items-center justify-center w-16 h-16 mb-4 bg-blue-100 rounded-full">
              <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
            </div>
            <p className="text-xl text-gray-600">Loading your job postings...</p>
          </div>
        ) : jobs.length === 0 ? (
          <div className="text-center py-16 bg-white rounded-2xl shadow-lg border border-gray-100">
            <div className="inline-flex items-center justify-center w-20 h-20 mb-6 bg-blue-50 rounded-full">
              <Briefcase className="h-10 w-10 text-blue-600" />
            </div>
            <h3 className="text-2xl font-semibold text-gray-900 mb-2">No Job Postings Yet</h3>
            <p className="text-gray-600 mb-6">Start attracting top talent by posting your first job opening</p>
            <Link
              href="/employer/jobs/new"
              className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              <Plus className="h-5 w-5" />
              Post Your First Job
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {jobs.map((job) => (
              <div 
                key={job.job_id} 
                className="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow border border-gray-100 p-6"
              >
                <div className="flex justify-between items-start mb-4">
                  <div className="flex items-start gap-4 flex-1">
                    <div className="p-3 bg-blue-50 rounded-lg">
                      <Briefcase className="h-6 w-6 text-blue-600" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold text-gray-900 mb-1">{job.job_title}</h3>
                      <p className="text-gray-600 font-medium mb-3">{job.department}</p>
                      <p className="text-gray-700 mb-4 line-clamp-2">{job.job_description}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3 ml-4">
                    {job.current_status === 'Posted' ? (
                      <span className="flex items-center gap-1 px-3 py-1.5 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                        <CheckCircle className="h-4 w-4" />
                        {job.current_status}
                      </span>
                    ) : (
                      <span className="flex items-center gap-1 px-3 py-1.5 bg-gray-100 text-gray-800 rounded-full text-sm font-medium">
                        <XCircle className="h-4 w-4" />
                        {job.current_status}
                      </span>
                    )}
                  </div>
                </div>

                <div className="grid md:grid-cols-3 gap-4 mb-4 p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-2">
                    <DollarSign className="h-5 w-5 text-blue-600" />
                    <div>
                      <p className="text-xs text-gray-600">Salary Range</p>
                      <p className="font-medium text-gray-900">
                        ${job.pay_range[0].toLocaleString()} - ${job.pay_range[1].toLocaleString()}
                      </p>
                      <p className="text-xs text-gray-500">{job.pay_unit}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Calendar className="h-5 w-5 text-blue-600" />
                    <div>
                      <p className="text-xs text-gray-600">Posted Date</p>
                      <p className="font-medium text-gray-900">{new Date(job.posted_date).toLocaleDateString()}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <GraduationCap className="h-5 w-5 text-blue-600" />
                    <div>
                      <p className="text-xs text-gray-600">Required Education</p>
                      <p className="font-medium text-gray-900">{job.education_level}</p>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3 pt-4 border-t border-gray-200">
                  <Link
                    href={`/employer/jobs/${job.job_id}/candidates`}
                    className="inline-flex items-center gap-2 px-6 py-2.5 bg-gradient-to-r from-purple-600 to-purple-500 text-white rounded-lg hover:from-purple-700 hover:to-purple-600 transition-all font-medium shadow-md hover:shadow-lg"
                  >
                    <Sparkles className="h-4 w-4" />
                    View AI Candidates
                  </Link>
                  <Link
                    href={`/employer/jobs/${job.job_id}`}
                    className="inline-flex items-center gap-2 px-4 py-2 text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-lg transition-colors font-medium"
                  >
                    <Edit2 className="h-4 w-4" />
                    Edit
                  </Link>
                  <button
                    onClick={() => handleDelete(job.job_id)}
                    className="inline-flex items-center gap-2 px-4 py-2 text-red-600 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors font-medium"
                  >
                    <Trash2 className="h-4 w-4" />
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}


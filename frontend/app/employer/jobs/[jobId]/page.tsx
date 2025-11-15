'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { useAuthStore } from '@/store/auth-store';
import { employerService } from '@/services/employer-service';
import { Job } from '@/types';
import { 
  Briefcase, 
  ArrowLeft, 
  Edit2, 
  Trash2, 
  Calendar, 
  DollarSign, 
  GraduationCap,
  MapPin,
  Clock,
  Users,
  CheckCircle,
  Building2,
  FileText
} from 'lucide-react';

export default function JobDetailPage() {
  const router = useRouter();
  const params = useParams();
  const jobId = params.jobId as string;
  const { isAuthenticated, checkAuth, logout } = useAuthStore();
  const [job, setJob] = useState<Job | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    loadJob();
  }, [isAuthenticated, jobId, router]);

  const loadJob = async () => {
    try {
      const data = await employerService.getJob(jobId);
      setJob(data);
    } catch (error) {
      console.error('Failed to load job:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this job posting?')) return;

    try {
      await employerService.deleteJob(jobId);
      router.push('/employer/jobs');
    } catch (error) {
      console.error('Failed to delete job:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-xl text-gray-600">Loading job details...</p>
        </div>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Job Not Found</h2>
          <Link
            href="/employer/jobs"
            className="text-blue-600 hover:text-blue-700 font-medium"
          >
            Back to Jobs
          </Link>
        </div>
      </div>
    );
  }

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
      <main className="container mx-auto px-4 py-8 max-w-5xl">
        {/* Back Button */}
        <Link
          href="/employer/jobs"
          className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium mb-6 transition-colors"
        >
          <ArrowLeft className="h-5 w-5" />
          Back to Jobs
        </Link>

        {/* Job Header */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
          <div className="flex justify-between items-start mb-6">
            <div className="flex items-start gap-4 flex-1">
              <div className="p-4 bg-blue-100 rounded-xl">
                <Briefcase className="h-8 w-8 text-blue-600" />
              </div>
              <div className="flex-1">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">{job.job_title}</h1>
                <div className="flex items-center gap-4 text-gray-600">
                  <span className="flex items-center gap-1">
                    <Building2 className="h-5 w-5" />
                    {job.department}
                  </span>
                  <span className="flex items-center gap-1">
                    <MapPin className="h-5 w-5" />
                    {job.hiring_manager || `${job.hire_mgr_first} ${job.hire_mgr_last}`}
                  </span>
                </div>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              {job.current_status === 'Posted' ? (
                <span className="flex items-center gap-1 px-4 py-2 bg-green-100 text-green-800 rounded-full text-sm font-semibold">
                  <CheckCircle className="h-4 w-4" />
                  {job.current_status}
                </span>
              ) : (
                <span className="px-4 py-2 bg-gray-100 text-gray-800 rounded-full text-sm font-semibold">
                  {job.current_status}
                </span>
              )}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-3 pt-6 border-t border-gray-200">
            <Link
              href={`/employer/jobs/${jobId}/edit`}
              className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              <Edit2 className="h-4 w-4" />
              Edit Job
            </Link>
            <button
              onClick={handleDelete}
              className="inline-flex items-center gap-2 px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
            >
              <Trash2 className="h-4 w-4" />
              Delete Job
            </button>
          </div>
        </div>

        {/* Job Details */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
            <FileText className="h-6 w-6 text-blue-600" />
            Job Details
          </h2>

          <div className="space-y-6">
            {/* Description */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Description</h3>
              <p className="text-gray-700 leading-relaxed">{job.job_description}</p>
            </div>

            {/* Key Information Grid */}
            <div className="grid md:grid-cols-2 gap-6 pt-6 border-t border-gray-200">
              <div className="flex items-start gap-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <DollarSign className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Salary Range</p>
                  <p className="font-semibold text-gray-900">
                    ${job.pay_range[0].toLocaleString()} - ${job.pay_range[1].toLocaleString()}
                  </p>
                  <p className="text-sm text-gray-600">{job.pay_unit}</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="p-2 bg-green-100 rounded-lg">
                  <GraduationCap className="h-5 w-5 text-green-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Education Level</p>
                  <p className="font-semibold text-gray-900">{job.education_level}</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Calendar className="h-5 w-5 text-purple-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Posted Date</p>
                  <p className="font-semibold text-gray-900">
                    {new Date(job.posted_date).toLocaleDateString()}
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="p-2 bg-amber-100 rounded-lg">
                  <Clock className="h-5 w-5 text-amber-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Work Schedule</p>
                  <p className="font-semibold text-gray-900">{job.work_schedule || 'Full-time'}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Hiring Manager */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
            <Users className="h-6 w-6 text-blue-600" />
            Hiring Manager
          </h2>
          <div className="space-y-3">
            <p className="text-gray-700">
              <span className="font-semibold">Name:</span> {job.hire_mgr_first} {job.hire_mgr_last}
            </p>
            <p className="text-gray-700">
              <span className="font-semibold">Department:</span> {job.department}
            </p>
          </div>
        </div>

        {/* Required Skills */}
        {job.key_skills && job.key_skills.length > 0 && (
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <FileText className="h-6 w-6 text-blue-600" />
              Required Skills
            </h2>
            <div className="flex flex-wrap gap-2">
              {job.key_skills.map((skill, index) => (
                <span
                  key={index}
                  className="px-4 py-2 bg-blue-100 text-blue-800 rounded-lg font-medium"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}


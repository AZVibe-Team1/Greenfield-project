'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useEmployerAuth } from '@/hooks/useAuth';
import { employerService } from '@/services/employer-service';
import { EmployerProfile, N8nStatusResponse } from '@/types';
import { 
  Briefcase, 
  Building2, 
  FileText, 
  Users, 
  LogOut, 
  MapPin, 
  Plus,
  TrendingUp,
  Clock,
  CheckCircle,
  Target,
  User,
  Edit,
  Activity
} from 'lucide-react';

export default function EmployerDashboard() {
  // Use the custom authentication hook for employer-specific protection
  // This implements the protected routes strategy from frontend_auth.txt
  const { user, isLoading: authLoading, logout } = useEmployerAuth();
  const [profile, setProfile] = useState<EmployerProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [n8nStatus, setN8nStatus] = useState<N8nStatusResponse | null>(null);

  // Load profile data once authentication is confirmed
  useEffect(() => {
    if (!authLoading && user) {
      loadProfile();
      loadN8nStatus();
    }
  }, [authLoading, user]);

  const loadProfile = async () => {
    try {
      const data = await employerService.getProfile();
      setProfile(data);
    } catch (error) {
      console.error('Failed to load profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadN8nStatus = async () => {
    try {
      const status = await employerService.getN8nStatus();
      setN8nStatus(status);
    } catch (error) {
      console.error('Failed to load n8n status:', error);
      setN8nStatus({ status: 'disconnected', message: 'Unable to check n8n status' });
    }
  };

  // Show loading state while authentication is being verified
  if (authLoading || loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-xl text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="flex items-center">
              <Briefcase className="h-8 w-8 text-blue-600" />
              <span className="ml-2 text-2xl font-bold text-gray-900">WorkAtlas</span>
            </Link>
            <div className="flex items-center gap-6">
              <span className="text-gray-700 font-medium hidden sm:block">
                {profile?.company_name}
              </span>
              <Link
                href="/employer/profile"
                className="flex items-center gap-2 text-gray-600 hover:text-blue-600 transition-colors"
              >
                <User className="h-5 w-5" />
                <span className="hidden sm:inline">Profile</span>
              </Link>
              <button
                onClick={logout}
                className="flex items-center gap-2 text-gray-600 hover:text-blue-600 transition-colors"
              >
                <LogOut className="h-5 w-5" />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Banner */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-500 rounded-2xl shadow-xl p-8 mb-8 text-white">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-3">
              <Building2 className="h-8 w-8" />
              <h1 className="text-3xl md:text-4xl font-bold">
                {profile?.company_name}
              </h1>
            </div>
            {/* n8n Status Indicator */}
            {n8nStatus && (
              <div className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
                n8nStatus.status === 'connected' 
                  ? 'bg-green-500/20 border border-green-300/30' 
                  : 'bg-red-500/20 border border-red-300/30'
              }`}>
                <Activity className={`h-4 w-4 ${
                  n8nStatus.status === 'connected' ? 'text-green-200' : 'text-red-200'
                }`} />
                <span className={`text-sm font-medium ${
                  n8nStatus.status === 'connected' ? 'text-green-100' : 'text-red-100'
                }`}>
                  Email: {n8nStatus.status === 'connected' ? 'Connected' : 'Disconnected'}
                </span>
              </div>
            )}
          </div>
          <p className="text-blue-100 text-lg">
            Building your team at {profile?.company_name} - Hire smarter with AI-powered insights.
          </p>
          {n8nStatus && n8nStatus.status === 'disconnected' && (
            <div className="mt-4 p-3 bg-red-500/20 border border-red-300/30 rounded-lg">
              <p className="text-red-100 text-sm">
                ⚠️ Email notifications are currently unavailable. Interview scheduling emails will not be sent until n8n is connected.
              </p>
            </div>
          )}
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {/* Active Jobs */}
          <Link
            href="/employer/jobs"
            className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all hover:-translate-y-1 cursor-pointer"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="bg-blue-100 p-3 rounded-lg">
                <Briefcase className="h-8 w-8 text-blue-600" />
              </div>
              <span className="text-3xl font-bold text-gray-900">
                {profile?.open_jobs.length || 0}
              </span>
            </div>
            <h3 className="text-gray-600 font-medium">Active Jobs</h3>
            <p className="text-sm text-gray-500 mt-1">Posted positions</p>
          </Link>

          {/* Total Applications */}
          <Link
            href="/employer/applications"
            className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all hover:-translate-y-1 cursor-pointer"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="bg-green-100 p-3 rounded-lg">
                <FileText className="h-8 w-8 text-green-600" />
              </div>
              <span className="text-3xl font-bold text-gray-900">
                {profile?.apps_received.length || 0}
              </span>
            </div>
            <h3 className="text-gray-600 font-medium">Applications</h3>
            <p className="text-sm text-gray-500 mt-1">Total received</p>
          </Link>

          {/* Applicants */}
          <Link
            href="/employer/applications"
            className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all hover:-translate-y-1 cursor-pointer"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="bg-purple-100 p-3 rounded-lg">
                <Users className="h-8 w-8 text-purple-600" />
              </div>
              <span className="text-3xl font-bold text-gray-900">
                {profile?.apps_received.length || 0}
              </span>
            </div>
            <h3 className="text-gray-600 font-medium">Applicants</h3>
            <p className="text-sm text-gray-500 mt-1">Unique candidates</p>
          </Link>

          {/* AI Matching Feature */}
          <Link
            href="/employer/jobs"
            className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all hover:-translate-y-1 cursor-pointer relative overflow-hidden border-2 border-purple-200"
          >
            <div className="flex flex-col h-full">
              <div className="flex items-center justify-between mb-4">
                <div className="bg-gradient-to-br from-purple-500 to-purple-600 p-3 rounded-lg shadow-md">
                  <Target className="h-8 w-8 text-white" />
                </div>
              </div>
              <h3 className="text-gray-900 font-bold text-lg mb-2">AI Candidate Matching</h3>
              <p className="text-sm text-purple-700 mb-4 flex-grow">
                Smart AI recommendations for your job postings
              </p>
              <div className="flex items-center justify-between">
                <span className="text-purple-600 font-semibold text-sm">View Matches</span>
                <div className="bg-purple-500 text-white rounded-full p-1">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </div>
          </Link>
        </div>

        {/* AI Feature Banner */}
        {profile && profile.open_jobs.length > 0 && (
          <div className="bg-gradient-to-r from-purple-600 to-purple-500 rounded-2xl shadow-xl p-6 mb-8 text-white">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="bg-white/20 p-3 rounded-xl">
                  <Target className="h-8 w-8 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-1">🎯 AI-Powered Candidate Matching Available</h3>
                  <p className="text-purple-100">
                    View AI-matched candidates with detailed scoring for each of your job postings
                  </p>
                </div>
              </div>
              <Link
                href="/employer/jobs"
                className="px-6 py-3 bg-white text-purple-600 rounded-lg font-semibold hover:bg-purple-50 transition-colors whitespace-nowrap"
              >
                Explore Now →
              </Link>
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Link
            href="/employer/jobs/new"
            className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all hover:-translate-y-1 group"
          >
            <div className="bg-blue-100 w-14 h-14 rounded-xl flex items-center justify-center mb-4 group-hover:bg-blue-600 transition-colors">
              <Plus className="h-7 w-7 text-blue-600 group-hover:text-white transition-colors" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Post a Job</h3>
            <p className="text-gray-600">Create a new job posting</p>
          </Link>

          <Link
            href="/employer/jobs"
            className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all hover:-translate-y-1 group"
          >
            <div className="bg-blue-100 w-14 h-14 rounded-xl flex items-center justify-center mb-4 group-hover:bg-blue-600 transition-colors">
              <Briefcase className="h-7 w-7 text-blue-600 group-hover:text-white transition-colors" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">My Jobs</h3>
            <p className="text-gray-600">{profile?.open_jobs.length || 0} active postings</p>
          </Link>

          <Link
            href="/employer/applications"
            className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all hover:-translate-y-1 group"
          >
            <div className="bg-blue-100 w-14 h-14 rounded-xl flex items-center justify-center mb-4 group-hover:bg-blue-600 transition-colors">
              <FileText className="h-7 w-7 text-blue-600 group-hover:text-white transition-colors" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Applications</h3>
            <p className="text-gray-600">{profile?.apps_received.length || 0} applications</p>
          </Link>
        </div>

        {/* Company Summary */}
        {profile && (
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                <Building2 className="h-6 w-6 text-blue-600" />
                Company Information
              </h3>
              <Link
                href="/employer/profile"
                className="inline-flex items-center gap-2 px-4 py-2 text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-lg transition-colors font-medium"
              >
                <Edit className="h-4 w-4" />
                Edit Profile
              </Link>
            </div>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="flex items-start gap-3">
                <div className="bg-blue-100 p-2 rounded-lg">
                  <Building2 className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">Company Name</p>
                  <p className="font-semibold text-gray-900">{profile.company_name}</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-green-100 p-2 rounded-lg">
                  <MapPin className="h-5 w-5 text-green-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">Location</p>
                  <p className="font-semibold text-gray-900">{profile.address.city}, {profile.address.state}</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-purple-100 p-2 rounded-lg">
                  <Users className="h-5 w-5 text-purple-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">Primary Contact</p>
                  <p className="font-semibold text-gray-900">{profile.contact_first_name} {profile.contact_last_name}</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-amber-100 p-2 rounded-lg">
                  <TrendingUp className="h-5 w-5 text-amber-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">Active Postings</p>
                  <p className="font-semibold text-gray-900">{profile.open_jobs.length} job{profile.open_jobs.length !== 1 ? 's' : ''}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Recent Job Postings */}
        {profile && profile.open_jobs.length > 0 ? (
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <Briefcase className="h-6 w-6 text-blue-600" />
              Recent Job Postings
            </h3>
            <div className="space-y-4">
              {profile.open_jobs.slice(0, 5).map((job) => (
                <div key={job.job_id} className="border border-gray-200 rounded-xl p-4 hover:border-blue-300 hover:bg-blue-50 transition-all">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <p className="font-bold text-gray-900 mb-1">{job.job_title}</p>
                      <div className="flex items-center gap-4 text-sm text-gray-600">
                        <span className="flex items-center gap-1">
                          <Building2 className="h-4 w-4" />
                          {job.department}
                        </span>
                        <span className="flex items-center gap-1">
                          <Clock className="h-4 w-4" />
                          Posted: {new Date(job.posted_date).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className={`px-4 py-2 rounded-lg text-sm font-semibold flex items-center gap-2 ${
                        job.current_status === 'Posted' ? 'bg-green-100 text-green-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {job.current_status === 'Posted' && <CheckCircle className="h-4 w-4" />}
                        {job.current_status}
                      </span>
                      <Link
                        href={`/employer/jobs/${job.job_id}/candidates`}
                        className="px-4 py-2 bg-purple-600 text-white rounded-lg text-sm font-medium hover:bg-purple-700 transition-colors"
                      >
                        AI Candidates →
                      </Link>
                      <Link
                        href={`/employer/jobs/${job.job_id}`}
                        className="text-blue-600 hover:text-blue-700 font-medium text-sm hover:underline"
                      >
                        Edit →
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            {profile.open_jobs.length > 5 && (
              <Link
                href="/employer/jobs"
                className="block text-center text-blue-600 font-bold mt-6 py-3 px-6 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
              >
                View all {profile.open_jobs.length} jobs →
              </Link>
            )}
          </div>
        ) : (
          <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
            <div className="bg-gray-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
              <Briefcase className="h-10 w-10 text-gray-400" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">No Job Postings Yet</h3>
            <p className="text-gray-600 mb-6">Create your first job posting to start attracting talent</p>
            <Link
              href="/employer/jobs/new"
              className="inline-flex items-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              <Plus className="h-5 w-5" />
              Post a Job
            </Link>
          </div>
        )}
      </main>
    </div>
  );
}


'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useEmployerAuth } from '@/hooks/useAuth';
import { employerService } from '@/services/employer-service';
import { EmployerProfile } from '@/types';
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
  Target
} from 'lucide-react';

export default function EmployerDashboard() {
  // Use the custom authentication hook for employer-specific protection
  // This implements the protected routes strategy from frontend_auth.txt
  const { user, isLoading: authLoading, logout } = useEmployerAuth();
  const [profile, setProfile] = useState<EmployerProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [avgMatchScore, setAvgMatchScore] = useState<number>(0);
  const [loadingMatchScore, setLoadingMatchScore] = useState(false);

  // Load profile data once authentication is confirmed
  useEffect(() => {
    if (!authLoading && user) {
      loadProfile();
    }
  }, [authLoading, user]);

  const loadProfile = async () => {
    try {
      const data = await employerService.getProfile();
      setProfile(data);
      // Load AI match scores after profile loads
      if (data.open_jobs.length > 0) {
        loadMatchScores(data.open_jobs);
      }
    } catch (error) {
      console.error('Failed to load profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadMatchScores = async (jobs: any[]) => {
    setLoadingMatchScore(true);
    try {
      // Fetch top candidates for each job (limit to 5 to speed up)
      const scoresPromises = jobs.slice(0, 5).map(job => 
        employerService.getCandidateRecommendations(job.job_id, 5, 0)
          .catch(() => []) // Return empty array if fails
      );
      
      const allCandidates = await Promise.all(scoresPromises);
      
      // Calculate average of top match scores across all jobs
      let totalScore = 0;
      let jobsWithCandidates = 0;
      
      allCandidates.forEach(candidates => {
        if (candidates.length > 0) {
          // Get the best match score for this job
          const topScore = candidates[0].match_score;
          totalScore += topScore;
          jobsWithCandidates++;
        }
      });
      
      const avgScore = jobsWithCandidates > 0 ? totalScore / jobsWithCandidates : 0;
      setAvgMatchScore(Math.round(avgScore));
    } catch (error) {
      console.error('Failed to load match scores:', error);
      setAvgMatchScore(0);
    } finally {
      setLoadingMatchScore(false);
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
              <span className="ml-2 text-2xl font-bold text-gray-900">JobPortal</span>
            </Link>
            <div className="flex items-center gap-6">
              <span className="text-gray-700 font-medium hidden sm:block">
                {profile?.company_name}
              </span>
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
          <div className="flex items-center gap-3 mb-2">
            <Building2 className="h-8 w-8" />
            <h1 className="text-3xl md:text-4xl font-bold">
              {profile?.company_name}
            </h1>
          </div>
          <p className="text-blue-100 text-lg">
            Manage your job postings and find the perfect candidates.
          </p>
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

          {/* Match Rate */}
          <Link
            href="/employer/jobs"
            className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all hover:-translate-y-1 cursor-pointer relative overflow-hidden"
          >
            {loadingMatchScore && (
              <div className="absolute inset-0 bg-white/80 flex items-center justify-center z-10">
                <div className="w-6 h-6 border-3 border-amber-600 border-t-transparent rounded-full animate-spin"></div>
              </div>
            )}
            <div className="flex items-center justify-between mb-4">
              <div className="bg-gradient-to-br from-amber-100 to-amber-200 p-3 rounded-lg">
                <Target className="h-8 w-8 text-amber-600" />
              </div>
              <span className="text-3xl font-bold text-gray-900">
                {avgMatchScore}%
              </span>
            </div>
            <h3 className="text-gray-600 font-medium">AI Match Rate</h3>
            <p className="text-sm text-gray-500 mt-1">Average best match score</p>
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
            <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <Building2 className="h-6 w-6 text-blue-600" />
              Company Information
            </h3>
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


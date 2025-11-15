'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useSeekerAuth } from '@/hooks/useAuth';
import { seekerService } from '@/services/seeker-service';
import { JobRecommendation } from '@/types';
import { 
  Sparkles, 
  Briefcase, 
  Brain, 
  TrendingUp,
  MapPin,
  DollarSign,
  GraduationCap,
  Tag,
  Building2,
  Calendar,
  ChevronRight,
  AlertCircle,
  Loader2
} from 'lucide-react';

export default function RecommendationsPage() {
  const { user, isLoading: authLoading, logout } = useSeekerAuth();
  const [recommendations, setRecommendations] = useState<JobRecommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedJob, setSelectedJob] = useState<JobRecommendation | null>(null);
  const [applying, setApplying] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && user) {
      loadRecommendations();
    }
  }, [authLoading, user]);

  const loadRecommendations = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await seekerService.getRecommendations();
      setRecommendations(data);
    } catch (error: any) {
      console.error('Failed to load recommendations:', error);
      setError(error.response?.data?.detail || 'Failed to load recommendations. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleApply = async (job: JobRecommendation) => {
    try {
      setApplying(job.job_id);
      await seekerService.applyForJob(job.job_id, job.employer_id);
      alert('Application submitted successfully!');
    } catch (error: any) {
      console.error('Failed to apply:', error);
      alert(error.response?.data?.detail || 'Failed to submit application. Please try again.');
    } finally {
      setApplying(null);
    }
  };

  const getMatchColor = (score: number) => {
    if (score >= 86) return 'text-green-600 bg-green-100 border-green-200';
    if (score >= 71) return 'text-blue-600 bg-blue-100 border-blue-200';
    if (score >= 41) return 'text-yellow-600 bg-yellow-100 border-yellow-200';
    return 'text-gray-600 bg-gray-100 border-gray-200';
  };

  const getMatchLabel = (score: number) => {
    if (score >= 86) return 'Excellent Match';
    if (score >= 71) return 'Good Match';
    if (score >= 41) return 'Moderate Match';
    return 'Poor Match';
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-emerald-50 to-white">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <Link href="/seeker/dashboard" className="text-2xl font-bold text-emerald-600 hover:text-emerald-700 transition-colors">
              Job Portal
            </Link>
            <nav className="flex items-center gap-6">
              <Link 
                href="/seeker/dashboard" 
                className="text-gray-700 hover:text-emerald-600 transition-colors font-medium"
              >
                Dashboard
              </Link>
              <Link 
                href="/seeker/jobs" 
                className="text-gray-700 hover:text-emerald-600 transition-colors font-medium"
              >
                Search Jobs
              </Link>
              <Link 
                href="/seeker/applications" 
                className="text-gray-700 hover:text-emerald-600 transition-colors font-medium"
              >
                My Applications
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
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-purple-100 to-emerald-100 rounded-lg">
                <Sparkles className="h-6 w-6 text-purple-600" />
              </div>
              <div>
                <h1 className="text-4xl font-bold text-gray-900">AI Job Recommendations</h1>
                <p className="text-gray-600">Personalized opportunities powered by artificial intelligence</p>
              </div>
            </div>
            <button
              onClick={loadRecommendations}
              disabled={loading}
              className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors font-medium disabled:opacity-50"
            >
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Brain className="h-4 w-4" />}
              Refresh
            </button>
          </div>
        </div>

        {loading ? (
          <div className="text-center py-16">
            <div className="inline-flex items-center justify-center w-16 h-16 mb-4 bg-emerald-100 rounded-full">
              <div className="w-8 h-8 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin"></div>
            </div>
            <p className="text-xl text-gray-600">Analyzing your profile and finding matches...</p>
          </div>
        ) : error ? (
          <div className="bg-red-50 border-2 border-red-200 rounded-xl p-6">
            <div className="flex items-start gap-4">
              <div className="p-2 bg-red-100 rounded-lg">
                <AlertCircle className="h-6 w-6 text-red-600" />
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-bold text-red-900 mb-2">Error Loading Recommendations</h3>
                <p className="text-red-800 mb-3">{error}</p>
                <button
                  onClick={loadRecommendations}
                  className="inline-flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
                >
                  Try Again
                </button>
              </div>
            </div>
          </div>
        ) : recommendations.length === 0 ? (
          <div className="bg-blue-50 border-2 border-blue-200 rounded-xl p-8 text-center">
            <Brain className="h-16 w-16 text-blue-600 mx-auto mb-4" />
            <h3 className="text-2xl font-bold text-blue-900 mb-4">
              No recommendations available yet
            </h3>
            <p className="text-blue-800 mb-6 max-w-xl mx-auto">
              We couldn't find any matching jobs at the moment. Try updating your profile with more skills or check back later for new opportunities.
            </p>
            <Link
              href="/seeker/profile"
              className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              Update Profile
            </Link>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Stats Summary */}
            <div className="grid md:grid-cols-3 gap-4 mb-6">
              <div className="bg-white rounded-xl shadow-md p-6 border-2 border-purple-100">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <Briefcase className="h-6 w-6 text-purple-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Total Matches</p>
                    <p className="text-2xl font-bold text-gray-900">{recommendations.length}</p>
                  </div>
                </div>
              </div>
              <div className="bg-white rounded-xl shadow-md p-6 border-2 border-green-100">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-green-100 rounded-lg">
                    <TrendingUp className="h-6 w-6 text-green-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Best Match</p>
                    <p className="text-2xl font-bold text-gray-900">{Math.round(recommendations[0]?.match_score || 0)}%</p>
                  </div>
                </div>
              </div>
              <div className="bg-white rounded-xl shadow-md p-6 border-2 border-blue-100">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Sparkles className="h-6 w-6 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Excellent Matches</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {recommendations.filter(r => r.match_score >= 86).length}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Recommendations List */}
            <div className="space-y-4">
              {recommendations.map((job) => (
                <div
                  key={job.job_id}
                  className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all p-6 border-2 border-gray-100 hover:border-emerald-200"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <div className="flex items-start gap-3 mb-2">
                        <div className="p-2 bg-emerald-50 rounded-lg">
                          <Building2 className="h-5 w-5 text-emerald-600" />
                        </div>
                        <div>
                          <h3 className="text-xl font-bold text-gray-900 mb-1">{job.job_title}</h3>
                          <p className="text-gray-600 font-medium">{job.company_name}</p>
                        </div>
                      </div>
                    </div>
                    <div className={`px-4 py-2 rounded-full border-2 ${getMatchColor(job.match_score)}`}>
                      <p className="text-sm font-semibold">{Math.round(job.match_score)}% Match</p>
                      <p className="text-xs">{getMatchLabel(job.match_score)}</p>
                    </div>
                  </div>

                  {/* Job Details */}
                  <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
                    <div className="flex items-center gap-2">
                      <DollarSign className="h-4 w-4 text-gray-500" />
                      <span className="text-sm text-gray-700">
                        ${job.pay_range[0].toLocaleString()} - ${job.pay_range[1].toLocaleString()} {job.pay_unit}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <GraduationCap className="h-4 w-4 text-gray-500" />
                      <span className="text-sm text-gray-700">{job.education_level} in {job.edu_focus}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Briefcase className="h-4 w-4 text-gray-500" />
                      <span className="text-sm text-gray-700">{job.department}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Calendar className="h-4 w-4 text-gray-500" />
                      <span className="text-sm text-gray-700">
                        {job.posted_date ? new Date(job.posted_date).toLocaleDateString() : 'Recently posted'}
                      </span>
                    </div>
                  </div>

                  {/* Skills */}
                  <div className="mb-4">
                    <p className="text-sm font-semibold text-gray-700 mb-2">Required Skills:</p>
                    <div className="flex flex-wrap gap-2">
                      {job.key_skills.map((skill, idx) => (
                        <span
                          key={idx}
                          className="inline-flex items-center gap-1 bg-emerald-50 text-emerald-700 px-3 py-1 rounded-full text-xs font-medium"
                        >
                          <Tag className="h-3 w-3" />
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Score Breakdown */}
                  <div className="bg-gray-50 rounded-lg p-4 mb-4">
                    <p className="text-sm font-semibold text-gray-700 mb-3">Match Breakdown:</p>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Skills</p>
                        <p className="text-lg font-bold text-gray-900">{Math.round(job.score_breakdown.skills_score)}%</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Education</p>
                        <p className="text-lg font-bold text-gray-900">{Math.round(job.score_breakdown.education_score)}%</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Salary</p>
                        <p className="text-lg font-bold text-gray-900">{Math.round(job.score_breakdown.pay_score)}%</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600 mb-1">Experience</p>
                        <p className="text-lg font-bold text-gray-900">{Math.round(job.score_breakdown.experience_score)}%</p>
                      </div>
                    </div>
                    {job.score_breakdown.reasoning && (
                      <div className="mt-3 pt-3 border-t border-gray-200">
                        <p className="text-xs text-gray-600 italic">{job.score_breakdown.reasoning}</p>
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex gap-3">
                    <button
                      onClick={() => setSelectedJob(job)}
                      className="flex-1 inline-flex items-center justify-center gap-2 px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium"
                    >
                      View Details
                      <ChevronRight className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleApply(job)}
                      disabled={applying === job.job_id}
                      className="flex-1 inline-flex items-center justify-center gap-2 px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors font-medium shadow-md hover:shadow-lg disabled:opacity-50"
                    >
                      {applying === job.job_id ? (
                        <>
                          <Loader2 className="h-4 w-4 animate-spin" />
                          Applying...
                        </>
                      ) : (
                        <>
                          <Briefcase className="h-4 w-4" />
                          Apply Now
                        </>
                      )}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Job Details Modal */}
        {selectedJob && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-2xl max-w-3xl w-full max-h-[80vh] overflow-y-auto p-8">
              <div className="flex items-start justify-between mb-6">
                <div>
                  <h2 className="text-3xl font-bold text-gray-900 mb-2">{selectedJob.job_title}</h2>
                  <p className="text-lg text-gray-600">{selectedJob.company_name}</p>
                </div>
                <button
                  onClick={() => setSelectedJob(null)}
                  className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <span className="text-2xl">&times;</span>
                </button>
              </div>
              
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Job Description</h3>
                  <p className="text-gray-700 whitespace-pre-wrap">{selectedJob.job_description}</p>
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Hiring Manager</h3>
                  <p className="text-gray-700">{selectedJob.hire_mgr_first} {selectedJob.hire_mgr_last}</p>
                </div>

                <button
                  onClick={() => {
                    handleApply(selectedJob);
                    setSelectedJob(null);
                  }}
                  disabled={applying === selectedJob.job_id}
                  className="w-full inline-flex items-center justify-center gap-2 px-6 py-4 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors font-medium shadow-md hover:shadow-lg disabled:opacity-50"
                >
                  {applying === selectedJob.job_id ? (
                    <>
                      <Loader2 className="h-5 w-5 animate-spin" />
                      Applying...
                    </>
                  ) : (
                    <>
                      <Briefcase className="h-5 w-5" />
                      Apply for this Position
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { useEmployerAuth } from '@/hooks/useAuth';
import { employerService } from '@/services/employer-service';
import { CandidateRecommendation, Job } from '@/types';
import { 
  ArrowLeft,
  User,
  Mail,
  Phone,
  MapPin,
  GraduationCap,
  DollarSign,
  Target,
  Briefcase,
  CheckCircle,
  TrendingUp,
  Award,
  FileText,
  Calendar,
  Sparkles
} from 'lucide-react';

export default function CandidateRecommendationsPage() {
  const { user, isLoading: authLoading, logout } = useEmployerAuth();
  const params = useParams();
  const router = useRouter();
  const jobId = params.jobId as string;

  const [job, setJob] = useState<Job | null>(null);
  const [candidates, setCandidates] = useState<CandidateRecommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [minScore, setMinScore] = useState(0);
  const [showAppliedOnly, setShowAppliedOnly] = useState(false);

  useEffect(() => {
    if (!authLoading && user) {
      loadData();
    }
  }, [authLoading, user, jobId]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [jobData, candidatesData] = await Promise.all([
        employerService.getJob(jobId),
        employerService.getCandidateRecommendations(jobId, 50, 0)
      ]);
      setJob(jobData);
      setCandidates(candidatesData);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredCandidates = candidates.filter(candidate => {
    if (showAppliedOnly && !candidate.has_applied) return false;
    if (candidate.match_score < minScore) return false;
    return true;
  });

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-700 bg-green-100 border-green-300';
    if (score >= 60) return 'text-blue-700 bg-blue-100 border-blue-300';
    if (score >= 40) return 'text-amber-700 bg-amber-100 border-amber-300';
    return 'text-gray-700 bg-gray-100 border-gray-300';
  };

  const getScoreBadgeColor = (score: number) => {
    if (score >= 80) return 'bg-green-500';
    if (score >= 60) return 'bg-blue-500';
    if (score >= 40) return 'bg-amber-500';
    return 'bg-gray-500';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-xl text-gray-600">Finding AI-matched candidates...</p>
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
      <main className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Back Button */}
        <Link
          href="/employer/jobs"
          className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-6 font-medium"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Jobs
        </Link>

        {/* Job Header */}
        {job && (
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8 border border-gray-100">
            <div className="flex items-start justify-between mb-6">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <div className="p-3 bg-blue-100 rounded-lg">
                    <Briefcase className="h-8 w-8 text-blue-600" />
                  </div>
                  <div>
                    <h1 className="text-3xl font-bold text-gray-900">{job.job_title}</h1>
                    <p className="text-gray-600 text-lg">{job.department}</p>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Sparkles className="h-6 w-6 text-purple-600" />
                <span className="text-lg font-semibold text-purple-600">AI-Powered Matching</span>
              </div>
            </div>

            <div className="grid md:grid-cols-4 gap-4 p-4 bg-gray-50 rounded-lg">
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
                <GraduationCap className="h-5 w-5 text-blue-600" />
                <div>
                  <p className="text-xs text-gray-600">Education</p>
                  <p className="font-medium text-gray-900">{job.education_level}</p>
                  <p className="text-xs text-gray-500">{job.edu_focus}</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <User className="h-5 w-5 text-blue-600" />
                <div>
                  <p className="text-xs text-gray-600">Hiring Manager</p>
                  <p className="font-medium text-gray-900">
                    {job.hire_mgr_first} {job.hire_mgr_last}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Target className="h-5 w-5 text-blue-600" />
                <div>
                  <p className="text-xs text-gray-600">Candidates Found</p>
                  <p className="font-medium text-gray-900">{candidates.length} matches</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-6 border border-gray-100">
          <div className="flex flex-wrap items-center gap-4">
            <div className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-gray-600" />
              <span className="font-medium text-gray-700">Filters:</span>
            </div>
            
            <div className="flex items-center gap-2">
              <label className="text-sm text-gray-600">Min Match Score:</label>
              <select
                value={minScore}
                onChange={(e) => setMinScore(Number(e.target.value))}
                className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value={0}>All (0%+)</option>
                <option value={40}>Good (40%+)</option>
                <option value={60}>Great (60%+)</option>
                <option value={80}>Excellent (80%+)</option>
              </select>
            </div>

            <button
              onClick={() => setShowAppliedOnly(!showAppliedOnly)}
              className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                showAppliedOnly
                  ? 'bg-green-100 text-green-700 border-2 border-green-300'
                  : 'bg-gray-100 text-gray-700 border-2 border-gray-300 hover:bg-gray-200'
              }`}
            >
              <span className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4" />
                {showAppliedOnly ? 'Applied Only' : 'Show Applied Only'}
              </span>
            </button>

            <div className="ml-auto text-sm text-gray-600">
              Showing <span className="font-bold text-gray-900">{filteredCandidates.length}</span> of {candidates.length} candidates
            </div>
          </div>
        </div>

        {/* Candidates List */}
        {filteredCandidates.length === 0 ? (
          <div className="text-center py-16 bg-white rounded-2xl shadow-lg border border-gray-100">
            <div className="inline-flex items-center justify-center w-20 h-20 mb-6 bg-gray-50 rounded-full">
              <User className="h-10 w-10 text-gray-400" />
            </div>
            <h3 className="text-2xl font-semibold text-gray-900 mb-2">No Candidates Found</h3>
            <p className="text-gray-600 mb-4">
              {minScore > 0 || showAppliedOnly
                ? 'Try adjusting your filters to see more candidates'
                : 'No matching candidates available at this time'}
            </p>
            {(minScore > 0 || showAppliedOnly) && (
              <button
                onClick={() => {
                  setMinScore(0);
                  setShowAppliedOnly(false);
                }}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                Reset Filters
              </button>
            )}
          </div>
        ) : (
          <div className="space-y-4">
            {filteredCandidates.map((candidate) => (
              <div 
                key={candidate.seeker_id} 
                className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all border border-gray-100 p-6"
              >
                {/* Candidate Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-start gap-4 flex-1">
                    <div className="p-4 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl">
                      <User className="h-8 w-8 text-white" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-2xl font-bold text-gray-900">
                          {candidate.first_name} {candidate.last_name}
                        </h3>
                        {candidate.has_applied && (
                          <span className="flex items-center gap-1 px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                            <CheckCircle className="h-4 w-4" />
                            Applied
                          </span>
                        )}
                      </div>
                      <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600 mb-3">
                        <span className="flex items-center gap-1">
                          <Mail className="h-4 w-4" />
                          {candidate.email}
                        </span>
                        <span className="flex items-center gap-1">
                          <Phone className="h-4 w-4" />
                          {candidate.phone}
                        </span>
                        <span className="flex items-center gap-1">
                          <MapPin className="h-4 w-4" />
                          {candidate.address.city}, {candidate.address.state}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Match Score Badge */}
                  <div className={`flex flex-col items-center px-6 py-4 rounded-xl border-2 ${getScoreColor(candidate.match_score)}`}>
                    <div className="flex items-center gap-2 mb-1">
                      <Target className="h-5 w-5" />
                      <span className="text-3xl font-bold">{Math.round(candidate.match_score)}%</span>
                    </div>
                    <span className="text-xs font-medium uppercase">Match Score</span>
                  </div>
                </div>

                {/* Score Breakdown */}
                <div className="mb-4 p-4 bg-gray-50 rounded-lg">
                  <h4 className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                    <Award className="h-4 w-4" />
                    Score Breakdown
                  </h4>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-3">
                    <div>
                      <div className="flex justify-between text-xs text-gray-600 mb-1">
                        <span>Skills</span>
                        <span className="font-medium">{Math.round(candidate.score_breakdown.skills_score)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${getScoreBadgeColor(candidate.score_breakdown.skills_score)}`}
                          style={{ width: `${candidate.score_breakdown.skills_score}%` }}
                        ></div>
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between text-xs text-gray-600 mb-1">
                        <span>Education</span>
                        <span className="font-medium">{Math.round(candidate.score_breakdown.education_score)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${getScoreBadgeColor(candidate.score_breakdown.education_score)}`}
                          style={{ width: `${candidate.score_breakdown.education_score}%` }}
                        ></div>
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between text-xs text-gray-600 mb-1">
                        <span>Pay Range</span>
                        <span className="font-medium">{Math.round(candidate.score_breakdown.pay_score)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${getScoreBadgeColor(candidate.score_breakdown.pay_score)}`}
                          style={{ width: `${candidate.score_breakdown.pay_score}%` }}
                        ></div>
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between text-xs text-gray-600 mb-1">
                        <span>Experience</span>
                        <span className="font-medium">{Math.round(candidate.score_breakdown.experience_score)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${getScoreBadgeColor(candidate.score_breakdown.experience_score)}`}
                          style={{ width: `${candidate.score_breakdown.experience_score}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                  <p className="text-xs text-gray-600 italic">
                    <span className="font-medium">AI Analysis:</span> {candidate.score_breakdown.reasoning}
                  </p>
                </div>

                {/* Candidate Details */}
                <div className="grid md:grid-cols-2 gap-4 mb-4 p-4 bg-blue-50 rounded-lg border border-blue-100">
                  <div className="flex items-center gap-2">
                    <GraduationCap className="h-5 w-5 text-blue-600" />
                    <div>
                      <p className="text-xs text-gray-600">Education</p>
                      <p className="font-medium text-gray-900">{candidate.education_level}</p>
                      <p className="text-xs text-gray-500">{candidate.edu_focus}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <DollarSign className="h-5 w-5 text-blue-600" />
                    <div>
                      <p className="text-xs text-gray-600">Desired Salary</p>
                      <p className="font-medium text-gray-900">
                        ${candidate.pay_range[0].toLocaleString()} - ${candidate.pay_range[1].toLocaleString()}
                      </p>
                      <p className="text-xs text-gray-500">{candidate.pay_unit}</p>
                    </div>
                  </div>
                </div>

                {/* Skills */}
                {candidate.key_skills.length > 0 && (
                  <div className="mb-4">
                    <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                      <Briefcase className="h-4 w-4" />
                      Skills
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {candidate.key_skills.map((skill, idx) => (
                        <span
                          key={idx}
                          className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Resume Preview */}
                {candidate.resume_preview && (
                  <div className="mb-4">
                    <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                      <FileText className="h-4 w-4" />
                      Resume Preview
                    </h4>
                    <p className="text-sm text-gray-700 bg-gray-50 p-3 rounded-lg border border-gray-200 line-clamp-3">
                      {candidate.resume_preview}
                    </p>
                  </div>
                )}

                {/* Actions */}
                <div className="flex items-center gap-3 pt-4 border-t border-gray-200">
                  <a
                    href={`mailto:${candidate.email}`}
                    className="inline-flex items-center gap-2 px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
                  >
                    <Mail className="h-4 w-4" />
                    Contact Candidate
                  </a>
                  <button
                    className="inline-flex items-center gap-2 px-6 py-2.5 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors font-medium"
                    disabled
                    title="Coming soon: Schedule interview via n8n"
                  >
                    <Calendar className="h-4 w-4" />
                    Schedule Interview (Coming Soon)
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


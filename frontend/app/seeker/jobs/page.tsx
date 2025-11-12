'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useSeekerAuth } from '@/hooks/useAuth';
import { seekerService } from '@/services/seeker-service';
import { Job } from '@/types';
import { 
  Search, 
  Briefcase, 
  Building2, 
  DollarSign, 
  GraduationCap, 
  Calendar, 
  User,
  Tag
} from 'lucide-react';

export default function JobSearchPage() {
  // Use the custom authentication hook for seeker-specific protection
  const { user, isLoading: authLoading, logout } = useSeekerAuth();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchType, setSearchType] = useState<'title' | 'company' | 'skill'>('title');

  // Load jobs once authentication is confirmed
  useEffect(() => {
    if (!authLoading && user) {
      loadJobs();
    }
  }, [authLoading, user]);

  const loadJobs = async () => {
    try {
      const data = await seekerService.searchJobs();
      setJobs(data);
    } catch (error) {
      console.error('Failed to load jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      loadJobs();
      return;
    }

    setLoading(true);
    try {
      const params: any = {};
      if (searchType === 'title') params.title = searchQuery;
      else if (searchType === 'company') params.company = searchQuery;
      else if (searchType === 'skill') params.skill = searchQuery;

      const data = await seekerService.searchJobs(params);
      setJobs(data);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleApply = async (job: Job) => {
    if (!job.employer_id) return;
    
    try {
      await seekerService.applyForJob(job.job_id, job.employer_id);
      // Reload jobs to update UI
      await loadJobs();
    } catch (error: any) {
      console.error('Failed to apply:', error);
    }
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
                href="/seeker/recommendations" 
                className="text-gray-700 hover:text-emerald-600 transition-colors font-medium"
              >
                AI Recommendations
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
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-emerald-100 rounded-lg">
              <Search className="h-6 w-6 text-emerald-600" />
            </div>
            <h1 className="text-4xl font-bold text-gray-900">Search Jobs</h1>
          </div>
          <p className="text-gray-600 ml-14">Find your next career opportunity</p>
        </div>

        {/* Search Form */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6 mb-8">
          <form onSubmit={handleSearch}>
            <div className="flex flex-col md:flex-row gap-4">
              <select
                value={searchType}
                onChange={(e) => setSearchType(e.target.value as any)}
                className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 font-medium text-gray-900 bg-white"
              >
                <option value="title">Job Title</option>
                <option value="company">Company</option>
                <option value="skill">Skill</option>
              </select>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder={`Search by ${searchType}...`}
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              />
              <button
                type="submit"
                className="inline-flex items-center justify-center gap-2 bg-emerald-600 text-white px-6 py-3 rounded-lg hover:bg-emerald-700 transition-colors font-medium"
              >
                <Search className="h-5 w-5" />
                Search
              </button>
              <button
                type="button"
                onClick={() => {
                  setSearchQuery('');
                  loadJobs();
                }}
                className="px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium"
              >
                Clear
              </button>
            </div>
          </form>
        </div>

        {/* Job Listings */}
        {loading ? (
          <div className="text-center py-16">
            <div className="inline-flex items-center justify-center w-16 h-16 mb-4 bg-emerald-100 rounded-full">
              <div className="w-8 h-8 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin"></div>
            </div>
            <p className="text-xl text-gray-600">Loading opportunities...</p>
          </div>
        ) : jobs.length === 0 ? (
          <div className="text-center py-16 bg-white rounded-2xl shadow-lg border border-gray-100">
            <div className="inline-flex items-center justify-center w-20 h-20 mb-6 bg-emerald-50 rounded-full">
              <Briefcase className="h-10 w-10 text-emerald-600" />
            </div>
            <h3 className="text-2xl font-semibold text-gray-900 mb-2">No Jobs Found</h3>
            <p className="text-gray-600">Try adjusting your search criteria</p>
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
                    <div className="p-3 bg-emerald-50 rounded-lg">
                      <Briefcase className="h-6 w-6 text-emerald-600" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold text-gray-900 mb-1">{job.job_title}</h3>
                      <div className="flex items-center gap-2 text-gray-600 mb-1">
                        <Building2 className="h-4 w-4" />
                        <span className="font-medium">{job.company_name}</span>
                      </div>
                      <p className="text-sm text-gray-500">{job.department}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => handleApply(job)}
                    className="inline-flex items-center gap-2 px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors font-medium shadow-md hover:shadow-lg ml-4"
                  >
                    <Briefcase className="h-5 w-5" />
                    Apply Now
                  </button>
                </div>

                <p className="text-gray-700 mb-4 line-clamp-3">{job.job_description}</p>

                <div className="grid md:grid-cols-2 gap-4 mb-4 p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-2">
                    <DollarSign className="h-5 w-5 text-emerald-600" />
                    <div>
                      <p className="text-xs text-gray-600">Salary Range</p>
                      <p className="font-medium text-gray-900">
                        ${job.pay_range[0].toLocaleString()} - ${job.pay_range[1].toLocaleString()}
                      </p>
                      <p className="text-xs text-gray-500">{job.pay_unit}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <GraduationCap className="h-5 w-5 text-emerald-600" />
                    <div>
                      <p className="text-xs text-gray-600">Education Required</p>
                      <p className="font-medium text-gray-900">{job.education_level}</p>
                      <p className="text-xs text-gray-500">{job.edu_focus}</p>
                    </div>
                  </div>
                </div>

                {job.key_skills.length > 0 && (
                  <div className="mb-4">
                    <div className="flex items-center gap-2 mb-2">
                      <Tag className="h-4 w-4 text-gray-600" />
                      <p className="text-sm text-gray-600 font-medium">Required Skills</p>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {job.key_skills.map((skill, index) => (
                        <span
                          key={index}
                          className="bg-emerald-100 text-emerald-800 px-3 py-1 rounded-full text-sm font-medium"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <div className="flex items-center gap-4 pt-4 border-t border-gray-200 text-sm text-gray-500">
                  <div className="flex items-center gap-1">
                    <Calendar className="h-4 w-4" />
                    <span>Posted: {new Date(job.posted_date).toLocaleDateString()}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <User className="h-4 w-4" />
                    <span>Manager: {job.hiring_manager || `${job.hire_mgr_first} ${job.hire_mgr_last}`}</span>
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


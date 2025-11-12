'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useSeekerAuth } from '@/hooks/useAuth';
import { seekerService } from '@/services/seeker-service';
import { 
  Sparkles, 
  Briefcase, 
  Brain, 
  TrendingUp, 
  Zap,
  AlertCircle
} from 'lucide-react';

export default function RecommendationsPage() {
  // Use the custom authentication hook for seeker-specific protection
  const { user, isLoading: authLoading, logout } = useSeekerAuth();
  const [recommendationData, setRecommendationData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // Load recommendations once authentication is confirmed
  useEffect(() => {
    if (!authLoading && user) {
      loadRecommendations();
    }
  }, [authLoading, user]);

  const loadRecommendations = async () => {
    try {
      const data = await seekerService.getRecommendations();
      setRecommendationData(data);
    } catch (error) {
      console.error('Failed to load recommendations:', error);
    } finally {
      setLoading(false);
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
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-gradient-to-br from-purple-100 to-emerald-100 rounded-lg">
              <Sparkles className="h-6 w-6 text-purple-600" />
            </div>
            <h1 className="text-4xl font-bold text-gray-900">AI Job Recommendations</h1>
          </div>
          <p className="text-gray-600 ml-14">Personalized opportunities powered by artificial intelligence</p>
        </div>

        {loading ? (
          <div className="text-center py-16">
            <div className="inline-flex items-center justify-center w-16 h-16 mb-4 bg-emerald-100 rounded-full">
              <div className="w-8 h-8 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin"></div>
            </div>
            <p className="text-xl text-gray-600">Loading recommendations...</p>
          </div>
        ) : (
          <div className="space-y-8">
            {/* Coming Soon Banner */}
            <div className="relative overflow-hidden bg-gradient-to-br from-purple-500 via-emerald-500 to-blue-500 rounded-3xl shadow-2xl p-12">
              <div className="absolute inset-0 bg-black opacity-10"></div>
              <div className="relative z-10 text-center text-white">
                <div className="inline-flex items-center justify-center w-24 h-24 mb-6 bg-white bg-opacity-20 rounded-full backdrop-blur-sm">
                  <Brain className="h-12 w-12 text-white animate-pulse" />
                </div>
                <h2 className="text-5xl font-bold mb-4">Coming Soon!</h2>
                <p className="text-2xl mb-6 text-white text-opacity-90">
                  AI-Powered Job Recommendations
                </p>
                <p className="text-lg max-w-2xl mx-auto mb-8 text-white text-opacity-80">
                  We're building an intelligent system that will analyze your profile, skills, and preferences 
                  to deliver personalized job recommendations that perfectly match your career goals.
                </p>
                <div className="inline-flex items-center gap-2 px-6 py-3 bg-white text-purple-600 rounded-full font-semibold">
                  <Zap className="h-5 w-5" />
                  Under Development
                </div>
              </div>
            </div>

            {/* Feature Preview Cards */}
            <div className="grid md:grid-cols-3 gap-6">
              <div className="bg-white rounded-2xl shadow-lg p-6 border-2 border-purple-100 hover:border-purple-300 transition-all">
                <div className="bg-purple-100 w-14 h-14 rounded-xl flex items-center justify-center mb-4">
                  <Brain className="h-7 w-7 text-purple-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Smart Matching</h3>
                <p className="text-gray-600">
                  Advanced AI algorithms will analyze your skills, experience, and preferences to find the perfect job matches.
                </p>
              </div>

              <div className="bg-white rounded-2xl shadow-lg p-6 border-2 border-emerald-100 hover:border-emerald-300 transition-all">
                <div className="bg-emerald-100 w-14 h-14 rounded-xl flex items-center justify-center mb-4">
                  <TrendingUp className="h-7 w-7 text-emerald-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Match Scores</h3>
                <p className="text-gray-600">
                  See how well you match with each opportunity based on multiple factors including skills, education, and location.
                </p>
              </div>

              <div className="bg-white rounded-2xl shadow-lg p-6 border-2 border-blue-100 hover:border-blue-300 transition-all">
                <div className="bg-blue-100 w-14 h-14 rounded-xl flex items-center justify-center mb-4">
                  <Sparkles className="h-7 w-7 text-blue-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Personalized</h3>
                <p className="text-gray-600">
                  Recommendations tailored specifically to your career aspirations, skills, and desired salary range.
                </p>
              </div>
            </div>

            {/* Current Status Info */}
            {recommendationData && (
              <div className="bg-blue-50 border-2 border-blue-200 rounded-xl p-6">
                <div className="flex items-start gap-4">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <AlertCircle className="h-6 w-6 text-blue-600" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-blue-900 mb-2">Development Status</h3>
                    <p className="text-blue-800 mb-3">{recommendationData.message}</p>
                    <div className="flex items-center gap-2">
                      <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                        Status: {recommendationData.status}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Call to Action */}
            <div className="bg-white rounded-2xl shadow-lg p-8 text-center border border-gray-200">
              <Briefcase className="h-16 w-16 text-emerald-600 mx-auto mb-4" />
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                In the meantime, explore available jobs
              </h3>
              <p className="text-gray-600 mb-6 max-w-xl mx-auto">
                While we're building the AI recommendation system, you can browse and apply to jobs manually 
                using our job search feature.
              </p>
              <Link
                href="/seeker/jobs"
                className="inline-flex items-center gap-2 px-8 py-4 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors font-medium text-lg shadow-lg hover:shadow-xl"
              >
                <Briefcase className="h-5 w-5" />
                Search Jobs Now
              </Link>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}


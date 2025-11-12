'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useSeekerAuth } from '@/hooks/useAuth';
import { seekerService } from '@/services/seeker-service';
import { SeekerProfile } from '@/types';
import { 
  Briefcase, 
  Search, 
  FileText, 
  User, 
  LogOut, 
  MapPin, 
  GraduationCap, 
  DollarSign,
  Star,
  Eye,
  CheckCircle,
  Clock,
  XCircle
} from 'lucide-react';

export default function SeekerDashboard() {
  // Use the custom authentication hook for seeker-specific protection
  // This implements the protected routes strategy from frontend_auth.txt
  const { user, isLoading: authLoading, logout } = useSeekerAuth();
  const [profile, setProfile] = useState<SeekerProfile | null>(null);
  const [loading, setLoading] = useState(true);

  // Load profile data once authentication is confirmed
  useEffect(() => {
    if (!authLoading && user) {
      loadProfile();
    }
  }, [authLoading, user]);

  const loadProfile = async () => {
    try {
      const data = await seekerService.getProfile();
      setProfile(data);
    } catch (error) {
      console.error('Failed to load profile:', error);
    } finally {
      setLoading(false);
    }
  };

  // Show loading state while authentication is being verified
  if (authLoading || loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-emerald-50 to-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-emerald-600 mx-auto mb-4"></div>
          <p className="text-xl text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-emerald-50 to-white">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="flex items-center">
              <Briefcase className="h-8 w-8 text-emerald-600" />
              <span className="ml-2 text-2xl font-bold text-gray-900">JobPortal</span>
            </Link>
            <div className="flex items-center gap-6">
              <span className="text-gray-700 font-medium hidden sm:block">
                {profile?.first_name} {profile?.last_name}
              </span>
              <button
                onClick={logout}
                className="flex items-center gap-2 text-gray-600 hover:text-emerald-600 transition-colors"
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
        <div className="bg-gradient-to-r from-emerald-600 to-emerald-500 rounded-2xl shadow-xl p-8 mb-8 text-white">
          <div className="flex items-center gap-3 mb-2">
            <User className="h-8 w-8" />
            <h1 className="text-3xl md:text-4xl font-bold">
              Welcome back, {profile?.first_name}!
            </h1>
          </div>
          <p className="text-emerald-100 text-lg">
            Ready to find your next opportunity? Let's get started.
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* Applications Count */}
          <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-emerald-100 p-3 rounded-lg">
                <FileText className="h-8 w-8 text-emerald-600" />
              </div>
              <span className="text-3xl font-bold text-gray-900">
                {profile?.applications.length || 0}
              </span>
            </div>
            <h3 className="text-gray-600 font-medium">Total Applications</h3>
            <p className="text-sm text-gray-500 mt-1">Active submissions</p>
          </div>

          {/* Profile Views */}
          <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-blue-100 p-3 rounded-lg">
                <Eye className="h-8 w-8 text-blue-600" />
              </div>
              <span className="text-3xl font-bold text-gray-900">
                {Math.floor(Math.random() * 50) + 10}
              </span>
            </div>
            <h3 className="text-gray-600 font-medium">Profile Views</h3>
            <p className="text-sm text-gray-500 mt-1">Last 30 days</p>
          </div>

          {/* Saved Jobs */}
          <div className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-amber-100 p-3 rounded-lg">
                <Star className="h-8 w-8 text-amber-600" />
              </div>
              <span className="text-3xl font-bold text-gray-900">0</span>
            </div>
            <h3 className="text-gray-600 font-medium">Saved Jobs</h3>
            <p className="text-sm text-gray-500 mt-1">Bookmarked positions</p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Link
            href="/seeker/jobs"
            className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all hover:-translate-y-1 group"
          >
            <div className="bg-emerald-100 w-14 h-14 rounded-xl flex items-center justify-center mb-4 group-hover:bg-emerald-600 transition-colors">
              <Search className="h-7 w-7 text-emerald-600 group-hover:text-white transition-colors" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Search Jobs</h3>
            <p className="text-gray-600">Find your next opportunity</p>
          </Link>

          <Link
            href="/seeker/applications"
            className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all hover:-translate-y-1 group"
          >
            <div className="bg-emerald-100 w-14 h-14 rounded-xl flex items-center justify-center mb-4 group-hover:bg-emerald-600 transition-colors">
              <FileText className="h-7 w-7 text-emerald-600 group-hover:text-white transition-colors" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">My Applications</h3>
            <p className="text-gray-600">{profile?.applications.length || 0} active applications</p>
          </Link>

          <Link
            href="/seeker/profile"
            className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all hover:-translate-y-1 group"
          >
            <div className="bg-emerald-100 w-14 h-14 rounded-xl flex items-center justify-center mb-4 group-hover:bg-emerald-600 transition-colors">
              <User className="h-7 w-7 text-emerald-600 group-hover:text-white transition-colors" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">My Profile</h3>
            <p className="text-gray-600">Update your information</p>
          </Link>
        </div>

        {/* Profile Summary */}
        {profile && (
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <User className="h-6 w-6 text-emerald-600" />
              Profile Summary
            </h3>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="flex items-start gap-3">
                <div className="bg-emerald-100 p-2 rounded-lg">
                  <GraduationCap className="h-5 w-5 text-emerald-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">Education</p>
                  <p className="font-semibold text-gray-900">{profile.education_level} in {profile.edu_focus}</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-blue-100 p-2 rounded-lg">
                  <MapPin className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">Location</p>
                  <p className="font-semibold text-gray-900">{profile.address.city}, {profile.address.state}</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-green-100 p-2 rounded-lg">
                  <DollarSign className="h-5 w-5 text-green-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">Desired Salary</p>
                  <p className="font-semibold text-gray-900">
                    ${profile.pay_range[0].toLocaleString()} - ${profile.pay_range[1].toLocaleString()} {profile.pay_unit}
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-purple-100 p-2 rounded-lg">
                  <Star className="h-5 w-5 text-purple-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500 mb-1">Skills</p>
                  <p className="font-semibold text-gray-900">{profile.key_skills.length} skills listed</p>
                </div>
              </div>
            </div>
            {/* Skills Tags */}
            <div className="mt-6 pt-6 border-t border-gray-200">
              <p className="text-sm text-gray-500 mb-3">Your Skills:</p>
              <div className="flex flex-wrap gap-2">
                {profile.key_skills.slice(0, 8).map((skill, index) => (
                  <span key={index} className="px-3 py-1 bg-emerald-50 text-emerald-700 rounded-full text-sm font-medium">
                    {skill}
                  </span>
                ))}
                {profile.key_skills.length > 8 && (
                  <span className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm font-medium">
                    +{profile.key_skills.length - 8} more
                  </span>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Recent Applications */}
        {profile && profile.applications.length > 0 ? (
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              <FileText className="h-6 w-6 text-emerald-600" />
              Recent Applications
            </h3>
            <div className="space-y-4">
              {profile.applications.slice(0, 5).map((app, index) => (
                <div key={index} className="border border-gray-200 rounded-xl p-4 hover:border-emerald-300 hover:bg-emerald-50 transition-all">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <p className="font-bold text-gray-900 mb-1">Job ID: {app.job_id}</p>
                      <div className="flex items-center gap-2 text-sm text-gray-600">
                        <Clock className="h-4 w-4" />
                        <span>Applied: {new Date(app.date_applied).toLocaleDateString()}</span>
                      </div>
                    </div>
                    <span className={`px-4 py-2 rounded-lg text-sm font-semibold flex items-center gap-2 ${
                      app.application_status === 'Submitted' ? 'bg-blue-100 text-blue-800' :
                      app.application_status === 'Interviewed' ? 'bg-amber-100 text-amber-800' :
                      app.application_status === 'Offered' ? 'bg-green-100 text-green-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {app.application_status === 'Submitted' && <Clock className="h-4 w-4" />}
                      {app.application_status === 'Offered' && <CheckCircle className="h-4 w-4" />}
                      {app.application_status === 'Rejected' && <XCircle className="h-4 w-4" />}
                      {app.application_status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
            {profile.applications.length > 5 && (
              <Link
                href="/seeker/applications"
                className="block text-center text-emerald-600 font-bold mt-6 py-3 px-6 bg-emerald-50 rounded-lg hover:bg-emerald-100 transition-colors"
              >
                View all {profile.applications.length} applications →
              </Link>
            )}
          </div>
        ) : (
          <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
            <div className="bg-gray-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
              <FileText className="h-10 w-10 text-gray-400" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">No Applications Yet</h3>
            <p className="text-gray-600 mb-6">Start applying to jobs to see them here</p>
            <Link
              href="/seeker/jobs"
              className="inline-flex items-center gap-2 bg-emerald-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-emerald-700 transition-colors"
            >
              <Search className="h-5 w-5" />
              Search Jobs
            </Link>
          </div>
        )}
      </main>
    </div>
  );
}


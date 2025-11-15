'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useEmployerAuth } from '@/hooks/useAuth';
import { employerService } from '@/services/employer-service';
import { EmployerProfile } from '@/types';
import { 
  Building2,
  MapPin,
  User,
  Mail,
  Save,
  ArrowLeft,
  Briefcase,
  Award,
  FileText,
  CheckCircle,
  AlertCircle
} from 'lucide-react';

export default function EmployerProfilePage() {
  const { user, isLoading: authLoading, logout } = useEmployerAuth();
  const router = useRouter();
  const [profile, setProfile] = useState<EmployerProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{type: 'success' | 'error', text: string} | null>(null);
  
  // Form fields
  const [contactFirstName, setContactFirstName] = useState('');
  const [contactLastName, setContactLastName] = useState('');
  const [benefits, setBenefits] = useState('');

  useEffect(() => {
    if (!authLoading && user) {
      loadProfile();
    }
  }, [authLoading, user]);

  const loadProfile = async () => {
    try {
      const data = await employerService.getProfile();
      setProfile(data);
      setContactFirstName(data.contact_first_name);
      setContactLastName(data.contact_last_name);
      setBenefits(data.benefits || '');
    } catch (error) {
      console.error('Failed to load profile:', error);
      setMessage({ type: 'error', text: 'Failed to load profile' });
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);

    try {
      console.log('Submitting profile update:', {
        contact_first_name: contactFirstName,
        contact_last_name: contactLastName,
        benefits: benefits
      });

      const response = await employerService.updateProfile({
        contact_first_name: contactFirstName,
        contact_last_name: contactLastName,
        benefits: benefits
      });
      
      console.log('Profile update response:', response);
      setMessage({ type: 'success', text: 'Profile updated successfully!' });
      
      // Reload profile to get updated data
      setTimeout(() => {
        loadProfile();
      }, 1000);
    } catch (error: any) {
      console.error('Failed to update profile:', error);
      console.error('Error details:', error.response?.data);
      const errorMessage = error.response?.data?.detail || 'Failed to update profile. Please try again.';
      setMessage({ type: 'error', text: errorMessage });
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-xl text-gray-600">Loading your profile...</p>
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
              <span className="text-blue-600 font-semibold border-b-2 border-blue-600 pb-1">
                Company Profile
              </span>
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
          href="/employer/dashboard"
          className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-6 font-medium"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Dashboard
        </Link>

        {/* Page Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-3 bg-blue-100 rounded-lg">
              <Building2 className="h-8 w-8 text-blue-600" />
            </div>
            <div>
              <h1 className="text-4xl font-bold text-gray-900">Company Profile</h1>
              <p className="text-gray-600">Manage your company information and settings</p>
            </div>
          </div>
        </div>

        {/* Success/Error Message */}
        {message && (
          <div className={`mb-6 p-4 rounded-lg flex items-center gap-3 ${
            message.type === 'success' 
              ? 'bg-green-50 border border-green-200 text-green-800' 
              : 'bg-red-50 border border-red-200 text-red-800'
          }`}>
            {message.type === 'success' ? (
              <CheckCircle className="h-5 w-5" />
            ) : (
              <AlertCircle className="h-5 w-5" />
            )}
            <span className="font-medium">{message.text}</span>
          </div>
        )}

        {profile && (
          <>
            {/* Company Overview (Read-Only) */}
            <div className="bg-white rounded-2xl shadow-xl p-8 mb-8 border border-gray-100">
              <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <Building2 className="h-6 w-6 text-blue-600" />
                Company Overview
              </h2>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div className="flex items-start gap-3 p-4 bg-blue-50 rounded-lg border border-blue-100">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Building2 className="h-5 w-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Company Name</p>
                    <p className="font-bold text-gray-900 text-lg">{profile.company_name}</p>
                    <p className="text-xs text-gray-500 mt-1">This cannot be changed</p>
                  </div>
                </div>

                <div className="flex items-start gap-3 p-4 bg-green-50 rounded-lg border border-green-100">
                  <div className="p-2 bg-green-100 rounded-lg">
                    <MapPin className="h-5 w-5 text-green-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Location</p>
                    <p className="font-semibold text-gray-900">{profile.address.city}, {profile.address.state}</p>
                    <p className="text-sm text-gray-600">{profile.address.street}</p>
                    <p className="text-sm text-gray-600">{profile.address.zip_code}</p>
                  </div>
                </div>

                {profile.industry && profile.industry.length > 0 && (
                  <div className="flex items-start gap-3 p-4 bg-purple-50 rounded-lg border border-purple-100 md:col-span-2">
                    <div className="p-2 bg-purple-100 rounded-lg">
                      <Award className="h-5 w-5 text-purple-600" />
                    </div>
                    <div className="flex-1">
                      <p className="text-sm text-gray-600 mb-2">Industry</p>
                      <div className="flex flex-wrap gap-2">
                        {profile.industry.map((ind, idx) => (
                          <span
                            key={idx}
                            className="px-3 py-1.5 bg-purple-100 text-purple-700 rounded-full text-sm font-medium"
                          >
                            {ind.description} ({ind.code})
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Editable Information Form */}
            <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
              <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <User className="h-6 w-6 text-blue-600" />
                Contact & Company Information
              </h2>

              <div className="space-y-6">
                {/* Contact Person */}
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label htmlFor="contactFirstName" className="block text-sm font-semibold text-gray-700 mb-2">
                      Contact First Name *
                    </label>
                    <input
                      type="text"
                      id="contactFirstName"
                      value={contactFirstName}
                      onChange={(e) => setContactFirstName(e.target.value)}
                      required
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                      placeholder="John"
                    />
                  </div>

                  <div>
                    <label htmlFor="contactLastName" className="block text-sm font-semibold text-gray-700 mb-2">
                      Contact Last Name *
                    </label>
                    <input
                      type="text"
                      id="contactLastName"
                      value={contactLastName}
                      onChange={(e) => setContactLastName(e.target.value)}
                      required
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                      placeholder="Smith"
                    />
                  </div>
                </div>

                {/* Benefits */}
                <div>
                  <label htmlFor="benefits" className="block text-sm font-semibold text-gray-700 mb-2">
                    Company Benefits & Perks
                  </label>
                  <p className="text-sm text-gray-500 mb-2">
                    Describe the benefits, perks, and culture that make your company a great place to work
                  </p>
                  <textarea
                    id="benefits"
                    value={benefits}
                    onChange={(e) => setBenefits(e.target.value)}
                    rows={8}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all font-sans"
                    placeholder="Example: We offer competitive healthcare, 401(k) matching, flexible work hours, remote work options, professional development budget, gym membership, free lunch, and a collaborative team environment..."
                  />
                  <p className="text-xs text-gray-500 mt-2">
                    💡 Tip: Highlight unique benefits that set your company apart from competitors
                  </p>
                </div>

                {/* Info Box */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-start gap-3">
                    <FileText className="h-5 w-5 text-blue-600 mt-0.5" />
                    <div>
                      <p className="font-semibold text-blue-900 mb-1">About This Information</p>
                      <p className="text-sm text-blue-800">
                        This information will be visible to job seekers when they view your company profile and job postings. 
                        Make it compelling to attract top talent!
                      </p>
                    </div>
                  </div>
                </div>

                {/* Submit Button */}
                <div className="flex items-center gap-4 pt-4 border-t border-gray-200">
                  <button
                    type="submit"
                    disabled={saving}
                    className="inline-flex items-center gap-2 px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {saving ? (
                      <>
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        Saving...
                      </>
                    ) : (
                      <>
                        <Save className="h-5 w-5" />
                        Save Changes
                      </>
                    )}
                  </button>

                  <button
                    type="button"
                    onClick={() => router.push('/employer/dashboard')}
                    className="px-6 py-3 text-gray-700 hover:text-gray-900 transition-colors font-medium"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </form>

            {/* Statistics */}
            <div className="bg-gradient-to-r from-blue-600 to-blue-500 rounded-2xl shadow-xl p-8 mt-8 text-white">
              <h2 className="text-2xl font-bold mb-6">Your Activity</h2>
              <div className="grid md:grid-cols-3 gap-6">
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-white/20 rounded-lg">
                    <Briefcase className="h-8 w-8" />
                  </div>
                  <div>
                    <p className="text-3xl font-bold">{profile.open_jobs.length}</p>
                    <p className="text-blue-100">Active Job Postings</p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-white/20 rounded-lg">
                    <FileText className="h-8 w-8" />
                  </div>
                  <div>
                    <p className="text-3xl font-bold">{profile.apps_received.length}</p>
                    <p className="text-blue-100">Applications Received</p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-white/20 rounded-lg">
                    <User className="h-8 w-8" />
                  </div>
                  <div>
                    <p className="text-3xl font-bold">{profile.apps_received.length}</p>
                    <p className="text-blue-100">Unique Candidates</p>
                  </div>
                </div>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}


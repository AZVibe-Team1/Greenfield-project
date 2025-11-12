'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useSeekerAuth } from '@/hooks/useAuth';
import { seekerService } from '@/services/seeker-service';
import { SeekerProfile } from '@/types';
import { 
  User, 
  Edit2, 
  Mail, 
  Phone, 
  MapPin, 
  GraduationCap, 
  Briefcase, 
  DollarSign,
  Tag,
  Save,
  X
} from 'lucide-react';

export default function SeekerProfilePage() {
  // Use the custom authentication hook for seeker-specific protection
  const { user, isLoading: authLoading, logout } = useSeekerAuth();
  const [profile, setProfile] = useState<SeekerProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    phone: '',
    edu_focus: '',
    key_skills: '',
  });

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
      setFormData({
        phone: data.phone,
        edu_focus: data.edu_focus,
        key_skills: data.key_skills.join(', '),
      });
    } catch (error) {
      console.error('Failed to load profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await seekerService.updateProfile({
        phone: formData.phone,
        edu_focus: formData.edu_focus,
        key_skills: formData.key_skills.split(',').map(s => s.trim()).filter(s => s),
      });
      setEditing(false);
      await loadProfile();
    } catch (error) {
      console.error('Failed to update profile:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-emerald-50 to-white flex items-center justify-center">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-emerald-100 rounded-full">
          <div className="w-8 h-8 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin"></div>
        </div>
      </div>
    );
  }

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
      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Page Header */}
        <div className="flex justify-between items-center mb-8">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-emerald-100 rounded-lg">
              <User className="h-6 w-6 text-emerald-600" />
            </div>
            <div>
              <h1 className="text-4xl font-bold text-gray-900">My Profile</h1>
              <p className="text-gray-600">Manage your personal information and preferences</p>
            </div>
          </div>
          {!editing && (
            <button
              onClick={() => setEditing(true)}
              className="inline-flex items-center gap-2 px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors font-medium shadow-md hover:shadow-lg"
            >
              <Edit2 className="h-5 w-5" />
              Edit Profile
            </button>
          )}
        </div>

        {profile && (
          <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
            {editing ? (
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-4">
                  <div>
                    <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                      <Phone className="h-4 w-4 text-emerald-600" />
                      Phone Number
                    </label>
                    <input
                      type="tel"
                      value={formData.phone}
                      onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                      placeholder="(555) 123-4567"
                    />
                  </div>

                  <div>
                    <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                      <GraduationCap className="h-4 w-4 text-emerald-600" />
                      Field of Study
                    </label>
                    <input
                      type="text"
                      value={formData.edu_focus}
                      onChange={(e) => setFormData({ ...formData, edu_focus: e.target.value })}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                      placeholder="e.g., Computer Science"
                    />
                  </div>

                  <div>
                    <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                      <Tag className="h-4 w-4 text-emerald-600" />
                      Skills (comma-separated)
                    </label>
                    <textarea
                      value={formData.key_skills}
                      onChange={(e) => setFormData({ ...formData, key_skills: e.target.value })}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
                      rows={3}
                      placeholder="e.g., Python, JavaScript, React"
                    />
                  </div>
                </div>

                <div className="flex gap-4 pt-4 border-t border-gray-200">
                  <button
                    type="button"
                    onClick={() => setEditing(false)}
                    className="flex-1 inline-flex items-center justify-center gap-2 px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium"
                  >
                    <X className="h-5 w-5" />
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="flex-1 inline-flex items-center justify-center gap-2 px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors font-medium shadow-md hover:shadow-lg"
                  >
                    <Save className="h-5 w-5" />
                    Save Changes
                  </button>
                </div>
              </form>
            ) : (
              <div className="space-y-8">
                {/* Personal Information Section */}
                <div>
                  <div className="flex items-center gap-2 mb-6 pb-3 border-b border-gray-200">
                    <User className="h-5 w-5 text-emerald-600" />
                    <h3 className="text-xl font-semibold text-gray-900">Personal Information</h3>
                  </div>
                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="flex items-start gap-3">
                      <div className="p-2 bg-emerald-50 rounded-lg">
                        <User className="h-5 w-5 text-emerald-600" />
                      </div>
                      <div>
                        <p className="text-sm text-gray-600 mb-1">Full Name</p>
                        <p className="font-semibold text-gray-900">{profile.first_name} {profile.last_name}</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="p-2 bg-emerald-50 rounded-lg">
                        <Mail className="h-5 w-5 text-emerald-600" />
                      </div>
                      <div>
                        <p className="text-sm text-gray-600 mb-1">Email Address</p>
                        <p className="font-semibold text-gray-900">{profile.email}</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="p-2 bg-emerald-50 rounded-lg">
                        <Phone className="h-5 w-5 text-emerald-600" />
                      </div>
                      <div>
                        <p className="text-sm text-gray-600 mb-1">Phone Number</p>
                        <p className="font-semibold text-gray-900">{profile.phone}</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="p-2 bg-emerald-50 rounded-lg">
                        <MapPin className="h-5 w-5 text-emerald-600" />
                      </div>
                      <div>
                        <p className="text-sm text-gray-600 mb-1">Location</p>
                        <p className="font-semibold text-gray-900">{profile.address.city}, {profile.address.state}</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Education & Experience Section */}
                <div>
                  <div className="flex items-center gap-2 mb-6 pb-3 border-b border-gray-200">
                    <GraduationCap className="h-5 w-5 text-emerald-600" />
                    <h3 className="text-xl font-semibold text-gray-900">Education & Experience</h3>
                  </div>
                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="flex items-start gap-3">
                      <div className="p-2 bg-emerald-50 rounded-lg">
                        <GraduationCap className="h-5 w-5 text-emerald-600" />
                      </div>
                      <div>
                        <p className="text-sm text-gray-600 mb-1">Education Level</p>
                        <p className="font-semibold text-gray-900">{profile.education_level}</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="p-2 bg-emerald-50 rounded-lg">
                        <Briefcase className="h-5 w-5 text-emerald-600" />
                      </div>
                      <div>
                        <p className="text-sm text-gray-600 mb-1">Field of Study</p>
                        <p className="font-semibold text-gray-900">{profile.edu_focus}</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Skills Section */}
                <div>
                  <div className="flex items-center gap-2 mb-6 pb-3 border-b border-gray-200">
                    <Tag className="h-5 w-5 text-emerald-600" />
                    <h3 className="text-xl font-semibold text-gray-900">Skills</h3>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {profile.key_skills.map((skill, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center gap-1 bg-emerald-100 text-emerald-800 px-4 py-2 rounded-full text-sm font-medium"
                      >
                        <Tag className="h-3 w-3" />
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Salary Expectations Section */}
                <div>
                  <div className="flex items-center gap-2 mb-6 pb-3 border-b border-gray-200">
                    <DollarSign className="h-5 w-5 text-emerald-600" />
                    <h3 className="text-xl font-semibold text-gray-900">Salary Expectations</h3>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-emerald-50 rounded-lg">
                      <DollarSign className="h-5 w-5 text-emerald-600" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 mb-1">Expected Salary Range</p>
                      <p className="font-semibold text-gray-900 text-lg">
                        ${profile.pay_range[0].toLocaleString()} - ${profile.pay_range[1].toLocaleString()}
                      </p>
                      <p className="text-sm text-gray-500">{profile.pay_unit}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}


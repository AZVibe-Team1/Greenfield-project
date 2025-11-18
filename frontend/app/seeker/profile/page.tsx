'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useSeekerAuth } from '@/hooks/useAuth';
import { seekerService } from '@/services/seeker-service';
import { SeekerProfile, AutoApplySettings } from '@/types';
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
  X,
  Sparkles,
  Settings,
  Zap,
  FileText,
  Upload,
  CheckCircle
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
    pay_range_min: 0,
    pay_range_max: 0,
    pay_unit: 'Yearly',
  });
  const [autoApplySettings, setAutoApplySettings] = useState<AutoApplySettings>({
    enabled: false,
    threshold: 80
  });
  const [savingAutoApply, setSavingAutoApply] = useState(false);
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [resumeText, setResumeText] = useState('');
  const [uploadingResume, setUploadingResume] = useState(false);
  const [resumeUploadSuccess, setResumeUploadSuccess] = useState(false);
  const [resumeUploadError, setResumeUploadError] = useState('');

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
        pay_range_min: data.pay_range[0],
        pay_range_max: data.pay_range[1],
        pay_unit: data.pay_unit,
      });
      
      // Load auto-apply settings
      try {
        const settings = await seekerService.getAutoApplySettings();
        setAutoApplySettings(settings);
      } catch (error) {
        console.error('Failed to load auto-apply settings:', error);
      }
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
        pay_range: [formData.pay_range_min, formData.pay_range_max],
        pay_unit: formData.pay_unit,
      });
      setEditing(false);
      await loadProfile();
    } catch (error) {
      console.error('Failed to update profile:', error);
    }
  };

  const handleAutoApplyChange = async (newSettings: AutoApplySettings) => {
    try {
      setSavingAutoApply(true);
      await seekerService.updateAutoApplySettings(newSettings);
      setAutoApplySettings(newSettings);
    } catch (error) {
      console.error('Failed to update auto-apply settings:', error);
      alert('Failed to update auto-apply settings. Please try again.');
    } finally {
      setSavingAutoApply(false);
    }
  };

  const handleResumeUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    setResumeUploadError('');
    setResumeUploadSuccess(false);

    if (!resumeFile && !resumeText.trim()) {
      setResumeUploadError('Please select a file or enter resume text');
      return;
    }

    try {
      setUploadingResume(true);
      await seekerService.uploadResume(resumeFile || undefined, resumeText.trim() || undefined);
      setResumeUploadSuccess(true);
      setResumeFile(null);
      setResumeText('');
      
      // Reload profile to get updated resume
      await loadProfile();
      
      // Clear success message after 3 seconds
      setTimeout(() => setResumeUploadSuccess(false), 3000);
    } catch (error: any) {
      console.error('Failed to upload resume:', error);
      setResumeUploadError(error.response?.data?.detail || 'Failed to upload resume. Please try again.');
    } finally {
      setUploadingResume(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Validate file type
      const allowedTypes = ['.pdf', '.docx', '.txt'];
      const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
      
      if (!allowedTypes.includes(fileExtension)) {
        setResumeUploadError('Invalid file type. Please upload a PDF, DOCX, or TXT file.');
        return;
      }
      
      // Validate file size (10MB max)
      const maxSize = 10 * 1024 * 1024; // 10MB in bytes
      if (file.size > maxSize) {
        setResumeUploadError('File size exceeds 10MB. Please upload a smaller file.');
        return;
      }
      
      setResumeFile(file);
      setResumeUploadError('');
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
              WorkAtlas
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
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-gray-900"
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
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-gray-900"
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
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-gray-900"
                      rows={3}
                      placeholder="e.g., Python, JavaScript, React"
                    />
                  </div>

                  <div>
                    <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                      <DollarSign className="h-4 w-4 text-emerald-600" />
                      Desired Salary Range
                    </label>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="text-xs text-gray-600 mb-1 block">Minimum</label>
                        <input
                          type="number"
                          value={formData.pay_range_min}
                          onChange={(e) => setFormData({ ...formData, pay_range_min: parseInt(e.target.value) || 0 })}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-gray-900"
                          placeholder="50000"
                          min="0"
                        />
                      </div>
                      <div>
                        <label className="text-xs text-gray-600 mb-1 block">Maximum</label>
                        <input
                          type="number"
                          value={formData.pay_range_max}
                          onChange={(e) => setFormData({ ...formData, pay_range_max: parseInt(e.target.value) || 0 })}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-gray-900"
                          placeholder="80000"
                          min="0"
                        />
                      </div>
                    </div>
                    <div className="mt-2">
                      <label className="text-xs text-gray-600 mb-1 block">Pay Unit</label>
                      <select
                        value={formData.pay_unit}
                        onChange={(e) => setFormData({ ...formData, pay_unit: e.target.value })}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-gray-900"
                      >
                        <option value="Hourly">Hourly</option>
                        <option value="Monthly">Monthly</option>
                        <option value="Yearly">Yearly</option>
                      </select>
                    </div>
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

                {/* Resume Section */}
                <div>
                  <div className="flex items-center gap-2 mb-6 pb-3 border-b border-gray-200">
                    <FileText className="h-5 w-5 text-emerald-600" />
                    <h3 className="text-xl font-semibold text-gray-900">Resume</h3>
                  </div>
                  {profile.resume ? (
                    <div className="flex items-start gap-3 mb-4">
                      <div className="p-2 bg-emerald-50 rounded-lg">
                        <FileText className="h-5 w-5 text-emerald-600" />
                      </div>
                      <div className="flex-1">
                        <p className="text-sm text-gray-600 mb-1">Resume Status</p>
                        <p className="font-semibold text-gray-900">Resume uploaded</p>
                        <p className="text-xs text-gray-500 mt-1">
                          {profile.resume.length > 100 
                            ? `${profile.resume.substring(0, 100)}...` 
                            : profile.resume}
                        </p>
                      </div>
                    </div>
                  ) : (
                    <div className="flex items-start gap-3 mb-4">
                      <div className="p-2 bg-gray-50 rounded-lg">
                        <FileText className="h-5 w-5 text-gray-400" />
                      </div>
                      <div>
                        <p className="text-sm text-gray-600 mb-1">Resume Status</p>
                        <p className="font-semibold text-gray-500">No resume uploaded</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Resume Upload Section */}
        {profile && !editing && (
          <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8 mt-6">
            <div className="flex items-center gap-2 mb-6 pb-3 border-b border-emerald-200">
              <div className="p-2 bg-emerald-100 rounded-lg">
                <Upload className="h-5 w-5 text-emerald-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Upload Resume</h3>
            </div>

            <form onSubmit={handleResumeUpload} className="space-y-6">
              <div className="space-y-4">
                {/* File Upload */}
                <div>
                  <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                    <FileText className="h-4 w-4 text-emerald-600" />
                    Upload Resume File
                  </label>
                  <div className="flex items-center gap-4">
                    <label className="flex-1 cursor-pointer">
                      <input
                        type="file"
                        accept=".pdf,.docx,.txt"
                        onChange={handleFileChange}
                        className="hidden"
                        disabled={uploadingResume}
                      />
                      <div className="w-full px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg hover:border-emerald-500 transition-colors text-center">
                        {resumeFile ? (
                          <div className="flex items-center justify-center gap-2 text-emerald-600">
                            <FileText className="h-5 w-5" />
                            <span className="font-medium">{resumeFile.name}</span>
                            <span className="text-xs text-gray-500">
                              ({(resumeFile.size / 1024).toFixed(2)} KB)
                            </span>
                          </div>
                        ) : (
                          <div className="text-gray-600">
                            <Upload className="h-6 w-6 mx-auto mb-2 text-gray-400" />
                            <p className="text-sm">Click to select a file</p>
                            <p className="text-xs text-gray-500 mt-1">PDF, DOCX, or TXT (max 10MB)</p>
                          </div>
                        )}
                      </div>
                    </label>
                    {resumeFile && (
                      <button
                        type="button"
                        onClick={() => setResumeFile(null)}
                        className="px-4 py-2 text-sm text-red-600 hover:text-red-700 transition-colors"
                        disabled={uploadingResume}
                      >
                        <X className="h-4 w-4" />
                      </button>
                    )}
                  </div>
                </div>

                {/* Or Divider */}
                <div className="relative">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-gray-300"></div>
                  </div>
                  <div className="relative flex justify-center text-sm">
                    <span className="px-2 bg-white text-gray-500">OR</span>
                  </div>
                </div>

                {/* Text Input */}
                <div>
                  <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                    <FileText className="h-4 w-4 text-emerald-600" />
                    Paste Resume Text
                  </label>
                  <textarea
                    value={resumeText}
                    onChange={(e) => setResumeText(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-gray-900"
                    rows={6}
                    placeholder="Paste your resume content here..."
                    disabled={uploadingResume}
                  />
                </div>
              </div>

              {/* Error Message */}
              {resumeUploadError && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-sm text-red-800">{resumeUploadError}</p>
                </div>
              )}

              {/* Success Message */}
              {resumeUploadSuccess && (
                <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-lg flex items-center gap-2">
                  <CheckCircle className="h-5 w-5 text-emerald-600" />
                  <p className="text-sm text-emerald-800">Resume uploaded successfully!</p>
                </div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={uploadingResume || (!resumeFile && !resumeText.trim())}
                className="w-full inline-flex items-center justify-center gap-2 px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors font-medium shadow-md hover:shadow-lg disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                {uploadingResume ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    Uploading...
                  </>
                ) : (
                  <>
                    <Upload className="h-5 w-5" />
                    Upload Resume
                  </>
                )}
              </button>
            </form>
          </div>
        )}

        {/* Auto-Apply Settings Section */}
        {profile && !editing && (
          <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8 mt-6">
            <div className="flex items-center gap-2 mb-6 pb-3 border-b border-purple-200">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Sparkles className="h-5 w-5 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900">AI Auto-Apply Settings</h3>
            </div>

            <div className="space-y-6">
              <p className="text-gray-600">
                Automatically apply to jobs that match your profile above a certain threshold. 
                This feature uses AI to find the best opportunities for you.
              </p>

              {/* Enable/Disable Toggle */}
              <div className="flex items-center justify-between p-4 bg-purple-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <Zap className="h-5 w-5 text-purple-600" />
                  </div>
                  <div>
                    <p className="font-semibold text-gray-900">Enable Auto-Apply</p>
                    <p className="text-sm text-gray-600">
                      Automatically apply to matching jobs
                    </p>
                  </div>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={autoApplySettings.enabled}
                    onChange={(e) => handleAutoApplyChange({
                      ...autoApplySettings,
                      enabled: e.target.checked
                    })}
                    disabled={savingAutoApply}
                    className="sr-only peer"
                  />
                  <div className="w-14 h-7 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[4px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all peer-checked:bg-purple-600"></div>
                </label>
              </div>

              {/* Threshold Slider */}
              {autoApplySettings.enabled && (
                <div className="space-y-3 p-4 bg-emerald-50 rounded-lg">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-emerald-100 rounded-lg">
                        <Settings className="h-5 w-5 text-emerald-600" />
                      </div>
                      <div>
                        <p className="font-semibold text-gray-900">Match Threshold</p>
                        <p className="text-sm text-gray-600">
                          Minimum match score to auto-apply
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-bold text-emerald-600">
                        {Math.round(autoApplySettings.threshold)}%
                      </p>
                    </div>
                  </div>
                  
                  <input
                    type="range"
                    min="0"
                    max="100"
                    step="5"
                    value={autoApplySettings.threshold}
                    onChange={(e) => setAutoApplySettings({
                      ...autoApplySettings,
                      threshold: parseFloat(e.target.value)
                    })}
                    onMouseUp={() => handleAutoApplyChange(autoApplySettings)}
                    onTouchEnd={() => handleAutoApplyChange(autoApplySettings)}
                    disabled={savingAutoApply}
                    className="w-full h-2 bg-emerald-200 rounded-lg appearance-none cursor-pointer slider"
                  />
                  
                  <div className="flex justify-between text-xs text-gray-600">
                    <span>0% - Any Match</span>
                    <span>50% - Moderate</span>
                    <span>100% - Perfect</span>
                  </div>

                  <div className="pt-3 border-t border-emerald-200">
                    <p className="text-sm text-gray-700">
                      <strong>Current setting:</strong> Auto-apply to jobs with {Math.round(autoApplySettings.threshold)}% or higher match score
                    </p>
                    {autoApplySettings.threshold >= 80 && (
                      <p className="text-xs text-emerald-700 mt-1">
                        ✓ Recommended: This threshold will focus on high-quality matches
                      </p>
                    )}
                    {autoApplySettings.threshold < 60 && (
                      <p className="text-xs text-yellow-700 mt-1">
                        ⚠️ Warning: Low threshold may result in many applications
                      </p>
                    )}
                  </div>
                </div>
              )}

              {savingAutoApply && (
                <div className="flex items-center justify-center gap-2 text-purple-600">
                  <div className="w-4 h-4 border-2 border-purple-600 border-t-transparent rounded-full animate-spin"></div>
                  <span className="text-sm">Saving settings...</span>
                </div>
              )}

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-start gap-3">
                  <Sparkles className="h-5 w-5 text-blue-600 mt-0.5" />
                  <div>
                    <p className="text-sm font-semibold text-blue-900 mb-1">How Auto-Apply Works</p>
                    <ul className="text-sm text-blue-800 space-y-1">
                      <li>• AI analyzes your profile and job postings</li>
                      <li>• Calculates match scores based on skills, education, and salary</li>
                      <li>• Automatically applies to jobs above your threshold</li>
                      <li>• You can review applications in "My Applications"</li>
                    </ul>
                  </div>
                </div>
              </div>

              <Link
                href="/seeker/recommendations"
                className="inline-flex items-center gap-2 px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors font-medium shadow-md hover:shadow-lg w-full justify-center"
              >
                <Sparkles className="h-5 w-5" />
                View AI Recommendations
              </Link>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}


'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { employerService } from '@/services/employer-service';
import { useEmployerAuth } from '@/hooks/useAuth';
import { 
  Briefcase, 
  ArrowLeft, 
  Plus,
  LogOut,
  Building2,
  DollarSign,
  GraduationCap,
  Users,
  CheckCircle
} from 'lucide-react';

export default function NewJobPage() {
  const router = useRouter();
  // Use the custom authentication hook for employer-specific protection
  const { logout } = useEmployerAuth();
  const [formData, setFormData] = useState({
    job_title: '',
    job_description: '',
    department: '',
    hire_mgr_first: '',
    hire_mgr_last: '',
    pay_range_min: '',
    pay_range_max: '',
    pay_unit: 'Yearly',
    education_level: 'BS',
    edu_focus: '',
    key_skills: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await employerService.createJob({
        job_title: formData.job_title,
        job_description: formData.job_description,
        department: formData.department,
        hire_mgr_first: formData.hire_mgr_first,
        hire_mgr_last: formData.hire_mgr_last,
        pay_range: [parseInt(formData.pay_range_min), parseInt(formData.pay_range_max)],
        pay_unit: formData.pay_unit,
        education_level: formData.education_level,
        edu_focus: formData.edu_focus,
        key_skills: formData.key_skills ? formData.key_skills.split(',').map(s => s.trim()) : [],
      });

      // Show success message
      setSuccess(true);
      
      // Redirect to dashboard after a brief delay to show success message
      setTimeout(() => {
        router.push('/employer/dashboard');
      }, 1500);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create job');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/employer/dashboard" className="flex items-center">
              <Briefcase className="h-8 w-8 text-blue-600" />
              <span className="ml-2 text-2xl font-bold text-gray-900">WorkAtlas</span>
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
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Back Button and Title */}
        <div className="mb-8">
          <Link 
            href="/employer/jobs" 
            className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium mb-4"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Jobs
          </Link>
          <div className="flex items-center gap-3">
            <div className="bg-blue-100 p-3 rounded-xl">
              <Plus className="h-8 w-8 text-blue-600" />
            </div>
            <h1 className="text-4xl font-bold text-gray-900">Post a New Job</h1>
          </div>
          <p className="text-gray-600 mt-2 ml-16">Fill in the details to create a new job posting</p>
        </div>

        {/* Success Message */}
        {success && (
          <div className="mb-6 p-4 bg-green-50 border border-green-200 text-green-700 rounded-xl flex items-start gap-3 animate-fade-in">
            <CheckCircle className="h-6 w-6 text-green-600 flex-shrink-0" />
            <div>
              <p className="font-semibold">Job Posted Successfully! 🎉</p>
              <p className="text-sm">Redirecting you to dashboard...</p>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl flex items-start gap-3">
            <span className="text-red-600">⚠️</span>
            <div>
              <p className="font-semibold">Error posting job</p>
              <p className="text-sm">{error}</p>
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-xl p-8 space-y-6">
          <fieldset disabled={loading || success} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Job Title *</label>
            <input
              type="text"
              required
              value={formData.job_title}
              onChange={(e) => setFormData({ ...formData, job_title: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
              placeholder="e.g. Senior Software Engineer"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Job Description *</label>
            <textarea
              required
              rows={6}
              value={formData.job_description}
              onChange={(e) => setFormData({ ...formData, job_description: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
              placeholder="Describe the role, responsibilities, and requirements..."
            />
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Department *</label>
              <input
                type="text"
                required
                value={formData.department}
                onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
                placeholder="e.g. Engineering"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Field of Study *</label>
              <input
                type="text"
                required
                value={formData.edu_focus}
                onChange={(e) => setFormData({ ...formData, edu_focus: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
                placeholder="e.g. Computer Science"
              />
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Hiring Manager First Name *</label>
              <input
                type="text"
                required
                value={formData.hire_mgr_first}
                onChange={(e) => setFormData({ ...formData, hire_mgr_first: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Hiring Manager Last Name *</label>
              <input
                type="text"
                required
                value={formData.hire_mgr_last}
                onChange={(e) => setFormData({ ...formData, hire_mgr_last: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
              />
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Min Salary *</label>
              <input
                type="number"
                required
                min="0"
                value={formData.pay_range_min}
                onChange={(e) => setFormData({ ...formData, pay_range_min: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
                placeholder="50000"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Max Salary *</label>
              <input
                type="number"
                required
                min="0"
                value={formData.pay_range_max}
                onChange={(e) => setFormData({ ...formData, pay_range_max: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
                placeholder="100000"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Pay Unit *</label>
              <select
                required
                value={formData.pay_unit}
                onChange={(e) => setFormData({ ...formData, pay_unit: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
              >
                <option value="Hourly">Hourly</option>
                <option value="Monthly">Monthly</option>
                <option value="Yearly">Yearly</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Required Education *</label>
            <select
              required
              value={formData.education_level}
              onChange={(e) => setFormData({ ...formData, education_level: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            >
              <option value="BA">BA</option>
              <option value="BS">BS</option>
              <option value="MA">MA</option>
              <option value="MS">MS</option>
              <option value="MBA">MBA</option>
              <option value="PhD">PhD</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Required Skills (comma-separated)</label>
            <input
              type="text"
              value={formData.key_skills}
              onChange={(e) => setFormData({ ...formData, key_skills: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
              placeholder="Python, JavaScript, React, Node.js"
            />
          </div>

          </fieldset>
          
          {/* Action Buttons */}
          <div className="flex gap-4 pt-6 border-t border-gray-200">
            <Link
              href="/employer/jobs"
              className="flex-1 bg-gray-100 text-gray-700 text-center py-4 rounded-xl hover:bg-gray-200 font-semibold transition-colors"
            >
              Cancel
            </Link>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-blue-600 text-white py-4 rounded-xl hover:bg-blue-700 disabled:bg-gray-400 font-semibold transition-colors shadow-md hover:shadow-lg flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  Posting...
                </>
              ) : (
                <>
                  <Plus className="h-5 w-5" />
                  Post Job
                </>
              )}
            </button>
          </div>
        </form>

        {/* Help Text */}
        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-xl">
          <p className="text-sm text-blue-800">
            <strong>💡 Tip:</strong> Be specific in your job description and requirements to attract the most qualified candidates.
          </p>
        </div>
      </main>
    </div>
  );
}


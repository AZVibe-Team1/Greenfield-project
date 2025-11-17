'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { employerService } from '@/services/employer-service';
import { useEmployerAuth } from '@/hooks/useAuth';
import { Job } from '@/types';
import { 
  Briefcase, 
  ArrowLeft, 
  Save,
  LogOut,
  CheckCircle
} from 'lucide-react';

export default function EditJobPage() {
  const router = useRouter();
  const params = useParams();
  const jobId = params.jobId as string;
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
    current_status: 'Posted',
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    loadJob();
  }, [jobId]);

  const loadJob = async () => {
    try {
      const job = await employerService.getJob(jobId);
      setFormData({
        job_title: job.job_title,
        job_description: job.job_description,
        department: job.department,
        hire_mgr_first: job.hire_mgr_first,
        hire_mgr_last: job.hire_mgr_last,
        pay_range_min: job.pay_range[0].toString(),
        pay_range_max: job.pay_range[1].toString(),
        pay_unit: job.pay_unit,
        education_level: job.education_level,
        edu_focus: job.edu_focus,
        key_skills: job.key_skills?.join(', ') || '',
        current_status: job.current_status,
      });
    } catch (error) {
      console.error('Failed to load job:', error);
      setError('Failed to load job details');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSaving(true);

    try {
      await employerService.updateJob(jobId, {
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
        current_status: formData.current_status,
      });

      // Show success message
      setSuccess(true);
      
      // Redirect back to job details after a brief delay
      setTimeout(() => {
        router.push(`/employer/jobs/${jobId}`);
      }, 1500);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update job');
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-xl text-gray-600">Loading job details...</p>
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
            href={`/employer/jobs/${jobId}`}
            className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium mb-4"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Job Details
          </Link>
          <div className="flex items-center gap-3">
            <div className="bg-blue-100 p-3 rounded-xl">
              <Briefcase className="h-8 w-8 text-blue-600" />
            </div>
            <h1 className="text-4xl font-bold text-gray-900">Edit Job</h1>
          </div>
          <p className="text-gray-600 mt-2 ml-16">Update the job posting details</p>
        </div>

        {/* Success Message */}
        {success && (
          <div className="mb-6 p-4 bg-green-50 border border-green-200 text-green-700 rounded-xl flex items-start gap-3 animate-fade-in">
            <CheckCircle className="h-6 w-6 text-green-600 flex-shrink-0" />
            <div>
              <p className="font-semibold">Job Updated Successfully! 🎉</p>
              <p className="text-sm">Redirecting you back to job details...</p>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl flex items-start gap-3">
            <span className="text-red-600">⚠️</span>
            <div>
              <p className="font-semibold">Error updating job</p>
              <p className="text-sm">{error}</p>
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-xl p-8 space-y-6">
          <fieldset disabled={saving || success} className="space-y-6">
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
            <label className="block text-sm font-medium text-gray-700 mb-1">Job Status *</label>
            <select
              required
              value={formData.current_status}
              onChange={(e) => setFormData({ ...formData, current_status: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            >
              <option value="Posted">Posted</option>
              <option value="Pending">Pending</option>
              <option value="Withdrawn">Withdrawn</option>
              <option value="Canceled">Canceled</option>
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
              href={`/employer/jobs/${jobId}`}
              className="flex-1 bg-gray-100 text-gray-700 text-center py-4 rounded-xl hover:bg-gray-200 font-semibold transition-colors"
            >
              Cancel
            </Link>
            <button
              type="submit"
              disabled={saving}
              className="flex-1 bg-blue-600 text-white py-4 rounded-xl hover:bg-blue-700 disabled:bg-gray-400 font-semibold transition-colors shadow-md hover:shadow-lg flex items-center justify-center gap-2"
            >
              {saving ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  Saving...
                </>
              ) : (
                <>
                  <Save className="h-5 w-5" />
                  Save Changes
                </>
              )}
            </button>
          </div>
        </form>

        {/* Help Text */}
        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-xl">
          <p className="text-sm text-blue-800">
            <strong>💡 Tip:</strong> Make sure all information is accurate before saving your changes.
          </p>
        </div>
      </main>
    </div>
  );
}


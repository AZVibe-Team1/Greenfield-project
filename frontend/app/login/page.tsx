'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuthStore } from '@/store/auth-store';
import { authService } from '@/services/auth-service';
import { Briefcase, User, Building2, ArrowLeft, LogIn } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuthStore();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    role: 'seeker' as 'seeker' | 'employer',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Call authentication service to login
      // This implements the login flow from frontend_auth.txt section 3
      const response = await authService.login(formData);
      
      // Store JWT token and user information in Zustand store
      // Token is also saved to localStorage for persistence
      login(response.access_token, {
        id: response.user_id,
        email: response.email,
        role: response.role as 'seeker' | 'employer',
      });

      // Redirect to appropriate dashboard based on user role
      // Implements role-based routing from frontend_auth.txt section 4
      if (response.role === 'seeker') {
        router.push('/seeker/dashboard');
      } else {
        router.push('/employer/dashboard');
      }
    } catch (err: any) {
      // Handle login errors with user-friendly messages
      // Implements error handling from frontend_auth.txt section 6
      console.error('Login error:', err);
      console.error('Error response:', err.response);
      console.error('Error message:', err.message);
      
      let errorMessage = 'Login failed. Please try again.';
      
      if (err.response) {
        // Server responded with error
        errorMessage = 
          err.response?.status === 401 
            ? 'Invalid email or password. Please check your credentials.'
            : err.response?.status === 500
            ? 'Server error. Please try again later.'
            : err.response?.data?.detail || `Server error (${err.response?.status})`;
      } else if (err.request) {
        // Request was made but no response received
        errorMessage = 'Cannot connect to server. Please check if the backend is running on http://localhost:8000';
      } else {
        // Something else happened
        errorMessage = err.message || 'Login failed. Please try again.';
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white py-12 px-4">
      {/* Header with Logo */}
      <div className="max-w-7xl mx-auto px-4 mb-8">
        <Link href="/" className="flex items-center text-gray-900 hover:text-blue-600 transition">
          <Briefcase className="h-8 w-8 text-blue-600 mr-2" />
          <span className="text-2xl font-bold">JobPortal</span>
        </Link>
      </div>

      <div className="max-w-md mx-auto">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="text-center mb-8">
            <div className="bg-blue-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
              <LogIn className="h-10 w-10 text-blue-600" />
            </div>
            <h1 className="text-4xl font-bold text-gray-900">Welcome Back</h1>
            <p className="text-gray-600 mt-2 text-lg">Login to your JobPortal account</p>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Role Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                I am a
              </label>
              <div className="flex gap-4">
                <button
                  type="button"
                  onClick={() => setFormData({ ...formData, role: 'seeker' })}
                  className={`flex-1 py-3 px-4 rounded-lg border-2 font-semibold transition-all ${
                    formData.role === 'seeker'
                      ? 'border-blue-600 bg-blue-50 text-blue-700 shadow-md'
                      : 'border-gray-300 text-gray-700 hover:border-gray-400'
                  }`}
                >
                  <div className="flex items-center justify-center gap-2">
                    <User className="h-5 w-5" />
                    <span>Job Seeker</span>
                  </div>
                </button>
                <button
                  type="button"
                  onClick={() => setFormData({ ...formData, role: 'employer' })}
                  className={`flex-1 py-3 px-4 rounded-lg border-2 font-semibold transition-all ${
                    formData.role === 'employer'
                      ? 'border-purple-600 bg-purple-50 text-purple-700 shadow-md'
                      : 'border-gray-300 text-gray-700 hover:border-gray-400'
                  }`}
                >
                  <div className="flex items-center justify-center gap-2">
                    <Building2 className="h-5 w-5" />
                    <span>Employer</span>
                  </div>
                </button>
              </div>
            </div>

            {/* Email */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                Email Address
              </label>
              <input
                id="email"
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-gray-900 placeholder:text-gray-400"
                placeholder="you@example.com"
              />
            </div>

            {/* Password */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                id="password"
                type="password"
                required
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-gray-900 placeholder:text-gray-400"
                placeholder="••••••••"
              />
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-4 rounded-lg font-semibold text-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-all shadow-md hover:shadow-lg"
            >
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </form>

          <div className="mt-8 text-center">
            <p className="text-gray-600">
              Don't have an account?{' '}
              <Link href="/register" className="text-blue-600 font-semibold hover:text-blue-700 transition">
                Register here
              </Link>
            </p>
          </div>

          <div className="mt-4 text-center">
            <Link href="/" className="flex items-center justify-center text-sm text-gray-500 hover:text-gray-700 transition">
              <ArrowLeft className="h-4 w-4 mr-1" />
              Back to home
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}


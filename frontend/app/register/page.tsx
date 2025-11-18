'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { authService } from '@/services/auth-service';
import { Briefcase, User, Building2, ArrowLeft, CheckCircle, FileText, Upload, X } from 'lucide-react';

function RegisterContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [role, setRole] = useState<'seeker' | 'employer'>('seeker');
  const [step, setStep] = useState(1);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Common fields
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  // Seeker fields
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [phone, setPhone] = useState('');
  const [street, setStreet] = useState('');
  const [city, setCity] = useState('');
  const [state, setState] = useState('');
  const [zipCode, setZipCode] = useState('');
  const [educationLevel, setEducationLevel] = useState('BS');
  const [eduFocus, setEduFocus] = useState('');
  const [skills, setSkills] = useState('');
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [resumeText, setResumeText] = useState('');
  const [resumeError, setResumeError] = useState('');

  // Employer fields
  const [companyName, setCompanyName] = useState('');
  const [contactFirstName, setContactFirstName] = useState('');
  const [contactLastName, setContactLastName] = useState('');
  const [industry1Code, setIndustry1Code] = useState('45');
  const [industry1Desc, setIndustry1Desc] = useState('Information Technology');
  const [industry2Code, setIndustry2Code] = useState('4510');
  const [industry2Desc, setIndustry2Desc] = useState('Software & Services');
  const [benefits, setBenefits] = useState('');

  useEffect(() => {
    const roleParam = searchParams.get('role');
    if (roleParam === 'employer' || roleParam === 'seeker') {
      setRole(roleParam);
    }
  }, [searchParams]);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setResumeError('');
      
      // Validate file type
      const allowedTypes = ['.txt'];
      const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
      
      if (!allowedTypes.includes(fileExtension)) {
        setResumeError('For registration, only TXT files are supported. PDF and DOCX files can be uploaded after registration.');
        return;
      }
      
      // Validate file size (10MB max)
      const maxSize = 10 * 1024 * 1024; // 10MB in bytes
      if (file.size > maxSize) {
        setResumeError('File size exceeds 10MB. Please upload a smaller file.');
        return;
      }
      
      // Read file content as text
      try {
        const text = await file.text();
        setResumeText(text);
        setResumeFile(file);
      } catch (error) {
        setResumeError('Failed to read file. Please try again.');
      }
    }
  };

  const handleSeekerRegister = async () => {
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);
    setError('');
    setResumeError('');

    try {
      // Prepare resume content (from file or text)
      let resumeContent: string | undefined = undefined;
      if (resumeText.trim()) {
        resumeContent = resumeText.trim();
      }

      await authService.registerSeeker({
        first_name: firstName,
        last_name: lastName,
        email,
        password,
        phone,
        street,
        city,
        state,
        zip_code: zipCode,
        education_level: educationLevel,
        edu_focus: eduFocus,
        key_skills: skills ? skills.split(',').map((s) => s.trim()) : [],
        resume: resumeContent,
      });

      router.push('/login');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleEmployerRegister = async () => {
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await authService.registerEmployer({
        company_name: companyName,
        contact_first_name: contactFirstName,
        contact_last_name: contactLastName,
        email,
        password,
        street,
        city,
        state,
        zip_code: zipCode,
        industry: [
          { code: industry1Code, description: industry1Desc },
          { code: industry2Code, description: industry2Desc },
        ],
        benefits,
      });

      router.push('/login');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (role === 'seeker') {
      await handleSeekerRegister();
    } else {
      await handleEmployerRegister();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white py-12 px-4">
      {/* Header with Logo */}
      <div className="max-w-7xl mx-auto px-4 mb-8">
        <Link href="/" className="flex items-center text-gray-900 hover:text-blue-600 transition">
          <Briefcase className="h-8 w-8 text-blue-600 mr-2" />
          <span className="text-2xl font-bold">WorkAtlas</span>
        </Link>
      </div>

      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900">Create Account</h1>
            <p className="text-gray-600 mt-2 text-lg">Join WorkAtlas today</p>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}

          {/* Role Selection */}
          {step === 1 && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-4">
                  I want to register as
                </label>
                <div className="flex gap-6">
                  <button
                    type="button"
                    onClick={() => setRole('seeker')}
                    className={`flex-1 py-6 px-6 rounded-xl border-2 font-medium transition-all transform hover:scale-105 ${
                      role === 'seeker'
                        ? 'border-blue-600 bg-blue-50 text-blue-700 shadow-lg'
                        : 'border-gray-300 text-gray-700 hover:border-gray-400 hover:shadow-md'
                    }`}
                  >
                    <div className="flex flex-col items-center">
                      <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mb-3">
                        <User className="h-8 w-8 text-blue-600" />
                      </div>
                      <span className="text-lg font-semibold">Job Seeker</span>
                    </div>
                  </button>
                  <button
                    type="button"
                    onClick={() => setRole('employer')}
                    className={`flex-1 py-6 px-6 rounded-xl border-2 font-medium transition-all transform hover:scale-105 ${
                      role === 'employer'
                        ? 'border-purple-600 bg-purple-50 text-purple-700 shadow-lg'
                        : 'border-gray-300 text-gray-700 hover:border-gray-400 hover:shadow-md'
                    }`}
                  >
                    <div className="flex flex-col items-center">
                      <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mb-3">
                        <Building2 className="h-8 w-8 text-purple-600" />
                      </div>
                      <span className="text-lg font-semibold">Employer</span>
                    </div>
                  </button>
                </div>
              </div>

              <button
                onClick={() => setStep(2)}
                className="w-full bg-blue-600 text-white py-4 rounded-lg font-semibold text-lg hover:bg-blue-700 transition-colors shadow-md hover:shadow-lg"
              >
                Continue
              </button>
            </div>
          )}

          {/* Registration Form */}
          {step === 2 && (
            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="flex items-center gap-3 mb-6">
                <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                  role === 'seeker' ? 'bg-blue-100' : 'bg-purple-100'
                }`}>
                  {role === 'seeker' ? (
                    <User className={`h-6 w-6 ${role === 'seeker' ? 'text-blue-600' : 'text-purple-600'}`} />
                  ) : (
                    <Building2 className={`h-6 w-6 ${role === 'employer' ? 'text-purple-600' : 'text-blue-600'}`} />
                  )}
                </div>
                <h2 className="text-2xl font-bold text-gray-900">
                  {role === 'seeker' ? 'Job Seeker Information' : 'Employer Information'}
                </h2>
              </div>

              {/* Common Fields */}
              <div className="grid md:grid-cols-2 gap-4">
                {role === 'seeker' ? (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">First Name *</label>
                      <input
                        type="text"
                        required
                        value={firstName}
                        onChange={(e) => setFirstName(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 text-gray-900 placeholder:text-gray-400"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Last Name *</label>
                      <input
                        type="text"
                        required
                        value={lastName}
                        onChange={(e) => setLastName(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 text-gray-900 placeholder:text-gray-400"
                      />
                    </div>
                  </>
                ) : (
                  <>
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-1">Company Name *</label>
                      <input
                        type="text"
                        required
                        value={companyName}
                        onChange={(e) => setCompanyName(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 text-gray-900 placeholder:text-gray-400"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Contact First Name *</label>
                      <input
                        type="text"
                        required
                        value={contactFirstName}
                        onChange={(e) => setContactFirstName(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 text-gray-900 placeholder:text-gray-400"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Contact Last Name *</label>
                      <input
                        type="text"
                        required
                        value={contactLastName}
                        onChange={(e) => setContactLastName(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 text-gray-900 placeholder:text-gray-400"
                      />
                    </div>
                  </>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email *</label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 text-gray-900"
                />
              </div>

              {role === 'seeker' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Phone *</label>
                  <input
                    type="tel"
                    required
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    placeholder="+12025550123"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 text-gray-900"
                  />
                </div>
              )}

              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Password *</label>
                  <input
                    type="password"
                    required
                    minLength={6}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 text-gray-900"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Confirm Password *</label>
                  <input
                    type="password"
                    required
                    minLength={6}
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 text-gray-900"
                  />
                </div>
              </div>

              {/* Address */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Street Address *</label>
                <input
                  type="text"
                  required
                  value={street}
                  onChange={(e) => setStreet(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 text-gray-900"
                />
              </div>

              <div className="grid md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">City *</label>
                  <input
                    type="text"
                    required
                    value={city}
                    onChange={(e) => setCity(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 text-gray-900"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">State *</label>
                  <input
                    type="text"
                    required
                    maxLength={2}
                    value={state}
                    onChange={(e) => setState(e.target.value.toUpperCase())}
                    placeholder="CA"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 text-gray-900"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">ZIP Code *</label>
                  <input
                    type="text"
                    required
                    value={zipCode}
                    onChange={(e) => setZipCode(e.target.value)}
                    placeholder="12345"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 text-gray-900"
                  />
                </div>
              </div>

              {/* Role-specific fields */}
              {role === 'seeker' ? (
                <>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Education Level *</label>
                      <select
                        required
                        value={educationLevel}
                        onChange={(e) => setEducationLevel(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 text-gray-900 placeholder:text-gray-400"
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
                      <label className="block text-sm font-medium text-gray-700 mb-1">Field of Study *</label>
                      <input
                        type="text"
                        required
                        value={eduFocus}
                        onChange={(e) => setEduFocus(e.target.value)}
                        placeholder="Computer Science"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 text-gray-900 placeholder:text-gray-400"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Skills (comma-separated)</label>
                    <input
                      type="text"
                      value={skills}
                      onChange={(e) => setSkills(e.target.value)}
                      placeholder="Python, JavaScript, React"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 text-gray-900"
                    />
                  </div>

                  {/* Resume Upload Section */}
                  <div className="space-y-3">
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      <FileText className="h-4 w-4 inline mr-1 text-blue-600" />
                      Resume (Optional)
                    </label>
                    
                    {/* File Upload */}
                    <div>
                      <label className="block text-xs text-gray-600 mb-2">Upload TXT File</label>
                      <div className="flex items-center gap-4">
                        <label className="flex-1 cursor-pointer">
                          <input
                            type="file"
                            accept=".txt"
                            onChange={handleFileChange}
                            className="hidden"
                            disabled={loading}
                          />
                          <div className="w-full px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 transition-colors text-center">
                            {resumeFile ? (
                              <div className="flex items-center justify-center gap-2 text-blue-600">
                                <FileText className="h-5 w-5" />
                                <span className="font-medium text-sm">{resumeFile.name}</span>
                                <span className="text-xs text-gray-500">
                                  ({(resumeFile.size / 1024).toFixed(2)} KB)
                                </span>
                              </div>
                            ) : (
                              <div className="text-gray-600">
                                <Upload className="h-5 w-5 mx-auto mb-1 text-gray-400" />
                                <p className="text-xs">Click to select TXT file</p>
                                <p className="text-xs text-gray-500 mt-1">PDF/DOCX can be uploaded after registration</p>
                              </div>
                            )}
                          </div>
                        </label>
                        {resumeFile && (
                          <button
                            type="button"
                            onClick={() => {
                              setResumeFile(null);
                              setResumeText('');
                            }}
                            className="px-3 py-2 text-sm text-red-600 hover:text-red-700 transition-colors"
                            disabled={loading}
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
                      <div className="relative flex justify-center text-xs">
                        <span className="px-2 bg-white text-gray-500">OR</span>
                      </div>
                    </div>

                    {/* Text Input */}
                    <div>
                      <label className="block text-xs text-gray-600 mb-2">Paste Resume Text</label>
                      <textarea
                        value={resumeText}
                        onChange={(e) => {
                          setResumeText(e.target.value);
                          setResumeFile(null);
                          setResumeError('');
                        }}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 text-sm text-gray-900"
                        rows={4}
                        placeholder="Paste your resume content here..."
                        disabled={loading}
                      />
                    </div>

                    {/* Error Message */}
                    {resumeError && (
                      <div className="p-2 bg-red-50 border border-red-200 rounded text-xs text-red-800">
                        {resumeError}
                      </div>
                    )}

                    <p className="text-xs text-gray-500">
                      Note: You can upload PDF or DOCX files after registration from your profile page.
                    </p>
                  </div>
                </>
              ) : (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Benefits</label>
                  <textarea
                    value={benefits}
                    onChange={(e) => setBenefits(e.target.value)}
                    placeholder="Health insurance, 401k, Remote work..."
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 text-gray-900"
                  />
                </div>
              )}

              <div className="flex gap-4 pt-4">
                <button
                  type="button"
                  onClick={() => setStep(1)}
                  className="flex-1 bg-gray-200 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-300 transition-colors shadow-sm"
                >
                  Back
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className={`flex-1 py-3 rounded-lg font-semibold transition-all shadow-md hover:shadow-lg disabled:bg-gray-400 disabled:cursor-not-allowed ${
                    role === 'seeker' 
                      ? 'bg-blue-600 text-white hover:bg-blue-700' 
                      : 'bg-purple-600 text-white hover:bg-purple-700'
                  }`}
                >
                  {loading ? 'Creating Account...' : 'Create Account'}
                </button>
              </div>
            </form>
          )}

          <div className="mt-8 text-center">
            <p className="text-gray-600">
              Already have an account?{' '}
              <Link href="/login" className="text-blue-600 font-semibold hover:text-blue-700 transition">
                Login here
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

export default function RegisterPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    }>
      <RegisterContent />
    </Suspense>
  );
}


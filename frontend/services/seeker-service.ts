/**
 * Job Seeker Service
 * 
 * API calls for job seeker operations
 */
import apiClient from '@/lib/api';
import { SeekerProfile, Job } from '@/types';

export const seekerService = {
  /**
   * Get current seeker profile
   */
  getProfile: async (): Promise<SeekerProfile> => {
    const response = await apiClient.get<SeekerProfile>('/seekers/me');
    return response.data;
  },

  /**
   * Update seeker profile
   */
  updateProfile: async (data: any): Promise<any> => {
    const response = await apiClient.put('/seekers/me', data);
    return response.data;
  },

  /**
   * Upload resume
   */
  uploadResume: async (resumeContent: string): Promise<any> => {
    const response = await apiClient.post('/seekers/resume', { resume_content: resumeContent });
    return response.data;
  },

  /**
   * Apply for a job
   */
  applyForJob: async (jobId: string, employerId: string): Promise<any> => {
    const response = await apiClient.post('/seekers/applications', {
      job_id: jobId,
      employer_id: employerId,
    });
    return response.data;
  },

  /**
   * Get all applications
   */
  getApplications: async (): Promise<any> => {
    const response = await apiClient.get('/seekers/applications');
    return response.data;
  },

  /**
   * Withdraw application
   */
  withdrawApplication: async (jobId: string): Promise<any> => {
    const response = await apiClient.delete(`/seekers/applications/${jobId}`);
    return response.data;
  },

  /**
   * Search jobs
   */
  searchJobs: async (params?: { title?: string; company?: string; skill?: string }): Promise<Job[]> => {
    const response = await apiClient.get<Job[]>('/seekers/jobs', { params });
    return response.data;
  },

  /**
   * Get job details
   */
  getJobDetails: async (jobId: string): Promise<Job> => {
    const response = await apiClient.get<Job>(`/seekers/jobs/${jobId}`);
    return response.data;
  },

  /**
   * Get AI-powered job recommendations
   */
  getRecommendations: async (): Promise<any> => {
    const response = await apiClient.get('/seekers/recommendations');
    return response.data;
  },
};


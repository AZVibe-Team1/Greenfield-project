/**
 * Employer Service
 * 
 * API calls for employer operations
 */
import apiClient from '@/lib/api-client';
import { EmployerProfile, Job, CreateJobRequest, CandidateRecommendation } from '@/types';

export const employerService = {
  /**
   * Get current employer profile
   */
  getProfile: async (): Promise<EmployerProfile> => {
    const response = await apiClient.get<EmployerProfile>('/employers/me');
    return response.data;
  },

  /**
   * Update employer profile
   */
  updateProfile: async (data: any): Promise<any> => {
    const response = await apiClient.put('/employers/me', data);
    return response.data;
  },

  /**
   * Create a new job posting
   */
  createJob: async (data: CreateJobRequest): Promise<Job> => {
    const response = await apiClient.post<Job>('/employers/jobs', data);
    return response.data;
  },

  /**
   * Get all jobs
   */
  getJobs: async (): Promise<Job[]> => {
    const response = await apiClient.get<Job[]>('/employers/jobs');
    return response.data;
  },

  /**
   * Get specific job
   */
  getJob: async (jobId: string): Promise<Job> => {
    const response = await apiClient.get<Job>(`/employers/jobs/${jobId}`);
    return response.data;
  },

  /**
   * Update job
   */
  updateJob: async (jobId: string, data: any): Promise<any> => {
    const response = await apiClient.put(`/employers/jobs/${jobId}`, data);
    return response.data;
  },

  /**
   * Delete job
   */
  deleteJob: async (jobId: string): Promise<any> => {
    const response = await apiClient.delete(`/employers/jobs/${jobId}`);
    return response.data;
  },

  /**
   * Get all applications received
   */
  getApplications: async (): Promise<any> => {
    const response = await apiClient.get('/employers/applications');
    return response.data;
  },

  /**
   * Get AI-powered candidate recommendations for a job
   * Note: This endpoint uses LLM processing and may take 10-30 seconds
   */
  getCandidateRecommendations: async (
    jobId: string, 
    nResults: number = 20, 
    minScore: number = 0.0
  ): Promise<CandidateRecommendation[]> => {
    const response = await apiClient.get<CandidateRecommendation[]>(
      `/employers/jobs/${jobId}/candidates`,
      {
        params: {
          n_results: nResults,
          min_score: minScore
        },
        // Set a longer timeout for AI processing (60 seconds)
        timeout: 60000
      }
    );
    return response.data;
  },
};


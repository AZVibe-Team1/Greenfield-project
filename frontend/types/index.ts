/**
 * TypeScript type definitions for Job Portal
 */

export interface User {
  id: string;
  email: string;
  role: 'seeker' | 'employer';
  first_name?: string;
  last_name?: string;
  company_name?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
  role: 'seeker' | 'employer';
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user_id: string;
  role: string;
  email: string;
}

export interface SeekerRegisterRequest {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  phone: string;
  street: string;
  city: string;
  state: string;
  zip_code: string;
  education_level: string;
  edu_focus: string;
  pay_range?: number[];
  pay_unit?: string;
  key_skills?: string[];
  resume?: string;
}

export interface EmployerRegisterRequest {
  company_name: string;
  contact_first_name: string;
  contact_last_name: string;
  email: string;
  password: string;
  street: string;
  city: string;
  state: string;
  zip_code: string;
  industry: { code: string; description: string }[];
  benefits?: string;
}

export interface SeekerProfile {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  address: {
    street: string;
    city: string;
    state: string;
    zip_code: string;
  };
  education_level: string;
  edu_focus: string;
  pay_range: number[];
  pay_unit: string;
  key_skills: string[];
  resume?: string;
  applications: Application[];
}

export interface EmployerProfile {
  id: string;
  company_name: string;
  contact_first_name: string;
  contact_last_name: string;
  address: {
    street: string;
    city: string;
    state: string;
    zip_code: string;
  };
  industry: { code: string; description: string }[];
  benefits: string;
  open_jobs: Job[];
  apps_received: ApplicationReceived[];
}

export interface Job {
  job_id: string;
  job_title: string;
  job_description: string;
  posted_date: string;
  department: string;
  hire_mgr_first: string;
  hire_mgr_last: string;
  current_status: string;
  pay_range: number[];
  pay_unit: string;
  education_level: string;
  edu_focus: string;
  key_skills: string[];
  company_name?: string;
  employer_id?: string;
  hiring_manager?: string;
  work_schedule?: string;
  required_skills?: string[]; // Alias for key_skills
}

export interface Application {
  job_id: string;
  employer_id: string;
  date_applied: string;
  application_status: string;
  job_title?: string;
  company_name?: string;
}

export interface ApplicationReceived {
  applicant_id: string;
  job_id: string;
  initial_daterec: string;
  current_status: string;
  previous_status?: string;
  current_status_date: string;
}

export interface CreateJobRequest {
  job_title: string;
  job_description: string;
  department: string;
  hire_mgr_first: string;
  hire_mgr_last: string;
  pay_range: number[];
  pay_unit: string;
  education_level: string;
  edu_focus: string;
  key_skills?: string[];
}

export interface ScoreBreakdown {
  skills_score: number;
  education_score: number;
  pay_score: number;
  experience_score: number;
  reasoning: string;
}

export interface JobRecommendation {
  job_id: string;
  job_title: string;
  company_name: string;
  employer_id: string;
  match_score: number;
  score_breakdown: ScoreBreakdown;
  job_description: string;
  key_skills: string[];
  education_level: string;
  edu_focus: string;
  pay_range: number[];
  pay_unit: string;
  department: string;
  posted_date: string | null;
  hire_mgr_first: string;
  hire_mgr_last: string;
}

export interface AutoApplySettings {
  enabled: boolean;
  threshold: number;
}

export interface CandidateRecommendation {
  seeker_id: string;
  first_name: string;
  last_name: string;
  email: string;
  match_score: number;
  score_breakdown: ScoreBreakdown;
  has_applied: boolean;
  resume_preview: string;
  key_skills: string[];
  education_level: string;
  edu_focus: string;
  pay_range: number[];
  pay_unit: string;
  phone: string;
  address: {
    street: string;
    city: string;
    state: string;
    zip_code: string;
  };
}

export interface ScheduleInterviewRequest {
  interview_date: string; // ISO datetime string
  interview_time: string; // Time string (e.g., "14:00")
  interview_type: 'In-person' | 'Video' | 'Phone';
  location_or_link: string;
  notes?: string | null;
}

export interface N8nStatusResponse {
  status: 'connected' | 'disconnected';
  message: string;
}


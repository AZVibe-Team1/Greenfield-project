/**
 * Authentication Service
 * 
 * API calls for authentication (login, register)
 */
import apiClient from '@/lib/api';
import {
  LoginRequest,
  LoginResponse,
  SeekerRegisterRequest,
  EmployerRegisterRequest,
} from '@/types';

export const authService = {
  /**
   * Login user
   */
  login: async (data: LoginRequest): Promise<LoginResponse> => {
    const response = await apiClient.post<LoginResponse>('/auth/login', data);
    return response.data;
  },

  /**
   * Register job seeker
   */
  registerSeeker: async (data: SeekerRegisterRequest): Promise<any> => {
    const response = await apiClient.post('/auth/register/seeker', data);
    return response.data;
  },

  /**
   * Register employer
   */
  registerEmployer: async (data: EmployerRegisterRequest): Promise<any> => {
    const response = await apiClient.post('/auth/register/employer', data);
    return response.data;
  },
};


/**
 * Authentication Service
 * 
 * API calls for authentication (login, register, token validation)
 * Implements JWT-based authentication following best practices from frontend_auth.txt
 */
import apiClient from '@/lib/api-client';
import {
  LoginRequest,
  LoginResponse,
  SeekerRegisterRequest,
  EmployerRegisterRequest,
  User,
} from '@/types';

export const authService = {
  /**
   * Login user
   * Sends credentials to backend and receives JWT token
   */
  login: async (data: LoginRequest): Promise<LoginResponse> => {
    const response = await apiClient.post<LoginResponse>('/auth/login', data);
    return response.data;
  },

  /**
   * Register job seeker
   * Creates a new seeker account with profile information
   */
  registerSeeker: async (data: SeekerRegisterRequest): Promise<any> => {
    const response = await apiClient.post('/auth/register/seeker', data);
    return response.data;
  },

  /**
   * Register employer
   * Creates a new employer account with company information
   */
  registerEmployer: async (data: EmployerRegisterRequest): Promise<any> => {
    const response = await apiClient.post('/auth/register/employer', data);
    return response.data;
  },

  /**
   * Validate token and get current user
   * Calls backend /auth/me endpoint to verify JWT token validity
   * This ensures the token hasn't expired and user still exists
   * 
   * @returns User information if token is valid
   * @throws Error if token is invalid or expired
   */
  validateToken: async (): Promise<User> => {
    const response = await apiClient.get<User>('/auth/me');
    return response.data;
  },
};


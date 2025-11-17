/**
 * Authentication Store (Zustand)
 * 
 * Global state management for authentication
 * Implements JWT token validation and session management
 * Following best practices from frontend_auth.txt
 */
import { create } from 'zustand';
import { User } from '@/types';
import { authService } from '@/services/auth-service';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  setUser: (user: User | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  login: (token: string, user: User) => void;
  logout: () => void;
  checkAuth: () => Promise<void>;
  validateAndRefreshAuth: () => Promise<boolean>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,
  
  setUser: (user) => set({ user, isAuthenticated: !!user }),
  
  setLoading: (loading) => set({ isLoading: loading }),
  
  setError: (error) => set({ error }),
  
  /**
   * Login user and store JWT token
   * Saves token in localStorage for persistence across sessions
   */
  login: (token, user) => {
    // Store JWT token in localStorage (as per frontend_auth.txt section 5)
    localStorage.setItem('access_token', token);
    localStorage.setItem('user_role', user.role);
    localStorage.setItem('user_id', user.id);
    set({ user, isAuthenticated: true, isLoading: false, error: null });
  },
  
  /**
   * Logout user and clear session
   * Removes all auth data from localStorage and redirects to login
   */
  logout: () => {
    // Clear all authentication data
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_role');
    localStorage.removeItem('user_id');
    set({ user: null, isAuthenticated: false, isLoading: false, error: null });
    
    // Redirect to login page
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
  },
  
  /**
   * Check authentication status on app initialization
   * Validates token with backend to ensure it's still valid
   * 
   * This implements the token validation strategy from frontend_auth.txt section 4:
   * - Check localStorage for token
   * - Validate with backend /auth/me endpoint
   * - Update user state with validated information
   */
  checkAuth: async () => {
    const token = localStorage.getItem('access_token');
    
    // If no token, user is not authenticated
    if (!token) {
      set({ user: null, isAuthenticated: false, isLoading: false, error: null });
      return;
    }
    
    try {
      set({ isLoading: true, error: null });
      
      // Validate token with backend (implements frontend_auth.txt section 4 - Token Validation)
      const userData = await authService.validateToken();
      
      // Token is valid, update user state
      set({
        user: userData,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error: any) {
      // Token is invalid or expired - clear auth state
      console.error('Token validation failed:', error);
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_role');
      localStorage.removeItem('user_id');
      set({ 
        user: null, 
        isAuthenticated: false, 
        isLoading: false,
        error: 'Session expired. Please login again.'
      });
    }
  },
  
  /**
   * Validate current token and refresh user data
   * Can be called to re-validate authentication state
   * 
   * @returns true if token is valid, false otherwise
   */
  validateAndRefreshAuth: async (): Promise<boolean> => {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
      return false;
    }
    
    try {
      // Validate token with backend
      const userData = await authService.validateToken();
      
      // Update user state with fresh data
      set({
        user: userData,
        isAuthenticated: true,
        error: null,
      });
      
      return true;
    } catch (error) {
      // Token is invalid
      get().logout();
      return false;
    }
  },
}));


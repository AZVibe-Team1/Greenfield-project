/**
 * Authentication Store (Zustand)
 * 
 * Global state management for authentication
 */
import { create } from 'zustand';
import { User } from '@/types';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  
  setUser: (user: User | null) => void;
  setLoading: (loading: boolean) => void;
  login: (token: string, user: User) => void;
  logout: () => void;
  checkAuth: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  
  setUser: (user) => set({ user, isAuthenticated: !!user }),
  
  setLoading: (loading) => set({ isLoading: loading }),
  
  login: (token, user) => {
    localStorage.setItem('access_token', token);
    localStorage.setItem('user_role', user.role);
    localStorage.setItem('user_id', user.id);
    set({ user, isAuthenticated: true, isLoading: false });
  },
  
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_role');
    localStorage.removeItem('user_id');
    set({ user: null, isAuthenticated: false, isLoading: false });
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
  },
  
  checkAuth: () => {
    const token = localStorage.getItem('access_token');
    const role = localStorage.getItem('user_role') as 'seeker' | 'employer' | null;
    const id = localStorage.getItem('user_id');
    
    if (token && role && id) {
      // Note: In production, you should validate the token with backend
      set({
        user: { id, email: '', role },
        isAuthenticated: true,
        isLoading: false,
      });
    } else {
      set({ user: null, isAuthenticated: false, isLoading: false });
    }
  },
}));


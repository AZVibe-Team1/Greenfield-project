/**
 * useAuth Hook
 * 
 * Custom React hook for authentication and protected routes
 * Implements authentication checks as described in frontend_auth.txt section 4
 */
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/auth-store';

interface UseAuthOptions {
  /**
   * Required role for access
   * If specified, user must have this role to access the page
   */
  requiredRole?: 'seeker' | 'employer';
  
  /**
   * Redirect path if authentication fails
   * Defaults to '/login'
   */
  redirectTo?: string;
  
  /**
   * Whether to redirect if user doesn't have required role
   * If true, redirects to appropriate dashboard
   * If false, just returns hasAccess as false
   */
  redirectOnWrongRole?: boolean;
}

interface UseAuthReturn {
  /**
   * Current authenticated user
   */
  user: ReturnType<typeof useAuthStore>['user'];
  
  /**
   * Whether user is authenticated
   */
  isAuthenticated: boolean;
  
  /**
   * Whether authentication is being checked
   */
  isLoading: boolean;
  
  /**
   * Whether user has access to this page
   */
  hasAccess: boolean;
  
  /**
   * Any authentication error
   */
  error: string | null;
  
  /**
   * Logout function
   */
  logout: () => void;
}

/**
 * Custom hook for authentication and route protection
 * 
 * This hook implements the protected routes strategy from frontend_auth.txt:
 * 1. Checks if user is authenticated
 * 2. Validates token with backend
 * 3. Redirects to login if not authenticated
 * 4. Optionally checks for required role
 * 
 * @example
 * // Simple authentication check
 * const { user, isAuthenticated, isLoading } = useAuth();
 * 
 * @example
 * // Protected page with role requirement
 * const { user, hasAccess } = useAuth({ requiredRole: 'employer' });
 * 
 * @example
 * // Custom redirect path
 * const { user } = useAuth({ redirectTo: '/unauthorized' });
 */
export function useAuth(options: UseAuthOptions = {}): UseAuthReturn {
  const {
    requiredRole,
    redirectTo = '/login',
    redirectOnWrongRole = true,
  } = options;
  
  const router = useRouter();
  const { user, isAuthenticated, isLoading, error, checkAuth, logout } = useAuthStore();
  
  // Check authentication on mount (implements frontend_auth.txt section 4 - Token Check)
  useEffect(() => {
    checkAuth();
  }, [checkAuth]);
  
  // Handle authentication and authorization
  useEffect(() => {
    // Wait for authentication check to complete
    if (isLoading) {
      return;
    }
    
    // If not authenticated, redirect to login page
    if (!isAuthenticated) {
      router.push(redirectTo);
      return;
    }
    
    // If a specific role is required, check if user has that role
    if (requiredRole && user?.role !== requiredRole && redirectOnWrongRole) {
      // Redirect to appropriate dashboard based on actual role
      if (user?.role === 'seeker') {
        router.push('/seeker/dashboard');
      } else if (user?.role === 'employer') {
        router.push('/employer/dashboard');
      }
    }
  }, [isAuthenticated, isLoading, user, requiredRole, redirectTo, redirectOnWrongRole, router]);
  
  // Determine if user has access
  const hasAccess = isAuthenticated && (!requiredRole || user?.role === requiredRole);
  
  return {
    user,
    isAuthenticated,
    isLoading,
    hasAccess,
    error,
    logout,
  };
}

/**
 * Hook specifically for seeker-only pages
 * Convenience wrapper around useAuth with requiredRole='seeker'
 */
export function useSeekerAuth(): UseAuthReturn {
  return useAuth({ requiredRole: 'seeker' });
}

/**
 * Hook specifically for employer-only pages
 * Convenience wrapper around useAuth with requiredRole='employer'
 */
export function useEmployerAuth(): UseAuthReturn {
  return useAuth({ requiredRole: 'employer' });
}


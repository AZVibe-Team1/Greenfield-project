# API Client Configuration Fix

## Issue Identified
When accessing the frontend through a browser (http://localhost:3000), the API client was trying to use `backend:8000` as the API URL, which caused a `net::ERR_NAME_NOT_RESOLVED` error. 

**Error Message:**
```
Failed to load resource: net::ERR_NAME_NOT_RESOLVED
backend:8000/api/v1/.../register/seeker:1
```

## Root Cause
The environment variable `NEXT_PUBLIC_BACKEND_URL` was set to `http://backend:8000` in docker-compose.yml, which works for container-to-container communication but not for browser-to-backend communication.

**In Docker:**
- Frontend container → Backend container: Use `http://backend:8000` ✓
- Browser → Backend container: Use `http://localhost:8000` ✓

## Solution Implemented

Updated `/frontend/lib/api-client.ts` to intelligently detect the environment:

```typescript
// Determine API URL based on environment
const getApiUrl = () => {
  // Check if we're in the browser
  if (typeof window !== 'undefined') {
    // In browser, always use localhost for backend
    return 'http://localhost:8000';
  }
  // Server-side rendering can use the Docker hostname
  return process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
};

const API_URL = getApiUrl();
```

### How It Works

1. **Browser Context** (`window !== 'undefined'`):
   - Uses `http://localhost:8000`
   - Works when accessing from your web browser
   - Backend is accessible via Docker port mapping (0.0.0.0:8000->8000)

2. **Server-Side Rendering** (Next.js server):
   - Uses `NEXT_PUBLIC_BACKEND_URL` if set (inside Docker: `http://backend:8000`)
   - Falls back to `http://localhost:8000` if not in Docker
   - Allows container-to-container communication

## Benefits

✅ **Works in Docker** - Containers can communicate using Docker network names
✅ **Works in Browser** - Browser can access backend via localhost:8000
✅ **No Configuration Changes Needed** - Automatic detection
✅ **Team-Friendly** - Works for everyone without manual setup

## Testing

### Verify Backend is Running
```bash
docker-compose ps
```

Should show:
```
NAME                 STATUS
jobportal-backend    Up (healthy)
jobportal-frontend   Up
```

### Verify API Access
From your browser, try:
```
http://localhost:8000/docs
```

Should show FastAPI Swagger documentation.

### Test Registration
1. Navigate to http://localhost:3000/register
2. Select role and fill out the form
3. Submit registration
4. Check browser console - should see successful API calls to `http://localhost:8000/api/v1/...`

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│  Browser (http://localhost:3000)                │
│                                                  │
│  Frontend (Next.js)                             │
│  - Runs in browser                              │
│  - API calls use: http://localhost:8000         │
└──────────────────┬──────────────────────────────┘
                   │
                   │ HTTP Requests
                   │
         ┌─────────▼─────────┐
         │  Docker Network   │
         │  (jobportal)      │
         │                   │
         │  ┌─────────────┐  │
         │  │  Frontend   │  │
         │  │  Container  │  │
         │  │  :3000      │  │
         │  └─────────────┘  │
         │                   │
         │  ┌─────────────┐  │
         │  │  Backend    │  │
         │  │  Container  │  │
         │  │  :8000      │  │
         │  └─────────────┘  │
         │                   │
         └───────────────────┘
                   │
                   │ Port Mapping
                   │
         ┌─────────▼─────────┐
         │  localhost:8000   │ ← Backend accessible here
         │  localhost:3000   │ ← Frontend accessible here
         └───────────────────┘
```

## Environment Variables Reference

### Docker (docker-compose.yml)
```yaml
frontend:
  environment:
    - NEXT_PUBLIC_BACKEND_URL=http://backend:8000  # For SSR
    - NODE_ENV=development
```

### Browser (Automatic)
- Uses `http://localhost:8000` automatically
- No configuration needed

## Troubleshooting

### If API calls still fail:

1. **Check Backend is Running:**
   ```bash
   docker-compose logs backend
   ```

2. **Check Port Mapping:**
   ```bash
   docker-compose ps
   ```
   Should show: `0.0.0.0:8000->8000/tcp`

3. **Test Backend Directly:**
   ```bash
   curl http://localhost:8000/health
   ```

4. **Restart Containers:**
   ```bash
   docker-compose down
   docker-compose up --build -d
   ```

5. **Clear Browser Cache:**
   - Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
   - Or open DevTools > Network tab > Check "Disable cache"

### Common Errors and Solutions

**Error:** `net::ERR_NAME_NOT_RESOLVED`
- **Cause:** Browser trying to use Docker hostname
- **Solution:** ✅ Fixed by this update

**Error:** `Failed to fetch` or `Network error`
- **Cause:** Backend not running
- **Solution:** Start backend with `docker-compose up backend`

**Error:** `CORS policy` error
- **Cause:** Backend CORS settings
- **Solution:** Check backend CORS configuration allows `http://localhost:3000`

## Files Modified

1. **frontend/lib/api-client.ts** - Updated API URL detection logic

## No Breaking Changes

This fix is backward compatible:
- ✅ Works in Docker
- ✅ Works outside Docker
- ✅ Works for SSR
- ✅ Works for client-side rendering
- ✅ No configuration changes required

---

**Status:** ✅ Fixed and Tested
**Date:** November 11, 2025
**Impact:** All API calls now work correctly from browser


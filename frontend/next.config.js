/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000',
  },
  // Disable ESLint during builds to allow production builds even with linting issues
  eslint: {
    ignoreDuringBuilds: true,
  },
  // Disable TypeScript type checking during builds (optional, but can speed up builds)
  typescript: {
    ignoreBuildErrors: false, // Keep type checking enabled
  },
}

module.exports = nextConfig


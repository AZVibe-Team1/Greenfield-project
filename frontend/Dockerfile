# Frontend Dockerfile for Job Portal (Next.js 14)
# This Dockerfile sets up a Node.js environment for Next.js application
# NOTE: This service is currently commented out in docker-compose.yml

# Use Node.js 20 LTS as base image
# Node.js 20 LTS provides long-term support and stability
FROM node:20-slim

# Set working directory inside the container
WORKDIR /app

# Set environment variables
# NODE_ENV=production optimizes Next.js builds
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1

# Install system dependencies if needed
# pnpm is an alternative package manager (can be changed to npm/yarn)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy package files first for better Docker layer caching
# This allows Docker to cache node_modules separately from code changes
COPY frontend/package*.json ./

# Install Node.js dependencies
# Using npm ci for faster, reliable, reproducible builds
RUN npm ci --only=production

# Copy the rest of the frontend application code
COPY frontend/ ./

# Build the Next.js application
# This creates an optimized production build
RUN npm run build

# Expose port 3000 - default Next.js port
EXPOSE 3000

# Start the Next.js production server
# Using 'next start' for production mode
CMD ["npm", "start"]


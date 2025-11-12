# Frontend Dockerfile for Job Portal (Next.js 14)
# This Dockerfile sets up a Node.js environment for Next.js application

# Use Node.js 20 LTS as base image for better compatibility
FROM node:20-slim

# Set working directory inside the container
WORKDIR /app

# Set environment variables
ENV NODE_ENV=development \
    NEXT_TELEMETRY_DISABLED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy package files first for better Docker layer caching
COPY package*.json ./

# Install all dependencies (including dev dependencies for development)
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose port 3000 - default Next.js port
EXPOSE 3000

# Start the Next.js development server with hot-reload
CMD ["npm", "run", "dev"]


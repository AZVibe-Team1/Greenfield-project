# Job Portal - Greenfield Project

A secure, scalable, and user-friendly platform connecting job seekers and employers with AI-powered recommendations.


**JM!!** - Right now, the containers bring up only the backend as I thought it would be easiest to start with one container.
The code added to /backend is temporary to show that the backend FastAPI runs at a basic level.

## Docker Setup

This project uses Docker Compose for containerized development and deployment.

### Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v2.0+

### Installing Docker

#### Windows

1. **Download Docker Desktop:**
   - Visit [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
   - Click "Download for Windows"
   - Download the installer (`Docker Desktop Installer.exe`)

2. **Install Docker Desktop:**
   - Run the installer
   - Follow the installation wizard
   - When prompted, ensure "Use WSL 2 instead of Hyper-V" is checked (recommended)
   - Restart your computer if prompted

3. **Launch Docker Desktop:**
   - After restart, launch Docker Desktop from the Start menu
   - Accept the service agreement
   - Wait for Docker to start (the Docker icon in the system tray will show "Docker Desktop is running")

4. **Verify Installation:**
   ```bash
   docker --version
   docker compose version
   ```

#### macOS

1. **Choose Your Mac Type:**
   - **Apple Silicon (M1/M2/M3)**: Download "Mac with Apple chip"
   - **Intel Mac**: Download "Mac with Intel chip"

2. **Download Docker Desktop:**
   - Visit [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
   - Click "Download for Mac"
   - The download will be a `.dmg` file

3. **Install Docker Desktop:**
   - Open the downloaded `.dmg` file
   - Drag Docker.app to your Applications folder
   - Open Docker from Applications (or Spotlight search)
   - Click "Open" when macOS asks for confirmation

4. **Complete Setup:**
   - Docker Desktop will start and may ask for your password to install networking components
   - Wait for Docker to finish starting (the Docker icon in the menu bar will show "Docker Desktop is running")

5. **Verify Installation:**
   ```bash
   docker --version
   docker compose version
   ```

**Note:** Docker Desktop includes Docker Compose, so you don't need to install it separately.

### Quick Start

1. **Copy environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and fill in your configuration values.

2. **Run the backend service:**
   ```bash
   docker compose run backend
   ```
   The backend API will be available at `http://localhost:8000`

   JM!! - Open a terminal in the backend container: 
    ```bash
   docker compose run backend bash
   ```

3. **Run the frontend service** (when ready):
   ```bash
   docker compose run frontend
   ```
   The frontend will be available at `http://localhost:3000`

4. **Run all services together:**
   ```bash
   docker compose up
   ```
   This starts all services (backend, frontend, and MongoDB) defined in `docker-compose.yml`


   **JM!!** - Rebuild all containers (start fresh build):
   ```bash
   docker compose up --build
   ```

   **JM!!** - Clean up containers (good to run after done with developing session):
   ```bash
   docker compose down -v --remove-orphans
   ```

   **JM!!** - To view what containers you have running:
   ```bash
   docker ps
   ```

### Docker Services

- **backend**: FastAPI application (Python 3.12+, uv package manager)
- **frontend**: Next.js 14 application (currently commented out)
- **n8n**: Workflow automation platform for email notifications
- **mongodb**: MongoDB 6.x database (currently commented out)

### Development

The Docker setup includes volume mounts for hot-reload during development. Code changes will be reflected automatically without rebuilding containers.

### Environment Variables

See `.env.example` for all required environment variables. Key variables include:
- Database connection strings
- JWT secrets
- AI/LLM API keys
- Email configuration
- CORS settings
- n8n configuration

---

## n8n Email Notifications

The Job Portal uses n8n (workflow automation platform) to send email notifications for interview scheduling. This enables employers to schedule interviews with candidates and automatically send email notifications through n8n workflows.

### Overview

n8n is integrated into the application via Docker and provides:
- **Interview Scheduling Emails**: Automatically send email notifications when employers schedule interviews with candidates
- **Workflow Automation**: Flexible workflow system for customizing email templates and notification logic
- **Status Monitoring**: Real-time status indicator on the employer dashboard showing n8n connection status

### Docker Setup

n8n is automatically included when you start the application with Docker Compose:

```bash
docker compose up
```

The n8n service will be available at:
- **Web UI**: `http://localhost:5678`
- **Internal API**: `http://n8n:5678` (for backend communication)

### Configuration

#### Environment Variables

Add the following variables to your `.env` file (see `env.template` for reference):

```bash
# n8n Configuration
# Docker: Use http://n8n:5678 for internal communication
# Local: Use http://localhost:5678 for local development
N8N_API_URL=http://n8n:5678

# Webhook URL will be available after creating the workflow in n8n UI
# Format: http://n8n:5678/webhook/interview-schedule
N8N_WEBHOOK_URL=http://n8n:5678/webhook/interview-schedule

# Optional: API key for n8n authentication (if enabled)
N8N_API_KEY=
```

**Note**: The `N8N_WEBHOOK_URL` will be available after you create and activate the interview scheduling workflow in the n8n UI.

#### Persistent Storage

n8n workflows and data are stored in the `./n8n_data` directory, which is mounted as a volume in Docker. This ensures your workflows persist across container restarts.

### n8n Workflow Setup

#### Step 1: Access n8n UI

1. Start the application: `docker compose up`
2. Wait for n8n to be ready (check health status)
3. Open your browser and navigate to: `http://localhost:5678`

#### Step 2: Create Interview Scheduling Workflow

1. **Create New Workflow**:
   - Click "Add workflow" or "New workflow" in the n8n UI
   - Give it a name: "Interview Scheduling"

2. **Add Webhook Trigger**:
   - Click "Add node" and search for "Webhook"
   - Select "Webhook" node
   - Configure the webhook:
     - **HTTP Method**: POST
     - **Path**: `/webhook/interview-schedule`
     - **Response Mode**: "Respond When Last Node Finishes"
   - Click "Listen for Test Event" to activate the webhook
   - **Copy the webhook URL** (e.g., `http://n8n:5678/webhook/interview-schedule`)
   - Update `N8N_WEBHOOK_URL` in your `.env` file with this URL

3. **Add Email Node**:
   - Click "Add node" after the Webhook node
   - Search for "Email" and select your email service:
     - **Gmail** (requires OAuth setup)
     - **SMTP** (works with any SMTP server)
     - **SendGrid**, **Mailgun**, or other email services
   - Configure the email node:
     - **To**: `{{ $json.seeker_email }}`
     - **Subject**: `Interview Scheduled: {{ $json.job_title }}`
     - **Email Body** (HTML or text):
       ```
       Dear Candidate,
       
       You have been scheduled for an interview for the position: {{ $json.body.job_title }}
       
       Interview Details:
       - Date: {{ $json.body.interview_date }}
       - Time: {{ $json.body.interview_time }}
       - Type: {{ $json.body.interview_type }}
       - Location/Link: {{ $json.body.location_or_link }}
       {% if $json.notes %}
       - Notes: {{ $json.body.notes }}
       {% endif %}
       
       Company: {{ $json.body.employer_name }}
       
       We look forward to speaking with you!
       ```

4. **Save and Activate**:
   - Click "Save" to save the workflow
   - Toggle the "Active" switch to activate the workflow
   - The workflow is now ready to receive webhook requests

#### Step 3: Test the Workflow

You can test the workflow by:
1. Using the n8n UI's "Test workflow" feature
2. Or scheduling an interview through the Job Portal frontend

### Using Interview Scheduling

#### For Employers

1. **Navigate to Candidate Recommendations**:
   - Go to "My Jobs" → Select a job → Click "View Candidates" or "AI Candidates"

2. **Schedule an Interview**:
   - Find a candidate you want to interview
   - Click the "Schedule Interview" button
   - Fill in the interview form:
     - **Date**: Select the interview date
     - **Time**: Enter the interview time
     - **Type**: Choose In-person, Video, or Phone
     - **Location/Link**: Enter address, video link, or phone number
     - **Notes**: Optional additional information
   - Click "Schedule Interview"

3. **Email Notification**:
   - The system will automatically send an email notification to the candidate via n8n
   - The application status will be updated to "Interviewed"
   - You'll see a success message confirming the email was sent

#### Status Monitoring

- **Dashboard Indicator**: The employer dashboard shows the n8n connection status
  - **Green "Connected"**: n8n is available and email notifications will be sent
  - **Red "Disconnected"**: n8n is unavailable, interview scheduling will fail with an error message

- **API Endpoint**: Check n8n status programmatically:
  ```bash
  GET /api/v1/employers/n8n/status
  ```

### Troubleshooting

#### n8n Service Not Starting

1. **Check Docker logs**:
   ```bash
   docker compose logs n8n
   ```

2. **Verify port availability**:
   - Ensure port 5678 is not already in use
   - Check firewall settings if needed

3. **Check health status**:
   ```bash
   docker compose ps
   ```

#### Webhook Not Receiving Requests

1. **Verify webhook URL**:
   - Check that `N8N_WEBHOOK_URL` in `.env` matches the webhook URL from n8n UI
   - Ensure the workflow is activated in n8n

2. **Check n8n logs**:
   ```bash
   docker compose logs n8n
   ```

3. **Test webhook manually**:
   - Use the n8n UI's "Test workflow" feature
   - Or use curl to test:
     ```bash
     curl -X POST http://localhost:5678/webhook/interview-schedule \
       -H "Content-Type: application/json" \
       -d '{"seeker_email":"test@example.com","job_title":"Test Job",...}'
     ```

#### Email Not Sending

1. **Check email service configuration**:
   - Verify SMTP credentials or OAuth setup
   - Test email node in n8n UI

2. **Check n8n workflow execution**:
   - View workflow execution history in n8n UI
   - Check for error messages in failed executions

3. **Verify email node settings**:
   - Ensure email addresses are correctly formatted
   - Check that email service limits/quota are not exceeded

### API Endpoints

#### Schedule Interview

```http
POST /api/v1/employers/jobs/{job_id}/candidates/{seeker_id}/schedule-interview
Authorization: Bearer <token>
Content-Type: application/json

{
  "interview_date": "2024-01-15T10:00:00Z",
  "interview_time": "14:00",
  "interview_type": "Video",
  "location_or_link": "https://meet.example.com/interview",
  "notes": "Please prepare for technical questions"
}
```

#### Get n8n Status

```http
GET /api/v1/employers/n8n/status
Authorization: Bearer <token>
```

Response:
```json
{
  "status": "connected",
  "message": "n8n service is available and responding"
}
```

### Additional Resources

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Webhook Guide](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/)
- [n8n Email Nodes](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.email/)

---

## Project Structure

- `backend/` - FastAPI backend application
- `frontend/` - Next.js frontend application
- `docker-compose.yml` - Docker Compose configuration
- `.env.example` - Environment variables template
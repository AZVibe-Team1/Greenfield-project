"""
n8n Service Module

This module provides integration with n8n workflow automation platform
for sending email notifications, particularly for interview scheduling.
"""

import os
from typing import Any

import httpx
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

# n8n Configuration
N8N_API_URL = os.getenv("N8N_API_URL", "http://n8n:5678")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://n8n:5678/webhook/interview-schedule")
N8N_API_KEY = os.getenv("N8N_API_KEY", "")


class N8nService:
    """
    Service for interacting with n8n workflow automation platform.
    
    Provides methods for checking connection status and triggering workflows.
    """
    
    def __init__(self):
        """Initialize n8n service with configuration from environment variables."""
        self.api_url = N8N_API_URL.rstrip("/")
        self.webhook_url = N8N_WEBHOOK_URL
        self.api_key = N8N_API_KEY
        self.timeout = 10.0  # 10 second timeout for requests
    
    async def check_n8n_connection(self) -> bool:
        """
        Check if n8n service is available and responding.
        
        Returns:
            True if n8n is accessible, False otherwise
        """
        try:
            # Try to access n8n health endpoint or root
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Try healthz endpoint first (n8n health check)
                try:
                    response = await client.get(f"{self.api_url}/healthz")
                    if response.status_code == 200:
                        logger.debug("n8n health check successful")
                        return True
                except httpx.RequestError:
                    pass
                
                # Fallback to root endpoint
                try:
                    response = await client.get(f"{self.api_url}/")
                    if response.status_code in [200, 302, 401]:  # 302 redirect, 401 auth required
                        logger.debug("n8n is accessible")
                        return True
                except httpx.RequestError:
                    pass
                
                logger.warning("n8n health check failed - service may be unavailable")
                return False
                
        except Exception as e:
            logger.error(f"Error checking n8n connection: {e}")
            return False
    
    async def trigger_interview_workflow(
        self,
        seeker_email: str,
        job_title: str,
        employer_name: str,
        employer_email: str,
        interview_details: dict[str, Any]
    ) -> bool:
        """
        Trigger n8n workflow to send interview scheduling email.
        
        Args:
            seeker_email: Email address of the job seeker
            job_title: Title of the job position
            employer_name: Name of the employer/company
            employer_email: Email address of the employer
            interview_details: Dictionary containing interview information:
                - interview_date: Date of the interview
                - interview_time: Time of the interview
                - interview_type: Type of interview (In-person, Video, Phone)
                - location_or_link: Location or video link
                - notes: Optional notes about the interview
        
        Returns:
            True if workflow was triggered successfully, False otherwise
        """
        try:
            # Prepare payload for n8n webhook
            payload = {
                "seeker_email": seeker_email,
                "job_title": job_title,
                "employer_name": employer_name,
                "employer_email": employer_email,
                "interview_date": str(interview_details.get("interview_date", "")),
                "interview_time": interview_details.get("interview_time", ""),
                "interview_type": interview_details.get("interview_type", ""),
                "location_or_link": interview_details.get("location_or_link", ""),
                "notes": interview_details.get("notes", "")
            }
            
            # Prepare headers
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["X-N8N-API-KEY"] = self.api_key
            
            # Send POST request to n8n webhook
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.webhook_url,
                    json=payload,
                    headers=headers
                )
                
                # n8n webhooks typically return 200 on success
                if response.status_code in [200, 201]:
                    logger.info(f"Successfully triggered n8n workflow for interview: {job_title} - {seeker_email}")
                    return True
                else:
                    logger.error(
                        f"n8n webhook returned status {response.status_code}: {response.text}"
                    )
                    return False
                    
        except httpx.TimeoutException:
            logger.error("Timeout while triggering n8n workflow")
            return False
        except httpx.RequestError as e:
            logger.error(f"Request error while triggering n8n workflow: {e}")
            return False
        except Exception as e:
            logger.error(f"Error triggering n8n workflow: {e}")
            return False
    
    async def get_n8n_status(self) -> dict[str, str]:
        """
        Get n8n service connection status.
        
        Returns:
            Dictionary with status and message:
            {
                "status": "connected" | "disconnected",
                "message": "Status message"
            }
        """
        is_connected = await self.check_n8n_connection()
        
        if is_connected:
            return {
                "status": "connected",
                "message": "n8n service is available and responding"
            }
        else:
            return {
                "status": "disconnected",
                "message": "n8n service is unavailable or not responding"
            }


# Singleton instance
_n8n_service: N8nService | None = None


def get_n8n_service() -> N8nService:
    """
    Get or create n8n service singleton instance.
    
    Returns:
        N8nService instance
    """
    global _n8n_service
    if _n8n_service is None:
        _n8n_service = N8nService()
    return _n8n_service


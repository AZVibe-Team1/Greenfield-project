"""n8n Integration Service for Interview Notifications."""

import httpx
from datetime import datetime
from loguru import logger
from pydantic import BaseModel, Field

from backend.db.settings import settings


class N8nInterviewWebhookPayload(BaseModel):
    """Payload structure for n8n interview webhook."""
    seeker_email: str = Field(..., description="Candidate email address")
    seeker_name: str = Field(..., description="Candidate full name")
    job_title: str = Field(..., description="Job position title")
    company_name: str = Field(..., description="Company name")
    interview_date: str = Field(..., description="Interview date (YYYY-MM-DD)")
    interview_time: str = Field(..., description="Interview time (e.g., 10:00 AM)")
    interview_type: str = Field(..., description="Type of interview")
    location_or_link: str = Field(..., description="Location or video link")
    notes: str = Field(default="", description="Additional notes")


class N8nService:
    """Service for n8n integration."""
    
    def __init__(self):
        self.webhook_url = getattr(settings, 'N8N_WEBHOOK_URL', None)
        self.timeout = 10.0  # seconds
    
    async def check_connection(self) -> dict[str, str]:
        """
        Check if n8n service is reachable.
        
        Returns:
            dict with status and message
        """
        if not self.webhook_url:
            return {
                "status": "disconnected",
                "message": "N8N_WEBHOOK_URL not configured"
            }
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # Try a HEAD request to check if endpoint exists
                response = await client.head(self.webhook_url)
                
                # n8n webhooks typically return 404 for HEAD requests
                # but 200/405 means the service is up
                if response.status_code in [200, 404, 405]:
                    return {
                        "status": "connected",
                        "message": "n8n service is reachable"
                    }
                else:
                    return {
                        "status": "disconnected",
                        "message": f"n8n returned status {response.status_code}"
                    }
        except httpx.TimeoutException:
            logger.warning("n8n connection timeout")
            return {
                "status": "disconnected",
                "message": "Connection timeout"
            }
        except httpx.ConnectError:
            logger.warning("n8n connection error - service may be down")
            return {
                "status": "disconnected",
                "message": "Cannot connect to n8n service"
            }
        except Exception as e:
            logger.error(f"Unexpected error checking n8n connection: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def trigger_interview_notification(
        self,
        seeker_email: str,
        seeker_name: str,
        job_title: str,
        company_name: str,
        interview_date: datetime,
        interview_time: str,
        interview_type: str,
        location_or_link: str,
        notes: str = ""
    ) -> tuple[bool, str]:
        """
        Trigger n8n workflow to send interview notification email.
        
        Args:
            seeker_email: Candidate's email
            seeker_name: Candidate's full name
            job_title: Job position title
            company_name: Company name
            interview_date: Interview date
            interview_time: Interview time string
            interview_type: Type of interview
            location_or_link: Location or video link
            notes: Additional notes
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.webhook_url:
            logger.warning("N8N_WEBHOOK_URL not configured - skipping notification")
            return False, "N8N_WEBHOOK_URL not configured"
        
        # Format date for email
        formatted_date = interview_date.strftime("%Y-%m-%d")
        
        # Prepare webhook payload
        payload = N8nInterviewWebhookPayload(
            seeker_email=seeker_email,
            seeker_name=seeker_name,
            job_title=job_title,
            company_name=company_name,
            interview_date=formatted_date,
            interview_time=interview_time,
            interview_type=interview_type,
            location_or_link=location_or_link,
            notes=notes
        )
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(f"Sending interview notification to n8n for {seeker_email}")
                logger.debug(f"Webhook URL: {self.webhook_url}")
                logger.debug(f"Payload: {payload.model_dump()}")
                
                response = await client.post(
                    self.webhook_url,
                    json=payload.model_dump(),
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code in [200, 201]:
                    logger.info(f"✅ n8n notification sent successfully to {seeker_email}")
                    return True, "Notification sent successfully"
                else:
                    logger.warning(
                        f"⚠️  n8n returned status {response.status_code}: {response.text}"
                    )
                    return False, f"n8n returned status {response.status_code}"
                    
        except httpx.TimeoutException:
            logger.error(f"❌ Timeout sending notification to n8n for {seeker_email}")
            return False, "Request timeout"
            
        except httpx.ConnectError as e:
            logger.error(f"❌ Connection error to n8n: {e}")
            return False, "Cannot connect to n8n service"
            
        except Exception as e:
            logger.error(f"❌ Unexpected error sending notification to n8n: {e}")
            return False, f"Unexpected error: {str(e)}"


# Singleton instance
n8n_service = N8nService()


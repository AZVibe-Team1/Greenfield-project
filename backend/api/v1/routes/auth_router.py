"""
Authentication API routes.

Handles user registration and login for both job seekers and employers.
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

from backend.core.security import create_access_token, hash_password, verify_password
from backend.db.employer_db_ops import EmployerCRUD
from backend.db.seeker_db_ops import SeekerCRUD
from backend.services.employer_services import EmployerService
from backend.services.seeker_services import SeekerService

router = APIRouter(prefix="/auth", tags=["Authentication"])


# Request/Response Models
class LoginRequest(BaseModel):
    """Login request body."""
    email: EmailStr
    password: str
    role: str = Field(..., description="User role: 'seeker' or 'employer'")


class LoginResponse(BaseModel):
    """Login response."""
    access_token: str
    token_type: str = "bearer"
    user_id: str
    role: str
    email: str


class SeekerRegisterRequest(BaseModel):
    """Job seeker registration request."""
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: str
    street: str
    city: str
    state: str
    zip_code: str
    education_level: str
    edu_focus: str
    pay_range: list[int] | None = None
    pay_unit: str = "Yearly"
    key_skills: list[str] | None = None


class EmployerRegisterRequest(BaseModel):
    """Employer registration request."""
    company_name: str = Field(..., min_length=1)
    contact_first_name: str = Field(..., min_length=1)
    contact_last_name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=6)
    street: str
    city: str
    state: str
    zip_code: str
    industry: list[dict[str, str]] = Field(..., min_length=2, max_length=2)
    benefits: str = ""


class RegisterResponse(BaseModel):
    """Registration response."""
    user_id: str
    email: str
    role: str
    message: str = "Registration successful"


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Authenticate user and return access token.
    
    Args:
        request: Login credentials (email, password, role)
        
    Returns:
        Access token and user information
        
    Raises:
        HTTPException: If credentials are invalid or user not found
    """
    try:
        if request.role == "seeker":
            # Find seeker by email
            seeker = await SeekerCRUD.get_seeker_by_email(request.email)
            if not seeker:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
            
            # Verify password
            if not verify_password(request.password, seeker.password_hash):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
            
            # Create access token
            access_token = create_access_token(
                data={"sub": str(seeker.id), "role": "seeker", "email": request.email}
            )
            
            return LoginResponse(
                access_token=access_token,
                user_id=str(seeker.id),
                role="seeker",
                email=request.email
            )
            
        elif request.role == "employer":
            # Find employer by email
            employer = await EmployerCRUD.get_employer_by_email(request.email)
            if not employer:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
            
            # Verify password
            if not verify_password(request.password, employer.password_hash):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
            
            # Create access token
            access_token = create_access_token(
                data={"sub": str(employer.id), "role": "employer", "email": request.email}
            )
            
            return LoginResponse(
                access_token=access_token,
                user_id=str(employer.id),
                role="employer",
                email=request.email
            )
            
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role. Must be 'seeker' or 'employer'"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.post("/register/seeker", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_seeker(request: SeekerRegisterRequest):
    """
    Register a new job seeker account.
    
    Args:
        request: Seeker registration data
        
    Returns:
        Created user information
        
    Raises:
        HTTPException: If registration fails or email already exists
    """
    try:
        # Check if email already exists
        existing_seeker = await SeekerCRUD.get_seeker_by_email(request.email)
        if existing_seeker:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        password_hash = hash_password(request.password)
        
        # Create seeker
        seeker = await SeekerService.create_new_seeker(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            phone=request.phone,
            street=request.street,
            city=request.city,
            state=request.state,
            zip_code=request.zip_code,
            password_hash=password_hash,
            education_level=request.education_level,
            edu_focus=request.edu_focus,
            pay_range=request.pay_range,
            pay_unit=request.pay_unit,
            key_skills=request.key_skills
        )
        
        if not seeker:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create seeker account"
            )
        
        return RegisterResponse(
            user_id=str(seeker.id),
            email=request.email,
            role="seeker"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/register/employer", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_employer(request: EmployerRegisterRequest):
    """
    Register a new employer account.
    
    Args:
        request: Employer registration data
        
    Returns:
        Created user information
        
    Raises:
        HTTPException: If registration fails or company already exists
    """
    try:
        # Check if company already exists
        existing_employer = await EmployerCRUD.get_employer_by_company_name(request.company_name)
        if existing_employer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Company already registered"
            )
        
        # Hash password
        password_hash = hash_password(request.password)
        
        # Create address
        address = {
            "street": request.street,
            "city": request.city,
            "state": request.state,
            "zip_code": request.zip_code
        }
        
        # Check if email already exists
        existing_email = await EmployerCRUD.get_employer_by_email(request.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create employer
        employer = await EmployerService.create_new_employer(
            company_name=request.company_name,
            address=address,
            industry=request.industry,
            contact_first_name=request.contact_first_name,
            contact_last_name=request.contact_last_name,
            email=request.email,
            password_hash=password_hash,
            benefits=request.benefits,
            open_jobs=[]
        )
        
        if not employer:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create employer account"
            )
        
        return RegisterResponse(
            user_id=str(employer.id),
            email=request.email,
            role="employer"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


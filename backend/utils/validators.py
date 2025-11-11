"""
US Address and Contact Validation Module

This module provides Pydantic V2 validators for US address components and contact
information including state abbreviations, ZIP codes, email addresses, and phone numbers.

Usage:
    from backend.utils.validators import StateAbbr, ZipCode, Email, PhoneNumber, USPhoneNumber, Address
    from pydantic import BaseModel

    class Contact(BaseModel):
        name: str
        email: Email
        phone: USPhoneNumber
        address: Address

    # Valid usage
    contact = Contact(
        name="Jane Doe",
        email="jane.doe@example.com",
        phone="+1-555-123-4567",
        address=Address(
            street="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001"
        )
    )
    
    # Also valid with ZIP+4 and different phone formats
    contact_extended = Contact(
        name="John Smith",
        email="john@company.org",
        phone="(555) 987-6543",
        address=Address(
            street="456 Oak Ave",
            city="Brooklyn",
            state="NY",
            zip_code="11201-1234"
        )
    )

State Validation Rules:
    - Must be exactly 2 characters long
    - Must be uppercase (case-sensitive)
    - Must match one of the valid US state or territory abbreviations

Valid State Abbreviations:
    States (50): AL, AK, AZ, AR, CA, CO, CT, DE, FL, GA, HI, ID, IL, IN, IA,
                 KS, KY, LA, ME, MD, MA, MI, MN, MS, MO, MT, NE, NV, NH, NJ,
                 NM, NY, NC, ND, OH, OK, OR, PA, RI, SC, SD, TN, TX, UT, VT,
                 VA, WA, WV, WI, WY
    
    District: DC (District of Columbia)
    
    Territories (5): PR (Puerto Rico), VI (Virgin Islands), 
                     GU (Guam), AS (American Samoa), MP (Northern Mariana Islands)

ZIP Code Validation Rules:
    - Must be 5 digits (e.g., "90210")
    - OR 5 digits followed by hyphen and 4 digits (ZIP+4 format, e.g., "90210-1234")
    - Only numeric digits allowed (except the optional hyphen in ZIP+4)

Email Validation Rules:
    - Must be a valid email address format (user@domain.com)
    - Validates domain structure and syntax
    - Uses Pydantic's EmailStr which validates against RFC 5322 standard

Phone Number Validation Rules:
    - PhoneNumber: Validates international phone numbers (any region)
    - USPhoneNumber: Validates US phone numbers specifically
    - Accepts various formats: "+1-555-123-4567", "(555) 123-4567", "555.123.4567"
    - Uses Google's libphonenumber library for accurate validation
    - Returns standardized phonenumbers.PhoneNumber object

Raises:
    ValidationError: If the input does not match validation rules for the respective type.
"""

from typing import Annotated, Union

import phonenumbers
from pydantic import BaseModel, EmailStr, Field, ValidationError
from pydantic_extra_types.phone_numbers import PhoneNumberValidator
from annotated_types import Len


# Regex pattern for all 50 US states + DC + territories (PR, VI, GU, AS, MP)
STATE_REGEX = r'^(AL|AK|AZ|AR|CA|CO|CT|DE|DC|FL|GA|HI|IA|ID|IL|IN|KS|KY|LA|MA|MD|ME|MI|MN|MO|MS|MT|NC|ND|NE|NH|NJ|NM|NV|NY|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VA|VT|WA|WI|WV|WY|PR|VI|GU|AS|MP)$'

# Regex pattern for US ZIP codes (5-digit or ZIP+4 format)
# ^\d{5}$ matches a 5-digit ZIP code
# ^\d{5}-\d{4}$ matches a ZIP+4 code
ZIP_CODE_REGEX = r"^\d{5}(?:-\d{4})?$"

# Define a custom type for US state abbreviations
# This can be used in any Pydantic model throughout the codebase
StateAbbr = Annotated[
    str,
    Field(
        pattern=STATE_REGEX,
        description="Valid US state or territory abbreviation (uppercase, 2 characters)"
    ),
    Len(2, 2)
]

# Define a custom type for US ZIP codes
# Supports both 5-digit (e.g., "90210") and ZIP+4 format (e.g., "90210-1234")
ZipCode = Annotated[
    str,
    Field(
        pattern=ZIP_CODE_REGEX,
        description="Valid US ZIP code (5 digits or ZIP+4 format)"
    )
]

# Define a type alias for email addresses
# Uses Pydantic's EmailStr which provides RFC 5322 compliant email validation
Email = EmailStr

# Define phone number types
# PhoneNumber: Accepts phone numbers from any region/country
PhoneNumber = Annotated[
    Union[str, phonenumbers.PhoneNumber],
    PhoneNumberValidator()
]

# USPhoneNumber: US-specific phone number validation
# Defaults to US region and only accepts US phone numbers
USPhoneNumber = Annotated[
    Union[str, phonenumbers.PhoneNumber],
    PhoneNumberValidator(supported_regions=['US'], default_region='US')
]


# Define Address class - reusable address model
class Address(BaseModel):
    """
    US Address model with validated components.
    
    This class provides a complete address structure with validation
    for street, city, state, and ZIP code fields.
    
    Attributes:
        street: Street address (e.g., "123 Main St")
        city: City name
        state: US state or territory abbreviation (validated)
        zip_code: US ZIP code in 5-digit or ZIP+4 format (validated)
    
    Example:
        address = Address(
            street="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001"
        )
    """
    street: str = Field(..., min_length=1, description="Street address")
    city: str = Field(..., min_length=1, description="City name")
    state: StateAbbr
    zip_code: ZipCode


# Example usage demonstrating the validators
if __name__ == "__main__":
    print("=== Address Validation Tests ===")
    
    # Test with valid address
    try:
        addr1 = Address(street="123 Main St", city="New York", state="NY", zip_code="10001")
        print(f"✓ Valid address: {addr1.street}, {addr1.city}, {addr1.state} {addr1.zip_code}")
    except ValidationError as e:
        print(f"✗ Error: {e}")

    print("\n=== State Validation Tests ===")
    
    # Test with valid US state in address
    try:
        addr2 = Address(street="456 Ocean Dr", city="San Juan", state="PR", zip_code="00901")
        print(f"✓ Valid state (PR): {addr2.state}")
    except ValidationError as e:
        print(f"✗ Error: {e}")

    # Test with invalid abbreviation
    try:
        addr_invalid = Address(street="789 Pine Ln", city="Nowhere", state="XX", zip_code="12345")
        print(f"✓ Valid: {addr_invalid}")
    except ValidationError as e:
        print(f"✗ Invalid state abbreviation caught: XX")

    # Test with lowercase (should fail - case sensitive)
    try:
        addr_lowercase = Address(street="321 Oak Ave", city="Boston", state="ny", zip_code="02101")
        print(f"✓ Valid: {addr_lowercase}")
    except ValidationError as e:
        print(f"✗ Invalid (lowercase not allowed): ny")

    print("\n=== ZIP Code Validation Tests ===")
    
    # Test with valid 5-digit ZIP
    try:
        addr3 = Address(street="123 Main St", city="Anytown", state="CA", zip_code="90210")
        print(f"✓ Valid 5-digit ZIP: {addr3.zip_code}")
    except ValidationError as e:
        print(f"✗ Error: {e}")

    # Test with valid ZIP+4
    try:
        addr4 = Address(street="456 Oak Ave", city="Otherville", state="NY", zip_code="10001-1234")
        print(f"✓ Valid ZIP+4: {addr4.zip_code}")
    except ValidationError as e:
        print(f"✗ Error: {e}")

    # Test with too short ZIP
    try:
        addr_short = Address(street="789 Pine Ln", city="Nowhere", state="TX", zip_code="123")
        print(f"✓ Valid: {addr_short}")
    except ValidationError as e:
        print(f"✗ Invalid ZIP (too short): 123")

    # Test with too long ZIP (6 digits)
    try:
        addr_long = Address(street="Another St", city="Another City", state="FL", zip_code="123456")
        print(f"✓ Valid: {addr_long}")
    except ValidationError as e:
        print(f"✗ Invalid ZIP (6 digits): 123456")

    # Test with invalid ZIP+4 format (missing hyphen)
    try:
        addr_no_hyphen = Address(street="Test St", city="Test City", state="WA", zip_code="981011234")
        print(f"✓ Valid: {addr_no_hyphen}")
    except ValidationError as e:
        print(f"✗ Invalid ZIP+4 (missing hyphen): 981011234")

    print("\n=== Email Validation Tests ===")
    
    class User(BaseModel):
        """Example model using Email validation"""
        name: str
        email: Email

    # Test with valid email
    try:
        user1 = User(name="Alice", email="alice@example.com")
        print(f"✓ Valid email: {user1.email}")
    except ValidationError as e:
        print(f"✗ Error: {e}")

    # Test with valid email (subdomain)
    try:
        user2 = User(name="Bob", email="bob.smith@company.co.uk")
        print(f"✓ Valid email (subdomain): {user2.email}")
    except ValidationError as e:
        print(f"✗ Error: {e}")

    # Test with invalid email (no domain)
    try:
        user_invalid = User(name="Charlie", email="invalid-email")
        print(f"✓ Valid: {user_invalid}")
    except ValidationError as e:
        print(f"✗ Invalid email (no domain): invalid-email")

    # Test with invalid email (no local part)
    try:
        user_invalid2 = User(name="David", email="@example.com")
        print(f"✓ Valid: {user_invalid2}")
    except ValidationError as e:
        print(f"✗ Invalid email (no local part): @example.com")

    # Test with invalid email (invalid domain)
    try:
        user_invalid3 = User(name="Eve", email="eve@.com")
        print(f"✓ Valid: {user_invalid3}")
    except ValidationError as e:
        print(f"✗ Invalid email (invalid domain): eve@.com")

    print("\n=== Phone Number Validation Tests ===")
    
    class ContactInfo(BaseModel):
        """Example model using PhoneNumber and USPhoneNumber validation"""
        name: str
        international_phone: PhoneNumber
        us_phone: USPhoneNumber

    # Test with valid US phone numbers
    try:
        contact1 = ContactInfo(
            name="Alice",
            international_phone="+1-202-555-0123",
            us_phone="+1-202-555-0123"
        )
        print(f"✓ Valid US phone (international format): {contact1.international_phone}")
    except ValidationError as e:
        print(f"✗ Error: {e}")

    # Test with various US phone formats
    try:
        contact2 = ContactInfo(
            name="Bob",
            international_phone="+12125550198",
            us_phone="+12125550198"
        )
        print(f"✓ Valid US phone (compact format): {contact2.us_phone}")
    except ValidationError as e:
        print(f"✗ Error: {e}")

    # Test with international phone (non-US)
    try:
        contact3 = ContactInfo(
            name="Carlos",
            international_phone="+44 20 7946 0958",  # UK number
            us_phone="+14155550100"
        )
        print(f"✓ Valid international phone (UK): {contact3.international_phone}")
    except ValidationError as e:
        print(f"✗ Error: {e}")

    # Test with invalid phone number
    try:
        contact_invalid = ContactInfo(
            name="David",
            international_phone="123",
            us_phone="123-4567"
        )
        print(f"✓ Valid: {contact_invalid}")
    except ValidationError as e:
        print(f"✗ Invalid phone number: 123")

    # Test with non-US phone in US-only field
    try:
        contact_invalid2 = ContactInfo(
            name="Eve",
            international_phone="+44 20 7946 0958",
            us_phone="+44 20 7946 0958"  # UK number in US field
        )
        print(f"✓ Valid: {contact_invalid2}")
    except ValidationError as e:
        print(f"✗ Non-US phone in US field: +44 20 7946 0958")


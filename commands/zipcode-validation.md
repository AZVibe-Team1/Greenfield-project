Using pydanticV2, build code that will take in a 5 character string that should be comprised of U.S. zip codes, and validate that it is a valid zip code.  This code will go in the backend/utils folder in the validators.py file.  As an example see:

import re
from pydantic import BaseModel, Field, ValidationError

# Regular expression for US ZIP codes (5-digit or ZIP+4)
# ^\d{5}$ matches a 5-digit ZIP code
# ^\d{5}-\d{4}$ matches a ZIP+4 code
US_ZIP_CODE_REGEX = r"^\d{5}(?:-\d{4})?$"

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str = Field(pattern=US_ZIP_CODE_REGEX)

# Example usage:
try:
    # Valid ZIP codes
    address1 = Address(street="123 Main St", city="Anytown", state="CA", zip_code="90210")
    print(f"Valid address 1: {address1}")

    address2 = Address(street="456 Oak Ave", city="Otherville", state="NY", zip_code="10001-1234")
    print(f"Valid address 2: {address2}")

    # Invalid ZIP code
    invalid_address = Address(street="789 Pine Ln", city="Nowhere", state="TX", zip_code="123")
    print(f"Invalid address (this line won't be reached): {invalid_address}")

except ValidationError as e:
    print(f"Validation error: {e}")

try:
    invalid_address_format = Address(street="Another St", city="Another City", state="FL", zip_code="123456")
    print(f"Invalid address format (this line won't be reached): {invalid_address_format}")
except ValidationError as e:
    print(f"Validation error for invalid format: {e}")
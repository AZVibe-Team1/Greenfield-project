Using pydanticV2, build code that will take in a 2 character string that should be comprised of U.S. state abbreviations, and validate that it is a valid state abbreviation.  As an example see:
from typing import Annotated
from pydantic import BaseModel, Field
from annotated_types import Len

# A simple regex for 2 uppercase letters (does not check for valid abbreviations)
# A more complex regex would be needed to list all valid ones
STATE_REGEX = r'^(AL|AK|AZ|AR|CA|CO|CT|DE|DC|FL|GA|HI|IA|ID|IL|IN|KS|KY|LA|MA|MD|ME|MI|MN|MO|MS|MT|NC|ND|NE|NH|NJ|NM|NV|NY|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VA|VT|WA|WI|WV|WY)$'

# Define a custom type
StateAbbr = Annotated[str, Field(pattern=STATE_REGEX), Len(2, 2)]

class Person(BaseModel):
    name: str
    residence_state: StateAbbr

# Example Usage
try:
    # Valid input
    person = Person(name="Jane Doe", residence_state="NY")
    print(person)
except ValidationError as e:
    print(e)

try:
    # Invalid input
    person_invalid = Person(name="John Doe", residence_state="XX")
    print(person_invalid)
except ValidationError as e:
    print(e)
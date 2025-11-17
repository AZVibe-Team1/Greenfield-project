Using pydanticV2, build code that will take in a string that should be a valid phone number. This code will go in the backend/utils folder in the validators.py file.  As an example see:


from typing import Annotated, Union

import phonenumbers
from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumberValidator

MyNumberType = Annotated[Union[str, phonenumbers.PhoneNumber], PhoneNumberValidator()]

USNumberType = Annotated[
    Union[str, phonenumbers.PhoneNumber], PhoneNumberValidator(supported_regions=['US'], default_region='US')
]


class SomeModel(BaseModel):
    phone_number: MyNumberType
    us_number: USNumberType
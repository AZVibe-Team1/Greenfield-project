Using pydanticV2, build code that will take in a string that should be a valid phone number. This code will go in the backend/utils folder in the validators.py file.  As an example see:


from pydantic import BaseModel, EmailStr, ValidationError

# Define the Pydantic model
class User(BaseModel):
    name: str
    email: EmailStr

# Valid email address
try:
    user1 = User(name="Alice", email="alice@example.com")
    print(f"User 1: {user1}")
except ValidationError as e:
    print(f"Error for User 1: {e}")

# Invalid email address
try:
    user2 = User(name="Bob", email="invalid-email")
    print(f"User 2: {user2}")
except ValidationError as e:
    print(f"Error for User 2: {e}")

# Another invalid email address
try:
    user3 = User(name="Charlie", email="charlie@.com")
    print(f"User 3: {user3}")
except ValidationError as e:
    print(f"Error for User 3: {e}")
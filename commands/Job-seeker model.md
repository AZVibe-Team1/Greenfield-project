# Job Seeker Model Specifications

Using Beanie, create a mongodb data structure that has the following requirements, uses the base model from utils.validators.py and is stored in the backend/schemas folder:

1. class name is Seeker
2. Entity: _id  type: mongodb
3. Entity: Information type: sub-document  Required
3.1 entity: FirstName type: string Required
3.2 entity: LastName type: string Required
3.3 entity: address type: class address from backend.utils.validators.py required
4. Entity: password_hash type: string Required Field(..., min_length=6, description="Hashed password")
5. Entity: created_at timestamp type: datetime Field(default_factory=datetime.now)
5.1 Entity: updated_at timestamp type: datetime Field(default_factory=datetime.now
6. Entity: Resume type: sub-document (string)
7. Entity: Pay_range type: integer array 2 element (high/low)
8. Entity: Pay_unit type: string {"Hourly", "Monthly", "Yearly"}
9. Entity: Education_level type: string {"BA", "BS", "MA", "MS", "MBA", "PhD"}  Required
10. Entity: Edu_Focus type: string Required
11. Entity: Key_Skills type: string array, max 15 elements
12. Entity: Applications: type: sub-document
12.1 entity: JobId (foreign key from Employer collection)
12.2 entity: EmployerId (foeign key from Employer collection)
12.3 entity: date_applied type: datetime
12.4 entity: application_status type: string {"Submitted", "Interviewd", "Offered", "Rejected"}

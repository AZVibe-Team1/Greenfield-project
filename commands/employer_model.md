# Employer Model Specifications

Using Beanie, create a mongodb data structure that has the following requirements, uses the base model from utils.validators.py and is stored in the backend/schemas folder:

1. class name is Employer
2. Entity: _id  type: mongodb
3. Entity: Company_Information type: sub-document  Required
3.1 Entity: Company_Name type: string Required
3.2 entity: address type: class address from backend.utils.validators.py required
3.3 entity: Industry type: string array 2 element code, description from backend.utils.gics.py
3.4 entity: Benefits type: string

4. Entity: Contact_FirstName type: string Required
5. entity: Contact_LastName type: string Required
6. entity: password_hash type: string Required Field(..., min_length=6, description="Hashed password")
7. Entity: created_at timestamp type: datetime Field(default_factory=datetime.now)
7.1 Entity: updated_at timestamp type: datetime Field(default_factory=datetime.now)
8. Entity: Open_Job type: sub-document Required
8.1 entity: Job_ID type: mongodb
8.2 entity: Job_Title type: string required
8.3 entity: Job_Description type: string required
8.4 entity: Posted_Date type: datetime required
8.5 entity: Department type: string required
8.6 entity: Hire_Mgr_First type: string required
8.7 entity: Hire_Mgr_Last type: string required
8.8 entity: current_status: Literal["Posted", "Withdrawn", "Pending", "Canceled"] =           Field( default="Posted")
8.9 entity: Pay_range type: integer array 2 element (high/low)required
8.10 entity: Pay_unit type: string {"Hourly", "Monthly", "Yearly"} required
8.11 entity: Education_level type: string {"BA", "BS", "MA", "MS", "MBA", "PhD"}  Required
8.12 entity: Edu_Focus type: string Required
8.13 entity: Key_Skills type: string array, max 15 elements
9. Entity: Apps_Received: type: sub-document
9.1 entity: Applicant_ID (foreign key from Seeker collection)
9.2 entity: Job_Id (foreign key from Employer collection)
9.3 entity: initial_daterec type: datetime
9.4 entity: Candidate_Tracking type: sub-document
9.41 entity: current_status type: string {"Received", "Interviewed", "Offered", "Rejected","Canceled"}
9.42 entity: previous_status type: string {"Received", "Interviewed", "Offered", "Rejected","Canceled"}
9.43 entity: current_status_date type: datetime
9.44 entity: previous_status_date type: datetime.

# Add EmployerID to schema and services layer

Modify the employer.py file in the schemas folder to add a field called "EmployerID".  This will be a UUID type 1.  It should be
the first data item in the class of employer.  It will be defined as 'required' before the employer record can be created
in the database.  
Next modify the employer_services.py file, located in the services folder.  Specifically on entry into the function 'create_new_employer',
insert code similiar to:
import uuid

EmployerID = uuid.uuid4()

Modify the seeker.py file in the schemas folder to add a field called "SeekerID".  This will be a UUID type 1.  It should be
the first data item in the class of seeker.  It will be defined as 'required' before the seeker record can be created
in the database.  
Next modify the seeker_services.py file, located in the services folder.  Specifically on entry into the function 'create_new_seeker',
insert code similiar to:
import uuid

SeekerID = uuid.uuid4()


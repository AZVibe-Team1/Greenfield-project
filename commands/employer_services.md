Using the employer.py class in backend/schemas, create the following services, and place the code in
the file employer_services.py in backend/services folder.
1. Create a new employer, called 'create_new_employer'.  This service will create a new employer record.  It will collect the items as described in
the information record at a minimum.  If the industryinfo field is populated, the value will be validated by a 
call to "validate_gics_code(cls, v: str)", which is in the utils folder.  It will also collect all other required information.  Once done, it will call
the create_employer db operation, to write the record out.  The field 'created_at' will be populated with the
current datetime value before writing to the database.
2. Update any/all of the employer's items.  Here any item, other than companyname can be updated, and then written 
back out to the record.  The field 'updated_at' will be populated with the current datetime value before 
being written to thedatabase.
4. Create_job.  Here the OpenJob record will be filled out, the status set to 'Posted' and the record
written to the database as a document within the Employer document.
5. Modify_job. Once a specific jobid is selected, the user can makes changes, including to status.  The updated record
will be written back to the database.
6. Delete_employer.  Here the employer document that is identified by the supplied companyname will be deleted
from the database.  
7. Delete_job.  Given a job id, and company name, this record will be deleted from the seekers collection.
8. Search_all_jobs  This will return a search of all jobs in the employer table.
  
9. Search_by_parameter. Given a parameter (jobtitle, companyname, skill), the employer collection will be searched, and
when any parameter is met, that information will be returned for display.
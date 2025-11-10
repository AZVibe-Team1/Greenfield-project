Using the seeker.py class in backend/schemas, create the following services, and place the code in
the file seeker_services.py in backend/services folder.
1. Create a new seeker, called 'create_new_seeker'.  This service will create a new seeker record.  It will collect the items as described in
the information record at a minimum.  It will also, collect all other required information.  Once done, it will call
the create_seeker db operation, to write the record out.  The field 'created_at' will be populated with the
current datetime value before writing to the database.
2. Create a upload resume operations, called 'upload_resume'.  This will allow the user to either type in all resume, or
provide a file location to upload.  A resume must be text only.  If the upload is a .pdf or .docx filetype, it must be converted
to text.  Once uploaded, it is written to the seeker record via the 'update_seeker' db operation.
The field 'updated_at' will be populated with the current datetime value before 
being written to thedatabase.
3. Update any/all of the seeker's items.  Here any item, other than firstname and lastname can be updated, and then written 
back out to the record.  The field 'updated_at' will be populated with the current datetime value before 
being written to thedatabase.
4. Apply_for_job.  Here the application record will be filled out, the status set to 'Submitted' and the record
written to the database as a document within the Seeker document.
5. Delete_user.  Here the Seeker document that is identified by the supplied firstname and lastname will be deleted
from the database.  
6. Delete_application.  Given a job id, and company name, this record will be deleted from the seekers collection.
7. Search_all_jobs  This will return a search of all jobs in the employer table.
8. Search_current_status.  A status will be passed in from the seeker, and all jobs applied to with that status will
be returned.  
9. Search_by_parameter. Given a parameter (jobtitle, companyname, skill), the employer collection will be searched, and
when any parameter is met, that information will be returned for display.
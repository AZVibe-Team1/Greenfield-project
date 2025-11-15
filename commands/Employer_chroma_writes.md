 # Add chroma add call to create_new_employer and new job, as wellas modify job.
 In the file employer_services.py file, modify the create_job function to add a call to write_collection function from the chroma_crud_ops.py file.
 this call will be placed right before the end of the create_job function and do the following:
 If the job description is not empty, then 
 a) create a Json variable called metadata that looks like:
 metadata_descr=[{"Title": job_title, "Post_Date": posted_date, "Employer_UUID", employer_identification }]
 b) call write_collection passing in following variables: Employer_JobDescr_Collection,"Employer_JobDescr_Collection", Job_Identification,job_description, metadata_descr
 #
 If the key_skills, or education_level or edu_focus have data, then
 a) create a variable called Skills that concatenates key_skills, education_level and edu_focus
 b) create a variable called metadata_skill=[{"Desired Skills", Skills]
 c) call write_collection passing in following variables: Employer_Skillswish_Collection, "mployer_Skillswish_Collection", Job_Identification,Skills, metadata_skill
 #
 In the modify_job function, add a call to update_collection with:
  a) create a Json variable called metadata that looks like:
 metadata_descr=[{"Title": job_title, "Post_Date": posted_date, "Employer_UUID", employer_identification }]
 b) call update_collection passing in following variables: Employer_JobDescr_Collection,"Employer_JobDescr_Collection", Job_Identification,job_description, metadata_descr
 then do 
 c) create a variable called Skills that concatenates key_skills, education_level and edu_focus
 d) create a variable called metadata_skill=[{"Desired Skills", Skills]
 e) call write_collection passing in following variables: Employer_Skillswish_Collection, "mployer_Skillswish_Collection", Job_Identification,Skills, metadata_skill
 #

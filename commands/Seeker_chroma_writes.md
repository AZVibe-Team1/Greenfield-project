 # Add chroma add call to create_new_seeker and update_seeker_profile.
 In the file seeker_services.py file, modify the create_new_seeker function to add a call to write_collection function from the chroma_crud_ops.py file.
 this call will be placed right before the end of the create_new_Seeker function and do the following:
 If the resume is not empty, then 
 a) create a Json variable called metadata that looks like:
 metadata_resume=[{"Post_Date": created_at}]
 b) call write_collection passing in following variables: Seeker_Resume_Collection,"Seeker_Resume_Collection", Seeker_Identification,resume, metadata_resume
 #
 If the key_skills, or education_level or edu_focus have data, then
 a) create a variable called Skills that concatenates key_skills, education_level and edu_focus
 b) create a variable called metadata_skill=[{"Desired Skills", Skills]
 c) call write_collection passing in following variables: Seeker_Skills_Collection, "Seeker_Skills_Collection", Seeker_Identification,Skills, metadata_skill
 #
 In the Update_seeker_profile function, add a call to update_collection with:
  a) create a Json variable called metadata that looks like:
 metadata_descr=[{"Post_Date": created_at}]
 b) call update_collection passing in following variables: Seeker_Resume/  _Collection,"Seeker_Resume_Collection", Seeker_Identification,resume, metadata_resume
 then do 
 c) create a variable called Skills that concatenates key_skills, education_level and edu_focus
 d) create a variable called metadata_skill=[{"Desired Skills", Skills]
 e) call write_collection passing in following variables: Seeker_Skills_Collection, "Seeker_Skills_Collection", Seeker_Identification,Skills, metadata_skill
 #

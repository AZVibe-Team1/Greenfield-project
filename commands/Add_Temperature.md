# Add 'Temperature' value to both employer and job seeker data classes and services.
## Employer update
Add a data item called temperature to the employer.py file in the schemas folder.  Place it in/near employer_id and before
company_informatoin in the Employer class.
This item will be a float value that can range from 0 to 1.  It's default value will be 0.75.
Then add this element to every function in the employer_services.py in the services folder, where ever the Employer class is used.
## Seeker update
Add a data item called temperature to the seeker.py file in the schemas folder.  Place it in/near seeker_id and before
 the information in the Seeker class.
This item will be a float value that can range from 0 to 1.  It's default value will be 0.75.
Then add this element to every function in the seeker_services.py in the services folder, where ever the Employer class is used.
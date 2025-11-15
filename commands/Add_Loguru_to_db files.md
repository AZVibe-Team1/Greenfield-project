# Add Loguru Logging to employer_db_ops.py and seeker_db_ops.py

Modify the employer_db_ops.py file, located in backend/db to include the use of loguru by modifying the following code: 
everywhere there is a print statement that is not in an exception or else clause, change the print statement to
a logger.debug(%x), where %x is the current value in the print statement.
Where the print statement is part of an exception or else caluse, change the print statement to logger.critical(%x), where %x is the
current value in the print statement.
Modify the seeker_db_ops.py file, located in backend/db to include the use of loguru by modifying the following code: 
everywhere there is a print statement that is not in an exception or else clause, change the print statement to
a logger.debug(%x), where %x is the current value in the print statement.
Where the print statement is part of an exception or else caluse, change the print statement to logger.critical(%x), where %x is the
current value in the print statement.

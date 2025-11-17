# Add Loguru Logging to settings.py

Modify the settings.py file, located in backend/db to include the use of loguru.  The first thing to do
is to add the statement logger.remove(0) right after the load_dotenv() call.  Then add 2 seperate log files.  the log files will
be written to the folder 'Logs' in the project.  The first file
will be defined by the statement logger.add("Debug_log.log", level="DEBUG", foramt="{time}  {level} {message}", rotation=50MB)
The second will be defined by the statement logger.add("Debug_log.log", level="DEBUG", foramt="{time}  {level} {message}", rotation=50MB)

Then,also in settings.py, modify the following code:
everywhere there is a print statement that is not in an exception or else clause, change the print statement to
a logger.debug(%x), where %x is the current value in the print statement.
Where the print statement is part of an exception or else caluse, change the print statement to logger.critical(%x), where %x is the
current value in the print statement.

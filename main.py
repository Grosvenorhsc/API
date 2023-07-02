import candidates     # import the candidates module
import placements     # import the placements module
import applications   # import the applications module
import companies      # import the companies module
import references     # import the references module
import questions      # import the questions module
import vacancys       # import the vacancy module
import actions       # import the actions module
import Workflow       # import the actions module
import applications_status_history       # import the actions module
import logging
import datetime
import logging.handlers
import os

# Configure logging
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create a log file with date timestamp
log_filename = "project.log"

# Create a rotating file handler with log rotation and compression
log_handler = logging.handlers.RotatingFileHandler(
    log_filename, maxBytes=10485760, backupCount=5)
log_handler.setFormatter(log_formatter)

# Create a logger and add the log handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# Start time of the run
start_time = datetime.datetime.now()

# Log the start time
logger.info("Run started at %s", start_time)

# End time of the run
end_time = None

try:

    companies.get_companies()
    vacancys.get_vacancys()
    candidates.get_candidates()
    questions.get_questions()
    references.get_refference()
    applications.get_applications()
    placements.get_placements()
    applications_status_history.get_status_history()
    # #Workflow.get_workflow()
    # #actions.get_actions()
finally:
    # Log the end time and duration
    end_time = datetime.datetime.now()
    logger.info("Run finished at %s", end_time)
    logger.info("Duration: %s", end_time - start_time)

    # Check if the log file has reached its maximum size
    if os.path.getsize(log_filename) >= log_handler.maxBytes:
        # Rename the log file to an archive file with a timestamp
        archive_filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".log"
        os.rename(log_filename, archive_filename)

        # Create a new log file
        log_handler.doRollover()

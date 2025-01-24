import candidates         # import the candidates module
import placements         # import the placements module
import applications       # import the applications module
import companies          # import the companies module
import references         # import the references module
import questions          # import the questions module
import vacancys           # import the vacancy module
import fixbroken          # import the fixbroken module
# import actions            # import the actions module
# import Workflow           # import the actions module
# import applications_status_history  # import the actions module

# # Import necessary data
print("getting company data")
companies.get_companies()
print("getting vacancy data")
vacancys.get_vacancys()
print("getting candidate data")
candidates.get_candidates()
print("getting applications data")
applications.get_applications()
print("getting placement data")
placements.get_placements()
print("getting question data")
questions.get_questions()
print("getting refference data")
references.get_refference()

# Fix broken dataf
fixbroken.fixbroken()

# applications_status_history.get_status_history()
# #Workflow.get_workflow()
# #actions.get_actions()


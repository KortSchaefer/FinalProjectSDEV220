'''This file created by: Derek Gerry is for the converting of the 
numbers for each server into meaningful output. '''
#-----------------------
import os
import django

# Add the full path to your project's folder to the Python path
import sys
sys.path.append(r'c:\Users\derek\Derek_LG\IVY tech SDEV 220\Final Project things\FinalProjectSDEV220')

# Configure Django settings module
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FinalProjectFolder.settings')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_project_folder.settings")

# Run the setup() function to load settings and populate the app registry
django.setup()

#1_Get each of the server's information for individual processing. 
'''This will come from the statistics worksheet or
from the data on each server individually.'''
    #Loop to obtain the data from the database(?)

#_____________________________________________
# def run_algorithm():
#     """
#     This function retrieves data from the MyModel and processes it.
#     """
#     all_items = MyModel.objects.all()

#     for item in all_items:
#         print(f"ID: {item.id}, Name: {item.name}, Upsell Score: {item.upsellScore}")

#         # You can now use the model data in your algorithm.
#         # For example, to calculate a new metric:
#         performance_score = item.upsellScore * item.length_of_employment
#         print(f"  Calculated Performance Score: {performance_score}\n")

# if __name__ == "__main__":
#     run_algorithm()
#____________________________________________

from servers.models import Server 

def run_algorithm():
    """
    Retrieves data from the Server model and runs a custom algorithm.
    """
    # Use the Django ORM to query the database
    all_servers = Server.objects.all()

    if not all_servers.exists(): #Error Handler
        print("No server data found in the database.")
        return

    # Loop through the results and access the data
    for server in all_servers:
        print(f"Processing server: {server.name}")

        # Access specific model attributes
        assigned_number = server.id
        
        upsell_score = server.upsellScore
        hours_scheduled = server.hoursScheduled
        #------------------------------------
        # id = models.CharField(max_length=50, primary_key=True)
        # name = models.CharField(max_length=100)
        # upsellScore = models.IntegerField()
        # sectionAssigned = models.CharField(max_length=50)
        # timeIn = models.DateTimeField()
        # hoursScheduled = models.IntegerField()
        # length_of_employment = models.IntegerField()
        # max_guests = models.IntegerField()
        # pyos = models.IntegerField()
        # pitty = models.IntegerField()
        #------------------------------------

        # Your algorithm logic goes here
        # For example, you can calculate a performance metric
        performance_metric = upsell_score + (hours_scheduled * 1.5)
        print(f"  Calculated performance metric: {performance_metric}")

        # Example: Filter for servers that worked a lot
        if hours_scheduled > 30:
            print(f"  Note: {server.name} worked {hours_scheduled} hours this week.")



#-------------------------------------------
    
#for eachServer in server:
    #server = Server.views.server_list(All)

#Bring these fields in from Models.Server
    # id = models.CharField(max_length=50, primary_key=True)
    # name = models.CharField(max_length=100)
    # upsellScore = models.IntegerField()
    # sectionAssigned = models.CharField(max_length=50)
    # timeIn = models.DateTimeField()
    # hoursScheduled = models.IntegerField()
    # length_of_employment = models.IntegerField()
    # max_guests = models.IntegerField()
    # pyos = models.IntegerField()
    # pitty = models.IntegerField()


#2_Process the data

#3_Set variable for server_score. This will be the output from this algorythm.

if __name__ == "__main__":
    run_algorithm()
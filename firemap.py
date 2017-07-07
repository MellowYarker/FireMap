"""This is the main file of the firemap program. """
import os
import webbrowser
# TODO make geocoding more efficient by checking if a location has already been geocoded
#   Maybe use a dictionary? At the bare minimum it won't need to geocoded an updated event
#   This would be most efficient if every time the firemap.py file ran, it could just check if the geocode exists already

# TODO If an event has been updated "UD:" then remove the previous version of the event
#   This can be done by comparing the location and event (Not description, just the event type)

# TODO consider altering the input of functions in the currator.py file, currently takes a string, try taking a list of strings to make it easier to check if a tweet has been updated or something idk I wanna go to tims I'm so hungry and I don't have class for 4 hours :(

os.system('python3 crawler.py')
os.system('python3 format.py')

"""This is the main file of the firemap program. """
import os
import webbrowser
# TODO make geocoding more efficient by checking if a location has already been geocoded
#   Maybe use a dictionary? At the bare minimum it won't need to geocoded an updated event
#   This would be most efficient if every time the firemap.py file ran, it could just check if the geocode exists already


os.system('python3 crawler.py')
os.system('python3 format.py')

Autogenerate a map that displays emergencies that the Toronto Fire Department has responded to.

To run it, add your twitter API tokens to crawler.py, and add your Google Maps API key to the long string in format.py (near the bottom).
Once you have done this, simply open a terminal, go to the directory you have this repo saved to, and type python3 firemap.py.
This should take some time (maybe 30 seconds if you're collecting 20 or more tweets) as the code hasn't been optimized yet.
Once map.html is created, view it in a webbrowser.
A legend still needes to be added:
blue = medical
green = alarm
pink = other
shades of red or just black = fire (the darker the red the more severe)


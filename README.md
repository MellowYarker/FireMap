Autogenerate a map that displays emergencies that the Toronto Fire Department has responded to.<br />

To run it, add your twitter API tokens to crawler.py, and add your Google Maps API key to the long string in format.py (near the bottom).<br />
Once you have done this, simply open a terminal, go to the directory you have this repo saved to, and type python3 firemap.py.<br />
This could quite a bit of time the first time you run it (as many locations have not been geocoded yet, and this takes some time). If you run it again it shouldn't take more than 6 seconds as the locations that did not have geocodes before have been added to a dictionary and serialized in the geocodes file.<br />
Once map.html is created, view it in a webbrowser.<br /><br />
A legend still needes to be added:<br />
darker blue = medical<br />
green = alarm<br />
lighter blue = vehicle <br />
pink = other<br />
shades of red or just black = fire (the darker the colour the more severe, black being the most dangerous level.)<br />


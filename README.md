# FireMap <br />
### Autogenerate a map that displays emergencies that the Toronto Fire Department has responded to.

### How to run it <br />
1. Add your API keys
	1. Twitter API tokens in crawler.py
	2. Google Maps API key in format.py (within the long string near the bottom of the file)
2. Open a terminal and navigate to the directory you have this repo saved to.
3. Type python3 firemap.py.
	* **This *could* take quite a bit of time the first time you run it** (took me 20-30 min for 3200 tweets and 0-1 second after on the same data set.)
	* This is due to the fact that many of the locations have not been geocoded yet.
		* Geocoding takes the bulk of the time
	* If you run it again it shouldn't take more than a few seconds as the locations that did not have geocodes before have been added to a dictionary and serialized in the geocodes file.
4. Once map.html is created, open it in a browser.
### Notes <br />

* I'm not a fan of how slow the process of geocoding is compared to accessing an existing geocode.<br />
	* If I find a decent open source dataset of all the intersections in Toronto and their geocodes, I'll try to implement that.
	    * Obvious downsides to this:
	        1. Having a massive file of intersections
	        2. Overhauling a lot of code
	* Until then I will continue to add locations (provided by the twitter page I get the data from) to increase the possibility of location matches in the future.
	    * To do this I wrote a simple script to gather a few thousand tweets every 2 days and try geocoding them.
	    * once the *fails* list is large enough I'll write a program to find similarities that cause failures and I'll implement solutions in clean.py's reformat funciton.<br />
* A legend still needs to be added:<br />
	* Lighter Bluish/Green = Vehicle <br />
	* Darker Blue = Medical<br />
	* Green = Alarm<br />
	* Shades of Red or just Black = Fire (the darker the colour the more severe, black being the most dangerous level.)<br />
	* Pink = Other<br /><br />

* **The idea is for it to use a *MVC* design.**
	* Accept inputs in browser, run computations in a model (class or file of functions), then display the result in a view.<br />

* I'll be adding more descriptive docstrings over time. The doctests in clean.py should give a pretty good intuition of what each function does.

* At the moment, the map is pretty useless (due to the lack of a legend and any interactive features).
	* I've been working with the backend so I can put a good chunk of time on the UI later, I might build a Django application where this fire map application will be part of something bigger.

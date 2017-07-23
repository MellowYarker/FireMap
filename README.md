# FireMap <br />
### Autogenerate a map that displays emergencies that the Toronto Fire Department has responded to.

* **Before this can work you'll need to install some python libraries.**
1. Open a terminal and navigate to the directory you saved this repo in
2. Type the following
	* sh install_dependencies.sh
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

![Map](https://github.com/MellowYarker/FireMap/blob/master/screenshots/map.png?raw=true "Map Example")<br />
### NOTICE <br />

* I'm not too invested in this project anymore because the rest is just developing functionality and design. It's not that I'm not interested in that stuff it's just not worth my time to continue the development. I built this tool for fun, not for usability, I accomplished what I set out to do.
	* At the time of writing you run a python script that does everything, I was hoping to have it work by clicking a 'scan' button on a web page.
	* I also planned on trying to track fire trucks, and finding optimal routes from fire stations to emergency locations.
	* Events aren't very descriptive at the moment either, there aren't even timestamps.
	* These things shouldn't be very difficult to implement.
* I may add to this over time but for now it's done. <br />

### Notes <br />
* I'm not a fan of how slow the process of geocoding is compared to accessing an existing geocode.<br />
	* If I find a decent open source dataset of all the intersections in Toronto and their geocodes, I'll try to implement that.
	    * Obvious downsides to this:
	        1. Having a massive file of intersections
	        2. Overhauling a lot of code
	* Until then I will continue to add locations (provided by the twitter page I get the data from) to increase the possibility of location matches in the future.
	    * To do this I wrote a simple script to gather a few thousand tweets every 2 days then try geocoding them.
			* After this a shell script is executed and it pushes the changes to github so you can access the same dictionaries that I can.
	    * Once the *fails* list is large enough I'll write a program to find similarities that cause failures and I'll implement solutions in clean.py's reformat function.<br />

* The legend needs improvement, a number line with coloured circles depicting alarm levels needs to be added
* Some tweets say b/w in the text, which means "between". For example "Yonge St b/w Bloor/ college" which means "Yonge street between Bloor and college". Instead of getting a point in between I just picked one of the streets and removed the other. 

* I'll be adding more descriptive docstrings over time. The doctests in clean.py should give a pretty good intuition of what each function does.

* The map is becoming more usable. I need to do a little more work on the backend before I can work on UI.

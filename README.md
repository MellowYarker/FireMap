# FireMap <br />
###Autogenerate a map that displays emergencies that the Toronto Fire Department has responded to.

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

I'm not a fan of how slow the process of geocoding is compared to accessing an existing geocode.
	* If I find a decent open source dataset of all the intersections in Toronto and their geocodes, I'll try to implement that.<br />
A legend still needs to be added:<br />
	Lighter Bluish/Green = Vehicle <br />
	Darker Blue = Medical<br />
	Green = Alarm<br />
	Shades of Red or just Black = Fire (the darker the colour the more severe, black being the most dangerous level.)<br />
	Pink = Other<br /><br />

This needs a lot of work, the basic functionality is there but there's a lot of redundant code; it's very 'hacked together'.<br />
I'm sure some of the code is actually irrelevant as the functions were originally developed to splice a string of html that was parsed using *BeautifulSoup* (before using the Twitter API I just built a simple webcrawler to grab the HTML from the webpage).<br />

The format.py file basically runs through like a script, which I don't really like. It's pretty challenging to follow the code, so I'll progressively turn everything into functions and possibly implement another class so that it's simple to follow.<br />

The idea is for it to use a MVC design. Accept inputs in browser, run computations in a model (class or file of functions), then display the result in a view.<br />

The documentation is also pretty sparce, it'll be descriptive enough soon.<br /><br />
At the moment, the map is pretty useless (due to the lack of a legend and any interactive features). I've been working with the backend so I can put a good chunk of time on the UI later, I might build a Django application where this fire map application will be part of something bigger.

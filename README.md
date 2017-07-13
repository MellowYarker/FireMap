Markup : # FireMap #<br />
<b>Autogenerate a map that displays emergencies that the Toronto Fire Department has responded to.</b> <br />

Markup: ### How to run it ###<br />
Markup: 1. Add your API keys
 			1. Twitter API tokens in crawler.py
			2. Google Maps API key in format.py (within the long string near the bottom of the file)
		2. Open a terminal and navigate to the directory you have this repo saved to.
		3. Type python3 firemap.py.
			* <b>This <i>could</i> take quite a bit of time the first time you run it</b>(took me 20-30 min for 3200 tweets.)
			* This is due to the fact that many of the locations have not been geocoded yet.
				* Geocoding takes the bulk of the time
			* If you run it again it shouldn't take more than a few seconds as the locations that did not have geocodes before have been added to a dictionary and serialized in the geocodes file.
		4. Once map.html is created, open it in a browser.
Markup: ## Notes ##<br />

I'm not a fan of how slow the process of geocoding is compared to accessing an existing geocode, so if I find a decent open source dataset of all the intersections in Toronto and their geocodes, I'll just use that.<br />
A legend still needes to be added:<br />
darker blue = medical<br />
green = alarm<br />
lighter bluish/green = vehicle <br />
pink = other<br />
shades of red or just black = fire (the darker the colour the more severe, black being the most dangerous level.)<br />

This needs a lot of work, the basic functionality is there but there's a lot of redundant code; it's very 'hacked together'.<br />
The format.py file basically runs through like a script, which I don't really like. It's pretty challenging to follow the code, so I'll progressively turn everything into functions and maybe implement another class so that it's simple to follow.<br /> The idea is for it to use a MVC design. Accept inputs in browser, run computations in a model (class or file of functions), then display the result in a view.<br /><br />
The documentation is also pretty sparce, it'll be descriptive enough soon.<br /><br />
At the moment, the map is pretty useless (due to the lack of a legend and any interactive features). I've been working with the backend so I can put a good chunk of time on the UI later, I might build a Django application where this fire map application will be part of something bigger.

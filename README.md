<b>Autogenerate a map that displays emergencies that the Toronto Fire Department has responded to.<b><br />

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

This needs a lot of work, the basic functionality is there but there's a lot of redundant code; it's very 'hacked together'.<br />
The format.py file basically runs through like a script, which I don't really like. It's pretty challenging to follow the code, so I'll progressively turn everything into functions and maybe implement another class so that it's simple to follow. <br /><br />
The documentation is also pretty sparce, it'll be descriptive enough soon.<br /><br />
The map itself doesn't really do much without a legend, or any interactive features, I've been dealing with the backend a lot so I can put a good chunk of time on the UI later.

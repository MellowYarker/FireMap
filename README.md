This program collects and currates data from a twitter page that posts updates
regarding situations that the Toronto Fire Department responds to and plots it
on a map.

The colour of the circle varies according to the type of emergency the fire
department is responding to, I wrote a script that found the occurences of each
type of emergency and automatically put them and the number of occurences in a
dictionary like this {'emergency': occurence}.

The size of the circle depends on the number of trucks responding to the call,
the more trucks the larger the circle, implying a more dire situation.

I might find the locations of all the firehouses to try to estiamte where the
trucks are actually coming from and depending on how much time has elapsed show
where the trucks might actually be

To execute the program, open a terminal and type
~ python3 firemap.py

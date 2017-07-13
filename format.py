import currator as currate
import geocoder
from event import Event
import os
import pickle
import time

now = time.time()

fname = 'extracted.txt'
with open(fname, 'r') as f:
    text = f.readlines()

# print(text)

tweet_list = currate.check_type_of_tweet(text)

# Check if updates.txt exists (if it does that means some tweets were updated
# so there won't be as many events on the map as there were tweets pulled from
# Twitter
if os.path.exists(os.getcwd()+'/updates.txt'):
    with open('updates.txt', 'r') as f:
        updates = f.readline()
    # print(updates)

# for i in tweet_list:
#     print(i[1], i[3], i[4])

# Try geocoding here, if it fails, reformat, if it still fails, remove the event
failed_index = []

# Check if the geocodes file exists, if it does load the dictionary of codes
# dictionary_exists = False
if os.path.exists(os.getcwd()+'/geocodes'):
    # dictionary_exists = True
    with open('geocodes', 'rb') as values:
        codes = pickle.load(values)
        # print(len(codes))
    # print(codes)
else:
    # if dictionary_exists is False:
    codes = {}


if os.path.exists(os.getcwd() + '/failed'):
    with open('failed', 'rb') as failures:
        fails = pickle.load(failures)
else:
    fails = {}


for location in range(len(tweet_list)):
    # print(str(location) + ': ', tweet_list[location][1])
    # Make sure the location hasn't already been geocoded
    if not isinstance(tweet_list[location][1], list):
        # If the geocode dictionary is not empty
        if len(codes) > 0:
            # Check if it is in the dictionary
            if tweet_list[location][1] in codes:
                # If it is, use that geocode.
                # print(codes[tweet_list[location][1]])
                tweet_list[location][1] = codes[tweet_list[location][1]]
            # If the dictionary of locations that failed is not empty
            elif len(fails) > 0:
                # Check if it is in this dictionary
                if tweet_list[location][1] in fails:
                    # If it is, increase the count of failures on that location.
                    # print(fails[tweet_list[location][1]])
                    fails[tweet_list[location][1]] += 1
                    failed_index.append(location)
                # If it is not in the dictionary, create the geocode and add it
                # to the correct dictionary.
                else:
                    g = geocoder.google(tweet_list[location][1])
                    if g.latlng != []:
                        # print(g.latlng)
                        codes[tweet_list[location][1]] = g.latlng
                        tweet_list[location][1] = g.latlng
                    else:
                        retry = currate.reformat(tweet_list[location][1])
                        g = geocoder.google(retry)
                        if g.latlng != []:
                            # print(g.latlng)
                            codes[tweet_list[location][1]] = g.latlng
                            tweet_list[location][1] = g.latlng
                        else:
                            fails[tweet_list[location][1]] = 1
                            # print(fails[tweet_list[location][1]])
                            failed_index.append(location)
            # If the fail dictionary is empty, create the geocode and add it to
            # the correct dictionary
            else:
                g = geocoder.google(tweet_list[location][1])
                if g.latlng != []:
                    # print(g.latlng)
                    codes[tweet_list[location][1]] = g.latlng
                    tweet_list[location][1] = g.latlng
                else:
                    retry = currate.reformat(tweet_list[location][1])
                    g = geocoder.google(retry)
                    if g.latlng != []:
                        # print(g.latlng)
                        codes[tweet_list[location][1]] = g.latlng
                        tweet_list[location][1] = g.latlng
                    else:
                        fails[tweet_list[location][1]] = 1
                        failed_index.append(location)

        # If the geocode dictionary is empty
        else:
            # If the dictionary of locations that failed is not empty
            if len(fails) > 0:
                # Check if it is in this dictionary
                if tweet_list[location][1] in fails:
                    # print(fails[tweet_list[location][1]])
                    # If it is, increase the count of failures on that location.
                    fails[tweet_list[location][1]] += 1
                    failed_index.append(location)
                # If it is not in the dictionary, create the geocode and add it
                # to the correct dictionary.
                else:
                    g = geocoder.google(tweet_list[location][1])
                    if g.latlng != []:
                        # print(g.latlng)
                        codes[tweet_list[location][1]] = g.latlng
                        tweet_list[location][1] = g.latlng
                    else:
                        retry = currate.reformat(tweet_list[location][1])
                        g = geocoder.google(retry)
                        if g.latlng != []:
                            # print(g.latlng)
                            codes[tweet_list[location][1]] = g.latlng
                            tweet_list[location][1] = g.latlng
                        else:
                            # Geocoding isn't gonna work on this value,
                            # need to make note of
                            # the index and remove outside the loop
                            fails[tweet_list[location][1]] = 1
                            failed_index.append(location)
            # If the fail dictionary is empty, create the geocode and add it to
            # the correct dictionary
            else:
                g = geocoder.google(tweet_list[location][1])
                if g.latlng != []:
                    # print(g.latlng)
                    codes[tweet_list[location][1]] = g.latlng
                    tweet_list[location][1] = g.latlng
                else:
                    retry = currate.reformat(tweet_list[location][1])
                    g = geocoder.google(retry)
                    if g.latlng != []:
                        # print(g.latlng)
                        codes[tweet_list[location][1]] = g.latlng
                        tweet_list[location][1] = g.latlng
                    else:
                        fails[tweet_list[location][1]] = 1
                        failed_index.append(location)

# Codes has been updated, serialize it again so it can be accessed later
with open('geocodes', 'wb') as values:
    pickle.dump(codes, values)

with open('failed', 'wb') as failures:
    pickle.dump(fails, failures)

# Remove locations that couldn't be geocoded
# Put all locations that could not be geocoded into a list to figure out why the
# geocoding failed and find a work around
if len(failed_index) > 0:
    # print('Some failed to geocode')
    # for i in failed_index:
        # print(tweet_list[i])

    # Every time an event is deleted from the list, the length of the list
    # gets smaller, so this accounts for that and decreases the index by 1
    failed_locations = []
    for index in range(len(failed_index)):
        failed_locations.append(tweet_list[failed_index[index]][1])
        del tweet_list[failed_index[index]]
        for i in range(len(failed_index)):
            failed_index[i] -= 1
    # for i in failed_locations:
    #     print(i)
# print(len(tweet_list))
final = []
for i in tweet_list:
    final.append(Event(i))
    # print(Event(i).location)


# TODO Add description to a marker
markers = []
for i in range(len(final)):
    markers.append("{number}: {bracket}center: {bracket}lat: {lat}, lng: {lng}{revbracket}, situation: {quote}{situation}{endquote}, trucks: {trucks}, alarm: {quote}{alarm}{endquote}{revbracket}".format(number=i, bracket='{', lat=final[i].location[0], lng=final[i].location[1], revbracket='}', quote="'", situation=final[i].event, endquote="'", trucks=final[i].trucks, alarm=final[i].alarm))

# print(markers)

str = ''
for i in range(len(markers)):
    if i < len(markers)-1:
        str += markers[i] + ', '
    else:
        str += markers[i]

# Create the map
with open('map.html', 'w') as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Fire Map</title>
    <style>
      /* Always set the map height explicitly to define the size of the div
       * element that contains the map. */
      #map {brack}
        height: 100%;
      {revbrack}
      /* Optional: Makes the sample page fill the window. */
      html, body {brack}
        height: 100%;
        margin: 0;
        padding: 0;
      {revbrack}
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>


      // Create an object that contains information about events.
      var eventMap = {brack}{values}{revbrack};

      function initMap() {brack}
        // Create the map.
        var map = new google.maps.Map(document.getElementById('map'), {brack}
          zoom: 12,
          center: {brack}lat: 43.7181552, lng: -79.5184833{revbrack},
        {revbrack});

        // Construct the circle for each value in eventMap.
        for (i in eventMap) {brack}
          if (eventMap[i].situation == 'Fire'){brack}
                var value = '#e62e00'
            {revbrack} else if (eventMap[i].situation == 'Medical'){brack}
                var value = '#2e2eb8'
            {revbrack} else if (eventMap[i].situation == 'Alarm'){brack}
                var value = '#ffff80'
            {revbrack} else if (eventMap[i].situation == 'Vehicle') {brack}
                var value = '#008B8B'
            {revbrack} else{brack}
                var value = '#79d279'{revbrack}
          if (eventMap[i].alarm == 'None'){brack}
                var alarm = 0
          {revbrack}else{brack}
                var alarm = parseInt(eventMap[i].alarm){revbrack}
          if (alarm == 1){brack}
                var value = '#e68200'
          {revbrack}
          else if (alarm == 2){brack}
                var value = '#e65f00'
          {revbrack}
          else if (alarm == 3){brack}
                var value = '#ff3f00'
          {revbrack}
          else if (alarm == 4){brack}
                var value = '#ff2600'
          {revbrack}
          else if (alarm == 5){brack}
                var value = '#9b0606'
          {revbrack}
          else if (alarm == 6){brack}
                var value = '#000000'
          {revbrack}
          else{brack}value = value{revbrack}
          // Add the circle for this city to the map.
          var eventCircle = new google.maps.Circle({brack}
            strokeColor: value,
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: value,
            fillOpacity: 0.5,
            map: map,
            center: eventMap[i].center,
            radius: 50
          {revbrack});
        {revbrack}
      {revbrack}
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=ADD_YOUR_KEY&callback=initMap">
    </script>
</body>
</html>""".format(brack='{', values=str, revbrack='}'))


print('Took {} seconds.'.format(int(time.time()-now)))

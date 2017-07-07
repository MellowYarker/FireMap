import currator as currate
import geocoder
from event import Event

fname = 'extracted.txt'
with open(fname, 'r') as f:
    text = f.readlines()

# This checks if there are any updated tweets
updated = False
for i in text:
    if 'UD:' in i:
        updated = True

tweet_list = [currate.check_type_of_tweet(i) for i in text]


# Check if any tweets have been updated (Maybe do this in the Currator.py file?
# TODO: show most recent update of tweets, if UD tweet exists, remove previous V

# Try geocoding here, if it fails, reformat, if it still fails, remove the event

for location in range(len(tweet_list)):
    # print(str(location) + ': ', tweet_list[location][1])
    if not isinstance(tweet_list[location][1], list):
        g = geocoder.google(tweet_list[location][1])
        if g.latlng != []:
            # print(g.latlng)
            tweet_list[location][1] = g.latlng
        else:
            retry = currate.reformat(tweet_list[location][1])
            g = geocoder.google(retry)
            if g.latlng != []:
                # print(g.latlng)
                tweet_list[location][1] = g.latlng
            else:
                tweet_list.remove(tweet_list[location])


final = []
for i in tweet_list:
    final.append(Event(i))

# Add description to a marker
markers = []
for i in range(len(final)):
    markers.append("{number}: {bracket}center: {bracket}lat: {lat}, lng: {lng}{revbracket}, event: {quote}{event}{endquote}, trucks: {trucks}, alarm: {quote}{alarm}{endquote}{revbracket}".format(number=i, bracket='{', lat=final[i].location[0], lng=final[i].location[1], revbracket='}', quote="'", event=final[i].event, endquote="'", trucks=final[i].trucks, alarm=final[i].alarm))

print(markers)

str = ''
for i in range(len(markers)):
    if i < len(markers)-1:
        str += markers[i] + ', '
    else:
        str += markers[i]

with open('js.html', 'w') as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Circles</title>
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
        for (var event in eventMap) {brack}
          if (eventMap[event].event == 'Fire'){brack}
                var value = '#e62e00'
            {revbrack} else if (eventMap[event].event == 'Medical'){brack}
                var value = '#2e2eb8'
            {revbrack} else if (eventMap[event].event == 'Alarm'){brack}
                var value = '#ffff80'
            {revbrack}
            else{brack}
                var value = '#79d279'{revbrack}
          if (eventMap[event].alarm == 'None'){brack}
                var alarm = 0
          {revbrack}else{brack}
                var alarm = parseInt(eventMap[event].alarm){revbrack}
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
            center: eventMap[event].center,
            radius: 50
          {revbrack});
        {revbrack}
      {revbrack}
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCrehsqQVFG2y8JDxrGwnsTlRoxK47dIyw&callback=initMap">
    </script>
</body>
</html>""".format(brack='{', values=str, revbrack='}'))



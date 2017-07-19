import clean as clean
from event import Event
import os
import pickle
import time

now = time.time()
print('Starting\n')
# Get the tweets from extracted.txt
fname = 'extracted.txt'
with open(fname, 'r') as f:
    text = f.readlines()

# format them to make them easier to work with
print("Formatting tweets...")
tweet_list = clean.check_type(text)
print("Done!\n")
# Check if updates.txt exists (if it does that means some tweets were updated
# so there won't be as many events on the map as there were tweets pulled from
# Twitter)
if os.path.exists(os.getcwd()+'/updates.txt'):
    with open('updates.txt', 'r') as f:
        updates = f.readline()

failed_index = []

# Check if the geocodes file exists, if it does load the dictionary of codes
if os.path.exists(os.getcwd()+'/geocodes'):
    with open('geocodes', 'rb') as values:
        codes = pickle.load(values)
else:
    codes = {}

# Check if the failed file exists, if it does load the dictionary of fails
if os.path.exists(os.getcwd() + '/failed'):
    with open('failed', 'rb') as failures:
        fails = pickle.load(failures)
else:
    fails = {}

print("Geocoding locations; this could take some time...")
# Try turning text locations to geocodes here.
try:
    clean.geocode(tweet_list, codes, fails, failed_index)
    print("Done!\n")
    # New codes might have been created. Serialize them to access them later
    with open('geocodes', 'wb') as values:
        pickle.dump(codes, values)

    # New fails might have been created. Serialize them to access them later
    with open('failed', 'wb') as failures:
        pickle.dump(fails, failures)

    print("Removing any locations that failed to be geocoded...")
    # Remove locations that couldn't be geocoded
    # Put all locations that could not be geocoded into a list
    failed_locations = clean.remove_failures(tweet_list, failed_index)
    print("Done!\n")
    # Turn every event into an Event object
    final = []
    for i in tweet_list:
        final.append(Event(i))
        # print(Event(i).location)

    markers = []
    for i in range(len(final)):
        markers.append(
            "{number}: {bracket}center: {bracket}lat: {lat}, lng: {lng}{revbracket}, situation: {quote}{situation}{endquote}, description: {quote}{description}{endquote}, trucks: {trucks}, alarm: {quote}{alarm}{endquote}{revbracket}".format(
                number=i, bracket='{', lat=final[i].location[0],
                lng=final[i].location[1], revbracket='}', quote="'",
                situation=final[i].event, description=final[i].description,
                endquote="'", trucks=final[i].trucks, alarm=final[i].alarm))

    # print(markers)

    str = ''
    for i in range(len(markers)):
        if i < len(markers) - 1:
            str += markers[i] + ', '
        else:
            str += markers[i]

    print("Building the map...")

    # link to icons
    icon = os.getcwd() + '/icons/'

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
          #legend {brack}
            font-family: Arial, sans-serif;
            background: #fff;
            padding: 20px;
            margin: 20px;
            border: 2px solid #000;
          {revbrack}
          #legend h3 {brack}
            margin-top: 0;
          {revbrack}
        </style>
      </head>
      <body>
        <div id="map"></div>
        <div id="legend"><h3>Legend</h3></div>
        <script>


          // Create an object that contains information about events.
          var eventMap = {brack}{values}{revbrack};

          function initMap() {brack}
            // Create the map.
            var map = new google.maps.Map(document.getElementById('map'), {brack}
              zoom: 12,
              center: {brack}lat: 43.7181552, lng: -79.5184833{revbrack},
            {revbrack});

            icons = '{icons}'
            var circles = {brack}
              fire: {brack}
                name: 'Fire',
                colour: icons + 'Red.png'
              {revbrack},
              alarm: {brack}
                name: 'Alarm',
                colour: icons + 'Yellow.png'
              {revbrack},
              medical: {brack}
                name: 'Medical',
                colour: icons + 'Blue.png'
              {revbrack},
              vehicle: {brack}
                name: 'Vehicle',
                colour: icons + 'Teal.png'
              {revbrack},
              other: {brack}
                name: 'Other',
                colour: icons + 'Green.png'
              {revbrack}
            {revbrack};

    		var counter = 0;

            // Construct the circle for each value in eventMap.
            for (i in eventMap) {brack}
              if (eventMap[i].situation == 'Fire'){brack}
                    var value = '#e62e00'
                {revbrack} else if (eventMap[i].situation == 'Medical'){brack}
                    var value = '#4545e0'
                {revbrack} else if (eventMap[i].situation == 'Alarm'){brack}
                    var value = '#ffff80'
                {revbrack} else if (eventMap[i].situation == 'Vehicle') {brack}
                    var value = '#00a8a8'
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
                clickable: true,
                description: eventMap[i].description,
                center: eventMap[i].center,
                radius: 50
              {revbrack});
              createClickableCircle(map, eventCircle, '<h2><b><u> ' + eventMap[i].situation + ' </u></b></h2><p>' + eventMap[i].description + '<br> Trucks dispatched: ' + eventMap[i].trucks + '<br> Alarm Level: ' + eventMap[i].alarm);
              counter++;
            {revbrack}
          var legend = document.getElementById('legend');
          for (var key in circles) {brack}
            var type = circles[key];
            var name = type.name;
            var colour = type.colour;
            var div = document.createElement('div');
            div.innerHTML = '<div style="float: left"><img src="' + colour + '"> ' + name;
            legend.appendChild(div);
          {revbrack}
          function createClickableCircle(map, circle, info){brack}
            var infowindow =new google.maps.InfoWindow({brack}
            content: info
            {revbrack});
            google.maps.event.addListener(circle, 'click', function(ev) {brack}
              // alert(infowindow.content);
              infowindow.setPosition(circle.getCenter());
              infowindow.open(map);
            {revbrack});
        {revbrack}

        map.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(legend);
        {revbrack}
        </script>
        <script async defer
        src="https://maps.googleapis.com/maps/api/js?key=ADD_YOUR_KEY&callback=initMap">
        </script>
    </body>
    </html>""".format(brack='{', values=str, revbrack='}', icons=icon))

    print("Done!\n")
    print('Took {} seconds.'.format(int(time.time() - now)))
    print('The map has been created, open map.html in a browser to view it.')

except "Error in geocoder library":
    print("Something went wrong in the geocoder library, scanning again "
          + "usually corrects this, so try again.")
    # Add failure message to the map/webpage.

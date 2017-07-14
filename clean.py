"""
This file contains functions that can be used to format tweets from the tofire
twitter page.
"""
# TODO check the type of tweet
import geocoder


def to_int(tweet):
    """(3 element list) -> 3 element list

    Take the fully spliced tweet and turn the last value into an individual int

    >>> to_int(['Vehicle (Personal Injury Highway)', 'North York', '3 trucks'])
    ['Vehicle (Personal Injury Highway)', 'North York', 3]
    """
    trucks = ''
    for i in tweet[2]:
        if i.isdigit():
            trucks += i
    tweet[2] = int(trucks)


def cut(tweet):
    """(list) -> list

    Remove everything after '/' in location index

    >>> cut(['Alarm Highrise Residential', \
    'Greenbrae Crct and Sedgemount Dr Greenholm Crct', 6])
    ['Alarm Highrise Residential', 'Greenbrae Crct and Sedgemount Dr', 6]
    """
    if '/' in tweet[1]:
        end = tweet[1].find('/')
        tweet[1] = tweet[1][:end-1] + ', Toronto'


def check_type(tweets):
    """Take a list of tweets and determine what to do with each tweet.
    >>> test = ['UD: Medical (Unconscious) - Drovers Lane @ Verner Lane, (3 Trucks)', 'Medical (Unconscious) - Drovers Lane @ Verner Lane, Toronto (2 Trucks)']
    >>> print(check_type(test))
     [['Medical (Unconscious)', 'Drovers Lane @ Verner Lane', 3, 'Medical', None]]
    >>> tweet = ['Check Call - Yonge St b/w Asquith Avenue / Yorkville Avenue, (3 Trucks)']
    >>> print(check_type(tweet))
    [['Check Call', 'Yonge St and Asquith Avenue, Toronto', 3, 'Other', None]]
    """

    event_list = []
    updated_count = 0
    for tweet in tweets:
        # Check if it is a valid event
        if '-' in tweet and tweet[0] != '[' and '-*-' not in tweet:
            # If the current tweet is an update
            if tweet[0:4] == 'UD: ':
                formatted = update(tweet)
                # If the event list is empty just add it
                if len(event_list) == 0:
                    event_list.append(formatted)
                else:
                    # Check if the tweet has already been updated or not
                    updated = exists(event_list, formatted)
                    # if this tweet hasn't been updated, add it to the list
                    if updated is False:
                        event_list.append(formatted)
                    else:
                        updated_count += 1

            # Now deal with a regular tweet
            elif '-' and ',' in tweet:
                formatted = regular(tweet)
                if len(event_list) == 0:
                    event_list.append(formatted)
                else:
                    # Check if the tweet has already been updated or not
                    updated = exists(event_list, formatted)
                    # if this tweet hasn't been updated, add it to the list
                    if updated is False:
                        event_list.append(formatted)
                    else:
                        updated_count += 1
    if updated_count > 0:
        with open("updates.txt", 'w') as f:
            f.write(str(updated_count))
    return event_list


def exists(events, tweet):
    """ Return True if a tweet has already been updated and False otherwise"""
    flag = False
    for event in events:
        if tweet[1] in event and (tweet[3] in event or tweet[3] == 'Other'):
            flag = True
    return flag


def regular(tweet):
    """Format a regular tweet

    >>> test = 'Alarm Residential - Botfield Avenue b/w Tyre Avenue / Mattice Avenue, Etobicoke (6 Trucks)'
    >>> print(regular(test))
    ['Alarm Residential', 'Botfield Avenue and Tyre Avenue, Toronto', 6, 'Alarm', None]
    """
    new_tweet = []
    strip_newline(tweet)
    level = None
    # Check if there is an alarm level
    check_alarm(tweet, level)
    # Replace b/w with 'and' for formatting purposes (for now)
    if "b/w" in tweet:
        tweet = tweet.replace("b/w", "and")

    # Find where to splice the string
    first = tweet.find('-')
    second = tweet.find(',')

    # Appened 3 new splices to one list
    new_tweet.append(tweet[:first - 1])
    new_tweet.append(tweet[first + 2:second])
    new_tweet.append(tweet[second:])

    # Turn last val in lst to an int
    to_int(new_tweet)

    # Remove irrelevant part of location
    cut(new_tweet)
    first = new_tweet[0].split()[0]
    # Add the event type to the new list
    add_event(new_tweet, first, level)
    # print(new_tweet)
    return new_tweet


def update(tweet):
    """Format an updated tweet

    >>> test
    """
    new_tweet = []

    strip_newline(tweet)
    # Remove first 4 characters
    tweet = tweet[4:]
    level = None
    # most cases
    if ',' in tweet:
        return regular(tweet)
    # Determine where to splice
    else:
        # Check if there is an alarm level
        check_alarm(tweet, level)
        val1 = tweet.find('-')

        # Second half of tweet
        # All the adition and subtraction in the splicing is to remove spaces
        other_half = tweet[val1 + 2:]
        val2 = other_half.find('(')

        # Append splices to list
        new_tweet.append(tweet[:val1 - 1])
        new_tweet.append(other_half[1:val2 - 1] + ', Toronto')
        new_tweet.append(other_half[val2 + 1:])

        # Change last str to int
        to_int(new_tweet)

        # print(lst)
        first = new_tweet[0].split()[0]
        # Add the event type to the new list
        add_event(new_tweet, first, level)
        return new_tweet


def strip_newline(tweet):
    """ If the final character in the tweet is a newline, remove it."""
    if tweet[-1] == '\n':
        tweet = tweet[:-1]


def check_alarm(tweet, level):
    """Check if a tweet has an alarm level"""
    if 'Alm]' in tweet:
        level = int(tweet[1:2])
        # Remove redundant [int alm]
        tweet = tweet[8:]


def add_event(lst, first, alarm):
    """ A helper function for regular and update.
    Adds the event type to the tweet"""
    if 'Alarm' in lst[0]:
        lst.append('Alarm')
    elif 'Fire' in lst[0]:
        lst.append('Fire')
    elif first == 'Medical':
        lst.append(first)
    elif first == 'Vehicle':
        lst.append(first)
    else:
        lst.append('Other')
    lst.append(alarm)


def geocode(tweets, codes={}, fails={}, failed_index=[]):
    """Turn the text location in every tweet to a functional geocode to be mapped.

    >>> test = [['Alarm Residential', 'Botfield Avenue and Tyre Avenue, Toronto', 6, 'Alarm', None]]
    >>> for event in test:
    ...     geocode(test)
    >>> print(test)
     [['Alarm Residential', [43.6444117, -79.53954139999999], 6, 'Alarm', None]]
    """
    for location in range(len(tweets)):
        # print(str(location) + ': ', tweet_list[location][1])
        # Make sure the location hasn't already been geocoded
        if not isinstance(tweets[location][1], list):
            # If the geocode dictionary is not empty
            if len(codes) > 0:
                # Check if the location is in the dictionary
                if tweets[location][1] in codes:
                    # If it is, use that geocode.
                    tweets[location][1] = codes[tweets[location][1]]
                # If the dictionary of locations that failed is not empty
                else:
                    check_fails(tweets, location, codes, fails, failed_index)
            # If the geocode dictionary is empty
            else:
                check_fails(tweets, location, codes, fails, failed_index)
                if len(fails) <= 0:
                    create_geocode(tweets, location, codes, fails, failed_index)


def create_geocode(tweets, location, codes, fails, failed_index):
    """Try to create the geocode here, if it fails, try reformatting."""
    g = geocoder.google(tweets[location][1])
    if g.latlng != []:
        # print(g.latlng)
        codes[tweets[location][1]] = g.latlng
        tweets[location][1] = g.latlng
    else:
        retry = reformat(tweets[location][1])
        g = geocoder.google(retry)
        if g.latlng != []:
            # print(g.latlng)
            codes[tweets[location][1]] = g.latlng
            tweets[location][1] = g.latlng
        else:
            fails[tweets[location][1]] = 1
            failed_index.append(location)


def check_fails(tweets, location, codes, fails, failed_index):
    """"""
    # If the fails dictionary is not empty
    if len(fails) > 0:
        # Check if it is in this dictionary
        if tweets[location][1] in fails:
            # If it is, increase the count of failures
            # on that location.
            # And add it's index to failed index (for later)

            fails[tweets[location][1]] += 1
            failed_index.append(location)
        # If it is not in the dictionary,
        # create the geocode and add it to the correct dictionary.
        else:
            create_geocode(tweets, location, codes, fails,
                           failed_index)


def reformat(tweet):
    """Make a location description more geocode friendly, sometimes geocoding
    fails due to difficult location descriptions.

    >>> a = 'Martin Grove Road and Martin Grove South Albion West Ramp'
    >>> b = 'Calderstone Crescent and Dear Gt'
    >>> reformat(a)
    >>> reformat(b)


    """
    # Remove n, s, e, w
    compass = ['North', 'South', 'East', 'West']
    for i in compass:
        if i in tweet:
            tweet = tweet.replace(i, '')

    # Turn Gt into Gate
    if 'Gt' in tweet:
        tweet = tweet.replace('Gt', 'Gate')

    if 'Crcl' in tweet:
        tweet = tweet.replace('Crcl', 'Cir')

    # Remove reoccuring street names
    tweet = tweet.split()
    temporary = []
    for i in tweet:
        if i not in temporary:
            temporary.append(i)

    # Put it all back together in a new string
    final_string = ''
    for i in temporary:
        final_string += str(i) + ' '

    return final_string


def remove_failures(tweets, failed):
    """Delte all locations that could not be geocoded and return them
    """
    failed_locations = []
    if len(failed) > 0:
        # Every time an event is deleted from the list, the length of the list
        # gets smaller, so this accounts for that and decreases the index by 1
        for index in range(len(failed)):
            failed_locations.append(tweets[failed[index]][1])
            del tweets[failed[index]]
            for i in range(len(failed)):
                failed[i] -= 1
    return failed_locations

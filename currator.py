"""This file contains functions that can be used to pull out the relevant data.
"""
import csv

event_list = []

# def to_csv(lst):
#     """Turns it into a csv file"""
#     with open('info.csv', 'a') as f:
#         wr = csv.writer(f, quoting=csv.QUOTE_ALL)
#         wr.writerow(lst)


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
        # elif i == ')':
        #     pass
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
        tweet[1] = tweet[1][:end-1]


def check_type_of_tweet(tweets):
    """(list) -> list of list of str

    Determine the type of tweet, then call the appropriate function

    >>> tweets = ['Alarm Highrise Residential - Eglinton Avenue b/w Centre St / Markham Road, Scarborough (6 Trucks)', 'UD: Vehicle (Personal Injury Highway) -  North York (3 Trucks)', 'UD: Vehicle (Personal Injury Highway) -  North York (3 Trucks)']
    >>> print(check_type_of_tweet(tweets))
    """

    updated_count = 0
    tweets = tweets[::-1]
    for tweet in tweets:

        # This flag represents if a tweet has already been updated
        updated = False

        # Determine if tweet begins with UD
        if '-' in tweet and tweet[0] != '[':
            # Check updated tweet
            if tweet[0:4] == 'UD: ':
                formatted = ud_tweet(tweet)
                # If the event list is empty just add it
                if len(event_list) == 0:
                    event_list.append(formatted)
                else:
                    # Check if the tweet location and event type exist
                    for event in event_list:
                        if formatted[1] in event and formatted[3] in event:
                            updated = True
                            updated_count += 1

                    if updated is False:
                        event_list.append(formatted)

            elif '-' and ',' in tweet:
                event_list.append(regular(tweet))
    if updated_count > 0:
        with open("updates.txt", 'w') as f:
            f.write(str(updated_count))
    return event_list[::-1]


def regular(tweet):
    """
    (str) -> [str, str, int]

    Create a list where the first index is a situation, second is a location, \
    the third is the number of trucks, and the fourth is the event type.

    >>> regular('Alarm Highrise Residential - Eglinton Avenue b/w Centre St / Markham Road, Scarborough (6 Trucks)')
    ['Alarm Highrise Residential', 'Eglinton Avenue and Centre St', 6, 'Alarm']
    """

    lst = []
    level = None
    # Check if there is an alarm level
    if 'Alm]' in tweet:
        level = int(tweet[1:2])
        # Remove redundant [int alm]
        tweet = tweet[8:]
    # Replace b/w with 'and' for formatting purposees
    tweet = tweet.replace("b/w", "and")

    # Find where to splice the string
    first = tweet.find('-')
    second = tweet.find(',')

    # Appened 3 new splices to one list
    lst.append(tweet[:first-1])
    lst.append(tweet[first+2:second] + ', Toronto')
    lst.append(tweet[second:])

    # Turn last val in lst to an int
    to_int(lst)

    # Remove irrelevant part of location
    cut(lst)
    # print(lst)
    first = lst[0].split()[0]
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
    lst.append(level)
    return lst
# print(regular('Alarm Highrise Residential - Lake Shore Boulevard b/w Third St / Fourth St, Etobicoke (10 Trucks)'))


def ud_tweet(tweet):
    """(str) -> [str, str, int]

    Determine if a Tweet is a UD: Tweet(Under development). Then splice it so
    that the list returns a situation, location, the number of trucks and event
    type.

    >>> ud_tweet('UD: Vehicle (Personal Injury Highway) -  North York (3 Trucks)')
    ['Vehicle (Personal Injury Highway)', 'North York, Toronto', 3, 'Vehicle', None]
    >>> ud_tweet('UD: [1 Alm] Fire (Residential) - Rustic Road b/w Blue Springs Road / Cleo Road, North York (14 Trucks)')
    ['Fire (Residential)', 'Rustic Road and Blue Springs Road', 14, 'Fire', 1]
    """

    lst = []

    # Remove first 4 characters
    tweet = tweet[4:]
    level = None

    if ',' in tweet:
        return regular(tweet)
    # Determine where to splice
    else:
        # Check if there is an alarm level
        if 'Alm]' in tweet:
            level = int(tweet[1:2])
            # Remove redundant [int alm]
            tweet = tweet[8:]

        val1 = tweet.find('-')

        # Second half of tweet
        # All the adition and subtraction in the splicing is to remove spaces
        other_half = tweet[val1 + 2:]
        val2 = other_half.find('(')

        # Append splices to list
        lst.append(tweet[:val1-1])
        lst.append(other_half[1:val2 - 1] + ', Toronto')
        lst.append(other_half[val2 + 1:])

        # Change last str to int
        to_int(lst)

        # print(lst)
        first = lst[0].split()[0]
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
        lst.append(level)
        return lst
# print(ud_tweet('UD: Alarm Highrise Residential - Lake Shore Boulevard b/w Third St / Fourth St, Etobicoke (10 Trucks)'))


def unknown(tweet):
    raise NotImplemented

# print(check_type_of_tweet('Public Hazard - -*- (2 Trucks)'))

def reformat(tweet):
    """Make a location description more geocode friendly, sometimes geocoding
    fails due to difficult location descriptions.

    >>> a = 'Martin Grove Road and Martin Grove South Albion West Ramp'
    >>> b = 'South Toronto'
    >>> reformat(a)

    """
    # Remove n, s, e, w
    compass = ['North', 'South', 'East', 'West']
    for i in compass:
        if i in tweet:
            tweet = tweet.replace(i, '')

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

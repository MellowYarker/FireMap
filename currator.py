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

    >>> test = ['UD: Medical (Unconscious) - Drovers Lane @ Verner Lane, Toronto (3 Trucks)', 'Medical (Unconscious) - Drovers Lane @ Verner Lane, Toronto (2 Trucks)']
    >>> print(check_type_of_tweet(test))
    >>> tweet = ['Check Call - Yonge St b/w Asquith Avenue / Yorkville Avenue, Toronto (3 Trucks)']
    >>> print(check_type_of_tweet(tweet))

    """

    event_list = []
    updated_count = 0
    for tweet in tweets:

        # This flag represents if a tweet has already been updated
        updated = False

        # Check if it is a valid event
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
                formatted = regular(tweet)
                if len(event_list) == 0:
                    event_list.append(formatted)
                else:
                    for event in event_list:
                        if formatted[1] in event and (formatted[3] in event or
                                                      formatted[3] == 'Other'):
                            updated = True
                            updated_count += 1
                    if updated is False:
                        event_list.append(formatted)

    if updated_count > 0:
        with open("updates.txt", 'w') as f:
            f.write(str(updated_count))
    return event_list


def regular(tweet):
    """
    (str) -> [str, str, int]

    Create a list where the first index is a situation, second is a location, \
    the third is the number of trucks, and the fourth is the event type.

    >>> regular('Alarm Highrise Residential - Eglinton Avenue b/w Centre St / Markham Road, Scarborough (6 Trucks)')
    ['Alarm Highrise Residential', 'Eglinton Avenue and Centre St', 6, 'Alarm']
    """
    # print(tweet)
    lst = []
    strip_newline(tweet)
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
    # print(lst)
    return lst


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
    strip_newline(tweet)
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


def strip_newline(tweet):
    """Remove redundant newlines in a tweet"""
    tweet = tweet[:-1]


def unknown(tweet):
    raise NotImplemented

# print(check_type_of_tweet('Public Hazard - -*- (2 Trucks)'))

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

if __name__ == '__main__':
    ultimate = ['Medical (Chest Pains) - Woolner Avenue b/w Rockcliffe Boulevard / Jane St, York (2 Trucks)\n', 'Alarm Residential - Coxwell Avenue b/w Dundas St East / Robbins Avenue, Toronto (6 Trucks)\n', 'UD: Vehicle (Personal Injury) - Weston Road @ St Phillips Road, York (2 Trucks)\n', 'Public Hazard - Weston Road @ St Phillips Road, York (2 Trucks)\n', 'UD: Medical (Unconscious) - Drovers Lane @ Verner Lane, Toronto (3 Trucks)\n', 'Medical (Unconscious) - Drovers Lane @ Verner Lane, Toronto (2 Trucks)\n', 'Medical (Vsa) - Phillip Avenue b/w Mcintosh St / Craiglee Dr, Scarborough (2 Trucks)\n', 'Fire (Grass/rubbish) - (Tedford Dr @ Clearfield Gt), Scarborough (2 Trucks)\n', 'Medical (Unconscious) - Chapman Avenue b/w Avis Crescent / Munford Crescent, East York (2 Trucks)\n', 'Medical (Vsa) - Calderstone Crescent b/w Dear Gt / Kirkdene Dr, Scarborough (2 Trucks)\n', 'Medical (Trouble Breathing) - Lawrence Avenue b/w Townley Avenue / Pharmacy Avenue, Scarborough (2 Trucks)\n', 'Medical (Unconscious) - Dundas St b/w Roncesvalles Avenue / Bloor St West, Toronto (2 Trucks)\n', 'Medical (Unconscious) - Victoria Park Avenue b/w Esquire Road / Sheppard Avenue East, Scarborough (2 Trucks)\n', 'Medical (Other) - Morningside Avenue b/w Military Trail / Tams Road, Scarborough (2 Trucks)\n', 'Check Call - Yonge St b/w Asquith Avenue / Yorkville Avenue, Toronto (3 Trucks)\n', 'Medical (Allergy) - Thorncliffe Park Dr b/w West Don River Trail / West Don River Trail, East York (2 Trucks)\n', 'Medical (Trouble Breathing) - Wiley Avenue b/w Milverton Boulevard / Sammon Avenue, East York (2 Trucks)\n', 'Tems Transferred (Read Remarks) - Rathburn Road b/w Melbert Road / Elmcrest Creek Trail, Etobicoke (2 Trucks)\n', 'UD: Vehicle (Personal Injury Highway) -  North York (5 Trucks)\n', 'Fire (Grass/rubbish) - Queen St b/w Jameson Avenue / Macdonell Avenue, Toronto (2 Trucks)\n']
    [print(i[1]) for i in check_type_of_tweet(ultimate)]
    # print(check_type_of_tweet(ultimate))
    print(check_type_of_tweet(['Medical (Assist) - Frank Rivers Dr b/w Ww West Warden South Steeles / Manilow St, Scarborough (2 Trucks)']))

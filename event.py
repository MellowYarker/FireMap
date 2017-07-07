class Event:
    """An event class"""

    def __init__(self, event):
        """Create a new Event

        @type self: Event
        @type event: List[description, location, number of trucks, event type, alarm, time]
        @rtype: None
        """

        self.event = event[3]
        self.description = event[0]
        self.location = event[1]
        self.trucks = event[2]
        # self.time = event[5]
        self.alarm = event[4]
        # if self.event == 'Fire':
        #     self.alarm = event[4]
        # else:
        #     self.alarm = None

if __name__ == "__main__":
    event1 = ['Alarm Highrise Residential', 'Lee Centre Dr and Corporate Dr', 7]
    event2 = ['Medical', 'iiiiidk', 1]
    event = [['Medical(heart)', 'iiiiidk', 1, 'Medical', 2], ['Alarm Highrise Residential', 'Lee Centre Dr and Corporate Dr', 7]]
    a = Event(event1)
    b = Event(event2)

    new = []
    for i in event:
        new.append(Event(i))
    for i in new:
        print(i.event)

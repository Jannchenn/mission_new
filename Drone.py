# ======================================================================
# FILE:        Drone.py
#
# DESCRIPTION: This file control the drone action
#
# ======================================================================

import math
from random import randrange
from Event import Event
from collections import defaultdict
import random

glb_time = 1734927

class Drone:
    # Tile Structure
    class __Tile:
        last_time_visit = 0
        has_event = False
        id = 0

    def __init__(self, board, policy, fix, r, row, col):
        """
        Initializes drone flight characteristcs
        :param board: The board for the drone to explore
        :param policy: function of direction drone will fly
        :param fix: a string that determines if the drone's flight is limited to movement or time
        :param r: integer of number of times drone will look for an event if drone flies according to a fixed movment
                      integer of number of minutes if drone flies according to fixed time
        :param row: the row number of the drone
        :param col: the col number of the drone
        """

        self.policy = policy
        self.fix = fix
        self.round = r
        self.__colDimension = col
        self.__rowDimension = row
        self.time_now = glb_time

        self.times_hasEvent = defaultdict(lambda: defaultdict(list))
        self.total_visit = 0
        self.total_events = 0
        self.movements = list()
        self.missed = defaultdict(int)
        self.start = 0
        self.end = 0
        self.count = 0
        self.event_set = set()

        self.speed = 46 #?????????

        self.__board = board.get_real_board()
        self.stay_expo = board.get_stay_expo()
        self.next_add_event_time = board.get_next_add_event_time()
        self.arrival_num = board.get_arrival_num()
        self.prob = board.get_prob()
        self.__total_events = board.get_total_events()
        self.die_expo = board.get_die_expo()
        self.arrival_rate = board.get_arrival_rate()

        self.explore = [[self.__Tile() for j in range(self.__colDimension)] for i in
                        range(self.__rowDimension)]  # The board includes information that drone catches
        self.__events = dict()

    def count_different(self):
        """
        :return: the number of different events
        """
        return len(self.times_hasEvent)

    # def missed_events(self):
    #     """
    #     Updates self.missed so that track the missed events for each sector.
    #     :return: the total number of events generated
    #     """
    #     count = 0
    #     for row in range(self.__rowDimension):
    #         for col in range(self.__colDimension):
    #             max_id = board_info.get_max_id(col, row)
    #             count += max_id
    #             if (col, row) not in self.times_hasEvent.keys():
    #                 self.missed[(col, row)] += max_id
    #             else:
    #                 events = self.times_hasEvent[(col, row)].keys()
    #                 for i in range(max_id):
    #                     if i + 1 not in events:
    #                         self.missed[(col, row)] += 1
    #     return count
    #
    # def total_missed_events(self):
    #     """
    #     This method will count the TOTAL missed events
    #     """
    #     result = 0
    #     for val in self.missed.values():
    #         result += val
    #     return result

    def run(self):
        """
        flies vehicle according to fixed time or fixed movement, which is
        determined in main
        """

        self.start = glb_time
        if self.fix == "time":
            timeout = glb_time + self.round  # round minutes from now
            while True:
                if self.time_now > timeout:
                    break
                self.fly()

        elif self.fix == "movement":
            for _ in range(self.round):
                self.fly()

        self.end = self.time_now
        #self.count = self.missed_events()

    def fly(self):
        """
        fly the drone according to the policy
        """
        data = self.policy()
        c = data[0]
        r = data[1]
        self.collect_data(c, r)
        self.time_now += 6  #!!!!!!!!!!!!!!!!!!!!
        self.update_map()

    def collect_data(self, c, r):
        """
        For each sector we reached, we need to collect information from it, aka fly log
        :param c: the coloum of the board; r: the row of the board; wpl: the loaction of the sector
        """
        # Collect and update explore map
        self.total_visit += 1
        self.movements.append((c, r))

        now_time = 18888 #!!!!!!!
        self.explore[c][r].last_time_visit = now_time
        events = self.get_event(c, r)
        has_event = False
        event_id = []
        if events:
            has_event = True
            self.total_events += len(events)
            for event in events:
                event_id.append(event.id)
                self.times_hasEvent[event][(c, r)].append(now_time)
                self.event_set.add(event)
        self.explore[c][r].has_event = has_event
        self.explore[c][r].id = event_id

        # print("EVENT: " + str(has_event))

    def update_map(self):  # !!!think and discuss about efficiency next time!!!
        """
        This method keeps updating the board with new events
        :return: None
        """
        time_now = self.time_now
        events_to_remove = []

        if time_now >= self.next_add_event_time:
            self.__setUpEvent()
        for event, coord in self.__events.items():
            c = coord[0]
            r = coord[1]
            if time_now >= event.die_time:
                self.__board[c][r].event_list.remove(event)
                events_to_remove.append(event)
            else:
                while time_now > event.finish_time:
                    cur_c = event.next_c
                    cur_r = event.next_r
                    event.update_sector(cur_c, cur_r)
                    event.update_next_sector()
                    stay_time = self.stay_expo()
                    event.update_next_move_time(stay_time)
                    self.__board[c][r].event_list.remove(event)
                    if time_now >= event.die_time:
                        events_to_remove.append(event)
                        break
                    self.__board[cur_c][cur_r].event_list.append(event)
                    self.__board[cur_c][cur_r].num_of_events += 1
                    self.__board[cur_c][cur_r].time_with_events += stay_time
                    self.__events[event] = (cur_c,cur_r)
                    c = cur_c
                    r = cur_r
        for event in events_to_remove:
            del self.__events[event]

    def __setUpEvent(self):
        """
        initializes events
        :return: None
        """
        for _ in range(self.arrival_num):
            c = random.randint(0,self.__colDimension-1)
            r = random.randint(0,self.__rowDimension-1)
            new_event = Event(self.prob, self.die_expo, self.__colDimension-1, self.__rowDimension-1)
            new_event.update_sector(c, r)
            new_event.update_die_time(self.next_add_event_time)
            new_event.update_next_sector()
            stay_time = self.stay_expo()
            new_event.update_next_move_time(self.next_add_event_time + stay_time)
            copy = list(self.__board[c][r].event_list)
            copy.append(new_event)
            self.__board[c][r].event_list = copy
            self.__total_events += 1
            self.__events[new_event] = (c, r)
            self.__board[c][r].num_of_events += 1
            self.__board[c][r].time_with_events += stay_time
            # self.__total_dur += stay_time
            self.next_add_event_time = self.next_add_event_time + self.arrival_rate()

    def get_stats_info(self):
        """
        returns a tuple that contains all the information needed
        """
        return (self.total_events, self.count_different(),
                self.__rowDimension, self.__colDimension,
                self.times_hasEvent, self.total_visit, self.round, self.speed)

    def get_time(self):
        """
        This function will get the flying time
        :return: a tuple of start and end time
        """
        return self.start, self.end

    def get_event(self, c, r):
        """
        This method will return if the list of events
        :param c: the column of the board
        :param r: the row of the board
        :return: True if there's event on the current sector, False otherwise
        """
        return self.__board[c][r].event_list

    def get_total_caught_event_include_same(self):
        return self.total_events

    def get_total_caught_event(self):
        return len(self.event_set)

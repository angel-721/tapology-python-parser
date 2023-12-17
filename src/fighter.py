#!/usr/bin/env python3
"""
This module represents a single fighter object.

Object will be turned into a record will either in a database or csv
"""


class Fighter:
    """
    The Fighter Class.

    fields:
        fighter_name: str
        fighter_record: tuple[wins: int, losses: int]
        streak: int
        height_reach: tuple[height: float, reach: float] both in cm

    """

    def __init__(self, fighter_name, wins, losses, streak, height, reach):
        """Create a fighter object."""
        self.fighter_name = fighter_name
        self.fighter_record = (wins, losses)
        self.streak = streak
        self.height_and_reach = (height, reach)

    def set_name(self, name):
        self.fighter_name = name

    def set_record_from_tuple(self, record):
        if len(record) > 2:
            raise ("A fighter record is just wins and losses.")
        if type(record[0]) != int:
            raise ("A fighter wins must be an int")
        if type(record[1]) != int:
            raise ("A fighter losses must be an int")
        if record[0] < 0 or record[1] < 0:
            raise ("A win or loss can not be less than 0")
        self.fighter_record = record

    def set_record(self, wins, losses):
        if wins < 0:
            raise ("Can not have negative wins")
        if losses < 0:
            raise ("Can not have negative losses")

        self.fighter_record = (wins, losses)

    def set_streak(self, streak):
        self.streak = streak

    def set_height_and_reach(self, height, reach):
        if height <= 0:
            raise ("A fighter can not have a height of", height, "cm")
        if reach <= 0:
            raise ("A fighter can not have a reach of", reach, "cm")
        self.height_and_reach = (height, reach)

    def set_height_and_reach_tuple(self, height_and_reach):
        if len(height_and_reach) > 2:
            raise ("The tuple should just have height(cm) and reach(cm).")
        if type(height_and_reach[0]) != float:
            raise ("A fighter height must be an float")
        if type(height_and_reach[1]) != float:
            raise ("A fighter reach must be an float")
        if height_and_reach[0] < 0 or height_and_reach[1] < 0:
            raise ("height or reach can not be less than 0")
        self.height_and_reach = (height_and_reach)

    def get_name(self): return self.fighter_name

    def get_record(self): return self.fighter_record

    def get_wins(self): return self.fighter_record[0]

    def get_losses(self): return self.fighter_record[1]

    def get_streak(self): return self.streak

    def get_height_and_reach_tuple(self): return self.height_and_reach

    def get_height(self): return self.height_and_reach[0]

    def get_reach(self): return self.height_and_reach[1]



class Fight:
    def __init__(self, red_fighter, blue_fighter) -> None:
        self.r_fighter = red_fighter
        self.b_fighter = blue_fighter

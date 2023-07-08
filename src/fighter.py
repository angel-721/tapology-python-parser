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

    def __init__(self, fighter_name, fighter_record, streak, height_reach):
        """Create a fighter object."""
        self.fighter_name = fighter_name
        self.fighter_record = fighter_record
        self.streak = streak
        self.height_reach = height_reach

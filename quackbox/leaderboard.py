from dataclasses import dataclass
from datetime import datetime
from typing import List

import requests

_ROUTE = "http://127.0.0.1:6174/api/v1/leaderboard"
MAX_PLAYERS = 8


@dataclass
class LeaderboardEntry:
    value_name: str
    value_num: float
    time_stamp: datetime

    @staticmethod
    def from_dict(d: dict) -> "LeaderboardEntry":
        return LeaderboardEntry(value_name=d["value_name"],
                                value_num=d["value_num"],
                                time_stamp=d["time_stamp"])


def add_leaderboard_entry(value_name: str, value_num: float,
                          player_slot: int = 1):
    """
    Insert a leaderboard entry into the QuackBox database

    :param value_name: The name of the value to be store i.e. Time, High Score, etc.
                       This name will be displayed at the top of any leaderboard tables
                       on the QuackBox
    :param value_num: The numeric value of the leaderboard entry. These values are
                      stored internally as 64-bit floats
    :param player_slot: The controller slot of the player for this data to be associated with.
                        The slots begin at number 1 and go up to number 8

    :raises AssertionError: if the player_slot is not a valid slot
    """
    assert 1 <= player_slot <= MAX_PLAYERS
    payload = {"value_name": value_name, "value_num": value_num,
               "player_slot": player_slot, }

    requests.post(_ROUTE, json=payload)


def get_user_lb_entries(value_name: str, count: int = 100,
                        player_slot: int = 1) -> List[LeaderboardEntry]:
    """
    Retrieve the leaderboard entries associated with a specific user in descending
    order according to the value stored

    :param value_name: the name of the leaderboard to be retrieved. This is the
                       same name that is displayed at the top of any leaderboard tables on the QuackBox
    :param count: the number of entries to retrieve
    :param player_slot: the controller slot of the player to retrieve entries for.
                        The slots begin at number 1 and go up to number 8

    :return: A list of LeaderboardEntry objects that contain a name, a value, and
             a timestamp

    :raises AssertionError: if the player_slot is not a valid slot
    """
    assert 1 <= player_slot <= MAX_PLAYERS
    params = {"value_name": value_name, "count": count,
              "player_slot": player_slot}
    response = requests.get(_ROUTE, params=params)
    return [LeaderboardEntry.from_dict(d) for d in response.json()]


def get_global_lb_entries(value_name: str, count: int = 100):
    """
    Retrieve the top leaderboard entries with a specific name in descending order.

    :param value_name: the name of the leaderboard to be retrieved. This is the
                       same name that is displayed at the top of any leaderboard tables on the QuackBox
    :param count: the number of entries to retrieve

    :return:  A list of LeaderboardEntry objects that contain a name, a value, and
              a timestamp
    """
    params = {"value_name": value_name, "count": count, "scope": "global"}
    response = requests.get(_ROUTE, params=params)
    return [LeaderboardEntry.from_dict(d) for d in response.json()]

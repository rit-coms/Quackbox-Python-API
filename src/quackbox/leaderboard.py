from dataclasses import dataclass
from datetime import datetime
from typing import List

import requests

_ROUTE = "http://127.0.0.1:6174/api/v1/leaderboard"


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
    payload = {
        "value_name": value_name,
        "value_num": value_num,
        "player_slot": player_slot,
    }

    requests.post(_ROUTE, json=payload)


def get_user_lb_entries(value_name: str, count: int = 100,
                        player_slot: int = 1) -> List[
    LeaderboardEntry]:
    params = {"value_name": value_name, "count": count,
              "player_slot": player_slot}
    response = requests.get(_ROUTE, params=params)
    return [LeaderboardEntry.from_dict(d) for d in response.json()]


def get_global_lb_entries(value_name: str, count: int = 100):
    params = {"value_name": value_name, "count": count, "scope": "global"}
    response = requests.get(_ROUTE, params=params)
    return [LeaderboardEntry.from_dict(d) for d in response.json()]

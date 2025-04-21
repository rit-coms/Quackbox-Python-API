import re
from dataclasses import dataclass
from typing import List

import requests

_ROUTE = "http://127.0.0.1:6174/api/v1/save-data"


@dataclass
class SaveDataEntry:
    file_name: str
    data: str
    time_stamp: int

    @staticmethod
    def from_dict(d: dict):
        return SaveDataEntry(file_name=d["file_name"], data=d["data"],
                             time_stamp=d["time_stamp"])


def get_save_file_names(player_slot: int = 1) -> List[str]:
    params = {"player_slot": player_slot}
    response = requests.get(_ROUTE, params=params)
    return [d["file_name"] for d in response.json()]


def get_save_data(regex: str, player_slot: int = 1) -> List[SaveDataEntry]:
    # Check that regex is valid
    re.compile(regex)

    response = requests.get(_ROUTE,
                            params={"player_slot": player_slot, "regex": regex})
    return [SaveDataEntry.from_dict(d) for d in response.json()]


def get_save_data_file(file_name: str, player_slot: int = 1) -> SaveDataEntry:
    response = requests.get(_ROUTE, params={"file_name": file_name,
                                            "player_slot": player_slot})
    return SaveDataEntry.from_dict(response.json()[0])


def add_save_data(file_name: str, data: str, player_slot: int = 1):
    payload = {"file_name": file_name, "data": data, "player_slot": player_slot}
    requests.post(_ROUTE, json=payload)

import re
from dataclasses import dataclass
from typing import List

import requests

_ROUTE = "http://127.0.0.1:6174/api/v1/save-data"
MAX_PLAYERS = 8


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
    """
    Retrieves all save file names from the QuackBox for a specific player.

    :param player_slot: The controller slot of the player to retrieve entries for.
                        The slots begin at number 1 and go up to number 8.

    :return: A list of save file names in the same format as they were stored using
             functions such as :py:func: `add_save_data()`.

    :raises AssertionError: If player_slot is not a valid controller slot.
    """
    assert 1 <= player_slot <= MAX_PLAYERS

    params = {"player_slot": player_slot}
    response = requests.get(_ROUTE, params=params)
    return [d["file_name"] for d in response.json()]


def get_save_data(regex: str, player_slot: int = 1) -> List[SaveDataEntry]:
    """
    Retrieves all save data from the QuackBox for a specific player.

    :param regex: A regular expression pattern to match save data file names against.
    :param player_slot: The controller slot of the player to retrieve entries for.
                        The slots begin at number 1 and go up to number 8.

    :return: A list of save data entries containing a string representation of the
             save data. This is in the same format as the data wes stored using
             functions such as :py:func: `add_save_data()`.

    :raises AssertionError: If player_slot is not a valid controller slot.
    """
    assert 1 <= player_slot <= MAX_PLAYERS

    # Check that regex is valid
    re.compile(regex)

    response = requests.get(_ROUTE,
                            params={"player_slot": player_slot, "regex": regex})
    return [SaveDataEntry.from_dict(d) for d in response.json()]


def get_save_data_file(file_name: str, player_slot: int = 1) -> SaveDataEntry:
    """
    Retrieves a single save data file from the QuackBox.

    :param file_name: The name of the file to retrieve.
    :param player_slot: The controller slot of the player to retrieve entries for.
                        The slots begin at number 1 and go up to number 8.

    :return: A single save data entry containing a string representation of the
             save data. This is in the same format as the data wes stored using
             methods such as :py:func: `add_save_data()`.

    :raises AssertionError: If player_slot is not a valid controller slot.
    """
    assert 1 <= player_slot <= MAX_PLAYERS

    response = requests.get(_ROUTE, params={"file_name": file_name,
                                            "player_slot": player_slot})
    return SaveDataEntry.from_dict(response.json()[0])


def add_save_data(file_name: str, data: str, player_slot: int = 1):
    """
    Insert new save file into the QuackBox database. This will overwrite any file
    stored with the same file_name.

    :param file_name: The name of the file to insert.
    :param data: A string representation of the save data. This can be in any format
                 and be returned as it is stored when using functions such as
                 :py:func:`get_save_data()`.
    :param player_slot: The controller slot of the player to retrieve entries for.
                        The slots begin at number 1 and go up to number 8.

    :raises AssertionError: If player_slot is not a valid controller slot.
    """
    assert 1 <= player_slot <= MAX_PLAYERS

    payload = {"file_name": file_name, "data": data, "player_slot": player_slot}
    requests.post(_ROUTE, json=payload)

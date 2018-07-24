# -*- coding: utf-8 -*-

from core.json import CANDIDATES, POLLING_STATIONS

def get_initial_values():
    return {
        "lion": '0',
        "bat": '0',
        "arrow": '0',
        "rabbit": '0',
        "bowl": '0',
        "cup": '0',
        "crane": '0'
    }


def get_urdu_candidate_name(name):
    for candidate in CANDIDATES:
        if candidate.get("name") == name:
            return candidate.get("urdu_name")


def get_lion_votes_string(lion_votes, max_votes, second_higest):
    if lion_votes == max_votes:
        vote_string = "{} lead by {}".format(str(lion_votes), str(lion_votes-second_higest))
    else:
        vote_string = "{} behind by {}".format(str(lion_votes), str(max_votes-lion_votes))
    return vote_string


def get_urdu_polling_station_name(name):
    for polling_station in POLLING_STATIONS:
        if polling_station.get("number") == name:
            return "{}: {}".format(name, polling_station.get("urdu_name"))

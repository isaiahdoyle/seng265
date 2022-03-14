#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 01 08:35:33 2022
@author: rivera

This is a text processor that allows to translate XML-based events to YAML-based events.
CAREFUL: You ARE NOT allowed using (i.e., import) modules/libraries/packages to parse XML or YAML
(e.g., yaml or xml modules). You will need to rely on Python collections to achieve the reading of XML files and the
generation of YAML files.
"""
from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
import sys
import datetime
import re
from types import NoneType  # regular expressions


def parse_args(args: list[str]) -> list[str]:
    """ Parses input arguments according to specified format.
    """
    startarg = args[1].lstrip("--start=")
    y, m, d = startarg.split("/")
    y = int(y)
    m = int(m)
    d = int(d)
    start = datetime.datetime(y, m, d)

    endarg = args[2].lstrip("--end=")
    y, m, d = endarg.split("/")
    y = int(y)
    m = int(m)
    d = int(d)
    end = datetime.datetime(y, m, d)

    events = re.search("--events=(.*)", args[3]).group(1)
    circuits = re.search("--circuits=(.*)", args[4]).group(1)
    broadcasters = re.search("--broadcasters=(.*)", args[5]).group(1)

    return (start, end, events, circuits, broadcasters)


def main():
    """ The main entry point for the program.
    """
    start, end, events, circuits, broadcasters = parse_args(sys.argv)

    events, circuits, broadcasters = parse_files(
        events, circuits, broadcasters)
    set_date(events)

    # events = filter_events(events, start, end)
    def get_date(event): return event["date"]
    events = sorted(filter_events(events, start, end), key=get_date)

    write_file(events, circuits, broadcasters)


def set_date(events: list[dict]) -> None:
    """ Replaces 'year', 'month', 'day', and time parameters on each event with a datetime object
            Input: list of 'event' dictionaries
            Output: none
    """
    for event in events:
        year = int(event["year"])
        del event["year"]
        month = int(event["month"])
        del event["month"]
        day = int(event["day"])
        del event["day"]
        hour, min = get_time(event["start"])
        del event["start"]

        event["date"] = datetime.datetime(year, month, day, hour, min)

        hour, min = get_time(event["end"])
        del event["end"]

        event["end"] = datetime.time(hour, min)


def get_time(time: str) -> tuple[int, int]:
    """ Splits a time string into two ints representing hours, minutes.
            Input: time string of format "hh:mm"
            Output: two ints for hour and minute
    """
    hour, min = time.split(":")
    return int(hour), int(min)


def filter_events(events: list[dict],
                  start: datetime.datetime,
                  end: datetime.datetime) -> list[dict]:
    """ Filters all 'event' dicts not within start-end from a list.
            Input: list of 'event' dicts, start datetime object, end datetime object
            Output: list of 'event' dicts incl. only those within times
    """
    filtered = []

    for event in events:
        date = event["date"]
        if start < date and date < end:
            filtered.append(event)

    return filtered


def parse_files(event_filename: str,
                circuit_filename: str,
                broadcaster_filename: str) -> tuple[list[dict], list[dict], list[dict]]:
    """ Entry point to file parsing scheme.
            Input: filename strings for events, circuits, and broadcasters
            Output: three lists of dicts representing events, circuits and broadcasters
    """
    events = parse_file(event_filename)
    circuits = parse_file(circuit_filename)
    broadcasters = parse_file(broadcaster_filename)

    return events, circuits, broadcasters


def parse_file(filename: str) -> list[dict]:
    """ Parses a file and populates a list of dicts representing events, circuits, or broadcasters.
            Input: filename string
            Output: list of dicts filled with data from file
    """
    items = []

    with open(filename) as file:
        cur = -1
        buff = file.readline()
        buff.rstrip()
        buff = re.search("<[a-z]*>", buff).group()
        lines = file.readlines()
        for line in lines:
            line.rstrip()
            tag = re.search("<[a-z]*>", line)
            if tag != None:
                tag = tag.group()
            if tag == "<event>" or tag == "<circuit>" or (buff == "<broadcasters>" and tag == "<broadcaster>"):
                cur += 1
                item = {}
                items.append(item)
            elif tag != None:
                data = re.search("\>(.*?)\<", line).group(1)
                populate_dict(tag, data, items[cur])

    return items


def populate_dict(tag: str, data: str, dict: dict) -> None:
    """ Sets a the value of <tag> key to <data> value in dict.
            Input: key (tag) string, data (value) string, dict to be set
            Output: none
    """
    tag = tag.strip("<>")
    dict[tag] = data


def write_file(events: list[dict],
               circuits: list[dict],
               broadcasters: list[dict]) -> None:
    """ Writes all formatted calendar data to output.yaml.
            Input: lists of dicts representing events, circuits, and broadcasters
    """
    with open("./output.yaml", "w") as file:
        file.write("events:")
        prev_date = 0

        for event in events:
            cur_date = event["date"].date()

            if (cur_date != prev_date):
                file.write(f'\n  - {event["date"].strftime("%d-%m-%Y:")}')
            circuit = get_circuit(circuits, event)
            cur_broadcasters = get_broadcasters(broadcasters, event)
            file.write(f'\n    - id: {event["id"]}\n')
            file.write(f'      description: {event["description"]}\n')
            file.write(f'      circuit: {circuit[0]} ({circuit[3]})\n')
            file.write(f'      location: {circuit[1]}\n')
            file.write(f'      when: {event["date"].strftime("%I:%M %p")} - ')
            file.write(f'{event["end"].strftime("%I:%M %p")} ')
            file.write(
                f'{event["date"].strftime("%A, %B %d, %Y")} ({circuit[2]})\n')
            file.write('      broadcasters:')
            for broadcaster in cur_broadcasters:
                file.write(f'\n        - {broadcaster["name"]}')

            prev_date = cur_date


def get_circuit(circuits: list[dict], event: dict) -> tuple[str, str, str, str]:
    """ Retrieves circuit name, location, timezone, and direction from event
            Input: list of 'circuit' dicts, 'event' dict
            Output: name, location, timezone, direction of corresponding circuit to given event's location
    """
    id = event["location"]
    circuit = next(
        (circuit for circuit in circuits if circuit["id"] == id), None)
    return circuit["name"], circuit["location"], circuit["timezone"], circuit["direction"]


def get_broadcasters(broadcasters: list[dict], event: dict) -> list[dict]:
    """ Retrieves broadcaster info based off event data
            Input: list of 'broadcaster' dicts, 'event' dict
            Output: list of broadcaster dicts corresponding to given event's broadcasters
    """
    ids = event["broadcaster"].split(",")
    ids = [int(id.lstrip("BR"))-1 for id in ids]
    actual_broadcasters = []

    for id in ids:
        broadcaster = broadcasters[id]
        actual_broadcasters.append(broadcaster)

    return actual_broadcasters


if __name__ == '__main__':
    main()

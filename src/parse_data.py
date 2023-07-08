#!/usr/bin/env python3
"""
Parse data from tapology.com.

Turn the data into a figther and fight record.
"""

import re

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

URL = 'GET YOUR OWN FIGHTER LINK'


def get_name(url) -> str:
    """Make https request to get the fighter name."""
    request = requests.get(
        url, verify=False, allow_redirects=False, headers=HEADERS
    )

    if request.status_code != 200:
        return "couldn't get code"
    content = BeautifulSoup(request.text, 'html.parser').find('title')
    name = str(content).split()

    # Strip out <title> which is the first 6 characters
    first_name = name[0][7:].strip()
    last_name = name[1]
    full_name = first_name + ' ' + last_name

    return full_name


def get_record(url):
    """Make https request to get the fighter record as int tuple."""
    request = requests.get(
        url, verify=False, allow_redirects=False, headers=HEADERS
    )

    if request.status_code != 200:
        return "couldn't get code"

    content = BeautifulSoup(request.text, 'html.parser').find_all(
        'h1', class_='prorecord'
    )

    record = str(content).split()[1]
    if record is None:
        print("Can't parse fighter record")
        return None

    record = re.search(r'>.+-', record).group().split('-')
    wins = int(record[0][1:])
    losses = int(record[1])
    fighter_record = (wins, losses)

    return fighter_record


print(get_record(URL))

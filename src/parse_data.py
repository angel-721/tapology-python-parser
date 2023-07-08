#!/usr/bin/env python3
"""
Parse data from tapology.com.

Turn the data into a figther and fight record.
"""
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def get_name(url):
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

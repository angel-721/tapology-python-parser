#!/usr/bin/env python3
"""
Parse data from tapology.com.

Turn the data into a fighter and fight record.
"""

import re
import requests
from bs4 import BeautifulSoup
from fighter import Fighter, Fight

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_soup(url) -> BeautifulSoup:
    try:
        request = requests.get(
            url, verify=False, allow_redirects=False, headers=HEADERS
        )
    except Exception as e:
        raise e
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup

def get_name(soup: BeautifulSoup) -> str:
    header_div = soup.find('div', class_='fighterUpcomingHeader')
    name_header = header_div.find('h1', class_=None)
    full_name = name_header.text
    return full_name

soup = get_soup("https://www.tapology.com/fightcenter/fighters/34779-jiri-prochazka")
get_name(soup)

# def get_record(url) -> (tuple[int,int]):
#     """Make https request to get the fighter record as int tuple."""
#     request = requests.get(
#         url, verify=False, allow_redirects=False, headers=HEADERS
#     )

#     if request.status_code != 200:
#         raise requests.exceptions.HTTPError

#     content = BeautifulSoup(request.text, 'html.parser').find_all(
#         'h1', class_='prorecord'
#     )

#     record = str(content).split()[1]
#     if record is None:
#         print("Can't parse fighter record")
#         return None

#     record = re.search(r'>.+-', record).group().split('-')
#     wins = int(record[0][1:])
#     losses = int(record[1])
#     fighter_record = (wins, losses)

#     return fighter_record


# def get_height_and_reach(url) -> tuple[float, float]:
#     """Make https request to get reach and height in a tuple of floats."""
#     request = requests.get(
#         url, verify=False, allow_redirects=False, headers=HEADERS
#     )

#     if request.status_code != 200:
#         raise requests.exceptions.HTTPError

#     content = BeautifulSoup(request.text, 'html.parser').find_all('span')

#     content = str(content).split()
#     if content is None:
#         print("Can't parse fighter record")
#         return None

#     group = []
#     for line in content:
#         word = re.search(r'\(.+cm\)', line)
#         if word is not None:
#             group.append(word.group().strip('cm)'))

#     height = float(group[0][1:])
#     reach = float(group[1][1:])
#     fighter_height_reach = (height, reach)
#     return fighter_height_reach


# def get_current_streak(url):
#     """Make https request to get current streak."""
#     request = requests.get(
#         url, verify=False, allow_redirects=False, headers=HEADERS
#     )

#     word_group = []

#     if request.status_code != 200:
#         raise requests.exceptions.HTTPError
#     content = BeautifulSoup(
#         request.text, 'html.parser').find_all(["strong", "span"])
#     content = str(content).split()

#     for i in range(len(content)):
#         if "Streak:</strong>" in content[i]:
#             streak_number = content[i+1].replace('<span>', '')
#             outcome = content[i+2].replace('</span>', '').replace(',', '')
#             break

#     if outcome is None or streak_number is None:
#         print("Can't parse fighter record")
#         return None

#     if outcome == 'win':
#         streak_number = int(streak_number)
#     elif outcome == 'loss':
#         streak_number = int(streak_number) * -1

#     return streak_number

# def parse_fight(url):
#     request = requests.get(
#         url, verify=False, allow_redirects=False, headers=HEADERS
#     )

#     if request.status_code != 200:
#         raise requests.exceptions.HTTPError

#     soup = BeautifulSoup(request.text, 'html.parser')
#     span_tags = soup.find_all("span", class_ ="fName")
#     a_tags = [tag.find('a') for tag in span_tags if tag.a != None]

#     links = [a.get('href') for a in a_tags]

#     for i in range(0, len(links)):
#         links[i] = "https://www.tapology.com" + links[i]

#     fighter_r = make_fighter_object(links[0])
#     fighter_b = make_fighter_object(links[1])
#     fight = Fight(fighter_r, fighter_b)
#     return Fight

# def make_fighter_object(url) -> Fighter:
#     name = get_name(url)
#     record = get_record(url)
#     wins = record[0]
#     losses = record[1]
#     streak = get_current_streak(url)
#     height_and_reach = get_height_and_reach(url)
#     height = height_and_reach[0]
#     reach = height_and_reach[1]
#     return Fighter(name, wins, losses, streak, height, reach)

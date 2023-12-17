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

def get_record(soup: BeautifulSoup) -> (tuple[int,int]):
    content = soup.find('h1', class_='prorecord')
    record_text = content.text.split('-')
    wins, losses = int(record_text[0]), int(record_text[1])
    return (wins,losses)

def get_height_and_reach(soup) -> tuple[float, float]:

    content = soup.find_all('span')

    content = str(content).split()

    group = []
    for line in content:
        word = re.search(r'\(.+cm\)', line)
        if word is not None:
            group.append(word.group().strip('cm)'))

    height = float(group[0][1:])
    reach = float(group[1][1:])
    return (height,reach)


def get_current_streak(soup):

    word_group = []

    content = soup.find_all(["strong", "span"])
    content = str(content).split()

    for i in range(len(content)):
        if "Streak:</strong>" in content[i]:
            streak_number = content[i+1].replace('<span>', '')
            outcome = content[i+2].replace('</span>', '').replace(',', '')
            break

    if outcome is None or streak_number is None:
        print("Can't parse fighter record")
        return None

    if outcome == 'Win':
        streak_number = int(streak_number)
    elif outcome == 'Loss':
        streak_number = int(streak_number) * -1

    return streak_number

def make_fighter_object(url) -> Fighter:
    soup = get_soup(url)
    name = get_name(soup)
    record = get_record(soup)
    wins = record[0]
    losses = record[1]

    streak = get_current_streak(soup)

    height_and_reach = get_height_and_reach(soup)
    height = height_and_reach[0]
    reach = height_and_reach[1]
    return Fighter(name, wins, losses, streak, height, reach)

def parse_fight(url) -> Fight:
    request = requests.get(
        url, verify=False, allow_redirects=False, headers=HEADERS
    )

    if request.status_code != 200:
        raise requests.exceptions.HTTPError

    soup = BeautifulSoup(request.text, 'html.parser')
    span_tags = soup.find_all("span", class_ ="fName")
    a_tags = [tag.find('a') for tag in span_tags if tag.a != None]

    links = [a.get('href') for a in a_tags]

    for i in range(0, len(links)):
        links[i] = "https://www.tapology.com" + links[i]

    fighter_r: Fighter = make_fighter_object(links[0])
    fighter_b: Fighter = make_fighter_object(links[1])
    fight: Fight = Fight(fighter_r, fighter_b)
    return fight

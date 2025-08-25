#!/usr/bin/env python3
"""
Parse data from tapology.com.

Turn the data into a fighter and fight record.
"""

import re

import requests
import urllib3
from bs4 import BeautifulSoup

from fighter import Fight, Fighter

urllib3.disable_warnings()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def get_soup(url: str) -> BeautifulSoup:
    try:
        request = requests.get(
            url, verify=False, allow_redirects=False, headers=HEADERS
        )
    except Exception as e:
        raise e

    soup = BeautifulSoup(request.text, "html.parser")
    return soup


def get_name(soup: BeautifulSoup) -> str:
    header_div = soup.find(
        "div",
        class_="div text-tap_3 text-[26px] leading-tight md:leading-none font-bold",
    )
    return header_div.text if header_div else ""


def get_record(soup: BeautifulSoup) -> tuple[int, int]:
    a_tag = soup.find("a", href="#fighterRecordHeader")
    if not a_tag:
        return (-1, -1)

    div = a_tag.find("div", class_="div text-tap_3 text-[26px]")  # type: ignore

    if not div:
        return (-1, -1)

    record_text = div.text.split("-")
    wins, losses = int(record_text[0]), int(record_text[1])

    return (wins, losses)


def get_height_and_reach(soup: BeautifulSoup) -> tuple[float, float]:
    content = soup.find_all("span")

    content = str(content).split()

    group = []
    for line in content:
        word = re.search(r"\(.+cm\)", line)

        if word is None:
            continue

        group.append(word.group().strip("cm)"))

    height = float(group[0][1:])
    reach = float(group[1][1:])
    return (height, reach)


def get_current_streak(soup: BeautifulSoup) -> int:
    content = soup.find_all(["strong", "span"])
    content = str(content).split()

    outcome = None
    streak_number_text = None
    streak_number = -99

    for i in range(len(content)):
        if "Streak:</strong>" in content[i]:
            streak_number_text = content[i + 1].replace("<span>", "")
            outcome = content[i + 2].replace("</span>", "").replace(",", "")
            break

    if not outcome or not streak_number_text:
        return -99

    if outcome == "Win":
        streak_number = int(streak_number_text)
    elif outcome == "Loss":
        streak_number = int(streak_number_text) * -1

    return streak_number


def make_fighter_object(url: str) -> Fighter:
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


def parse_fight(url: str) -> Fight:
    request = requests.get(url, verify=False, allow_redirects=False, headers=HEADERS)

    if request.status_code != 200:
        raise requests.exceptions.HTTPError

    soup = BeautifulSoup(request.text, "html.parser")
    div_tags = soup.find_all(
        "div",
        class_="div w-1/3 md:w-[261px] flex flex-col text-sm md:text-xs font-bold items-center truncate",
    )
    a_tags = [tag.find("a") for tag in div_tags if tag.a != None]

    links = [a.get("href") for a in a_tags]

    for i in range(0, len(links)):
        links[i] = "https://www.tapology.com" + links[i]

    fighter_r: Fighter = make_fighter_object(links[0])
    fighter_b: Fighter = make_fighter_object(links[1])
    fight: Fight = Fight(fighter_r, fighter_b)

    return fight

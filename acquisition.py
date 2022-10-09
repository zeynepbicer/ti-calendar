import requests
from bs4 import BeautifulSoup
from typing import List
from models import Match
from datetime import datetime
import pytz
import pandas as pd

def get_matches():
    page = requests.get("https://liquipedia.net/dota2/The_International/2022/Last_Chance_Qualifier")
    soup = BeautifulSoup(page.content, 'html.parser')
    match_details = soup.findAll('div', class_='brkts-popup brkts-match-info-popup')
    matches: List[Match] = []
    for m in match_details:
        team_left = m.select('.brkts-popup-header-opponent-left .name')
        team_right = m.select('.brkts-popup-header-opponent-right .name')
        dt = m.select('.timer-object')
        if dt:
            dt = dt[0].get_text()
            dt = dt.replace('SGT', 'UTC+0800')
            dt =  datetime.strptime(dt,'%B %d, %Y - %H:%M %Z%z').astimezone(pytz.timezone("Europe/London"))
        match: Match = {
            'team_left': team_left[0].get_text() if team_left else None,
            'team_right': team_right[0].get_text() if team_right else None,
            'date': dt if dt else None,
        }
        if match['date']:
            matches.append(match)
    return pd.DataFrame(matches)
# # print(pytz.common_timezones)
# date = datetime.strptime('January 1, 2022 - 12:00 UTC+0800','%B %d, %Y - %H:%M %Z%z').astimezone(pytz.timezone("Europe/London"))
# print(datetime.strftime(date, format = '%Y-%m-%d %H:%M'))

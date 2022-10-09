from ics import Calendar, Event
from datetime import tzinfo, timedelta
from datetime import datetime as dt
from typing import List
from models import Match
from acquisition import get_matches

calendar = Calendar()

def date_range(start:str, end:str):
    start_date = dt.strptime(start,'%Y-%m-%d')
    end_date = dt.strptime(end,'%Y-%m-%d')
    delta = (end_date-start_date).days
    dates = [start_date + timedelta(i) for i in range(delta+1)]
    return dates

ti_dates = {
    'Last Chance Qualifiers': {f'Day {i+1}': date for i,date in enumerate(date_range('2022-10-08', '2022-10-12'))},
    'Group Stage': {f'Day {i+1}': date for i,date in enumerate(date_range('2022-10-15', '2022-10-18'))},
    'Main Event': {f'Day {i+1}': date for i,date in enumerate(date_range('2022-10-20', '2022-10-23') + date_range('2022-10-29', '2022-10-30'))},
}

lcq_matches = get_matches()
print(lcq_matches)
for _, info in lcq_matches.iterrows():
        e = Event()
        e.name = f"{info['team_left']} vs. {info['team_right']} \n BO2"
        e.begin = info['date']
        e.description = 'Last Chance Qualifiers'
        e.duration = timedelta(hours=2, minutes=30)
        calendar.events.add(e)

print(calendar.events)
with open('ti-calendar.ics', 'w') as my_file:
    my_file.writelines(calendar.serialize_iter())
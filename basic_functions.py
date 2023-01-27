import pandas as pd
from datetime import datetime, timedelta
from mplcal import MplCalendar
from calendar import monthrange

### DATA READERS
## in the future you will add name of user who is logging

def all_friends_reader():
    all_friends = pd.read_csv('friends.csv').dropna()
    all_friends['contacted'] = pd.to_datetime(all_friends['contacted'])
    return all_friends

def session_data_reader():
    sessiondata = pd.read_csv('session/session_data.csv').dropna()
    sessiondata['today'] = pd.to_datetime(sessiondata['today'])
    return sessiondata

def future_week_reader():
    future = pd.read_csv('future.csv').dropna()
    future['call'] = pd.to_datetime(future['call'])
    yest = datetime.today() - timedelta(days=1)
    future = future[future['call'] >= yest]
    return future

### ADD FRIENDS

def person(name, surname, love, frequency, last_contact):
    name = name.lower()
    surname = surname.lower()
    person_dict = {
        'name': [name],
        'surname': [surname],
        'love': [love],
        'frequency': [frequency],
        'contacted': [last_contact]
        }
    person_df = pd.DataFrame(person_dict)
    person_df['contacted'] = pd.to_datetime(person_df['contacted'])
    return person_df

def add_friend(person, all_friends):
    all_friends = all_friends.append(person)
    all_friends.to_csv('friends.csv', index=False)
    return all_friends

def future_person(name, surname, call_time):
    name = name.lower()
    surname = surname.lower()
    person_dict = {
        'name': [name],
        'surname': [surname],
        'call': [call_time]
        }
    person_df = pd.DataFrame(person_dict)
    person_df['call'] = pd.to_datetime(person_df['call'])
    return person_df


### SCORE RELATED

def date_reset(all_friends, name_to_text_today, surname_to_text_today):
    today = datetime.today()
    current_date = today.strftime("%m/%d/%y")
    all_friends.loc[(all_friends['name'] == name_to_text_today) & (all_friends['surname'] == surname_to_text_today), 'contacted'] = current_date
    all_friends.to_csv('friends.csv', index=False)

def day_score_calculator(all_friends):
    days_passed = [datetime.today() - event for event in all_friends['contacted']]
    days_passed = [time.days for time in days_passed]
    return days_passed

def rule_based_score(all_friends, day_score):
    eligibility = []
    for row in range(len(day_score)):
        if (day_score[row]/7 + 1) >= all_friends['frequency'][row]:
            eligible = 1
        else:
            eligible = 0
        eligibility.append(eligible)
    return eligibility

def total_score_calculator(all_friends, day_score, rule_based_score):
    total_score = day_score * rule_based_score * all_friends['love']
    total_score = pd.Series(total_score)
    return total_score

### OUTPUT RELATED

def person_to_write_calculator(sessiondata, all_friends, future):
    todays_string = datetime.today().date().strftime("%Y-%m-%d")
    # was the code already run today?
    if (todays_string == sessiondata['today'][0].strftime("%Y-%m-%d")):
        name_to_text_today = sessiondata['name to text'][0]
        surname_to_text_today = sessiondata['surname to text'][0]
    else: 
        # calculate scores
        day_score = day_score_calculator(all_friends)
        total_score = (total_score_calculator(all_friends, day_score))
        name_to_text_today = all_friends[total_score == max(total_score)].reset_index()['name'][0]
        surname_to_text_today = all_friends[total_score == max(total_score)].reset_index()['surname'][0]
        date_reset(all_friends, name_to_text_today, surname_to_text_today)
        # update session data
        sessiondata['today'] = todays_string
        sessiondata['name to text'] = name_to_text_today
        sessiondata['surname to text'] = surname_to_text_today
        sessiondata.to_csv('session/session_data.csv', index=False)

        # update future call log
        date_to_call = (datetime.today().date() + timedelta(days = 7)).strftime("%Y-%m-%d")
        person = future_person(name_to_text_today, surname_to_text_today, date_to_call)
        future = future.append(person)
        future.to_csv('future.csv', index=False)
    return name_to_text_today, surname_to_text_today

def person_to_call_calculator(future):
    todays_string = datetime.today().date().strftime("%Y-%m-%d")
    if len(future[future['call'] == todays_string]) == 0:
        name_to_call = 'no one'
        surname_to_call = 'to call today'
    else: 
        name_to_call = future[future['call'] == todays_string]['name'][0]
        surname_to_call = future[future['call'] == todays_string]['surname'][0]
    return name_to_call, surname_to_call



### CALENDAR DISPLAY
import requests
import csv
from tabulate import tabulate
from collections import Counter

def get_csv_from_url(drive_link):
    orig_url=drive_link
    file_id = orig_url.split('/')[-2]
    dwn_url='https://drive.google.com/uc?export=download&id=' + file_id
    url = requests.get(dwn_url)
    rows = url.text.splitlines()
    table = csv.reader(rows)    
    final_list = [row for row in table]
    return final_list

def display_result(winner):
    print(tabulate(winner,headers=["HOME-TEAM","AWAY-TEAM","SCORE","WINNER"],tablefmt="grid"))

def display_wins(teams):
    result = dict(Counter(teams))
    matches_won = [[team,wins] for team,wins in result.items()]
    print(tabulate(matches_won,headers=["TEAM","MATCHES_WON"],tablefmt="grid"))

def home_team_results(results):
    home_team_wins = []
    for item in results:
        if item[0] == item[3]:
            home_team_wins.append(item[0])
    return home_team_wins

def away_team_results(results):
    away_team_wins = []
    for item in results:
        if item[1] == item[3]:
            away_team_wins.append(item[1])
    return away_team_wins

def calc_win_loss_draw(result,match):
    if result[0] > result[1]:
        result = [match[0]]
    elif result[1] > result[0]:
        result = [match[1]]
    else:
        result = ["DRAW"]
    match.extend(result)
    return match

def get_match_data():
    url = "https://drive.google.com/file/d/1thhBK4uFRw_3FguVYMw5y8HNDWesG10D/view?usp=sharing"
    match_data,results = get_csv_from_url(url),[]
    matches = [[row[3],row[4],row[7]] for row in match_data]
    for i in range(1,len(matches)):
        _,_,score = matches[i]
        result = [int(row) for row in score.split("–")]
        results.append(calc_win_loss_draw(result,matches[i]))
    display_result(results)
    result1 = home_team_results(results)
    result2 = away_team_results(results)
    result1.extend(result2)
    display_wins(result1)

get_match_data()
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

def display_match_winners_table(winners):
    print(tabulate(winners,headers=["HOME-TEAM","AWAY-TEAM","SCORE","WINNER"],tablefmt="grid"))
    winners.insert(0,["HOME-TEAM","AWAY-TEAM","SCORE","WINNER"])
    return winners

def display_matches_won(teams):
    result = dict(Counter(teams))
    matches_won = [[team,wins] for team,wins in result.items()]
    print(tabulate(matches_won,headers=["TEAM","MATCHES_WON"],tablefmt="grid"))
    matches_won.insert(0,["TEAM","MATCHES_WON"])
    return matches_won

def calc_win_loss_draw(result,match):
    if result[0] > result[1]:
        result = [match[0]]
    elif result[1] > result[0]:
        result = [match[1]]
    else:
        result = ["DRAW"]
    match.extend(result)
    return match

def output_to_csv_file(final_result,num):
    with open(f"Soccer_Analytics/match_results{num}.csv","w",newline="\n") as file:
        writer = csv.writer(file)
        writer.writerows(final_result)

def get_match_data():
    url = "https://drive.google.com/file/d/1thhBK4uFRw_3FguVYMw5y8HNDWesG10D/view?usp=sharing"
    match_data,results = get_csv_from_url(url),[]
    matches = [[row[3],row[4],row[7]] for row in match_data]
    for i in range(1,len(matches)):
        _,_,score = matches[i]
        result = [int(row) for row in score.split("–")]
        results.append(calc_win_loss_draw(result,matches[i]))
    winning_teams = list(filter(lambda team: team[3]!="DRAW",results))
    final_result = [team[3] for team in winning_teams]
    match_winners = display_match_winners_table(results)
    matches_won = display_matches_won(final_result)
    num = 1
    for matches_list in match_winners,matches_won:
        output_to_csv_file(matches_list,num)
        num+=1
get_match_data()
import sys
import csv
import json
from tabulate import tabulate
from collections import Counter

def get_input(csv_file):
    with open(f"{csv_file}","r",encoding='utf8') as file:
        table = csv.reader(file)    
        final_list = [row for row in table]
    return final_list

def calc_win_loss_draw(result,match):
    if result[0] > result[1]:
        result = [match[0]]
    elif result[1] > result[0]:
        result = [match[1]]
    else:
        result = ["DRAW"]
    match.extend(result)
    return match

def output_to_csv_file(file_name,final_result):
    with open(f"{file_name}","w",newline="\n") as file:
        writer = csv.writer(file)
        writer.writerows(final_result)

def process_input(matches):
    match_winners=[]
    matches = [[row[3],row[4],row[7]] for row in matches]
    for i in range(1,len(matches)):
        _,_,score = matches[i]
        result = [int(row) for row in score.split("–")]
        match_winners.append(calc_win_loss_draw(result,matches[i]))
    winning_teams = list(filter(lambda team: team[3]!="DRAW",match_winners))
    teams = [team[3] for team in winning_teams]
    result = dict(Counter(teams))
    matches_won = [[team,wins] for team,wins in result.items()]
    match_winners.insert(0,["HOME-TEAM","AWAY-TEAM","SCORE","WINNER"])
    matches_won.insert(0,["TEAM","MATCHES_WON"])
    return match_winners,matches_won

def display_output(winners,teams):
    print(tabulate(winners,tablefmt="grid"))
    print(tabulate(teams,tablefmt="grid"))

def write_output(match_winners,matches_won,file_path1,file_path2):
    output_to_csv_file(file_path1,match_winners)
    output_to_csv_file(file_path2,matches_won)

def get_json(json_input):
    with open(f"{json_input}","r") as file:
        paths = json.load(file)
    return paths

def main():
    cli_input = sys.argv
    json_input=cli_input[1]
    file_paths = get_json(json_input)
    MatchData = get_input(file_paths["input_csv_path"])
    match_winners,matches_won=process_input(MatchData)
    display_output(match_winners,matches_won)
    write_output(match_winners,matches_won,
    file_paths["output_csv_path_MatchWinners"],
    file_paths["output_csv_path_MatchesWon"])
main()


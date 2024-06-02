#Import necessary libraries
import sys 
import csv 
import json 
import os 
import pandas as pd
from tabulate import tabulate
from collections import Counter

#Read csv file using pandas 
def read_input(csv_file): 
    df = pd.read_csv(csv_file) 
    return df
 
#Calc win,loss,draw between teams 
def calc_win_loss_draw(matches): 
    match_winners = [] 
    for index,row in matches.iterrows(): 
        if int(row["score"][0]) > int(row["score"][2]): 
            match_winners.append(row["home_team"]) 
        elif int(row["score"][0]) < int(row["score"][2]): 
            match_winners.append(row["away_team"]) 
        else: 
            match_winners.append("DRAW") 
    matches["winner"] = match_winners 
    return matches,match_winners 

def output_to_csv_file(file_name,final_result): 
    with open(f"{file_name}","w",newline="\n") as file: 
        writer = csv.writer(file) 
        writer.writerows(final_result) 
        
def display_write_output(winners,teams,action): 
    if action == "match_winners.csv": 
        print(tabulate(winners,tablefmt="grid")) 
        output_to_csv_file(action,winners) 
    elif action == "matches_won.csv": 
        print(tabulate(teams,tablefmt="grid")) 
        output_to_csv_file(action,teams) 
    else: 
        print(tabulate(winners,tablefmt="grid")) 
        print(tabulate(teams,tablefmt="grid")) 
        output_to_csv_file("match_winners.csv",winners) 
        output_to_csv_file("matches_won.csv",teams)

def process_input(matches): 
    matches,match_winners = calc_win_loss_draw(matches) 
    match_winners = matches[["home_team","away_team","score","winner"]].values.tolist() 
    winning_teams = list(filter(lambda team:team[3]!="DRAW" ,match_winners))
    teams = dict(Counter([team[3] for team in winning_teams]))
    matches_won = [[team,wins] for team,wins in teams.items()]
    match_winners.insert(0,["HOME_TEAM","AWAY_TEAM","SCORE","WINNER"])
    matches_won.insert(0,["TEAM","WINS"])
    return match_winners,matches_won

def read_config(json_input): 
    with open(f"{json_input}","r") as file: 
        paths = json.load(file) 
        return paths
     
def main(): 
    cli_input = sys.argv 
    #Get value from environment variable 
    config_path = os.getenv("config_file") 
    # Process according to user input either match_winners or matches_won or none 
    try: 
        action_to_perform = cli_input[1] 
    except Exception as e: 
        action_to_perform="" 
    file_paths = read_config(config_path)
    match_data = read_input(file_paths["input_csv_path"]) 
    match_winners,matches_won=process_input(match_data) 
    display_write_output(match_winners,matches_won,action_to_perform)

main()
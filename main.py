import requests
import json
def write_json(data, filename='info.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 
def create_comp(team):
    page = requests.get(f'https://www.nitrotype.com/api/teams/{team}')
    info = json.loads(page.text)
    with open('info.json', 'r+') as f:
        f.truncate()
        data = {
            "accounts": [

            ]
        }
        try:
            for elem in info['data']['members']:
                data['accounts'].append({
                    "username": elem['username'],
                    "starting-races": elem['played'],
                    "ending-races": elem['played'],
                    "total-races": 0
                })
            write_json(data)
        except KeyError:
            print('This team doesn\'t exist!')
def update_comp(team):
    page = requests.get(f'https://www.nitrotype.com/api/teams/{team}')
    info = json.loads(page.text)
    with open('info.json', 'r+') as f:
        data = json.load(f)
        for elem in info['data']['members']:
            for users in data['accounts']:
                if users['username'] == elem['username']:
                    users['ending-races'] = elem['played']
                    users['total-races'] = users['ending-races'] - users['starting-races']
                    users['stillinteam'] = True
        write_json(data)
def leaderboard(kicked=False):
    with open('info.json') as f:
        data = json.load(f)
        races = []
        racers = []
        inteam = []
        for users in data['accounts']:
            races.append(users['total-races'])
            racers.append(users['username'])
            inteam.append(users['stillinteam'])
        racesnow = sorted(races, reverse=True)
        zipped_lists = zip(races, racers)
        sorted_zipped_lists = sorted(zipped_lists, reverse=True)
        sorted_list1 = [element for _, element in sorted_zipped_lists]
        rank = 1
        for elem in sorted_list1:
            index = racers.index(elem)
            if kicked:
                print(f'{rank}. {elem} ({racesnow[rank-1]}) [inteam:{inteam[index]}]')
                rank = rank + 1
            elif kicked == False:
                if inteam[index]:
                    print(f'{rank}. {elem} ({racesnow[rank-1]})')
                    rank = rank + 1
                elif inteam[index] == False:
                    continue
options = input('Create or leaderboard? (c, l)')
team = input('What is your team?\n')
if options == 'c':
    create_comp(team)
if options == 'l':
    update_comp(team)
    kicked = input('Do you want to see kicked members\' races?(y, n)')
    if kicked == 'y':
        leaderboard(True)
    else:
        leaderboard()

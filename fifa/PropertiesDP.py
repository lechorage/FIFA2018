from util import *
from trueskill import Rating, rate, BETA, global_env, setup, quality
import itertools
import math
import pandas as pd


# 根据 Trueskill 的 rating 模型，计算胜率
def win_probability(team1, team2):
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    denom = math.sqrt(size * (BETA * BETA) + sum_sigma)
    ts = global_env()
    return ts.cdf(delta_mu / denom)


data = load_json(' 1data/wc_sofifa.json')
df = pd.DataFrame(data)[['name', 'overall', 'positions', 'club']]

elos = load_json('data/elo.json')
df['elo'] = df['club'].apply(lambda x: elos[x])
df[df['club'] == 'Peru']

matchups = [
    {
        'Denmark': [83, 80, 82, 71, 73, 77, 78, 89, 76, 78, 74],
        'Peru': [76, 75, 74, 74, 76, 78, 77, 75, 80, 79, 75]
    },
]
# 0.22 来自所有国家队比赛数据
setup(draw_probability=0.22, sigma=2000 / 3, beta=2000 / 3 / 2)


def calculate_with_matchup(matchup):
    teams = []
    nations = []
    for nation, indexes in matchup.items():
        ratings = []
        nations.append(nation)
        #         print(nation)
        for i in indexes:
            player = df.iloc[i]
            ratings.append(Rating(mu=player['overall'] + player['elo']))
        #             print(player['name'], ratings[-1])
        teams.append(ratings)
    print("{0} 胜率：".format(nations[0]), win_probability(teams[0], teams[1]))
    print("{0} 胜率：".format(nations[1]), win_probability(teams[1], teams[0]))
    print("平局概率：", quality(teams))
    print()


for item in matchups:
    calculate_with_matchup(item)

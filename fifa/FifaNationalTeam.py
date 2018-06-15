import re

from requests import get
from bs4 import BeautifulSoup
import json
import time
import os


def api(offset=0):
    return "https://sofifa.com/teams/national?offset=0" + str(offset)


HEADERS = {
    'user-agent':
        (
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'),
    # noqa: E501
    'Dnt': ('1'),
    'Accept-Encoding': ('gzip, deflate, sdch'),
    'Accept-Language': ('en'),
    'origin': ('http://www.baidu.com')
}


def load_json(file_name):
    with open(file_name) as json_data:
        d = json.load(json_data)
        return d


def write_json(file_name, json_data):
    print('writting:' + file_name)
    with open(file_name, 'w') as outfile:
        json.dump(json_data, outfile)
        return json_data
    print('writing done:' + file_name)


def national_team():
    offset = 0
    item = {}
    i = 0
    avg = 0
    country = 'begin'
    payload = {}
    while True:
        response = get(api(offset=offset), headers=HEADERS, timeout=50)
        resHtml = response.text
        html = BeautifulSoup(resHtml, 'html.parser')
        if len(html.select('td')) <= 0:
            break
        for td in html.select('td'):
            if 'id' in td.attrs:
                if len(td.select('div > span')) > 0:
                    payload[td.attrs['id']] = td.select('div > span')[0].text
                    avg += int(td.select('div > span')[0].text)
                    i += 1
                    if i % 4 == 0:
                        payload['avg'] = avg / 4.0
                        item[country].append({'BASIC': payload})
                        avg = 0
                        payload = {}
            if len(td.select('a')) > 0:
                item[td.select('a')[0].text] = [{'REGION': td.select('a')[1].text}]
                country = td.select('a')[0].text
        # write_json('/Users/panpangu/FIFA2018/dataset/NationalTeam', item)
        offset += 60
    return item


def average():
    total_oa = 0
    total_at = 0
    total_md = 0
    total_df = 0
    total_avg = 0
    count = 0
    data = national_team()
    for key, value in data.items():
        if len(value) == 2:
            total_oa += int(value[1]['BASIC']['oa'])
            total_at += int(value[1]['BASIC']['at'])
            total_md += int(value[1]['BASIC']['md'])
            total_df += int(value[1]['BASIC']['df'])
            total_avg += int(value[1]['BASIC']['avg'])
            count += 1
    payload = {'avg_oa': total_oa / count, 'avg_at': total_at / count, 'avg_md': total_md / count,
               'avg_df': total_df / count, 'total_avg': total_avg / count}
    data['avg'] = payload
    write_json('/Users/panpangu/FIFA2018/dataset/NationalTeam', data)


if __name__ == '__main__':
    average()

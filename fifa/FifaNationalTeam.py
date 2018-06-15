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
        write_json('/Users/panpangu/FIFA2018/fifa/dataset/NationalTeam', item)
        offset += 60


if __name__ == '__main__':
    national_team()

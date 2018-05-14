"""
Display your grailed listings and bumps them where possible

Usage: python autobump.py <your email> <your password>

"""

import argparse
import requests


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("email")
    parser.add_argument("password")
    args = parser.parse_args()

    session = requests.Session()
    resp = session.get("https://www.grailed.com")
    token = (resp.text.split('<meta name="csrf-token" content="')[1]
             .split('"')[0])
    headers = {'x-csrf-token': token}

    data = {'email': args.email, 'password': args.password}
    resp = session.post("https://www.grailed.com/api/sign_in", data=data)
    data = resp.json()
    if 'error' in data:
        raise ValueError(data['error'])

    url = ("https://www.grailed.com/api/users/{}/wardrobe"
           .format(data['data']['user']['id']))
    resp = session.get(url)
    items = resp.json()['data']
    for item in items:
        url = "https://www.grailed.com/api/listings/{}/bump".format(item['id'])
        resp = session.post(url, headers=headers)
        bumped = "" if 'error' in resp.json() else "bumped!"
        print(u"{:<50} $ {:<6} \u2764 {:<6} {}".format(
            item['designer']['name'] + " " + item['title'],
            item['price'],
            item['follower_count'],
            bumped))

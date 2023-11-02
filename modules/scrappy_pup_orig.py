# Scrappy Pup v0.5
# empty_circle - 2023
# Scrappy Pup is a rudimentary website scraper.

import requests
import re
import argparse
import configparser
from bs4 import BeautifulSoup
from tabulate import tabulate
import os

def get_url_from_user():
    url = input("Enter the URL of the website you want to scrape: ")
    return url

def get_keywords_from_config():
    config = configparser.ConfigParser()
    if not os.path.exists('scrappy_pup_config.ini'):
        return []
    config.read('scrappy_pup_config.ini')
    try:
        keywords = config.get('keywords', 'list').split(',')
    except (configparser.NoSectionError, configparser.NoOptionError):
        return []
    return [keyword.strip() for keyword in keywords]

def extract_links(soup):
    return [a['href'] for a in soup.find_all('a', href=True)]

def extract_usernames(soup):
    return [span.text for span in soup.find_all('span', {'class': 'username'})]

def extract_email_addresses(soup):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, str(soup))

def extract_ip_addresses(soup):
    ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    return re.findall(ip_pattern, str(soup))

def extract_bitcoin_addresses(soup):
    bitcoin_pattern = r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b'
    return re.findall(bitcoin_pattern, str(soup))

def extract_dates(soup):
    return [time['datetime'] for time in soup.find_all('time', {'datetime': True})]

def find_keywords(soup, keywords):
    found_keywords = []
    for keyword in keywords:
        if keyword in str(soup).lower():
            found_keywords.append(keyword)
    return found_keywords

def main():
    parser = argparse.ArgumentParser(description='Scrappy Pup v1.1 - A rudimentary website scraper')
    parser.add_argument('-u', '--url', help='The URL of the website to scrape', default=None)
    args = parser.parse_args()

    if args.url:
        url = args.url
    else:
        url = get_url_from_user()

    headers = {'User-Agent': 'Scrappy Pup v1.1'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        links = extract_links(soup)
        usernames = extract_usernames(soup)
        emails = extract_email_addresses(soup)
        ip_addresses = extract_ip_addresses(soup)
        bitcoin_addresses = extract_bitcoin_addresses(soup)
        dates = extract_dates(soup)
        keywords = get_keywords_from_config()
        found_keywords = find_keywords(soup, keywords)

        data = [
            ('Links', links),
            ('Usernames', usernames),
            ('Email addresses', emails),
            ('IP addresses', ip_addresses),
            ('Bitcoin addresses', bitcoin_addresses),
            ('Dates and timestamps', dates),
            ('Found keywords', found_keywords),
        ]

        table = tabulate(data, headers=['Category', 'Results'], tablefmt='grid')

        print(table)

        try:
            with open('scrappy_pup_results.txt', 'w') as f:
                f.write(table)
        except PermissionError:
            print("Permission denied: Cannot write to scrappy_pup_results.txt'.")

    elif response.status_code == 403:
        print("Access Denied.")
    else:
        print(f"An error occurred. HTTP Status Code: {response.status_code}")

if __name__ == "__main__":
    main()

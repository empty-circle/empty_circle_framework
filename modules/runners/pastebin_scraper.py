import requests
import re

API_ENDPOINT = "https://pastebin.com/api/api_scrape_item.php"
API_PUBLIC_PASTE_KEY = 'YOUR_DEV_KEY' # Replace with your key
KEYWORDS = ['keyword1', 'keyword2', 'keyword3'] # replace with your keywords

def fetch_public_pastes():
    response = requests.get(API_ENDPOINT, params={
        'api_dev_key': API_PUBLIC_PASTE_KEY,
        'api_option': 'trends', # gets latest trending public pastes
    })

    if response.status_code == 200:
        return response.text.split('\r\n')
    else:
        print("Failed to fetch public pastes. Status code:", response.status_code)

def search_pastes(pastes):
    matches = []
    for paste in pastes:
        for keyword in KEYWORDS:
            if re.search(keyword, paste, re.IGNORECASE): # Case insensitive search
                matches.append(paste)
                break # if keyword is found, no need to check the rest of the keywords for this paste

    return matches

def main():
    pastes = fetch_public_pastes()
    matches = search_pastes(pastes)

    print("Pastes containing the specified keywords:")
    for paste in matches:
        print(paste)

if __name__ == "__main__":
    main()

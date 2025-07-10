import requests
import re
import time

def SendTelegramNotification(i):
    chat_id = "1760514861"
    TOKEN = "5696092807:AAGMeYmZH23Er2E0rllHd9-FKHgO0klYGaQ"
    #url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={i}&parse_mode=MarkdownV2"
    print(requests.get(url).json())     # this sends the message

# Custom headers (mimicking a browser)
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://privatedelights.ch/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# List of users
users = [
    "Exoticbabeh", "MissKateJoin", "Susana_Roze", "Itsriribabe", "SexyLindsey", "Sofia_sweet",
    "LikaStar", "LovelyVioletWinters", "Masha_poland", "Katia600", "Elsi",
    "Miss_Mari", "Lalalexilove", "AlexPetson", "SashaXo", "sxyisadora",
    "TiffanyDiamond", "Marcevip", "KyliePeyton"
]

# List of cities to check
cities = [
    "San-Jose", "Sunnyvale", "Santa-Clara", "Milpitas", "Campbell", "Cupertino",
    "Palo-Alto", "San-Mateo", "Los-Altos", "Mountain-View", "Redwood-City",
    "Fresno", "Los-Gatos", "Saratoga", "Fremont", "Morgan-Hill"
]

# Base URL format
base_url = "https://privatedelights.ch/USA/California/{city}/{user}"

# Time threshold: 2 days ago in milliseconds
two_days_ago_ms = int(time.time() - 2 * 24 * 60 * 60) * 1000

# Regex to extract time value
time_regex = re.compile(r'"time":(\d{13})')
### INSIDE SOURCE: size":"C","nolist":[],"time":1751385131011,"bump":

# Check each user
for user in users:
    found = False
    for city in cities:
        url = base_url.format(city=city, user=user)
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                # Extract time from page
                match = time_regex.search(response.text)
                if match:
                    timestamp = int(match.group(1))
                    if timestamp >= two_days_ago_ms:
                        print(f"Y | {user}  {city}  - ACTIVE"); user = user.replace('_', '\\_')
                        SendTelegramNotification(f"_*PD:*_ {user} in {city.replace('-', ' ')}\\!")
                        found = True
                        break  # Found and active, move to next user
                    else:
                        print(f"Y | {user}  {city}  - not active")
                        # Do NOT break, keep looking
                else:
                    print(f"Y | {user}  {city} (time not found)")
                    # Optionally continue searching other cities
            else:
                print(f"\t\tX... {user}  {city} (HTTP {response.status_code})");
        except requests.RequestException:
            continue  # Ignore error and try next city
    if not found:
        print(f"\t\tX | {user}")

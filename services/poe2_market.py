from utils.api_helper import fetch_safe
import urllib.parse

def get_active_league():
    data = fetch_safe("https://poe.ninja/api/data/getindexstate?game=poe2")
    if data and 'economyLeagues' in data:
        for l in data['economyLeagues']:
            if l.get('active') and 'SSF' not in l.get('name', '') and 'HC' not in l.get('name', ''):
                return l.get('name')
    return "Runes of Aldur"

def get_price(item_name):
    league = get_active_league()
    url = f"https://poe.ninja/api/data/currencyoverview?game=poe2&league={urllib.parse.quote(league)}&type=Currency"
    data = fetch_safe(url)
    if data and 'lines' in data:
        for line in data['lines']:
            if line.get('currencyTypeName', '').lower() == item_name.lower():
                return line.get('chaosEquivalent', 0), league
    return None, league

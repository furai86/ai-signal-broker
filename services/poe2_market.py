from utils.api_helper import fetch_safe
import urllib.parse

def get_active_league():
    data = fetch_safe("https://poe.ninja/api/data/getindexstate?game=poe2")
    
    # Dodajemy diagnostykę do logów Cloud Run
    print(f"DEBUG poe.ninja response: {data}")
    
    if data and 'economyLeagues' in data:
        for l in data['economyLeagues']:
            name = l.get('name', '')
            is_active = l.get('active', False)
            print(f"Liga: {name}, Aktywna: {is_active}")
            
            if is_active and 'SSF' not in name and 'HC' not in name:
                return name
                
    raise ValueError("BŁĄD: Nie udało się dynamicznie wykryć aktywnej ligi z API poe.ninja!")

def get_price(item_name):
    league = get_active_league()
    url = f"https://poe.ninja/api/data/currencyoverview?game=poe2&league={urllib.parse.quote(league)}&type=Currency"
    data = fetch_safe(url)
    
    if data and 'lines' in data:
        for line in data['lines']:
            if line.get('currencyTypeName', '').lower() == item_name.lower():
                return line.get('chaosEquivalent', 0), league
                
    return None, league
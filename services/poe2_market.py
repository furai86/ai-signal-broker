from utils.api_helper import fetch_safe
import urllib.parse

def get_active_league():
    """
    Dynamicznie pobiera listę lig z poe.ninja i wybiera aktywną (ni-SSF, ni-HC).
    Jeśli API zawiedzie, zwraca bezpieczny fallback 'Standard'.
    """
    url = "https://poe.ninja/api/data/getindexstate?game=poe2"
    data = fetch_safe(url)
    
    # Diagnostyka widoczna w logach Cloud Run
    print(f"DEBUG poe.ninja response: {data}")
    
    if data and isinstance(data, dict) and 'economyLeagues' in data:
        for l in data['economyLeagues']:
            name = l.get('name', '')
            is_active = l.get('active', False)
            
            # Warunek: liga musi być aktywna i nie może być SSF ani Hardcore
            if is_active and 'SSF' not in name and 'HC' not in name:
                return name
                
    # Fallback biznesowy gwarantujący, że zapytanie nigdy nie wybuchnie 500-tką
    return "Standard"

def get_price(item_name):
    """
    Pobiera cenę przedmiotu w Chaos Orbach dla dynamicznie wykrytej ligi.
    """
    league = get_active_league()
    url = f"https://poe.ninja/api/data/currencyoverview?game=poe2&league={urllib.parse.quote(league)}&type=Currency"
    data = fetch_safe(url)
    
    if data and isinstance(data, dict) and 'lines' in data:
        for line in data['lines']:
            if line.get('currencyTypeName', '').lower() == item_name.lower():
                return line.get('chaosEquivalent', 0), league
                
    return None, league
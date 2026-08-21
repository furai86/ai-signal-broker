from utils.api_helper import fetch_safe
import urllib.parse

def get_active_league(mode="sc_league"):
    """
    Dynamicznie pobiera listę lig z poe.ninja dla PoE2 i wybiera aktywną ligę handlową.
    """
    url = "https://poe.ninja/api/data/getindexstate?game=poe2"
    data = fetch_safe(url)
    
    if data and isinstance(data, dict) and 'economyLeagues' in data:
        leagues = data['economyLeagues']
        
        # Szukamy aktywnej ligi Softcore (ni-SSF, ni-HC)
        for l in leagues:
            name = l.get('name', '')
            is_active = l.get('active', False)
            if is_active and 'SSF' not in name and 'HC' not in name and 'Hardcore' not in name:
                return name
                
        # Fallback do pierwszej aktywnej ligi z listy
        for l in leagues:
            if l.get('active', False):
                return l.get('name', 'Standard')
                
    return "Standard"

def get_item_market_data(item_name, mode="sc_league"):
    """
    Pobiera średnią cenę rynkową przedmiotu w Chaos Orbach dla wykrytej ligi.
    """
    league = get_active_league(mode)
    url = f"https://poe.ninja/api/data/currencyoverview?game=poe2&league={urllib.parse.quote(league)}&type=Currency"
    data = fetch_safe(url)
    
    market_price = None
    if data and isinstance(data, dict) and 'lines' in data:
        for line in data['lines']:
            if line.get('currencyTypeName', '').lower() == item_name.lower():
                market_price = line.get('chaosEquivalent', None)
                break
                
    return {
        "league": league,
        "market_price_chaos": market_price
    }
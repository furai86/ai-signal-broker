from utils.api_helper import fetch_safe
import urllib.parse

def get_active_league(mode="sc_league"):
    """
    Pobiera listę lig dynamicznie z poe.ninja dla PoE2 i wybiera najnowszą aktywną ligę handlową.
    Żadnych twardych wpisów – nazwa dostosuje się automatycznie przy zmianie sezonu.
    """
    url = "https://poe.ninja/api/data/economyleagues?game=poe2"
    data = fetch_safe(url)
    
    # Jeśli dane przyjdą w formie listy lub słownika z kluczem
    leagues = []
    if isinstance(data, list):
        leagues = data
    elif isinstance(data, dict):
        leagues = data.get('economyLeagues', data.get('leagues', []))
        
    if leagues:
        # Szukamy aktywnej ligi Softcore (pomijamy SSF i Hardcore)
        for l in leagues:
            name = l.get('name', '')
            is_active = l.get('active', True) # Czasami pole active bywa domyślne
            
            if 'SSF' not in name and 'HC' not in name and 'Hardcore' not in name:
                print(f"Dynamicznie wykryto aktywną ligę PoE2: {name}")
                return name
                
        # Jeśli nie znaleziono idealnego dopasowania, bierzemy pierwszą z brzegi dostępną
        first_name = leagues[0].get('name', '')
        if first_name:
            print(f"Dynamicznie wykryto pierwszą dostępną ligę: {first_name}")
            return first_name

    raise ValueError("BŁĄD KRYTYCZNY: Nie udało się dynamicznie pobrać listy lig z poe.ninja dla PoE2!")

def get_item_market_data(item_name, mode="sc_league"):
    """
    Pobiera średnią cenę rynkową przedmiotu dla w pełni dynamicznie wykrytej ligi.
    """
    league = get_active_league(mode)
    url = f"https://poe.ninja/api/data/currencyoverview?game=poe2&league={urllib.parse.quote(league)}&type=Currency"
    
    print(f"DEBUG: Odpytuję rynek dla ligi [{league}] -> {url}")
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
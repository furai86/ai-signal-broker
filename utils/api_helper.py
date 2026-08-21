from curl_cffi import requests as tls_requests

def fetch_safe(url):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://poe.ninja/'
    }
    try:
        response = tls_requests.get(url, impersonate="chrome120", headers=headers, timeout=10)
        print(f"DEBUG: Status HTTP dla {url} -> {response.status_code}")
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"DEBUG: Zablokowano lub błąd! Treść: {response.text[:150]}")
            return None
    except Exception as e:
        print(f"DEBUG: Wyjątek podczas pobierania API: {str(e)}")
        return None
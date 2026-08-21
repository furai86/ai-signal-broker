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
        print(f"DEBUG: URL -> {url} | Status HTTP: {response.status_code}")
        
        if response.status_code == 200:
            try:
                return response.json()
            except Exception as json_err:
                # Jeśli Cloudflare zwróciło HTML zamiast JSON, zobaczysz to w logach Cloud Run!
                print(f"DEBUG BŁĄD JSON: Nie udało się sparsować odpowiedzi. Początek treści: {response.text[:200]}")
                return None
        else:
            print(f"DEBUG BŁĄD HTTP: Status {response.status_code}. Treść: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"DEBUG WYJĄTEK SIECIOWY: {str(e)}")
        return None
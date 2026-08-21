from curl_cffi import requests as tls_requests

def fetch_safe(url):
    headers = {'Accept': 'application/json', 'Referer': 'https://poe.ninja/'}
    try:
        response = tls_requests.get(url, impersonate="chrome120", headers=headers, timeout=10)
        return response.json() if response.status_code == 200 else None
    except:
        return None

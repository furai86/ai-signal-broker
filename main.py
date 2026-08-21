import functions_framework
from services import poe2_market
from utils.ai_engine import get_ai_response
import json

@functions_framework.http
def main_router(request):
    """
    Główny router API obsługujący zarówno żądania GET (query parameters), 
    jak i POST (JSON body).
    """
    # Pobieramy dane niezależnie od tego, czy przyszły w JSON-ie, czy w adresie URL (GET)
    request_json = request.get_json(silent=True)
    request_args = request.args.to_dict()
    
    # Łączymy słowniki (args mają pierwszeństwo lub odwrotnie, w zależności od potrzeb)
    data = {**request_args, **(request_json or {})}
    
    # Określamy usługę lub grę
    service = data.get('service', 'poe2').lower()
    game = data.get('game', 'POE2').upper()
    item_name = data.get('item_name', 'Divine Orb')
    
    if service == 'poe2' or game == 'POE2':
        try:
            price, league = poe2_market.get_price(item_name)
            
            prompt = (
                f"Asset: {item_name}, League: {league}, "
                f"Market Price (Chaos): {price if price is not None else 'Brak danych'}. "
                f"Daj krótką, precyzyjną analizę ekonomiczną oraz rekomendację w formacie JSON."
            )
            
            result = get_ai_response(prompt)
            return (result, 200, {'Content-Type': 'application/json'})
            
        except Exception as e:
            error_payload = {"error": str(e), "status": "failed"}
            return (json.dumps(error_payload), 500, {'Content-Type': 'application/json'})
    
    return (json.dumps({"error": "Service not found"}), 404, {'Content-Type': 'application/json'})

if __name__ == "__main__":
    from functions_framework import create_app
    app = create_app(target="main_router")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
import functions_framework
from services import poe2_market
from utils.ai_engine import get_ai_response
import json

@functions_framework.http
def main_router(request):
    data = request.get_json(silent=True) or request.args.to_dict()
    service = data.get('service', 'poe2')
    
    if service == 'poe2':
        item_name = data.get('item_name', 'Divine Orb')
        price, league = poe2_market.get_price(item_name)
        prompt = f"Asset: {item_name}, League: {league}, Market Price (Chaos): {price}. Daj krótką analizę i rekomendację w formacie JSON."
        result = get_ai_response(prompt)
        return (result, 200, {'Content-Type': 'application/json'})
    
    return (json.dumps({"error": "Service not found"}), 404, {'Content-Type': 'application/json'})

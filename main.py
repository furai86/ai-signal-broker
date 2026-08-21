import functions_framework
from services import poe2_market
from utils.ai_engine import get_ai_response
import json

@functions_framework.http
def main_router(request):
    """
    Główny router agenta PoE2 oceniający opłacalność oferty gracza względem rynku.
    """
    request_json = request.get_json(silent=True) or {}
    request_args = request.args.to_dict()
    data = {**request_args, **request_json}
    
    game = data.get('game', 'poe2').lower()
    mode = data.get('mode', 'sc_league')
    item_name = data.get('item_name', 'Divine Orb')
    
    try:
        client_price = float(data.get('current_price', 0))
    except (ValueError, TypeError):
        client_price = 0.0

    if game == 'poe2':
        try:
            # Pobieramy realne dane rynkowe i ligę
            market_data = poe2_market.get_item_market_data(item_name, mode)
            league = market_data["league"]
            market_price = market_data["market_price_chaos"]
            
            # Tworzymy inteligentny prompt dla Gemini 3.6 Flash
            prompt = (
                f"Jesteś ekspertem analitykiem rynkowym w grze Path of Exile 2 (PoE2).\n"
                f"Przedmiot: {item_name}\n"
                f"Aktualna dynamiczna liga: {league}\n"
                f"Średnia cena rynkowa z poe.ninja: {market_price if market_price is not None else 'Brak danych'} Chaos Orb.\n"
                f"Cena znaleziona przez gracza na giełdzie handlowej: {client_price} Chaos Orb.\n\n"
                f"Oceń, czy ta oferta jest opłacalna. Weź pod uwagę różnicę cenową, dynamikę rynku oraz cykl życia ligi.\n"
                f"Zwróć wynik WŁĄCZNIE w formacie JSON z polami:\n"
                f"- 'asset': nazwa przedmiotu,\n"
                f"- 'league': nazwa ligi,\n"
                f"- 'market_price_chaos': średnia rynkowa,\n"
                f"- 'client_price_chaos': cena gracza,\n"
                f"- 'verdict': (np. 'GOOD_DEAL', 'OVERPRICED', 'FAIR'),\n"
                f"- 'analysis': szczegółowa analiza ekonomiczna,\n"
                f"- 'recommendation': konkretna rekomendacja handlowa."
            )
            
            ai_result = get_ai_response(prompt)
            return (ai_result, 200, {'Content-Type': 'application/json'})
            
        except Exception as e:
            error_payload = {"error": str(e), "status": "failed"}
            return (json.dumps(error_payload), 500, {'Content-Type': 'application/json'})
            
    return (json.dumps({"error": "Service not found"}), 404, {'Content-Type': 'application/json'})
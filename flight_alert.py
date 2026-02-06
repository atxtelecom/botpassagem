import datetime
import time

import requests

API_KEY = "SUA_CHAVE_DA_API_DE_VOOS"
TELEGRAM_TOKEN = "SEU_TELEGRAM_TOKEN"
CHAT_ID = "SEU_CHAT_ID"
ORIGIN = "VCP"
DESTINATION = "PMG"
MAX_PRICE = 600


def send_telegram(msg):
    requests.get(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": msg},
    )


def search_flights(departure_date, return_date):
    url = "https://api.apidevoos.dev/v1/search"
    payload = {
        "origin": ORIGIN,
        "destination": DESTINATION,
        "departureDate": departure_date,
        "returnDate": return_date,
        "adults": 1,
    }
    headers = {"Authorization": f"Bearer {API_KEY}"}

    res = requests.post(url, json=payload, headers=headers)
    if res.status_code == 200:
        return res.json()
    return None


def main():
    start = datetime.date(2026, 2, 1)
    end = datetime.date(2026, 6, 30)

    delta = datetime.timedelta(days=1)

    while start <= end:
        for stay_days in range(5, 11):
            return_date = start + datetime.timedelta(days=stay_days)
            data = search_flights(start.isoformat(), return_date.isoformat())
            if not data:
                continue
            for offer in data.get("offers", []):
                price = float(offer.get("price", {}).get("total", 0))
                if price <= MAX_PRICE:
                    msg = (
                        "Passagem barata encontrada! R$ "
                        f"{price} de {ORIGIN} -> {DESTINATION} "
                        f"indo {start} e voltando {return_date}"
                    )
                    send_telegram(msg)
        start += delta
        time.sleep(1)  # evita limites de requisições


if __name__ == "__main__":
    main()

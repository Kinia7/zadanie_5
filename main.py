import asyncio
import aiohttp
from datetime import datetime, timedelta

API_URL = "https://api.nbp.pl/api/exchangerates/tables/A"
TODAY = datetime.today().strftime("%Y-%m-%d")

async def get_rates(date):
    """Pobiera wszystkie kursy wymiany dla danego dnia."""
    url = f"{API_URL}/{date}/?format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            elif response.status == 404:
                print(f"Brak danych dla dnia {date}")
                return None  
            else:
                raise RuntimeError(f"Błąd pobierania danych: {response.status}")

async def main(days):
    """Pobiera kursy wymiany dla kilku dni."""
    currencies = ['EUR', 'USD']
    tasks = [get_rates((datetime.strptime(TODAY, "%Y-%m-%d") - timedelta(days=i)).strftime("%Y-%m-%d")) for i in range(days)]
    results = await asyncio.gather(*tasks)
    
    for i, result in enumerate(results):
        date = (datetime.strptime(TODAY, "%Y-%m-%d") - timedelta(days=i)).strftime("%Y-%m-%d")
        print(f"Dane z dnia {date}:")
        if result:
            rates = result[0]["rates"]
            for currency in currencies:
                rate_info = next((rate for rate in rates if rate['code'] == currency), None)
                if rate_info:
                    print(f"{rate_info['code']}: {rate_info['mid']:.4f}")
                else:
                    print(f"Brak danych dla {currency}")
        else:
            print("Brak danych")
        print()

if __name__ == "__main__":
    try:
        days = int(input("Podaj liczbę dni (maksymalnie 10): "))
        if days > 10:
            raise ValueError("Liczba dni nie może być większa niż 10")
    except ValueError as e:
        print(f"Błąd: {e}")
    else:
        asyncio.run(main(days))

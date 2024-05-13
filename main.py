import asyncio
import aiohttp
from datetime import datetime, timedelta

API_URL = "https://api.nbp.pl/api/exchangerates/tables/a/"
TODAY = datetime.today().strftime("%Y-%m-%d")

async def get_rates(currency, date):
    """Pobiera kursy wymiany dla danego dnia i waluty."""
    url = f"{API_URL}{currency}/{date}?format=json"
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
    """Pobiera kursy wymiany dla kilku dni i walut."""
    currencies = ['EUR', 'USD']
    for currency in currencies:
        print(f"Kursy wymiany dla waluty: {currency}")
        tasks = [get_rates(currency, (datetime.strptime(TODAY, "%Y-%m-%d") - timedelta(days=i)).strftime("%Y-%m-%d")) for i in range(days)]
        results = await asyncio.gather(*tasks)
        for i, result in enumerate(results, 1):
            print(f"Dane z dnia {datetime.strptime(TODAY, '%Y-%m-%d') - timedelta(days=i)}:")
            if result is not None:  
                for currency_data in result[0]["rates"]:
                    if currency_data['code'] == currency:
                        print(f"{currency_data['code']:3} {currency_data['mid']:.4f}")
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

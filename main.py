# main.py - Core logic for the currency converter bot

import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load the .env file from the script's directory
# This is a robust way to ensure the .env file is found
dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

API_KEY = os.getenv("EXCHANGERATE_API_KEY")
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}"

def get_exchange_rate(base_currency, target_currency):
    """
    Fetches the real-time exchange rate from ExchangeRate-API.com.
    """
    if not API_KEY:
        print("Error: API key is not configured.")
        return None

    url = f"{BASE_URL}/pair/{base_currency}/{target_currency}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        
        if data.get("result") == "success":
            return data.get("conversion_rate")
        else:
            print(f"Error from API: {data.get('error-type')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    print("Currency Converter Bot Engine")
    
    if API_KEY:
        base = "USD"
        target = "MYR"
        print(f"Fetching latest rate for {base} to {target}...")
        
        rate = get_exchange_rate(base, target)
        
        if rate:
            amount = 100
            converted_amount = amount * rate
            print(f"{amount} {base} is equal to {converted_amount:.2f} {target}")
    else:
        print("Could not run test because API key is missing.")

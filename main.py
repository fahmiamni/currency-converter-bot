# main.py - Core logic for the currency converter bot

import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load the .env file from the script's directory
dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

API_KEY = os.getenv("EXCHANGERATE_API_KEY")
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}"

def get_exchange_rate(base_currency, target_currency):
    """
    Fetches the real-time exchange rate for a single pair.
    """
    if not API_KEY:
        print("Error: API key is not configured.")
        return None
    url = f"{BASE_URL}/pair/{base_currency}/{target_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("result") == "success":
            return data.get("conversion_rate")
        else:
            print(f"Error from API: {data.get('error-type')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_all_rates(base_currency="USD"):
    """
    Fetches all exchange rates for a given base currency.
    This is much more efficient for the UI.
    """
    if not API_KEY:
        print("Error: API key is not configured.")
        return None
    url = f"{BASE_URL}/latest/{base_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("result") == "success":
            return data.get("conversion_rates")
        else:
            print(f"Error from API: {data.get('error-type')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    print("--- Currency Converter Bot Engine Test ---")
    
    if API_KEY:
        # --- New Test for the UI ---
        print("\\nTesting the new get_all_rates function...")
        base = "MYR"
        print(f"Fetching all rates with {base} as the base currency...")
        all_rates = get_all_rates(base)
        
        if all_rates:
            # Display a few examples based on the app screenshot
            print(f"\\n--- Example Conversions for 1 {base} ---")
            print(f"QAR: {all_rates.get('QAR')}")
            print(f"IQD: {all_rates.get('IQD')}")
            print(f"KWD: {all_rates.get('KWD')}")
            print(f"USD: {all_rates.get('USD')}")
    else:
        print("Could not run test because API key is missing.")

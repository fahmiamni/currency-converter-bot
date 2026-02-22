# main.py - Core logic for the currency converter bot

import requests
import os
from dotenv import load_dotenv
from pathlib import Path

print("--- Starting Debug ---")

# 1. Check if the .env file exists where we think it does
dotenv_path = Path('.') / '.env'
print(f"Looking for .env file at: {dotenv_path.resolve()}")
print(f"Does .env file exist? -> {dotenv_path.exists()}")

# 2. Try to load the .env file and see if it was successful
was_loaded = load_dotenv(dotenv_path=dotenv_path)
print(f"Was .env file loaded successfully? -> {was_loaded}")

# 3. Check what value is actually being loaded into the API_KEY variable
API_KEY = os.getenv("EXCHANGERATE_API_KEY")
print(f"Value of API_KEY after loading: -> '{API_KEY}'")

print("--- End Debug ---")

# The rest of the original code
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}"

def get_exchange_rate(base_currency, target_currency):
    if not API_KEY:
        print("\nError: API key is still not configured.")
        return None
    
    # ... (rest of the function is the same, no need to change)
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

if __name__ == "__main__":
    print("\nCurrency Converter Bot Engine")
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
        print("\nCould not run test because API key is missing.")


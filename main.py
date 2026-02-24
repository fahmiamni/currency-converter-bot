# main.py - Core logic for the currency converter bot

import requests
import os

# Your API key will be stored in an environment variable for security
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
    
    # --- Instructions for User ---
    # 1. Sign up for a free API key at https://www.exchangerate-api.com
    # 2. Set the environment variable like this in your terminal before running:
    #    export EXCHANGERATE_API_KEY='your_api_key_here'
    
    # --- Example Usage ---
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
        print("\\nPlease configure your API key to run a test.")


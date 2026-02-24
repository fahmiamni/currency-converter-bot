# Currency Converter Bot

A simple Python-based currency converter bot that utilizes the [ExchangeRate-API](https://www.exchangerate-api.com) to fetch real-time exchange rates. This tool allows users to convert amounts between different currencies easily.

## Features

- **Real-time Exchange Rates:** Fetches up-to-date currency conversion rates.
- **Simple Usage:** Easy-to-understand Python script for quick integration.
- **Secure API Key Handling:** Uses environment variables to keep your API key safe.

## Prerequisites

Before running the bot, ensure you have the following installed:

- Python 3.x
- `requests` library

You can install the required library using pip:

```bash
pip install requests
```

## Setup

1.  **Get an API Key:**
    Sign up for a free API key at [ExchangeRate-API.com](https://www.exchangerate-api.com).

2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/currency-converter-bot.git
    cd currency-converter-bot
    ```

3.  **Configure Environment Variable:**
    Set your API key as an environment variable.

    **On Linux/macOS:**
    ```bash
    export EXCHANGERATE_API_KEY='your_api_key_here'
    ```

    **On Windows (Command Prompt):**
    ```cmd
    set EXCHANGERATE_API_KEY=your_api_key_here
    ```

    **On Windows (PowerShell):**
    ```powershell
    $env:EXCHANGERATE_API_KEY="your_api_key_here"
    ```

## Usage

Run the script directly from your terminal:

```bash
python main.py
```

### Example Output

If configured correctly, you should see output similar to this:

```text
Currency Converter Bot Engine
Fetching latest rate for USD to MYR...
100 USD is equal to 475.50 MYR
```

## Code Overview

The core logic resides in `main.py`:

-   `get_exchange_rate(base_currency, target_currency)`: Fetches the conversion rate for a given pair.
-   The script checks for the `EXCHANGERATE_API_KEY` environment variable.
-   It demonstrates a sample conversion (e.g., 100 USD to MYR).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open-source and available under the [MIT License](LICENSE).

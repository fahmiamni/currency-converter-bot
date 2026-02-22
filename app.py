# app.py - The main file for our Kivy user interface

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import mainthread, Clock
from functools import partial

# Import our currency conversion engine
from main import get_all_rates

# A custom widget for our currency rows to keep the code clean
class CurrencyRow(BoxLayout):
    def __init__(self, currency_code, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.currency_code = currency_code

        self.add_widget(Label(text=currency_code, size_hint_x=0.2, font_size=20))
        self.amount_input = TextInput(
            text='0.00',
            font_size=24,
            multiline=False,
            halign='right',
            input_filter='float' # Only allow numbers and a decimal point
        )
        self.add_widget(self.amount_input)


class CurrencyApp(App):
    def build(self):
        # --- UI Layout ---
        self.title = 'Currency Converter'
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # The list of currencies we want to display in our app
        self.display_currencies = ['MYR', 'QAR', 'IQD', 'KWD', 'USD', 'EUR']
        
        # This dictionary will hold our custom row widgets
        self.currency_rows = {}

        # Create and add a row for each currency
        for currency in self.display_currencies:
            row = CurrencyRow(currency_code=currency)
            # When text is entered, call the on_amount_changed function
            row.amount_input.bind(text=partial(self.on_amount_changed, row))
            self.currency_rows[currency] = row
            self.main_layout.add_widget(row)

        return self.main_layout

    def on_start(self):
        # --- Data & Logic ---
        self.rates = {}  # This will store all rates relative to USD
        self._is_updating = False # A flag to prevent infinite update loops
        Clock.schedule_once(self.fetch_initial_rates)

    def fetch_initial_rates(self, *args):
        # Fetch all rates with USD as the universal base currency
        print("Fetching initial rates from API...")
        self.rates = get_all_rates("USD")
        if self.rates:
            print("Rates fetched successfully.")
            # Set an initial value to start with (e.g., 1 USD)
            self.update_all_rows(1.0, "USD")
        else:
            print("Failed to fetch rates. Check API key and connection.")
            for row in self.currency_rows.values():
                row.amount_input.text = "Error"

    def on_amount_changed(self, source_row, instance, new_text):
        # This is the core logic that runs when you type in any box
        if self._is_updating or not self.rates or not new_text:
            return

        try:
            amount_in_source_currency = float(new_text)
        except ValueError:
            return

        source_code = source_row.currency_code
        
        # 1. Convert the input amount back to our universal base (USD)
        rate_to_usd = 1 / self.rates.get(source_code, 1)
        amount_in_usd = amount_in_source_currency * rate_to_usd

        # 2. Update all other rows based on the new USD amount
        self.update_all_rows(amount_in_usd, source_code)

    @mainthread
    def update_all_rows(self, amount_in_usd, source_code_to_skip):
        # This function updates the text in all the boxes
        self._is_updating = True # Set the flag to prevent loops
        
        for code, row in self.currency_rows.items():
            if code == source_code_to_skip:
                continue # Don't update the box the user is currently typing in
            
            rate_from_usd = self.rates.get(code, 0)
            converted_amount = amount_in_usd * rate_from_usd
            row.amount_input.text = f'{converted_amount:,.2f}'

        self._is_updating = False # Unset the flag

if __name__ == '__main__':
    CurrencyApp().run()

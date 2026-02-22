# app.py - The main file for our Kivy user interface

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.clock import Clock
from functools import partial
import os

# Import our currency conversion engine
from main import get_all_rates

# A custom widget for our currency rows to keep the code clean
class CurrencyRow(BoxLayout):
    def __init__(self, currency_code, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 15
        self.size_hint_y = None
        self.height = 48 # Set a fixed height for each row
        self.currency_code = currency_code

        # --- Flag Image ---
        # Construct the path to the flag image.
        # Note: We use the first two letters of the currency code. 
        # For EUR, we need a special case.
        country_code = "EU" if currency_code == "EUR" else currency_code[:2]
        flag_path = f"images/{country_code}.png"
        
        if os.path.exists(flag_path):
            self.add_widget(Image(source=flag_path, size_hint_x=None, width=40))
        else:
            self.add_widget(Label(text="?", size_hint_x=None, width=40)) # Placeholder if no flag

        # --- Currency Code Label ---
        self.add_widget(Label(text=currency_code, size_hint_x=0.3, font_size=20))
        
        # --- Amount Input Box ---
        self.amount_input = TextInput(
            text='0.00',
            font_size=24,
            multiline=False,
            halign='right',
            input_filter='float'
        )
        self.add_widget(self.amount_input)


class CurrencyApp(App):
    def build(self):
        self.title = 'Currency Converter'
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.display_currencies = ['MYR', 'QAR', 'IQD', 'KWD', 'USD', 'EUR']
        self.currency_rows = {}

        for currency in self.display_currencies:
            row = CurrencyRow(currency_code=currency)
            row.amount_input.bind(on_text_validate=partial(self.on_amount_changed, row),
                                  focus=partial(self.on_focus, row))
            self.currency_rows[currency] = row
            self.main_layout.add_widget(row)

        return self.main_layout

    def on_start(self):
        self.rates = {}
        self._is_updating = False
        Clock.schedule_once(self.fetch_initial_rates)

    def fetch_initial_rates(self, *args):
        print("Fetching initial rates from API...")
        self.rates = get_all_rates("USD")
        if self.rates:
            print("Rates fetched successfully.")
            self.update_all_rows(1.0, "USD") # Start with 1 USD as the base
        else:
            print("Failed to fetch rates. Check API key and connection.")
            for row in self.currency_rows.values():
                row.amount_input.text = "Error"

    def on_focus(self, source_row, instance, is_focused):
        # When a user clicks into a text box, we'll re-calculate based on its value
        if is_focused:
            self.on_amount_changed(source_row, instance)

    def on_amount_changed(self, source_row, instance):
        if self._is_updating or not self.rates or not instance.text:
            return

        try:
            amount_in_source_currency = float(instance.text)
        except ValueError:
            return

        source_code = source_row.currency_code
        
        # Convert the input amount back to our universal base (USD)
        rate_to_usd = 1 / self.rates.get(source_code, 1)
        amount_in_usd = amount_in_source_currency * rate_to_usd

        # Update all other rows based on the new USD amount
        self.update_all_rows(amount_in_usd, source_code)

    def update_all_rows(self, amount_in_usd, source_code_to_skip):
        self._is_updating = True
        
        for code, row in self.currency_rows.items():
            if code == source_code_to_skip:
                continue
            
            rate_from_usd = self.rates.get(code, 0)
            converted_amount = amount_in_usd * rate_from_usd
            row.amount_input.text = f'{converted_amount:.2f}'

        self._is_updating = False

if __name__ == '__main__':
    CurrencyApp().run()

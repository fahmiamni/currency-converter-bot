# app.py - The main file for our Kivy user interface

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import mainthread

# Import our currency conversion engine
from main import get_all_rates

class CurrencyApp(App):
    def build(self):
        # --- UI Layout ---
        self.title = 'Currency Converter'
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Let's set our base currency and the list of currencies we want to display
        self.base_currency = 'IQD' # This is the currency of the main input box
        self.display_currencies = ['MYR', 'QAR', 'KWD', 'USD']
        
        # This dictionary will hold our label widgets so we can update them easily
        self.result_labels = {}

        # The main input display
        self.main_input = TextInput(
            text='50000', 
            font_size=32, 
            multiline=False, 
            halign='right'
        )
        # Binds the update_results function to be called whenever the text changes
        self.main_input.bind(text=self.update_results)
        
        main_layout.add_widget(Label(text=f'Base Currency: {self.base_currency}', size_hint_y=0.1))
        main_layout.add_widget(self.main_input)

        # Create labels for each currency we want to display
        for currency in self.display_currencies:
            label = Label(text=f'{currency}: ...', font_size=20)
            self.result_labels[currency] = label
            main_layout.add_widget(label)

        return main_layout

    def on_start(self):
        # This function runs when the app starts
        print("App started! Fetching initial currency rates...")
        self.rates = get_all_rates(self.base_currency)
        if self.rates:
            print("Rates fetched successfully.")
            # Update the display with the initial value
            self.update_results(self.main_input)
        else:
            print("Failed to fetch rates. Check your API key and connection.")

    @mainthread
    def update_results(self, instance, *args):
        # This function is called whenever the text in the main_input box changes
        if not self.rates:
            return # Don't do anything if we don't have the rates

        try:
            # Get the number from the input box
            base_amount = float(instance.text)
        except ValueError:
            # If the user types something that isn't a number, do nothing
            base_amount = 0.0

        # Loop through our display currencies and update their labels
        for currency in self.display_currencies:
            rate = self.rates.get(currency, 0)
            converted_amount = base_amount * rate
            self.result_labels[currency].text = f'{currency}: {converted_amount:,.2f}'

if __name__ == '__main__':
    CurrencyApp().run()

# app.py - The main file for our Kivy user interface

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class CurrencyApp(App):
    def build(self):
        # The main layout will be a vertical box
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Let's create a placeholder for the main input display
        # This will be like the 'IQD' row in your screenshot
        self.main_input = TextInput(
            text='50000', 
            font_size=32, 
            multiline=False, 
            halign='right'
        )
        main_layout.add_widget(self.main_input)

        # Add a few labels to represent the other currencies
        # We will make these dynamic later
        main_layout.add_widget(Label(text='MYR: (result will show here)'))
        main_layout.add_widget(Label(text='QAR: (result will show here)'))
        main_layout.add_widget(Label(text='KWD: (result will show here)'))

        return main_layout

if __name__ == '__main__':
    CurrencyApp().run()

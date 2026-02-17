from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)

class ExpenseApp(App):

    def build(self):
        self.expenses = []

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Inputs
        self.amount_input = TextInput(
            hint_text="Amount",
            multiline=False,
            input_filter="float",
            size_hint=(1, None),
            height=50
        )

        self.category_input = TextInput(
            hint_text="Category",
            multiline=False,
            size_hint=(1, None),
            height=50
        )

        self.desc_input = TextInput(
            hint_text="Description",
            multiline=False,
            size_hint=(1, None),
            height=50
        )

        add_btn = Button(
            text="Add Expense",
            size_hint=(1, None),
            height=50,
            background_color=(0, 0.5, 1, 1)
        )
        add_btn.bind(on_press=self.add_expense)

        # Scroll area
        self.scroll = ScrollView()
        self.expense_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.expense_layout.bind(minimum_height=self.expense_layout.setter('height'))
        self.scroll.add_widget(self.expense_layout)

        main_layout.add_widget(self.amount_input)
        main_layout.add_widget(self.category_input)
        main_layout.add_widget(self.desc_input)
        main_layout.add_widget(add_btn)
        main_layout.add_widget(self.scroll)

        self.load_data()

        return main_layout

    def add_expense(self, instance):
        amount = self.amount_input.text.strip()
        category = self.category_input.text.strip()
        desc = self.desc_input.text.strip()

        if not amount or not category or not desc:
            return

        expense_line = f"{amount},{category},{desc}"
        self.expenses.append(expense_line)

        with open("expenses.txt", "a") as f:
            f.write(expense_line + "\n")

        self.display_expense(amount, category, desc)

        self.amount_input.text = ""
        self.category_input.text = ""
        self.desc_input.text = ""

    def display_expense(self, amount, category, desc):
        label = Label(
            text=f"₹{amount} | {category} | {desc}",
            size_hint_y=None,
            height=40,
            color=(0, 0, 0, 1)
        )
        self.expense_layout.add_widget(label)

    def load_data(self):
        try:
            with open("expenses.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(",")

                    # SAFE CHECK (prevents crash)
                    if len(parts) == 3:
                        amount, category, desc = parts
                        self.display_expense(amount, category, desc)

        except FileNotFoundError:
            pass


if __name__ == "__main__":
    ExpenseApp().run()
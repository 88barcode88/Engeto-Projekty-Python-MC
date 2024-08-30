import json
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout

class TaskButton(RelativeLayout):
    def __init__(self, text, priority, category, due_date, edit_callback, delete_callback, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 50
        self.priority = priority
        self.category = category
        self.due_date = due_date

        self.main_button = Button(text=text, background_color=self.get_color_for_priority(priority))
        self.main_button.bind(on_press=edit_callback)
        self.add_widget(self.main_button)

        self.delete_button = Button(text='X', size_hint=(None, None), size=(25, 25), 
                                    pos_hint={'right': 0.98, 'top': 0.9}, background_color=[0, 0, 0, 1])
        self.delete_button.bind(on_press=delete_callback)
        self.add_widget(self.delete_button)

        self.due_date_label = Label(text=self.format_due_date(), font_size='10sp', size_hint=(None, None), 
                                    size=(150, 20), pos_hint={'right': 0.98, 'top': 0.4})
        self.add_widget(self.due_date_label)

    def get_color_for_priority(self, priority):
        return {
            'Vysoká': [1, 0, 0, 1],
            'Střední': [1, 0.65, 0, 1],
            'Nízká': [0, 1, 0, 1]
        }.get(priority, [0, 0, 1, 1])

    def format_due_date(self):
        if self.due_date:
            return f"Do: {self.due_date}"
        return ""

class EditPopup(Popup):
    def __init__(self, task_button, save_callback, categories, **kwargs):
        super().__init__(**kwargs)
        self.task_button = task_button
        self.save_callback = save_callback
        self.title = 'Upravit úkol'
        self.size_hint = (0.9, 0.9)

        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.task_input = TextInput(text=task_button.main_button.text, multiline=False)
        content.add_widget(self.task_input)

        self.priority_spinner = Spinner(text=task_button.priority, values=('Vysoká', 'Střední', 'Nízká'))
        content.add_widget(self.priority_spinner)

        self.category_spinner = Spinner(text=task_button.category, values=categories)
        content.add_widget(self.category_spinner)

        self.due_date_input = TextInput(text=task_button.due_date or '', hint_text='DD.MM.YYYY HH:MM', multiline=False)
        content.add_widget(self.due_date_input)

        save_button = Button(text='Uložit', size_hint_y=None, height=40)
        save_button.bind(on_press=self.save_task)
        content.add_widget(save_button)

        self.content = content

    def save_task(self, instance):
        new_text = self.task_input.text
        new_priority = self.priority_spinner.text
        new_category = self.category_spinner.text
        new_due_date = self.due_date_input.text

        self.save_callback(self.task_button, new_text, new_priority, new_category, new_due_date)
        self.dismiss()

class OrganizerLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.categories = ['Práce', 'Osobní', 'Nákupy', 'Jiné']
        self.tasks = []

        self.header = Label(text='Můj Organizér', font_size=24, bold=True, size_hint_y=None, height=40)
        self.add_widget(self.header)

        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.task_input = TextInput(multiline=False, hint_text='Zadejte nový úkol', size_hint_x=0.4)
        input_layout.add_widget(self.task_input)

        self.priority_spinner = Spinner(text='Střední', values=('Vysoká', 'Střední', 'Nízká'), size_hint_x=0.2)
        input_layout.add_widget(self.priority_spinner)

        self.category_spinner = Spinner(text='Práce', values=self.categories, size_hint_x=0.2)
        input_layout.add_widget(self.category_spinner)

        self.due_date_input = TextInput(multiline=False, hint_text='DD.MM.YYYY HH:MM', size_hint_x=0.2)
        input_layout.add_widget(self.due_date_input)

        self.add_widget(input_layout)

        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        add_button = Button(text='Přidat úkol', size_hint_x=0.25)
        add_button.bind(on_press=self.add_task)
        button_layout.add_widget(add_button)

        self.sort_spinner = Spinner(text='Bez řazení', values=('Bez řazení', 'Podle priority', 'Podle data'), size_hint_x=0.25)
        self.sort_spinner.bind(text=self.on_sort_change)
        button_layout.add_widget(self.sort_spinner)

        self.filter_spinner = Spinner(text='Všechny kategorie', values=['Všechny kategorie'] + self.categories, size_hint_x=0.25)
        self.filter_spinner.bind(text=self.on_filter_change)
        button_layout.add_widget(self.filter_spinner)

        help_button = Button(text='?', size_hint_x=0.25)
        help_button.bind(on_press=self.show_help)
        button_layout.add_widget(help_button)

        self.add_widget(button_layout)

        self.tasks_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(self.tasks_layout)
        self.add_widget(scroll_view)

        self.load_tasks()

    def add_task(self, instance):
        task = self.task_input.text.strip()
        priority = self.priority_spinner.text
        category = self.category_spinner.text
        due_date = self.due_date_input.text.strip()
        if task:
            task_button = TaskButton(text=task, priority=priority, category=category, due_date=due_date,
                                     edit_callback=self.edit_task, delete_callback=self.delete_task)
            self.tasks.append(task_button)
            self.tasks_layout.add_widget(task_button)
            self.task_input.text = ''
            self.due_date_input.text = ''
            self.save_tasks()

    def edit_task(self, instance):
        for task in self.tasks:
            if task.main_button == instance:
                popup = EditPopup(task, self.save_edited_task, self.categories)
                popup.open()
                break

    def save_edited_task(self, task_button, new_text, new_priority, new_category, new_due_date):
        task_button.main_button.text = new_text
        task_button.priority = new_priority
        task_button.category = new_category
        task_button.due_date = new_due_date
        task_button.main_button.background_color = task_button.get_color_for_priority(new_priority)
        task_button.due_date_label.text = task_button.format_due_date()
        self.save_tasks()

    def delete_task(self, instance):
        for task in self.tasks:
            if task.delete_button == instance:
                self.tasks_layout.remove_widget(task)
                self.tasks.remove(task)
                break
        self.save_tasks()

    def save_tasks(self):
        tasks_data = [{'text': task.main_button.text, 'priority': task.priority, 
                       'category': task.category, 'due_date': task.due_date} 
                      for task in self.tasks]
        with open('tasks.json', 'w') as f:
            json.dump(tasks_data, f)

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as f:
                tasks_data = json.load(f)
            for task_data in tasks_data:
                task_button = TaskButton(text=task_data['text'], priority=task_data['priority'],
                                         category=task_data['category'], due_date=task_data['due_date'],
                                         edit_callback=self.edit_task, delete_callback=self.delete_task)
                self.tasks.append(task_button)
                self.tasks_layout.add_widget(task_button)
        except FileNotFoundError:
            pass

    def on_sort_change(self, spinner, text):
        if text == 'Podle priority':
            self.tasks.sort(key=lambda x: {'Vysoká': 0, 'Střední': 1, 'Nízká': 2}[x.priority])
        elif text == 'Podle data':
            self.tasks.sort(key=lambda x: x.due_date or '9999-99-99')
        self.update_task_layout()

    def on_filter_change(self, spinner, text):
        self.update_task_layout()

    def update_task_layout(self):
        self.tasks_layout.clear_widgets()
        for task in self.tasks:
            if self.filter_spinner.text == 'Všechny kategorie' or task.category == self.filter_spinner.text:
                self.tasks_layout.add_widget(task)

    def show_help(self, instance):
        help_text = """
Vítejte v aplikaci Organizér!

Přidání úkolu:
1. Zadejte text úkolu do pole "Zadejte nový úkol"
2. Vyberte prioritu a kategorii
3. Volitelně zadejte datum a čas splnění ve formátu DD.MM.YYYY HH:MM
4. Klikněte na "Přidat úkol"

Úprava úkolu:
- Klikněte na úkol pro jeho úpravu

Smazání úkolu:
- Klikněte na "X" v pravém horním rohu úkolu

Řazení úkolů:
- Použijte rozbalovací menu "Bez řazení" pro řazení podle priority nebo data

Filtrování úkolů:
- Použijte rozbalovací menu "Všechny kategorie" pro filtrování podle kategorie

Barvy priorit:
Červená - Vysoká priorita
Oranžová - Střední priorita
Zelená - Nízká priorita

Datum splnění (pokud je nastaveno) je zobrazeno pod tlačítkem pro smazání každého úkolu.
        """
        popup = Popup(title='Nápověda',
                      content=Label(text=help_text),
                      size_hint=(0.9, 0.9))
        popup.open()

class OrganizerApp(App):
    def build(self):
        return OrganizerLayout()

if __name__ == '__main__':
    OrganizerApp().run()

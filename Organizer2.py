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
from kivy.uix.checkbox import CheckBox

class TaskButton(RelativeLayout):
    def __init__(self, text, priority, category, due_date, edit_callback, delete_callback, date_added=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 50
        self.priority = priority
        self.category = category
        self.due_date = due_date
        self.date_added = date_added or datetime.now().isoformat()

        # Hlavní tlačítko s textem úkolu
        self.main_button = Button(text=text, background_color=self.get_color_for_priority(priority))
        self.main_button.bind(on_press=edit_callback)
        self.add_widget(self.main_button)

        # Label s datem splnění
        self.due_date_label = Label(text=self.format_due_date(), font_size='10sp', size_hint=(None, None), 
                                    size=(150, 20), pos_hint={'right': 1, 'top': 1})
        self.add_widget(self.due_date_label)

        # Label s datem a časem vytvoření
        create_date = datetime.fromisoformat(self.date_added).strftime("%d.%m.%Y %H:%M")
        self.create_date_label = Label(text=create_date, font_size='10sp', size_hint=(None, None), 
                                       size=(150, 20), pos_hint={'right': 1, 'y': 0})
        self.add_widget(self.create_date_label)

        # Tlačítko pro smazání
        delete_button = Button(text='X', size_hint=(None, None), size=(30, 30), 
                               pos_hint={'left': 1, 'top': 1}, background_color=[0, 0, 0, 1],
                               color=[1, 1, 1, 1])
        delete_button.bind(on_release=delete_callback)
        self.add_widget(delete_button)

    def get_color_for_priority(self, priority):
        return {
            'Vysoká': [1, 0, 0, 1],
            'Střední': [1, 0.65, 0, 1],
            'Nízká': [0, 1, 0, 1]
        }.get(priority, [0, 0, 1, 1])

    def format_due_date(self):
        if self.due_date:
            try:
                due_date = datetime.fromisoformat(self.due_date)
                if due_date.hour == 0 and due_date.minute == 0:
                    return f"Do: {due_date.strftime('%d.%m.%Y')}"
                else:
                    return f"Do: {due_date.strftime('%d.%m.%Y %H:%M')}"
            except ValueError:
                return "Neplatné datum"
        return ""

class EditPopup(Popup):
    def __init__(self, task_button, save_callback, categories, **kwargs):
        super().__init__(**kwargs)
        self.task_button = task_button
        self.save_callback = save_callback
        self.title = 'Upravit úkol'
        self.size_hint = (0.9, 0.7)

        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.task_input = TextInput(text=task_button.main_button.text, multiline=False)
        content.add_widget(self.task_input)

        self.priority_spinner = Spinner(text=task_button.priority, values=('Vysoká', 'Střední', 'Nízká'))
        content.add_widget(self.priority_spinner)

        self.category_spinner = Spinner(text=task_button.category, values=categories)
        content.add_widget(self.category_spinner)

        due_date_layout = BoxLayout(orientation='horizontal')
        self.due_date_input = TextInput(hint_text='Datum splnění (DD.MM.YYYY)', multiline=False)
        due_date_layout.add_widget(self.due_date_input)
        self.due_time_input = TextInput(hint_text='Čas (HH:MM)', multiline=False)
        due_date_layout.add_widget(self.due_time_input)
        content.add_widget(due_date_layout)

        if task_button.due_date:
            due_date = datetime.fromisoformat(task_button.due_date)
            self.due_date_input.text = due_date.strftime('%d.%m.%Y')
            if due_date.hour != 0 or due_date.minute != 0:
                self.due_time_input.text = due_date.strftime('%H:%M')

        save_button = Button(text='Uložit', size_hint_y=None, height=40)
        save_button.bind(on_press=self.save_task)
        content.add_widget(save_button)

        self.content = content

    def save_task(self, instance):
        new_text = self.task_input.text
        new_priority = self.priority_spinner.text
        new_category = self.category_spinner.text
        
        new_due_date = None
        if self.due_date_input.text:
            try:
                new_due_date = datetime.strptime(self.due_date_input.text, '%d.%m.%Y')
                if self.due_time_input.text:
                    time = datetime.strptime(self.due_time_input.text, '%H:%M')
                    new_due_date = new_due_date.replace(hour=time.hour, minute=time.minute)
                new_due_date = new_due_date.isoformat()
            except ValueError:
                print("Neplatné datum nebo čas")

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

        self.due_date_input = TextInput(multiline=False, hint_text='Datum splnění', size_hint_x=0.2)
        input_layout.add_widget(self.due_date_input)

        self.add_widget(input_layout)

        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        add_button = Button(text='Přidat úkol', size_hint_x=0.25)
        add_button.bind(on_press=self.add_task)
        button_layout.add_widget(add_button)

        self.sort_spinner = Spinner(text='Bez řazení', values=('Bez řazení', 'Podle priority', 'Podle data vytvoření', 'Podle data splnění'), size_hint_x=0.25)
        self.sort_spinner.bind(text=self.on_sort_change)
        button_layout.add_widget(self.sort_spinner)

        self.filter_spinner = Spinner(text='Všechny kategorie', values=['Všechny kategorie'] + self.categories, size_hint_x=0.25)
        self.filter_spinner.bind(text=self.on_filter_change)
        button_layout.add_widget(self.filter_spinner)

        help_button = Button(text='?', size_hint_x=0.1)
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
        due_date = None
        if self.due_date_input.text:
            try:
                due_date = datetime.strptime(self.due_date_input.text, '%d.%m.%Y')
                due_date = due_date.isoformat()
            except ValueError:
                print("Neplatné datum")
        if task:
            task_button = TaskButton(text=task, priority=priority, category=category, due_date=due_date,
                                     edit_callback=self.edit_task, 
                                     delete_callback=self.delete_task)
            self.tasks.append(task_button)
            self.task_input.text = ''
            self.due_date_input.text = ''
            self.apply_filter_and_sort()
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
        self.apply_filter_and_sort()
        self.save_tasks()

    def delete_task(self, instance):
        for task in self.tasks:
            if task.children[0] == instance:
                self.tasks.remove(task)
                break
        self.apply_filter_and_sort()
        self.save_tasks()

    def save_tasks(self):
        tasks_data = [{'text': task.main_button.text, 
                       'priority': task.priority, 
                       'category': task.category,
                       'due_date': task.due_date,
                       'date_added': task.date_added} 
                      for task in self.tasks]
        with open('tasks.json', 'w') as f:
            json.dump(tasks_data, f)

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as f:
                tasks_data = json.load(f)
            
            if isinstance(tasks_data, list):
                for task_data in tasks_data:
                    if isinstance(task_data, dict) and all(key in task_data for key in ['text', 'priority', 'category']):
                        task_button = TaskButton(text=task_data['text'], 
                                                 priority=task_data['priority'],
                                                 category=task_data['category'],
                                                 due_date=task_data.get('due_date'),
                                                 edit_callback=self.edit_task,
                                                 delete_callback=self.delete_task, 
                                                 date_added=task_data.get('date_added'))
                        self.tasks.append(task_button)
                self.apply_filter_and_sort()
            else:
                print("Načtená data nejsou ve formátu seznamu.")
        except FileNotFoundError:
            print("Soubor s úkoly nebyl nalezen. Začínáme s prázdným seznamem.")
        except json.JSONDecodeError:
            print("Chyba při načítání úkolů. Soubor může být poškozen.")
        except Exception as e:
            print(f"Nastala neočekávaná chyba při načítání úkolů: {e}")

    def on_sort_change(self, spinner, text):
        self.apply_filter_and_sort()

    def on_filter_change(self, spinner, text):
        self.apply_filter_and_sort()

    def apply_filter_and_sort(self):
        self.tasks_layout.clear_widgets()
        
        filtered_tasks = self.tasks
        if self.filter_spinner.text != 'Všechny kategorie':
            filtered_tasks = [task for task in self.tasks if task.category == self.filter_spinner.text]
        
        sorted_tasks = self.sort_tasks(filtered_tasks)
        
        if self.filter_spinner.text == 'Všechny kategorie':
            tasks_by_category = {category: [] for category in self.categories}
            for task in sorted_tasks:
                tasks_by_category[task.category].append(task)
            
            for category in self.categories:
                if tasks_by_category[category]:
                    category_label = Label(text=category, size_hint_y=None, height=30, bold=True)
                    self.tasks_layout.add_widget(category_label)
                    for task in tasks_by_category[category]:
                        self.tasks_layout.add_widget(task)
        else:
            for task in sorted_tasks:
                self.tasks_layout.add_widget(task)

    def sort_tasks(self, tasks):
        if self.sort_spinner.text == 'Podle priority':
            priority_order = {'Vysoká': 0, 'Střední': 1, 'Nízká': 2}
            return sorted(tasks, key=lambda x: priority_order[x.priority])
        elif self.sort_spinner.text == 'Podle data vytvoření':
            return sorted(tasks, key=lambda x: x.date_added, reverse=True)
        elif self.sort_spinner.text == 'Podle data splnění':
            return sorted(tasks, key=lambda x: x.due_date if x.due_date else datetime.max.isoformat())
        else:  # 'Bez řazení'
            return tasks

    def show_help(self, instance):
        help_text = """
Barvy priorit:
Červená - Vysoká priorita
Oranžová - Střední priorita
Zelená - Nízká priorita

Úkoly jsou seskupeny podle kategorií, když je vybráno 'Všechny kategorie'.

Kliknutím na úkol ho upravíte.
Kliknutím na 'X' úkol smažete.
Datum a čas vytvoření úkolu je zobrazen malým písmem vpravo dole.
Datum splnění úkolu (pokud je nastaveno) je zobrazeno malým písmem vpravo nahoře.

Při přidávání nebo úpravě úkolu můžete zadat datum splnění ve formátu DD.MM.YYYY.
Čas splnění je volitelný a zadává se ve formátu HH:MM.

Použijte rozbalovací menu pro řazení a filtrování úkolů.
        """
        popup = Popup(title='Nápověda',
                      content=Label(text=help_text),
                      size_hint=(0.8, 0.8))
        popup.open()

class OrganizerApp(App):
    def build(self):
        return OrganizerLayout()

if __name__ == '__main__':
    OrganizerApp().run()
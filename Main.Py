import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.metrics import dp


class TodoApp(App):
    def build(self):
        self.title = "My Offline To-Do"
        self.data_file = os.path.join(self.user_data_dir, "todos.json")
        self.tasks = self.load_tasks()

        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))

        input_row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        self.task_input = TextInput(
            hint_text="Enter a new task...",
            multiline=False,
            font_size=dp(16),
        )
        self.task_input.bind(on_text_validate=self.add_task)

        add_btn = Button(
            text="Add",
            size_hint_x=None,
            width=dp(80),
            font_size=dp(16),
        )
        add_btn.bind(on_release=self.add_task)

        input_row.add_widget(self.task_input)
        input_row.add_widget(add_btn)
        root.add_widget(input_row)

        scroll = ScrollView()
        self.list_layout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(6),
        )
        self.list_layout.bind(minimum_height=self.list_layout.setter("height"))
        scroll.add_widget(self.list_layout)
        root.add_widget(scroll)

        self.refresh_list()
        return root

    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return []
        return []

    def save_tasks(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, *_):
        text = self.task_input.text.strip()
        if not text:
            return
        self.tasks.append({"text": text, "done": False})
        self.task_input.text = ""
        self.save_tasks()
        self.refresh_list()

    def toggle_task(self, index, value):
        self.tasks[index]["done"] = value
        self.save_tasks()
        self.refresh_list()

    def delete_task(self, index):
        self.tasks.pop(index)
        self.save_tasks()
        self.refresh_list()

    def refresh_list(self):
        self.list_layout.clear_widgets()
        for idx, item in enumerate(self.tasks):
            row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))

            cb = CheckBox(
                active=item["done"],
                size_hint_x=None,
                width=dp(40),
            )
            cb.bind(active=lambda instance, val, i=idx: self.toggle_task(i, val))

            label_text = f"[s]{item['text']}[/s]" if item["done"] else item["text"]
            lbl = Label(
                text=label_text,
                markup=True,
                halign="left",
                valign="middle",
                font_size=dp(16),
            )
            lbl.bind(size=lambda inst, sz: setattr(inst, "text_size", (sz[0], None)))

            del_btn = Button(
                text="X",
                size_hint_x=None,
                width=dp(44),
                background_color=(0.85, 0.25, 0.25, 1),
            )
            del_btn.bind(on_release=lambda inst, i=idx: self.delete_task(i))

            row.add_widget(cb)
            row.add_widget(lbl)
            row.add_widget(del_btn)
            self.list_layout.add_widget(row)


if __name__ == "__main__":
    TodoApp().run()

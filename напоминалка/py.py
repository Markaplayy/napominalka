import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pickle
import os
import threading
import time

class ReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Напоминалка")
        self.reminders = []
        self.is_running = False

        # Создание интерфейса
        self.create_gui()

    def create_gui(self):
        # Ввод сообщения
        self.label_message = ttk.Label(self.root, text="Сообщение:")
        self.label_message.grid(row=0, column=0, sticky=tk.W)

        self.entry_message = ttk.Entry(self.root)
        self.entry_message.grid(row=0, column=1, sticky=(tk.W, tk.E))

        # Выбор папки
        self.label_app_path = ttk.Label(self.root, text="Путь к приложению (необязательно):")
        self.label_app_path.grid(row=1, column=0, sticky=tk.W)

        self.entry_app_path = ttk.Entry(self.root)
        self.entry_app_path.grid(row=1, column=1, sticky=(tk.W, tk.E))

        self.button_browse = ttk.Button(self.root, text="Обзор", command=self.browse_app_path)
        self.button_browse.grid(row=1, column=2, sticky=tk.W)

        # Ввод времени
        self.label_hour = ttk.Label(self.root, text="Час (0-23):")
        self.label_hour.grid(row=2, column=0, sticky=tk.W)

        self.entry_hour = ttk.Entry(self.root)
        self.entry_hour.grid(row=2, column=1, sticky=(tk.W, tk.E))

        self.label_minute = ttk.Label(self.root, text="Минута (0-59):")
        self.label_minute.grid(row=3, column=0, sticky=tk.W)

        self.entry_minute = ttk.Entry(self.root)
        self.entry_minute.grid(row=3, column=1, sticky=(tk.W, tk.E))

        # Кнопки
        self.button_add = ttk.Button(self.root, text="Добавить напоминание", command=self.add_reminder)
        self.button_add.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))

        self.button_view = ttk.Button(self.root, text="Просмотреть напоминания", command=self.view_reminders)
        self.button_view.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))

        self.button_start = ttk.Button(self.root, text="Запустить напоминания", command=self.start_reminders)
        self.button_start.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E))

        self.button_stop = ttk.Button(self.root, text="Остановить напоминания", command=self.stop_reminders)
        self.button_stop.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E))

        self.button_save = ttk.Button(self.root, text="Сохранить напоминания", command=self.save_reminders)
        self.button_save.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E))

        self.button_load = ttk.Button(self.root, text="Загрузить напоминания", command=self.load_reminders)
        self.button_load.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E))

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def browse_app_path(self):
        app_path = filedialog.askopenfilename()
        self.entry_app_path.delete(0, tk.END)
        self.entry_app_path.insert(0, app_path)

    def add_reminder(self):
        message = self.entry_message.get()
        app_path = f'"{self.entry_app_path.get()}"' if self.entry_app_path.get() else ""
        hour = int(self.entry_hour.get())
        minute = int(self.entry_minute.get())

        # Установка секунд в 00
        second = 0

        self.reminders.append({"message": message, "app_path": app_path, "hour": hour, "minute": minute, "second": second})
        messagebox.showinfo("Напоминание добавлено", "Напоминание добавлено!")

    def view_reminders(self):
        text = "Список напоминаний:\n\n"
        for i, reminder in enumerate(self.reminders, start=1):
            text += f"{i}. Сообщение: {reminder['message']}, Приложение: {reminder['app_path']}, Время: {reminder['hour']}:{reminder['minute']}:{reminder['second']}\n"

        messagebox.showinfo("Напоминания", text)

    def run_reminders(self):
        while self.is_running:
            current_time = time.localtime()
            for reminder in self.reminders:
                if (
                    reminder["hour"] == current_time.tm_hour
                    and reminder["minute"] == current_time.tm_min
                    and reminder["second"] == current_time.tm_sec
                ):
                    messagebox.showinfo("Напоминание", reminder["message"])
                    if reminder["app_path"]:
                        os.system(reminder["app_path"])

            # Подождем 1 секунду перед проверкой снова
            time.sleep(1)

    def start_reminders(self):
        self.is_running = True
        thread = threading.Thread(target=self.run_reminders)
        thread.start()

    def stop_reminders(self):
        self.is_running = False

    def on_close(self):
        self.stop_reminders()
        self.root.destroy()

    def save_reminders(self):
        with open("reminders.pkl", "wb") as f:
            pickle.dump(self.reminders, f)
        messagebox.showinfo("Сохранение", "Напоминания сохранены!")

    def load_reminders(self):
        try:
            with open("reminders.pkl", "rb") as f:
                self.reminders = pickle.load(f)
            messagebox.showinfo("Загрузка", "Напоминания загружены!")
        except FileNotFoundError:
            messagebox.showwarning("Загрузка", "Файл с напоминаниями не найден.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()
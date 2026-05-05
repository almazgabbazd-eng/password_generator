import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
from generator import generate_password
from history import load_history, add_to_history

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.setup_ui()
        self.update_history_table()

    def setup_ui(self):
        # Основная рамка
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)

        # Заголовок
        ttk.Label(main_frame, text="Генератор случайных паролей",
                   font=("Helvetica", 16, "bold")).pack(pady=10)

        # Настройки длины
        length_frame = ttk.LabelFrame(main_frame, text="Длина пароля", padding=10)
        length_frame.pack(fill="x", pady=5)

        self.length_var = tk.IntVar(value=12)
        ttk.Scale(length_frame, from_=4, to=64,
                 variable=self.length_var,
                 orient="horizontal").pack(fill="x")
        ttk.Label(length_frame, textvariable=self.length_var).pack()

        # Чекбоксы для символов
        options_frame = ttk.LabelFrame(main_frame, text="Типы символов", padding=10)
        options_frame.pack(fill="x", pady=5)

        self.letters_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.special_var = tk.BooleanVar(value=False)

        ttk.Checkbutton(options_frame, text="Буквы (a-z, A-Z)",
                       variable=self.letters_var).pack(anchor="w")
        ttk.Checkbutton(options_frame, text="Цифры (0-9)",
                       variable=self.digits_var).pack(anchor="w")
        ttk.Checkbutton(options_frame, text="Спецсимволы (!@#$%)",
                       variable=self.special_var).pack(anchor="w")

        # Кнопка генерации
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)

        ttk.Button(button_frame, text="Сгенерировать пароль",
                 command=self.generate_and_display).pack()

        # Поле вывода пароля
        result_frame = ttk.LabelFrame(main_frame, text="Сгенерированный пароль", padding=10)
        result_frame.pack(fill="x", pady=5)

        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(result_frame, textvariable=self.password_var,
                              state="readonly", font=("Courier", 12))
        password_entry.pack(fill="x")

        copy_button = ttk.Button(result_frame, text="Копировать в буфер",
                           command=self.copy_to_clipboard)
        copy_button.pack(pady=5)

        # Таблица истории
        history_frame = ttk.LabelFrame(main_frame, text="История паролей", padding=10)
        history_frame.pack(fill="both", expand=True, pady=5)

        columns = ("Password", "Length", "Timestamp")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=8)

        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical",
                         command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        self.history_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def generate_and_display(self):
        try:
            length = self.length_var.get()
            if length < 4:
                messagebox.showerror("Ошибка", "Минимальная длина пароля — 4 символа")
                return
            if length > 64:
                messagebox.showerror("Ошибка", "Максимальная длина пароля — 64 символа")
                return

            password = generate_password(
                length,
                self.letters_var.get(),
                self.digits_var.get(),
                self.special_var.get()
            )
            self.password_var.set(password)

            add_to_history(
                password,
                length,
                self.letters_var.get(),
                self.digits_var.get(),
                self.special_var.get()
            )
            self.update_history_table()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена")

    def update_history_table(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        history = load_history()
        for entry in reversed(history[-20:]):  # Последние 20 записей
            self.history_tree.insert("", "end", values=(
                entry["password"],
                entry["length"],
                entry["timestamp"][:19]  # Убираем миллисекунды
            ))

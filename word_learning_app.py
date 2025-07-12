import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import argparse


class WordLearningApp:
    def _make_button(self, parent, text, command, color, hover):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            activebackground=hover,
            **self.button_cfg,
        )
        button.bind("<Enter>", lambda e: button.config(bg=hover))
        button.bind("<Leave>", lambda e: button.config(bg=color))
        return button
    def __init__(self, excel_path: str):
        """Initialize the application with words from an Excel file."""
        self.df = pd.read_excel(excel_path)
        required_columns = {"English", "Turkish", "Example Sentence"}
        missing = required_columns - set(self.df.columns)
        if missing:
            raise ValueError(f"Missing columns in Excel file: {', '.join(missing)}")
        # Track learning status for each word
        self.df['Status'] = 'not_learned'
        self.current_index = None

        # Setup UI
        self.root = tk.Tk()
        self.root.title("Word Learning App")
        self.root.configure(background="#f8f9fa")
        self.root.option_add("*Font", "Segoe UI 12")

        shadow = tk.Frame(self.root, bg="#d0d2d4")
        shadow.pack(padx=30, pady=30)

        self.card = tk.Frame(shadow, bg="white")
        self.card.pack(padx=2, pady=2)

        content = tk.Frame(self.card, bg="white")
        content.pack(padx=20, pady=20)

        self.word_label = tk.Label(
            content,
            text="",
            font=("Segoe UI", 28, "bold"),
            bg="white",
        )
        self.word_label.pack(pady=(0, 10))

        self.sentence_label = tk.Label(
            content,
            text="",
            wraplength=400,
            justify="center",
            font=("Segoe UI", 14),
            bg="white",
        )
        self.sentence_label.pack(pady=5)

        self.translation_label = tk.Label(
            content,
            text="",
            fg="#003366",
            wraplength=400,
            justify="center",
            font=("Segoe UI", 14, "italic"),
            bg="white",
        )
        self.translation_label.pack(pady=5)

        # Progress and filtering
        self.filter_var = tk.StringVar(value="All")
        filter_frame = tk.Frame(content, bg="white")
        filter_frame.pack(pady=(10, 0))
        tk.Label(filter_frame, text="Çalışma Modu:", bg="white").pack(side="left")
        options = ["All", "learned", "repeat", "not_learned"]
        self.filter_menu = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=options,
            state="readonly",
            width=15,
        )
        self.filter_menu.bind("<<ComboboxSelected>>", lambda e: self.next_word())
        self.filter_menu.pack(side="left", padx=5)

        self.button_cfg = {
            "font": ("Segoe UI", 12, "bold"),
            "bd": 0,
            "relief": "flat",
            "cursor": "hand2",
        }

        self.list_button = self._make_button(
            filter_frame,
            "Listeleri Göster",
            self.show_lists,
            "#007bff",
            "#0069d9",
        )
        self.list_button.pack(side="left", padx=5)

        self.progress_label = tk.Label(
            content,
            text="",
            font=("Consolas", 12, "bold"),
            bg="white",
            fg="#333",
        )
        self.progress_label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(content, length=300, maximum=100)
        self.progress_bar.pack(pady=(0, 10))

        button_frame = tk.Frame(content, bg="white")
        button_frame.pack(pady=10)

        self.show_tr_button = self._make_button(
            button_frame,
            "Çeviriyi Göster",
            self.show_translation,
            "#007bff",
            "#0069d9",
        )
        self.show_tr_button.grid(row=0, column=0, padx=5)

        self.learned_button = self._make_button(
            button_frame,
            "Öğrendim",
            self.mark_learned,
            "#28a745",
            "#218838",
        )
        self.learned_button.grid(row=0, column=1, padx=5)

        self.repeat_button = self._make_button(
            button_frame,
            "Tekrar et",
            self.mark_repeat,
            "#ffc107",
            "#e0a800",
        )
        self.repeat_button.grid(row=0, column=2, padx=5)

        self.not_learned_button = self._make_button(
            button_frame,
            "Öğrenmedim",
            self.mark_not_learned,
            "#dc3545",
            "#c82333",
        )
        self.not_learned_button.grid(row=0, column=3, padx=5)

        self.next_word()

    def filtered_words(self):
        """Return DataFrame filtered according to the selected study mode."""
        mode = self.filter_var.get()
        if mode == "All":
            return self.df
        return self.df[self.df['Status'] == mode]

    def next_word(self):
        words = self.filtered_words()
        if words.empty:
            messagebox.showinfo("Bilgi", "Seçilen kategoride kelime yok")
            return
        row = words.sample().iloc[0]
        self.current_index = row.name
        self.word_label.config(text=row['English'])
        self.sentence_label.config(text=row['Example Sentence'])
        self.translation_label.config(text="")
        self.update_progress()

    def update_progress(self):
        learned = (self.df['Status'] == 'learned').sum()
        repeat = (self.df['Status'] == 'repeat').sum()
        not_learned = (self.df['Status'] == 'not_learned').sum()
        total = len(self.df)
        percent = (learned / total * 100) if total else 0
        self.progress_label.config(
            text=f"Öğrenilen: {learned}  Tekrar: {repeat}  Öğrenilmedi: {not_learned}  (%{percent:.1f} öğrenildi)"
        )
        self.progress_bar['value'] = percent

    def show_translation(self):
        turkish = self.df.loc[self.current_index, 'Turkish']
        self.translation_label.config(text=turkish)

    def mark_learned(self):
        self.df.loc[self.current_index, 'Status'] = 'learned'
        self.next_word()

    def mark_repeat(self):
        self.df.loc[self.current_index, 'Status'] = 'repeat'
        self.next_word()

    def mark_not_learned(self):
        self.df.loc[self.current_index, 'Status'] = 'not_learned'
        self.next_word()

    def run(self):
        self.root.mainloop()

    def show_lists(self):
        top = tk.Toplevel(self.root)
        top.title("Kelime Listeleri")
        top.configure(background="#f8f9fa")
        statuses = [("learned", "Öğrenilenler"), ("repeat", "Tekrar"), ("not_learned", "Öğrenilmedi")]
        for status, title in statuses:
            frame = tk.Frame(top, bg="#f8f9fa")
            frame.pack(side="left", padx=5, pady=5, fill="both", expand=True)
            tk.Label(frame, text=title, bg="#f8f9fa").pack()
            listbox = tk.Listbox(frame, width=25)
            listbox.pack(fill="both", expand=True)
            for word in self.df[self.df['Status'] == status]['English']:
                listbox.insert("end", word)


def main():
    parser = argparse.ArgumentParser(description="Simple word learning application")
    parser.add_argument("excel", help="Path to Excel file with columns English, Turkish, Example Sentence")
    args = parser.parse_args()

    app = WordLearningApp(args.excel)
    app.run()


if __name__ == "__main__":
    main()

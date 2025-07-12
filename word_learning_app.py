import pandas as pd
import tkinter as tk
from tkinter import messagebox
import argparse


class WordLearningApp:
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
        self.root.configure(background="#f0f8ff")

        self.word_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 24, "bold"),
            bg="#f0f8ff",
        )
        self.word_label.pack(pady=10)

        self.sentence_label = tk.Label(
            self.root,
            text="",
            wraplength=400,
            justify="center",
            font=("Helvetica", 14),
            bg="#f0f8ff",
        )
        self.sentence_label.pack(pady=10)

        self.translation_label = tk.Label(
            self.root,
            text="",
            fg="#003366",
            wraplength=400,
            justify="center",
            font=("Helvetica", 14, "italic"),
            bg="#f0f8ff",
        )
        self.translation_label.pack(pady=10)

        # Progress and filtering
        self.filter_var = tk.StringVar(value="All")
        filter_frame = tk.Frame(self.root, bg="#f0f8ff")
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, text="Çalışma Modu:", bg="#f0f8ff").pack(side="left")
        options = ["All", "learned", "repeat", "not_learned"]
        self.filter_menu = tk.OptionMenu(filter_frame, self.filter_var, *options, command=lambda _: self.next_word())
        self.filter_menu.config(bg="#e1e1e1")
        self.filter_menu.pack(side="left")

        self.list_button = tk.Button(
            filter_frame,
            text="Listeleri Göster",
            command=self.show_lists,
            bg="#008CBA",
            fg="white",
        )
        self.list_button.pack(side="left", padx=5)

        self.progress_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 12),
            bg="#f0f8ff",
        )
        self.progress_label.pack(pady=5)

        button_frame = tk.Frame(self.root, bg="#f0f8ff")
        button_frame.pack(pady=10)

        self.show_tr_button = tk.Button(
            button_frame,
            text="Show Translation",
            command=self.show_translation,
            bg="#008CBA",
            fg="white",
        )
        self.show_tr_button.grid(row=0, column=0, padx=5)

        self.learned_button = tk.Button(
            button_frame,
            text="Öğrendim",
            command=self.mark_learned,
            bg="#4CAF50",
            fg="white",
        )
        self.learned_button.grid(row=0, column=1, padx=5)

        self.repeat_button = tk.Button(
            button_frame,
            text="Tekrar et",
            command=self.mark_repeat,
            bg="#FFC107",
        )
        self.repeat_button.grid(row=0, column=2, padx=5)

        self.not_learned_button = tk.Button(
            button_frame,
            text="Öğrenmedim",
            command=self.mark_not_learned,
            bg="#F44336",
            fg="white",
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
        top.configure(background="#f0f8ff")
        statuses = [("learned", "Öğrenilenler"), ("repeat", "Tekrar"), ("not_learned", "Öğrenilmedi")]
        for status, title in statuses:
            frame = tk.Frame(top, bg="#f0f8ff")
            frame.pack(side="left", padx=5, pady=5, fill="both", expand=True)
            tk.Label(frame, text=title, bg="#f0f8ff").pack()
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

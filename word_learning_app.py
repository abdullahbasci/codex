import pandas as pd
import tkinter as tk
from tkinter import messagebox
import random
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

        self.word_label = tk.Label(self.root, text="", font=("Helvetica", 20))
        self.word_label.pack(pady=10)

        self.sentence_label = tk.Label(self.root, text="", wraplength=400, justify="center")
        self.sentence_label.pack(pady=10)

        self.translation_label = tk.Label(self.root, text="", fg="blue", wraplength=400, justify="center")
        self.translation_label.pack(pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.show_tr_button = tk.Button(button_frame, text="Show Translation", command=self.show_translation)
        self.show_tr_button.grid(row=0, column=0, padx=5)

        self.learned_button = tk.Button(button_frame, text="Öğrendim", command=self.mark_learned)
        self.learned_button.grid(row=0, column=1, padx=5)

        self.repeat_button = tk.Button(button_frame, text="Tekrar et", command=self.mark_repeat)
        self.repeat_button.grid(row=0, column=2, padx=5)

        self.not_learned_button = tk.Button(button_frame, text="Öğrenmedim", command=self.mark_not_learned)
        self.not_learned_button.grid(row=0, column=3, padx=5)

        self.next_word()

    def pending_words(self):
        """Return DataFrame of words that are not yet learned."""
        return self.df[self.df['Status'] != 'learned']

    def next_word(self):
        pending = self.pending_words()
        if pending.empty:
            messagebox.showinfo("Congratulations", "Tüm kelimeleri öğrendiniz!")
            self.root.quit()
            return
        row = pending.sample().iloc[0]
        self.current_index = row.name
        self.word_label.config(text=row['English'])
        self.sentence_label.config(text=row['Example Sentence'])
        self.translation_label.config(text="")

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


def main():
    parser = argparse.ArgumentParser(description="Simple word learning application")
    parser.add_argument("excel", help="Path to Excel file with columns English, Turkish, Example Sentence")
    args = parser.parse_args()

    app = WordLearningApp(args.excel)
    app.run()


if __name__ == "__main__":
    main()

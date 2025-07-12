# Word Learning Application

This repository contains a simple Tkinter application for practising English vocabulary using an Excel file. The Excel file must contain the following columns:

- **English** – the word to learn
- **Turkish** – its translation
- **Example Sentence** – a sample usage of the word

## Usage

1. Prepare an Excel file with the required columns (an `.xlsx` file). Place it somewhere accessible.
2. Install the dependencies:

```bash
pip install pandas openpyxl
```

3. Run the application and pass the path to your Excel file:

```bash
python word_learning_app.py words.xlsx
```

A window will appear displaying the English word and its example sentence. Use the buttons to reveal the translation and mark the word as learned, to repeat later or not learned.

All words start in the *not learned* state. Selecting **Öğrendim** moves it to the learned group, **Tekrar et** moves it to the repeat group, and **Öğrenmedim** keeps it in the not learned group. When all words are marked as learned the application notifies you and exits.

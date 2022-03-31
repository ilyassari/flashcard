import tkinter as tk
import pandas
import random

BG_COLOR = '#d5e3f4'
FONT_TITLE = ("Ariel", 18, "italic")
FONT_FRONT = ("Ariel", 24, "bold")
FONT_BACK = ("Ariel", 22)
data_file = "data/machinery_words.csv"
to_learn = dict()
current_card = dict()

lang1, lang2 = pandas.read_csv(data_file, nrows=0).columns
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv(data_file)
finally:
    to_learn = data.to_dict(orient='records')


def next_card():
    global current_card, flip_timer
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text=lang1, fill='black')
    canvas.itemconfig(card_word, text=current_card[lang1], fill='black', font=FONT_FRONT)
    canvas.itemconfig(card_bg, image=front_image)
    root.after_cancel(flip_timer)
    flip_timer = root.after(3000, func=flip_card)


def word_learned():
    to_learn.remove(current_card)
    data_to_learn = pandas.DataFrame(to_learn)
    data_to_learn.to_csv('data/words_to_learn.csv', index=False)
    next_card()


def flip_card():
    canvas.itemconfig(card_title, text=lang2, fill='white')
    canvas.itemconfig(card_word, text=current_card[lang2], fill='white', font=FONT_BACK)
    canvas.itemconfig(card_bg, image=back_image)


root = tk.Tk()
root.title("Flashcards")
root.config(padx=20, pady=20, bg=BG_COLOR)

flip_timer = root.after(3000, func=flip_card)

canvas = tk.Canvas(root, width=400, height=220, bg=BG_COLOR, highlightthickness=0)
front_image = tk.PhotoImage(file='assets/card_front.png')
back_image = tk.PhotoImage(file='assets/card_back.png')
card_bg = canvas.create_image(200, 110, image=front_image)
card_title = canvas.create_text(200, 30, text='')
card_word = canvas.create_text(200, 110, text='')
canvas.grid(row=0, column=0, columnspan=2)

unknown_image = tk.PhotoImage(file='assets/unknown24.png')
unknown_button = tk.Button(root, image=unknown_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0, sticky='W')

known_image = tk.PhotoImage(file='assets/known24.png')
known_button = tk.Button(root, image=known_image, highlightthickness=0, command=word_learned)
known_button.grid(row=1, column=1, sticky='E')

next_card()

root.mainloop()

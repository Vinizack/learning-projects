from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

data = pandas.read_csv("data/french_words.csv")
aprender = data.to_dict(orient="records")
carta_atual = {}



def next_card():
    global carta_atual, tempo_virar
    tela.after_cancel(tempo_virar)
    carta_atual = random.choice(aprender)
    canvas.itemconfig(titulo_carta, text="Frances", fill="black")
    canvas.itemconfig(palavra_carta, text=carta_atual["French"], fill="black")
    canvas.itemconfig(card_background, image=cartao_frente)
    tempo_virar = tela.after(3000, func=virar_carta)


def virar_carta():
    canvas.itemconfig(titulo_carta, text="Ingles", fill="white")
    canvas.itemconfig(palavra_carta, text=carta_atual["English"], fill="white")
    canvas.itemconfig(card_background, image=cartao_costa)

def saber():
    aprender.remove(carta_atual)
    next_card()



tela = Tk()
tela.title("Flash Card")
tela.config(padx=50,pady=50, background=BACKGROUND_COLOR)

tempo_virar = tela.after(3000, func=virar_carta)

canvas = Canvas(width=800, height=526)
cartao_frente = PhotoImage(file="images/card_front.png")
cartao_costa = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=cartao_frente)
titulo_carta = canvas.create_text(400, 150, text="", font=("Ariel", 40 , "italic"))
palavra_carta = canvas.create_text(400, 263, text="", font=("Ariel", 60 , "bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1,column=0)

check_image = PhotoImage(file="images/right.png")
check_button = Button(image=check_image, highlightthickness=0, command=saber)
check_button.grid(row=1,column=1)

next_card()























tela.mainloop()
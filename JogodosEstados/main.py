import pandas
import turtle


tela = turtle.Screen()
tela.title("Mapa dos EUA - Adivinhe os estados")
imagem = "blank_states_img.gif"
tela.addshape(imagem)
turtle.shape(imagem)


data = pandas.read_csv("50_states.csv")
all_states = data.state.to_list()

guessed_states = []

while len(guessed_states) < 50:
    title_text = f"{len(guessed_states)}/50 Estados corretos"

    answer_state = tela.textinput(title=title_text, prompt="Qual o próximo estado? (ou digite 'Exit' para sair)")

    if answer_state is None:
        answer_state = "Exit"

    answer_state = answer_state.title()  

    if answer_state == "Exit":

        missing = [state for state in all_states if state not in guessed_states]
        pandas.DataFrame(missing, columns=["state"]).to_csv("states_to_learn.csv", index=False)
        print("Jogo finalizado. Arquivo states_to_learn.csv criado com os estados faltantes.")
        break

    if answer_state in all_states and answer_state not in guessed_states:
        guessed_states.append(answer_state)

        state_row = data[data.state == answer_state]
        x, y = int(state_row.x), int(state_row.y)
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        t.goto(x, y)
        t.write(answer_state, align="center", font=("Arial", 8, "normal"))


    if len(guessed_states) == 50:
        print("Parabéns! Você nomeou todos os 50 estados!")
        break

tela.exitonclick()

import pandas
import turtle

tela = turtle.Screen()
tela.title("Mapa dos EUA")
imagem = "blank_states_img.gif"
tela.addshape(imagem)
turtle.shape(imagem)

data = pandas.read_csv("50_states.csv")
estados = data.state.to_list()

answer_state = tela.textinput(title="adivinhe o estado", prompt="fale os outros")
print(answer_state)

if answer_state in estados:
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    data_estados = data[data.state == answer_state]
    t.goto(data_estados.x.item(), data_estados.y.item())
    t.write(answer_state)




tela.exitonclick()
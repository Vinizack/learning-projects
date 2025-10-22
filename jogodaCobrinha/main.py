from cobra import Cobra
from turtle import Screen, Turtle
from comida import Comida
from placar import Placar
import time


tela = Screen()
tela.setup(width=600,height=600)
tela.bgcolor("black")
tela.title("Jogo da Cobrinha")
tela.tracer(0)

posicoes_iniciais = [(0,0), (-20,0), (-40,0)]


cobra = Cobra()
comida = Comida()
placar = Placar()

tela.listen()
tela.onkey(cobra.up,"Up")
tela.onkey(cobra.down,"Down")
tela.onkey(cobra.left,"Left")
tela.onkey(cobra.right,"Right")

game_on = True

while game_on:
    tela.update()
    time.sleep(0.1)
    cobra.andar()


    if cobra.cabeca.distance(comida) < 15:
        comida.refresh()
        cobra.crescer()
        placar.aumentar()

    if cobra.cabeca.xcor() > 280 or cobra.cabeca.xcor() < -280 or cobra.cabeca.ycor() > 280 or cobra.cabeca.ycor() < -280:
        placar.reset()
        cobra.reset()



    for segmento in cobra.segmentos:
        if segmento == cobra.cabeca:
            pass
        elif cobra.cabeca.distance(segmento) < 10:
            placar.reset()
            cobra.reset()










tela.exitonclick()
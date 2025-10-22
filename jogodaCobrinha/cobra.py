from turtle import Turtle
POSICOES_INICAIS = [(0,0), (-20,0), (-40,0)]
DISTANCIA_ANDAR = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

class Cobra:

    def __init__(self):
        self.segmentos = []
        self.criar_cobra()
        self.cabeca = self.segmentos[0]


    def criar_cobra(self):
        for posicao in POSICOES_INICAIS:
            self.add_segmento(posicao)


    def add_segmento(self, posicao):
        new_segment = Turtle("square")
        new_segment.color("white")
        new_segment.penup()
        new_segment.goto(posicao)
        self.segmentos.append(new_segment)


    def reset(self):
        for seg in self.segmentos:
            seg.goto(1000,1000)

        self.segmentos.clear()
        self.criar_cobra()
        self.cabeca = self.segmentos[0]



    def crescer(self):
        self.add_segmento(self.segmentos[-1].position())


    def andar(self):
        for seg_num in range(len(self.segmentos) - 1, 0, -1):
            novo_x = self.segmentos[seg_num - 1].xcor()
            novo_y = self.segmentos[seg_num - 1].ycor()
            self.segmentos[seg_num].goto(novo_x, novo_y)
        self.cabeca.forward(DISTANCIA_ANDAR)

    def up(self):
        if self.cabeca.heading() != DOWN:
            self.cabeca.setheading(UP)

    def down(self):
        if self.cabeca.heading() != UP:
            self.cabeca.setheading(DOWN)

    def left(self):
        if self.cabeca.heading() != RIGHT:
            self.cabeca.setheading(LEFT)

    def right(self):
        if self.cabeca.heading() != LEFT:
            self.cabeca.setheading(RIGHT)
from turtle import Turtle


class Placar(Turtle):

    def __init__(self):
        super().__init__()
        self.score = 0
        with open("data.txt") as data:
            self.maior_pontuacao = int(data.read())
        self.color("white")
        self.penup()
        self.goto(0, 270)
        self.hideturtle()
        self.placar_atualizado()

    def placar_atualizado(self):
        self.clear()
        self.write(f"Pontuacao:{self.score} Maior Pontuacao: {self.maior_pontuacao}", align="center", font=("Arial", 24, "normal"))


    def reset(self):
        if self.score > self.maior_pontuacao:
            self.maior_pontuacao = self.score
            with open("data.txt", mode="w") as data:
                data.write(f"{self.maior_pontuacao}")
        self.score = 0
        self.placar_atualizado()



    def aumentar(self):
        self.score += 1
        self.placar_atualizado()

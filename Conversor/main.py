from tkinter import *

def Km_para_Milhas():
    quilometros = float(km_input.get())
    milhas = round(quilometros / 1.609)
    resultado.config(text=f"{milhas}")


janela = Tk()
janela.title("Quilometros em Milhas")
janela.config(padx=20,pady=20)

#Milhas
Milhas = Label(text="label", font=("Arial", 24))
Milhas.config(text="Milhas")
Milhas.grid(column=2,row=1)


#KM
KM = Label(text="label", font=("Arial", 24))
KM.config(text="KM")
KM.grid(column=2,row=0)


#Botao
botao_calculo = Button(text="Converter", command=Km_para_Milhas)
botao_calculo.grid(column=1,row=2)


#Entrada
km_input = Entry(width=7)
km_input.grid(column=1,row=0)

#Resultado
resultado = Label(text="0")
resultado.grid(column=1,row=1)


comparar_label = Label(text="é igual a")
comparar_label.grid(column=0,row=1)




janela.mainloop()









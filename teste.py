from flask import Flask, render_template, request, redirect, session, flash
import os, pymongo, base64
import altair as alt
import pandas as pd
#Importando os módulos necessários para o projeto Flask.

class Usuario:
    def __init__(self,nome,genero,idade,estado,id):
        self.nome = nome
        self.genero = genero
        self.idade = idade
        self.estado = estado
        self.id = id

def espaco(quantos):
    for q in range(quantos):
        print("")

app = Flask(__name__)
app.secret_key = 'enzo'
#Criando uma instância do objeto Flask e definindo a chave secreta para uso nas sessões.

os.system("cls")
#Executando o comando "cls" para limpar a tela do console.

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["biblioteca"]
collection = db["users"]
collection_infos = db["infos"]

livros_id = collection_infos.find()
generos = []
ids = []
nomes = []
estados = []
idades = []
users = []
for item in livros_id:
    v_nome = item["nome"]
    v_id = item["id"]
    v_genero = item["genero"]
    v_estado = item["estado"]
    v_idades = item["idade"]

    usuario = Usuario(nome=v_nome, genero=v_genero, idade=v_idades, estado=v_estado, id=int(v_id))

    users.append(usuario)




print("O que você quer saber?")
print("1. Quantas usuarios tem o site?")
print("2. Qual a proporção de gênero dos usuarios?")
print("3. Qual estado os usuarios moram?")
print("4. Qual a idade de nossos usuarios?")
espaco(1)

op = int(input())
match(op):
    case 1:
        qtd = 0
        for usuario in users:
            qtd += 1

        print("Temos {} usuarios em nosso site!".format(qtd))
        
    case 2:
        qtdm = 0
        qtdf = 0
        qtdnb = 0
        for usuario in users:
            if usuario.genero == "Masculino":
                qtdm += 1
            elif usuario.genero == "Feminino":
                qtdf += 1
            else:
                qtdnb += 1
        espaco(2)
        print("Temos {} usuarios do genero masculino, {} usuarios do genero feminino e {} de gênero não binario!".format(qtdm,qtdf,qtdnb))
        espaco(2)
        pctm = (qtdm*100)/len(users)
        pctf = (qtdf*100)/len(users)
        pctnb = (qtdnb*100)/len(users)
        print("Isso corresponde a mais ou menos:")
        print("{}% Masculinos".format(pctm))
        print("{}% Femininos".format(pctf))
        print("{}% Não binários".format(pctnb))

    case 3:
        qtdm = 0
        for usuario in users:
            if usuario.estado == "São Paulo":
                qtdm += 1
        espaco(1)
        print("Temos {} usuarios morando em São Paulo e só!".format(qtdm))
        espaco(1)
        pctm = (qtdm*100)/len(users)
        print("Isso corresponde a mais ou menos:")
        print("{}% São Paulo".format(pctm))
        print("0% Outros")
        espaco(1)
    case 4:
        dzot = 0
        dzst = 0
        dzss = 0
        qnze = 0  
        for usuario in users:
            if usuario.idade == "18":
                dzot += 1
            elif usuario.idade == "17":
                dzst += 1
            elif usuario.idade == "16":
                dzss += 1
            else:
                qnze += 1
        espaco(1)
        print("Temos {} usuarios de 18 anos, {} usuarios de 17 anos, {} usuarios de 16 anos e {} usuarios de 15 anos!".format(dzot,dzst,dzss,qnze))
        espaco(1)
        pdoito = (dzot*100)/len(users)
        pdsete = (dzst*100)/len(users)
        pdseis = (dzss*100)/len(users)
        pquinz = (qnze*100)/len(users)
        print("Isso corresponde a mais ou menos:")
        print("{}% 18".format(round(pdoito)))
        print("{}% 17".format(round(pdsete)))
        print("{}% 16".format(round(pdseis)))
        print("{}% 15".format(round(pquinz)))
        espaco(1) 



"""idade_data = [20, 30, 25, 35, 40]
idade_labels = ['20-24', '25-29', '30-34', '35-39', '40+']

 Criação do DataFrame com os dados
data = pd.DataFrame({'idade': idade_data, 'label': idade_labels})



grafico_altair = alt.Chart(data).mark_circle(size=200).encode(
        alt.X('idade:O', title='Idade'),
        alt.Y('sum(idade):Q', title='Quantidade de Usuários'),
        tooltip='sum(idade):Q'
    ).properties(
        width=400,
        height=300,
        title='Distribuição de Idade dos Usuários'
    ).interactive()


grafico_altair.show()"""

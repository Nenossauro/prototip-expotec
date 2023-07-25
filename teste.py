from flask import Flask, render_template, request, redirect, session, flash
import os, pymongo, base64
import altair as alt
import pandas as pd
#Importando os módulos necessários para o projeto Flask.

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
for item in livros_id:
    v_nome = item["nome"]
    v_id = item["id"]
    v_genero = item["genero"]
    v_estado = item["estado"]
    v_idades = item["idade"]
    nomes.append(v_nome)
    generos.append(v_genero)
    estados.append(v_estado)
    idades.append(v_idades)
    ids.append(int(v_id))

idade_data = [20, 30, 25, 35, 40]
idade_labels = ['20-24', '25-29', '30-34', '35-39', '40+']

# Criação do DataFrame com os dados
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


grafico_altair.show()

from flask import Flask, render_template, request, redirect, session, flash
import os, pymongo, base64, altair, pandas
  
#Importando os módulos necessários para o projeto Flask.

app = Flask(__name__)
app.secret_key = 'enzo'
#Criando uma instância do objeto Flask e definindo a chave secreta para uso nas sessões.

os.system("cls")
#Executando o comando "cls" para limpar a tela do console.

class Usuario:
    def __init__(self,nome,genero,idade,estado,id):
        self.nome = nome
        self.genero = genero
        self.idade = idade
        self.estado = estado
        self.id = id

        


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["biblioteca"]
collection = db["users"]
collection_infos = db["infos"]
#Estabelecendo a conexão com o banco de dados MongoDB, especificando o banco de dados "biblioteca" e a coleção "users".
#Se você quiser abrir o programa ai na sua casa, é só criar um banco de dados com essas caracteristicas

@app.route('/')
def index():
    return render_template('index.html')
#Definindo a rota principal (/) para renderizar o template 'index.html'.

@app.route('/inicio')
def inicio():
    if 'user_logged' not in session or session['user_logged'] == None:
        return redirect('/')
    
    if request.cookies.get('samuel'):
        meu_cookie = request.cookies.get('samuel')
    else:
        meu_cookie = '0'
    livros_id = collection_infos.find()
    users = []
    for item in livros_id:
        v_nome = item["nome"]
        v_id = item["id"]
        v_genero = item["genero"]
        v_estado = item["estado"]
        v_idades = item["idade"]
        usuario = Usuario(nome=v_nome, genero=v_genero, idade=v_idades, estado=v_estado, id=int(v_id))
        users.append(usuario)
    idadesp = ["18","17","16","15"]
    

    idades = []
    for ages in users:
       t_ages = ages.idade
       idades.append(t_ages)
    relacao = []
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
    relacao.append(dzot)
    relacao.append(dzst)
    relacao.append(dzss)
    relacao.append(qnze)
    total_usuarios = len(users)
    df = pandas.DataFrame({'idade':relacao, 'Idades':idadesp})
    df['porcentagem'] = round((df['idade'] / total_usuarios) * 100)
    print("Quantidade de cada idade:",relacao)
    print("Idades possiveis:",idadesp)
    grafico_altair_idade = altair.Chart(df).mark_arc(size=100).encode(
        theta='idade:Q',
        color='Idades:O',
        tooltip='porcentagem:N'
        
    ).properties(
        width=200,
        height=150,
        title='Distribuição de Idade dos Usuários em %'
    )



    fem = 0
    masc = 0
    nb = 0
    relgen = []
    generos = ["Masculino","Feminino","Não Binário"]

    for usuario in users:
        if usuario.genero == "Masculino":
            masc += 1
        elif usuario.genero == "Feminino":
            fem += 1
        else:
            nb += 1
    relgen.append(masc) 
    relgen.append(fem)
    relgen.append(nb)
    print("Quantidade de cada genero:",relgen)
    print("Generos possiveis:",generos)
    dfg = pandas.DataFrame({'Genero':relgen,'Generos':generos})
    dfg['porcentagem'] = round((dfg['Genero'] / total_usuarios) * 100)
    
    grafico_altair_genero = altair.Chart(dfg).mark_arc(size=100).encode(
        theta='Genero:Q',
        color='Generos:O',
        tooltip='porcentagem:N'
        
    ).properties(
        width=200,
        height=150,
        title='Distribuição de genero dos Usuários em %'
    )

    










    grafico_altair_idade_json = grafico_altair_idade.to_json()
    grafico_altair_genero_json = grafico_altair_genero.to_json()


    return render_template('land.html',pessoa =session['user_logged'], id_liv = int(meu_cookie), grafico_altair=grafico_altair_idade_json,grafico_altair_genero=grafico_altair_genero_json)
#Definindo a rota '/inicio', que requer autenticação. 
#Se o usuário não estiver logado, será redirecionado para a página principal ('/'). 
#Caso contrário, o template 'land.html' será renderizado, passando a variável 'pessoa' com o valor da sessão 'user_logged'.
@app.route('/form')
def form():
    if 'user_logged' not in session or session['user_logged'] == None:
        return redirect('/')
    livros_id = collection_infos.find()
    ids = []
    for item in livros_id:
        v_id = item["id"]
        ids.append(int(v_id))
    return render_template('form.html', idp = len(ids))

@app.route('/inserir', methods=['POST',])
def inserir():
    livros_id = collection_infos.find()
    ids = []
    for item in livros_id:
        v_id = item["id"]
        ids.append(int(v_id))
    id = len(ids)
    
    nome = request.form['txtnome']
    genero = request.form['txtgenero']
    estado = request.form['txtestado']
    idade = request.form['txtidade']
    collection_infos.insert_one({"nome":nome,"genero":genero,"estado":estado,"idade":idade,"id":id})
    return redirect('/form')
@app.route('/criar', methods=['POST',])
def criar():
    user = request.form['userr']
    nome = request.form['nomer']
    senha = request.form['senhar']
    collection.insert_one({"nome":user,"email":nome,"senha":senha})
    return redirect('/')
#Definindo a rota '/criar', que recebe uma solicitação POST para criar um novo usuário. 
#Os dados do formulário são recuperados e um novo documento é inserido na coleção 'users' no banco de dados. 
#Após a inserção, o usuário é redirecionado para a página principal ('/').

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        temp_user = ''
        temp_senha = ''
        usuario = collection.find({"email": nome})
        for users in usuario:
            temp_user = users["email"]
            temp_senha = users["senha"]
            nome_user = users["nome"]
        if nome == temp_user:
            if senha == temp_senha:
                session['user_logged'] = nome_user
                flash(session['user_logged']+'! Usuario logado com sucesso!')
                return redirect('/form')
            else:
                flash("Senha invalida")
                return redirect('/')
        else:
            flash("Email invalido")
            return redirect('/')
    else:
        return "Método não permitido."
#Definindo a rota '/autenticar', que recebe uma solicitação POST com os dados do formulário de login. 
#A função verifica se as credenciais fornecidas correspondem a um usuário existente no banco de dados. 
#Se as credenciais forem válidas, o usuário é autenticado e armazenado na sessão. Caso contrário, mensagens de erro são exibidas. 
#A função também inclui o uso de flash messages para fornecer feedback ao usuário.    
    
@app.route('/logout')
def logout():
    session['user_logged'] = None
    return redirect('/')
#Definindo a rota '/logout' para efetuar o logout do usuário. 
#A sessão 'user_logged' é definida como None e o usuário é redirecionado para a página principal ('/').







app.run()
#Iniciando o servidor Flask.
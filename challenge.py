import json
import csv
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3

# Função para enviar o email
def enviar_email(manager_email, owner_name, base, classificacao):
    # Configurar os detalhes do email
    subject = "Revalidar a classificação da base de dados"
    message = f"Estimado/a {owner_name},\n\na base de dados '{base}' com classificação '{classificacao}' está pendente de revalidação. Por favor, confirme sua aprovação\n\nAtenciosamente,\nEquipe de CyberSecurity"
    sender_email = "EMAIL_GMAIL"  # Insira o seu endereço de email do Gmail | pode inserir via input
    password = "SENHA_APP"  # Insira a sua senha do Gmail | configurações->segurança->senha de app | pode inserir via input

    # Configurar o objeto MIMEMultipart para compor o email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = manager_email
    msg['Subject'] = subject

    # Adicionar o corpo da mensagem ao objeto MIMEMultipart
    msg.attach(MIMEText(message, 'plain'))

    # Iniciar uma conexão SMTP segura com o Gmail
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, manager_email, msg.as_string())
        print(f"[+] Email enviado para ---> {manager_email}")

# Função para processar o arquivo JSON
def processar_arquivo_json(json_file):
    with open(json_file) as file:
        data = json.load(file)
    return data['db_list']

# Função para processar o arquivo CSV
def processar_arquivo_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        data = {}
        for row in reader:
            data[row[1]] = row[3]  # mapear o ID do usuário ao email do manager
    return data

# Função para salvar os dados na base de dados SQLite
def salvar_dados_na_base_de_dados(json_data, csv_data):
    conn = sqlite3.connect('revdb.db')  # defina um nome para salvar a base de revalidacao
    cursor = conn.cursor()

    # Criar a tabela se não existir
    cursor.execute('''CREATE TABLE IF NOT EXISTS revdb
                      (bdtest text, owner_name text, manager_email text, classificacao text)''')

    # Inserir os dados do arquivo JSON na tabela
    for item in json_data:
        bd = item['dn_name']
        owner_name = item['owner'].get('name', '')  # pega o valor do campo 'name' ou uma string vazia caso não exista
        manager_email = csv_data.get(item['owner']['uid'],'') # pega o email do manager ou vazio(string) 
        classificacao = item['classification']['integrity']

        cursor.execute("INSERT INTO revdb VALUES (?, ?, ?, ?)",
                       (bd, owner_name, manager_email, classificacao))

        # Verificar se a classificação é alta (high) e enviar o email ao manager
        if classificacao.lower() == 'high':
            enviar_email(manager_email, owner_name, bd, classificacao)

    # Commit das alterações e fechamento da conexão
    conn.commit()
    conn.close()

# Executar o script
if __name__ == '__main__':
    json_data = processar_arquivo_json('dblist.json')  # Insira o nome do arquivo JSON | pode altar para entrada input e passar o caminho do arquivo, se quiser
    csv_data = processar_arquivo_csv('user_manager.csv')  # Insira o nome do arquivo CSV
    salvar_dados_na_base_de_dados(json_data, csv_data)

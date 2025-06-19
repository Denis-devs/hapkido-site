
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL = 'seuemail@gmail.com'
SENHA = 'suasenha'

def enviar_email(destinatario, titulo, mensagem):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = destinatario
    msg['Subject'] = titulo
    msg.attach(MIMEText(mensagem, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
        servidor.starttls()
        servidor.login(EMAIL, SENHA)
        servidor.send_message(msg)

def enviar_para_todos():
    with open('alunos.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            email = row['Email']
            nome = row['Nome']
            mensagem = f"Olá {nome},\n\nTemos um novo evento!\n\n{evento_msg}"
            enviar_email(email, evento_titulo, mensagem)

evento_titulo = "Exemplo de Evento"
evento_msg = "Venha participar do nosso novo evento de Hapkido no sábado às 15h!"

enviar_para_todos()

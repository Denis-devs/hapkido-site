import gspread
from oauth2client.service_account import ServiceAccountCredentials
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

# Autenticação com Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("CadastroAlunos").sheet1

# Lê os dados
dados = sheet.get_all_records()

# Configurações de envio de email
EMAIL = "seuemail@gmail.com"
SENHA = "suasenha"

def enviar_email(destinatario, assunto, mensagem):
    msg = MIMEText(mensagem)
    msg["Subject"] = assunto
    msg["From"] = EMAIL
    msg["To"] = destinatario
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, SENHA)
            server.sendmail(EMAIL, destinatario, msg.as_string())
        print(f"Email enviado para {destinatario}")
    except Exception as e:
        print(f"Erro ao enviar para {destinatario}: {e}")

# Verificar mensalidades
hoje = datetime.today()
for aluno in dados:
    nome = aluno.get("Nome")
    email = aluno.get("Email")
    vencimento_str = aluno.get("Vencimento")
    try:
        vencimento = datetime.strptime(vencimento_str, "%d/%m/%Y")
        dias = (vencimento - hoje).days
        if 0 <= dias <= 3:
            mensagem = (f"Olá, {nome} Sua mensalidade vence em {dias} dias. Pague antecipado e ganhe 15% de desconto!"
            enviar_email(email, "Aviso de Vencimento", mensagem))
    except:
        continue
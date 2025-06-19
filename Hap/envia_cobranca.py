import gspread
import datetime
import smtplib
from email.mime.text import MIMEText
from oauth2client.service_account import ServiceAccountCredentials

# CONFIGURE AQUI:
PLANILHA = 'Alunos'           # Nome da planilha
GUIA = 'Página1'              # Nome da guia
REMETENTE = 'denis.lemos.rodrigues@gmail.com'  # Seu e-mail Gmail
SENHA_APP = 'rmul meli lbgo ltvq'    # Senha de App do Gmail

# Setup acesso ao Google Sheets
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open(PLANILHA).worksheet(GUIA)

# Lê todos os dados (exceto cabeçalho)
dados = sheet.get_all_records()

# Função para enviar email
def envia_email(destinatario, nome):
    msg = MIMEText(f"""Olá, {nome}.
Sua mensalidade deste mês está próxima do vencimento, aproveite o desconto de 15% e pague 3 dias antes.""")
    msg['Subject'] = 'Cobrança de Mensalidade - Instituto Dok Su Ri'
    msg['From'] = REMETENTE
    msg['To'] = destinatario

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(REMETENTE, SENHA_APP)
        server.sendmail(REMETENTE, destinatario, msg.as_string())
        print(f"E-mail enviado para {nome} - {destinatario}")

# Verifica vencimento e envia
hoje = datetime.datetime.now().date()
for aluno in dados:
    nome = aluno['Nome']
    email = aluno['E-mail']
    venc = aluno['Vencimento']
    try:
        venc_data = datetime.datetime.strptime(venc, "%d/%m/%Y").date()
        dias_restantes = (venc_data - hoje).days
        if 0 <= dias_restantes <= 5:  # Ajuste o range como preferir
            envia_email(email, nome)
    except Exception as e:
        print(f"Erro com {nome}: {e}")

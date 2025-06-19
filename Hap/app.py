
from flask import Flask, request, render_template_string
import bcrypt, uuid, time
from email.message import EmailMessage
import smtplib

app = Flask(__name__)
tokens = {}

@app.route('/esqueci-senha')
def esqueci_senha():
    return render_template_string(open('forgot_password.html').read())

@app.route('/enviar-token', methods=['POST'])
def enviar_token():
    email = request.form['email']
    token = str(uuid.uuid4())
    tokens[token] = {'email': email, 'expira': time.time() + 900}
    enviar_email(email, token)
    return 'Um link foi enviado para seu e-mail.'

def enviar_email(destinatario, token):
    link = f"http://localhost:5000/nova-senha?token={token}"
    msg = EmailMessage()
    msg['Subject'] = "Redefinição de Senha - Instituto Dok Su Ri"
    msg['From'] = "institutodoksuri@gmail.com"
    msg['To'] = destinatario
    msg.set_content(f"Clique no link para redefinir sua senha: {link}")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("institutodoksuri@gmail.com", "SUA_SENHA_AQUI")
        smtp.send_message(msg)

@app.route('/nova-senha')
def nova_senha():
    token = request.args.get('token')
    if token not in tokens or tokens[token]['expira'] < time.time():
        return "Token expirado ou inválido."
    return render_template_string(open('reset_password.html').read().replace("{{token}}", token))

@app.route('/redefinir-senha', methods=['POST'])
def redefinir():
    token = request.form['token']
    senha_nova = request.form['senha']
    if token not in tokens or tokens[token]['expira'] < time.time():
        return "Token expirado ou inválido."
    senha_hash = bcrypt.hashpw(senha_nova.encode(), bcrypt.gensalt()).decode()
    # Aqui deve atualizar no Google Sheets
    del tokens[token]
    return "Senha atualizada com sucesso."

if __name__ == '__main__':
    app.run(debug=True)

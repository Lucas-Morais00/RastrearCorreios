import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from twilio.rest import Client

app = Flask('IntegracaoCorreios')

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/enviado')
def enviado():
	#Scrapping Correio
	codigo = request.args.get('codigo')
	url = f'https://www.linkcorreios.com.br/?id={codigo}'

	try:
		r_correio = requests.get(url)
	except:
		print(f"{url} nao disponivel")

	html_correio = r_correio.text

	soup = BeautifulSoup(html_correio, 'html.parser')

	classe = soup.find("div", class_="card-header") 
	li_list = classe.find_all("li")
	status = classe.find_all("b")

	info_list = []

	for item in li_list:
		info_list.append(item.string)

	info_list.append(status)

	info_list.pop(0)

	data = info_list[0]
	local = info_list[1]
	status = str(info_list[2])
	status = status.replace("<b>",'').replace("</b>",'')
	status = status.replace("[",'').replace("]",'')
	if 'Ã' in status:
		status = status.replace("Ã¡","á" )

	#Twilio
	account_sid = 'SID_TWILIO'
	auth_token = 'TOKEN_TWILIO'
	client = Client(account_sid, auth_token)
	numero = request.args.get('numero')
	numero = numero.replace('%','').replace('B','')
	numero = '+'+ numero
	
	client.messages.create(
		to=numero,
		from_='NUMERO_TWILIO',
		body= f"Status da compra: {status}, {data}, {local}"
		)

	return render_template('enviado.html')


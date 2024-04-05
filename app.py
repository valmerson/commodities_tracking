import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import pytz
import randomheaders
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from google.oauth2.service_account import Credentials
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def limpa_texto(text):
  return text.replace('\r', '').replace('\n', '').strip()

def coleta_dados_commodities(trade_sopa):
  trade_total = trade_sopa.findAll('div', {'class': 'col-xl-12'})
  trade_total_string = trade_total[0]
  trade_headers = trade_total_string.find('tr')
  headers = limpa_texto(trade_headers.text)

  trade_elemento = trade_total_string.findAll('td', {'class': 'datatable-item-first'})
  trade_elemento_total = [limpa_texto(elemento.find('b').text) for elemento in trade_elemento]

  trade_preco = trade_total_string.find_all('td', id='p')
  trade_preco_total = [limpa_texto(preco.get_text()) for preco in trade_preco]

  trade_day = trade_total_string.find_all('td', id='nch')
  trade_day_total = [limpa_texto(day.get_text()) for day in trade_day]

  trade_percent = trade_total_string.find_all('td', id='pch')
  trade_percent_total = [limpa_texto(percent.get_text()) for percent in trade_percent]

  trade_period = trade_total_string.find_all('td', {'class': 'datatable-item datatable-heatmap'})
  trade_period_total = [limpa_texto(period.get_text()) for period in trade_period]

  trade_weekly_total = [trade_period_total[i] for i in range(0, len(trade_period_total), 3)]
  trade_monthly_total = [trade_period_total[i] for i in range(1, len(trade_period_total), 3)]
  trade_yoy_total = [trade_period_total[i] for i in range(2, len(trade_period_total), 3)]

  trade_date = trade_total_string.find_all('td', id='date')
  trade_date_total = [limpa_texto(date.get_text()) for date in trade_date]

  trade_area = ['Energy'] * 14 + ['Metals'] * 9 + ['Agricultural'] * 22 + ['Industrial'] * 26 + ['Livestock'] * 8 + ['Index'] * 9 + ['Electricity'] * 5

  trade_unit = trade_total_string.findAll('div', style='font-size: 10px;')
  trade_unit_total = [limpa_texto(unit.get_text()) for unit in trade_unit]

  br_time = pytz.timezone('America/Sao_Paulo')
  collection_date = datetime.datetime.now(br_time)
  
  df_trade_final = pd.DataFrame({
    'Market Area': trade_area,
    'Element': trade_elemento_total,
    'Unit': trade_unit_total,
    'Price': trade_preco_total,
    'Day': trade_day_total,
    '%': trade_percent_total,
    'Weekly %': trade_weekly_total,
    'Monthly %': trade_monthly_total,
    'YoY %': trade_yoy_total,
    'Date': trade_date_total,
    'Scraping Date': collection_date
  })
  return df_trade_final

#Raspagem da fonte e organização do DF final e da lista com sublistas de referência para chamada no html dinâmico que será enviado por e-mail     
trade_econo=requests.get('https://tradingeconomics.com/commodities', headers=randomheaders.LoadHeader())
if trade_econo.status_code ==200:
   trade_html=trade_econo.content
   trade_sopa=BeautifulSoup(trade_html)
   print("A requisição foi concluída com sucesso")
else: 
   print(f"A requisição retornou o erro: {trade_econo.status_code}") 

df_trade_final = coleta_dados_commodities(trade_sopa)
df_trade_final['Scraping Date'] = df_trade_final['Scraping Date'].astype(str)
lista_dados_final=[df_trade_final.columns.tolist()]+df_trade_final.values.tolist()


#conexão e envio da tabela final para o google sheets
API_GOOGLE_SHEETS=os.environ["api_google_sheets"]
SHEET_ID=os.environ["google_sheets_id"]

credencial=(API_GOOGLE_SHEETS)
conta_servico = ServiceAccountCredentials.from_json_keyfile_name(credencial)
API_acesso= gspread.authorize(conta_servico)
table = API_acesso.open_by_key(SHEET_ID)
sheet_id= table.worksheet("commodities")

sheet_id.append_rows(lista_dados_final)

#Configuração do envio do e-mail com html dinâmico
EMAIL_KEY=os.environ["email_key"]
BREVO_PASSWORD=os.environ["brevo_credential"]

smtp_server = "smtp-relay.brevo.com"
port = 587
email = EMAIL_KEY 
password = BREVO_PASSWORD  


remetente = "EMAIL_KEY"  
destinatarios = ["professional_email_key","email_key"]  
titulo = "Weekly Commodities Price Tracking Status"
html = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Commodities Tracking</title>
  </head>
  <body>
    <h1>Commodities Price tracking</h1>
    <p>
      The last data collection worked! Your most recent data is: 
      
"""
ultimo_elemento = lista_dados_final[-1][-1]
html += f'<p> <b> {ultimo_elemento} <b/> </p>'

selected_values_mail=[]
for lista in lista_dados_final:
    selected_values=lista[1:4]
    selected_values_mail.append(selected_values)

html += f' <ul> <p> See below the main up-to-date prices from the international commodities market:</p>'
html += f'<p> <span style="color: black">&bull;</span> <b>Element: </b> {selected_values_mail[0][0]}, <b>Currency/Unit: </b>{selected_values_mail[0][1]}, <b>Price: </b>{selected_values_mail[0][2]} </p>' 
html += f'<p> <span style="color: black">&bull;</span> <b>Element: </b> {selected_values_mail[1][0]}, <b>Currency/Unit: </b>{selected_values_mail[1][1]}, <b>Price: </b>{selected_values_mail[1][2]} </p>'
html += f'<p> <span style="color: black">&bull;</span> <b>Element: </b> {selected_values_mail[2][0]}, <b>Currency/Unit: </b>{selected_values_mail[2][1]}, <b>Price: </b>{selected_values_mail[2][2]} </p>'
html += f'<p> <span style="color: black">&bull;</span> <b>Element: </b> {selected_values_mail[3][0]}, <b>Currency/Unit: </b>{selected_values_mail[3][1]}, <b>Price: </b>{selected_values_mail[3][2]} </p>'
html += f'<p> <span style="color: black">&bull;</span> <b>Element: </b> {selected_values_mail[4][0]}, <b>Currency/Unit: </b>{selected_values_mail[4][1]}, <b>Price: </b>{selected_values_mail[4][2]} </ul></p>'
html += f'<p> <b>Source: </b> Trade Economics </p>'
html += f'<p> To have access to the full data base including all the updated commodities price information, request access to: "https://docs.google.com/spreadsheets/d/1-9nbK5vvsNxUZavn6nV2rj5bj26f6gBNEAL67bLTy3E/edit#gid=0"</p>'
html += f'<p>Kindest Regards</p>'
html += f'<p>Valmerson Silva</p>'  
html += f'<p>BMI LATAM Team</p>'

html += """
      </p>
  </body>
</html>
"""

server = smtplib.SMTP(smtp_server, port) 
server.starttls() 
server.login(email, password) 


mensagem = MIMEMultipart()
mensagem["From"] = remetente
mensagem["To"] = ",".join(destinatarios)
mensagem["Subject"] = titulo
conteudo_html = MIMEText(html, "html") 
mensagem.attach(conteudo_html)

#Envio do e-mail 
server.sendmail(remetente, destinatarios, mensagem.as_string())
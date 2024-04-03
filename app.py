from flask import Flask
import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import pytz
import randomheaders
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

@app.route("/commoditiestracking", methods=["POST"])
def commoditie_tracking():
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
     
    trade_econo=requests.get('https://tradingeconomics.com/commodities', headers=randomheaders.LoadHeader())
    if trade_econo.status_code ==200:
     trade_html=trade_econo.content
     trade_sopa=BeautifulSoup(trade_html)
     print("A requisição foi concluída com sucesso")
    else: 
     print(f"A requisição retornou o erro: {trade_econo.status_code}") 

    df_trade_final = coleta_dados_commodities(trade_sopa)
    lista_dados_final=[df_trade_final.columns.tolist()]+df_trade_final.values.tolist()

    credencial=("api_google_sheets")
    conta_servico = ServiceAccountCredentials.from_json_keyfile_name(credencial)
    API_acesso= gspread.authorize(conta_servico)
    table = API_acesso.open_by_key("google_sheets_id")
    sheet_id= table.worksheet("commodities")

    ultimo_elemento = lista_dados_final[-1][-1]

    # Template HTML com o último elemento incluído dinamicamente
    html_template = f"""
    <!DOCTYPE html>
      <html lang="pt-br">
       <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Commodities Tracking: Control Tower</title>
       </head>
       <body>F
        <h1>Último Momento:</h1>
         <p>{ultimo_elemento}</p>
       </body>
       </html>
       """

# html = """
# <!DOCTYPE html>
# <html>
#   <head>
#     <title>Commodities Tracheing </title>
#   </head>
#   <body>
#     <h1>Ronda Estadão</h1>
#     <p>
#       As matérias encontradas foram:
#       <ul>
# """
# for materia in materias_home_estadao():
#     palavras = normaliza(materia["titulo"]).split(" ")
#     if "dengue" in palavras or "lula" in palavras or "bolsonaro" in palavras:
#         html += f'<li> <a href="{materia["url"]}">{materia["titulo"]}</a> </li>'
# html += """
#       </ul>
#     </p>
#   </body>
# </html>
# """


# # Pegar o último elemento da lista
# ultimo_elemento = lista_dados_final[-1]

# # Template HTML com o último elemento incluído dinamicamente
# html_template = f"""
# <!DOCTYPE html>
# <html lang="pt-br">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Commodities Tracking: Control Tower</title>
# </head>
# <body>
#     <h1>Último Momento:</h1>
#     <p>{ultimo_elemento}</p>
# </body>
# </html>
# """

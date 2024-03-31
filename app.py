trade_econo=requests.get('https://tradingeconomics.com/commodities', headers=randomheaders.LoadHeader())
if trade_econo.status_code ==200:
    trade_html=trade_econo.content
    trade_sopa=BeautifulSoup(trade_html)
    print("A requisição foi concluída com sucesso")
else: 
    print(f"A requisição retornou o erro: {trade_econo.status_code}")   
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


Este é o repositório dedicado ao projeto **"Weekly Commodities Price Tracking Status"** desenvolvido po mim, Valmerson Silva no bojo da Disciplina Algoritmos de Automação do Master em Jornalismo de Dados, Automação e Data Storytelling do INSPER, ministrada por Alvaro Justen. 

O código executa a raspagem e organização de dados de **preço das Commodities no mercado internacional** tendo como fonte a Trading Economics e **atualiza semanalmente de forma automática** uma planilha de referência no google sheets. 
Após a coleta e armazenamento, um **e-mail com html dinâmico é disparado automaticamente para um mailing estratégico** informando os detalhes da coleta, e as informações 
de preço das principais commodities na data, além de apresentar o caminho para a planilha com os dados completos armazenados. 

Qualquer dúvida, uso, replicação ou sugestão do/no código desenvolvido deve ser orientada para o e-mail: **valmerson.sistema@gmail.com**
O projeto é coberto pelas seguintes etapas: 

1-Raspagem de Dados:
Utilizamos bibliotecas Python, como BeautifulSoup e Requests, para extrair dados de preços de commodities de um site confiável.
As informações coletadas incluem o preço atual de 93 commodities diferentes, bem como as variações de preço em relação à última semana, mês e ano.

2-Armazenamento e Manipulação de Dados:
Os dados coletados são armazenados em uma planilha do Google Sheets.
Registramos a data e hora da coleta para rastreabilidade e análise histórica.
Utilizamos técnicas de manipulação de dados para extrair informações relevantes e gerar relatórios dinâmicos.

3-Envio de Email Dinâmico:
O sistema gera automaticamente um e-mail HTML dinâmico com os dados mais recentes das commodities.
Os destinatários específicos recebem o e-mail com informações sobre a última coleta, juntamente com os registros das 5 principais commodities da indústria de eletrodomésticos.

Benefícios do Projeto:
Redução significativa do tempo gasto na coleta e distribuição manual de dados.
Disponibilização de informações atualizadas e relevantes para tomada de decisão estratégica.
Maior eficiência e precisão na análise de tendências de mercado e variações de preços.

Site inicial: https://commodities-tracking.onrender.com/


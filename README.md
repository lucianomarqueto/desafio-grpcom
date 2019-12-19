# Desafio - GRPCOM

# ETL
Todo o tratamento do dados e cálculos são efetuados pelo script  `src/etl.py` o script está comentado linha a linha para facilitar o entendimento.
Para execução local do script é necessário instalar os itens abaixo:


```sh
Python 3.7
pandas
```

# Dashboard

Click para acesse o [DASHBOARD](https://lucianomarqueto.github.io/desafio-grpcom/) 

O aquivo `index.html` conten um JS para criação do gráfico utilizando a lib highcharts, o JS utiliza o `/data/result/chart.json` como fonte de dados para o gráfico, esse arquivo foi criado ao executar o script python `src/etl.py`

Nenhuma intalação é necessária para execução local no entanto pode ocorrer um erro de [CORS](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Controle_Acesso_CORS) quando o JS tenta obter o aquivo JSON se os aquivos não estiverem sendo servido adequadamente por um serviço. Para simplicar uma execução local é possível descomentar o bloco de linhas após a linha 190 e carregar o JSON manualmente na variável.

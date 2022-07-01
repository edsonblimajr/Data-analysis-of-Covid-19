# Data-analysis-of-Covid-19
Analise da dados da Covid-19 da cidade de Arcoverde - Pernambuco.

O objetivo deste trabalho é analisar os dados da Covid-19 da cidade de
Arcoverde que está localizada no estado de Pernambuco. A análise dos dados foi
feita a partir do cálculo do ajuste polinomial dos dados, utilizando o Método dos
Mínimos Quadrados, ao qual foi implementado em uma linguagem computacional, o
Python.
Os dados da Covid-19 da cidade de Arcoverde, foram obtidos no site
https://covid.saude.gov.br/, no dia 1 de outubro 2021, e por meio deles, foram
calculados a média móvel para uma janela de 7 dias dos casos novos diários e o
ajuste polinomial do número de casos confirmados acumulados para uma janela de
21 dias. Varrendo todos os dias dos dados realizamos uma extrapolação do ajuste
efetuando uma previsão para o próximo dia dos casos confirmados acumulado.

# Execução
## 1. Python 3.8+
## 2. Instalações necéssarias no terminal
    pip install numpy
   
    pip install pandas
   
    pip install openpyxl

## 3. Executar no terminal ou Compilar em uma IDE
    analise_calculo_numerico.py
    
Após a execução do código será criado na pasta local do arquivo duas tabelas .xlsx, contendo os coeficientes de previsões para o 21º dia e da média movel do periodo de 7 dias dos casos analisados.

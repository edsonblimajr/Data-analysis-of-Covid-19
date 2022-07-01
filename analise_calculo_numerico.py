# Aluno: Edson Barbosa Lima Junior
# Trabalho Calculo Numerico

import numpy as np
import pandas as pd

# Lendo os dados do covid-19 da cidade de Arcoverde-PE
dados_BD = pd.read_excel("ARCOVERDE_PE_HIST_PAINEL_COVIDBR_01out2021.xlsx")

# Listas Globais
lista_dias = []
lista_v1 = []
lista_casos_acumulados = []
lista_casos_novos = []
lista_casos_acumulados = dados_BD["casosAcumulado"].tolist()
lista_casos_novos = dados_BD["casosNovos"].tolist()
lista_datas7 = dados_BD["data"].tolist()
lista_datas21 = dados_BD["data"].tolist()
for i in range(1,len(lista_casos_acumulados)+1):
  lista_dias.append(int(i))
  lista_v1.append(int(1))
del(lista_datas21[0:21])

# Funcao que Calcula as Medias Moveis dos casos novos em uma janela de 7 dias
def media_movel_7dias():
  pos = ind = 7
  aux = valor_sum_7dias = 0
  lista_valor_sum_7dias = []
  media_movel = []
  while pos < len(lista_dias)+1:
    for _ in range(1):
      lista_7dias = lista_casos_novos[aux:aux+ind]
      valor_Sum_7dias = sum(lista_7dias)
      lista_valor_sum_7dias.append(valor_Sum_7dias)
      media_movel.append(round((valor_Sum_7dias/ind),4))
      # Data Frame contendo as listas da janela de dias, dos valores do somatorio dos 7 dias e da media movel
      data_frame1 = pd.DataFrame(list(zip(lista_datas7,lista_valor_sum_7dias,media_movel)), columns = ["Dia","Sum7dias"," Media.Movel"])
    aux += 1
    pos +=1
  # Criando a tabela do excel contendo os dados presentes no Data Frame  
  data_frame1.to_excel("TabelaMediaMovel7dias.xlsx",index=False,na_rep="  NaN")
  
# Funcao que calcula o erro do ajuste
def erro_do_ajuste(valor_a0,valor_a1,valor_a2):
  soma_desvio = 0.0
  for c in range(0,21):
    funcao = valor_a0 + valor_a1 * (c+1) + valor_a2 * pow(c+1,2) 
    soma_desvio += ((pow((funcao - lista_casos_acumulados[c]),2))/21)
  
  return (pow(soma_desvio,1/2))

# Funcao que calcula o sistema linear, retornando uma lista contendo os coeficientes a0, a1 e a2
def calculo_sistema_linear(g1g1,g1g2,g1g3,g2g1,g2g2,g2g3,g3g1,g3g2,g3g3,fxg1,fxg2,fxg3):
  #Calculando o sistema linear para encontrar os coeficientes a0,a1,a2
  A = np.array([[g1g1,g1g2,g1g3],[g2g1,g2g2,g2g3],[g3g1,g3g2,g3g3]])
  #print(A) 
  B = np.array([[fxg1],[fxg2],[fxg3]])
  #print(B)        
  X = np.linalg.solve(A,B).tolist()
  return (X)

# Funcao que calcula o erro relativo em %
def erro_relativo(pos2,valor_previsao):
  erro_rel = abs((valor_previsao - np.float64(lista_casos_acumulados[pos2-1]))/np.float64(lista_casos_acumulados[pos2-1]))*100
  return (erro_rel)

# Principal funçao do codigo, calcula o desvio quadratico medio, e chama as outras funcoes
def desvio_quadratico_medio():
  pos2 = ind2 = 21
  aux2 = 0
  g1g1 = g1g2 = g1g3 = g2g1 = g2g2 = g2g3 = 0.0
  g3g1 = g3g2 = g3g3 = fxg1 = fxg2 = fxg3 = 0.0
  valor_a0 = valor_a1 = valor_a2 = valor_previsao = 0.0
  a0 = []
  a1 = []
  a2 = []
  previsao = []
  lista_erro_ajuste = []
  lista_erro_relativo = []
  casos_confirmados = []    
  while pos2 < len(lista_dias)+1:
    for j in range(1):
      arrayg1 = np.array([lista_v1[aux2:aux2+ind2]])
      arrayg2 = np.array([lista_dias[0:21]])
      arrayfx = np.array([lista_casos_acumulados[aux2:aux2+ind2]])
      #Produto interno para calcular os (g)ij
      for k in arrayg1:
        g1g1 += np.array(np.dot(k,k)) 
      for l in arrayg2:
        arrayg3 = np.array([l*l])    
      for k in arrayg1:
        for l in arrayg2:
          g1g2 += np.array(np.dot(k,l))
          g2g2 += np.array(np.dot(l,l))
      for k in arrayg1:
        for m in arrayg3:
          g1g3 += np.array(np.dot(k,m))
          g3g3 += np.array(np.dot(m,m))
      for l in arrayg2:
        for m in arrayg3:
          g2g3 += np.array(np.dot(l,m))
      for o in arrayfx:
        for k in arrayg1:
          fxg1 += np.array(np.dot(o,k))
      for o in arrayfx:
        for l in arrayg2:
          fxg2 += np.array(np.dot(o,l))
      for o in arrayfx:
        for m in arrayg3:
          fxg3 += np.array(np.dot(o,m))         
      g2g1 = g1g2
      g3g1 = g1g3
      g3g2 = g2g3  
      # Chamando a funcao calculo_sistema_linear para encontrar os coeficientes
      coeficientes = calculo_sistema_linear(g1g1,g1g2,g1g3,g2g1,g2g2,g2g3,g3g1,g3g2,g3g3,fxg1,fxg2,fxg3)
      # Valores de a0, a1 e a2
      valor_a0 = coeficientes[0][0]
      valor_a1 = coeficientes[1][0]
      valor_a2 = coeficientes[2][0]
      a0.append(round(float(coeficientes[0][0]),4))
      a1.append(round(float(coeficientes[1][0]),4))
      a2.append(round(float(coeficientes[2][0]),4))        
      # Calculo da previsao para o dia 22, para os diferentes coeficientes encontrados
      valor_previsao = valor_a0 + valor_a1 * 22 + valor_a2 * pow(22,2)
      previsao.append(round(valor_previsao,4))
      # Chamando a funcao erro_do_ajuste para encontrar o erro do ajuste pelo Desvio Padrao
      valor_erro_ajuste = erro_do_ajuste(valor_a0,valor_a1,valor_a2)
      lista_erro_ajuste.append(round(valor_erro_ajuste,4))
      # Chamando a funcao erro_relativo para encontrar o erro relativo
      valor_erro_relativo = erro_relativo(pos2,valor_previsao)
      lista_erro_relativo.append(round(valor_erro_relativo,2))
      # Lista contendo os casos acumulados
      casos_confirmados.append(lista_casos_acumulados[pos2-1])
      # Data Frame contendo as listas dos coeficientes, dos erros do ajuste, das previsoes, dos casos confirmados e do erro relativo
      data_frame2 = pd.DataFrame(list(zip(lista_datas21,a0,a1,a2,lista_erro_ajuste,previsao,casos_confirmados,lista_erro_relativo)), columns = ['Dia','a0.pol','a1.pol','a2.pol','Erro.pol','Previsao','Casos.Conf',' Erro.Prev(%)'])       
    g1g1 = g1g2 = g1g3 = g2g1 = g2g2 = g2g3 = 0.0
    g3g1 = g3g2 = g3g3 = fxg1 = fxg2 = fxg3 = 0.0
    aux2 += 1
    pos2 += 1
  data_frame2.to_excel("TabelaCoeficientePrevisoes.xlsx",index=False,na_rep="  NaN")
 
# Como na funcao erro_relativo retorna valores 'NaN', o python retorna Warning, codigo abaixo impede de aparecer esse Warning
import warnings
warnings.filterwarnings("ignore")

# Funcao main chamando as funcoes media_movel_7dias e desvio_quadratico_medio 
def main():
  print("Executando codigo... ")
  media_movel_7dias()
  desvio_quadratico_medio()
  print("Codigo Executado com sucesso! ")
  print("As tabelas TabelaCoeficientePrevisoes e TabelaMediaMovel7dias foram criadas na pasta onde está o arquivo trabalho_calculo_numerico.py! ")

  

# Chamando a funcao main para a execucao do codigo
if __name__ == "__main__":
  main()

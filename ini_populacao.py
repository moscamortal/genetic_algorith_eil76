import random as rd
from math import sqrt

pontos_mapa = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75]
ponto_posic_X = [22,36,21,45,55,33,50,55,26,40,55,35,62,62,62,21,33,9,62,66,44,26,11,7,17,41,55,35,52,43,31,22,26,50,55,54,60,47,30,30,12,15,16,21,50,51,50,48,12,15,29,54,55,67,10,6,65,40,70,64,36,30,20,15,50,57,45,38,50,66,59,35,27,40,40,40]
ponto_posic_Y = [22,26,45,35,20,34,50,45,59,66,65,51,35,57,24,36,44,56,48,14,13,13,28,43,64,46,34,16,26,26,76,53,29,40,50,10,15,66,60,50,17,14,19,48,30,42,15,21,38,56,39,38,57,41,70,25,27,60,64,4,6,20,30,5,70,72,42,33,4,8,5,60,24,20,37,40]
populacao_Main = []
distancias = []
valor_rota = []
tamanho_populacao = 50
menor = 999999
distancia_geracoes = []
melhor_cada_geracao = []

def permutar_populacao():
    vet_permutado=[]
    for i in range(tamanho_populacao):
        vet_permutado.append(rd.sample(pontos_mapa,76))
        i = i+1
    return vet_permutado

def distancia_pontos(populacao,distancias):
    distancias_temp = []
    distancias.clear()
    for i in range(len(populacao)):
        for j in range(75):
            indice_A = populacao[i][j]
            indice_B = populacao[i][j+1]

            xA = ponto_posic_X[indice_A]
            yA = ponto_posic_Y[indice_A]

            xB = ponto_posic_X[indice_B]
            yB = ponto_posic_Y[indice_B]

            a = (xB-xA)**2 + (yB-yA)**2
            raiz = int(sqrt(a))
            distancias_temp.append(raiz)

        distancias.append(distancias_temp.copy())
        distancias_temp.clear()
        #print(distancias[i])

def valor_total_rota(populacao):
    valor_rota.clear()
    for i in range(tamanho_populacao):
        total = sum(distancias[i])
        valor_rota.append(total)


def calc_menor_distancia(disntacias):
    minimo = min(disntacias)
    return disntacias.index(minimo)

def valor_menor_rota(disntacias):
    minimo = min(disntacias)
    return minimo

def reproducao(indice_melhor, populacao_Atual):
    nova_populacao = []
    nova_populacao.append(populacao_Atual[indice_melhor])
    for i in range (tamanho_populacao):
        corte = gerar_aleatorio(1,75)
        pedaco_1 = nova_populacao[0][0:corte]
        pedaco_2 = populacao_Atual[i][corte:len(populacao_Atual[0])]
        nova_populacao.append(pedaco_1+pedaco_2)
        #Validar se a solução é factivel
        validar_solucao(nova_populacao)
        #nova_populacao.append(populacao_Atual[[1:corte] + populacao_Atual[corte:len(populacao_Atual)]])
    return nova_populacao

def gerar_aleatorio(a,b):
    aleatorio = rd.randint(a,b)
    return aleatorio

def validar_solucao(nova_populacao):
    itens_duplicado = []
    itens_faltando = []
    for i in range(len(nova_populacao)):
        for j in range(len(pontos_mapa)):
            if nova_populacao[i].count(pontos_mapa[j]) > 1:
                itens_duplicado.append(nova_populacao[i].index(pontos_mapa[j]))
                #print(nova_populacao[i].index(pontos_mapa[j]))
            if nova_populacao[i].count(pontos_mapa[j]) < 1:
                itens_faltando.append(pontos_mapa[j])
        solucao_ajustada = ajuste_solucao(itens_duplicado,itens_faltando,nova_populacao,i)
        nova_populacao[i] = solucao_ajustada
    return nova_populacao

def ajuste_solucao(itens_duplicado,itens_faltando,nova_populacao,indice):
    for i in range(len(itens_faltando)):
        nova_populacao[indice][itens_duplicado[i]] = itens_faltando[i]
    return nova_populacao[indice]

def chance_mutacao():
    chance = rd.randint(0,100) < 10
    return chance

def mutacao(populacao_Main):
    for i in range(tamanho_populacao):
        for j in range(len(populacao_Main[i])):
            if chance_mutacao():
                trocado1 =  populacao_Main[i][j]
                trocado2 = rd.randint(0,75)
                populacao_Main[i][j] = populacao_Main[i][trocado2]
                populacao_Main[i][trocado2] = trocado1
        validar_solucao(populacao_Main)
    return populacao_Main

#______________________________ MAIN
def main():
    ## Gerando a população inicial
    populacao_Main = permutar_populacao()

    ##Loop de gerações
    for i in range (100):
        ##Calculando valor total das diastancias
        distancia_pontos(populacao_Main,distancias)

        ##Calcula o valor de todas as distâncias
        valor_total_rota(populacao_Main)

        ##Seleção
        indice_melhor_caminho = calc_menor_distancia(valor_rota)

        ##Reprodução
        populacao_Main = reproducao(indice_melhor_caminho,populacao_Main)

        ##Mutação
        mutacao(populacao_Main)

        ##Calcula o valor de todas as distâncias
        valor_total_rota(populacao_Main)

        ##Seleção
        indice_melhor_caminho = calc_menor_distancia(valor_rota)

        ##Memoria de soluções
        distancia_geracoes.append(valor_menor_rota(valor_rota))
        melhor_cada_geracao.append(populacao_Main[indice_melhor_caminho])

        #print("Solução da " + str(i) + "° geração" + str(populacao_Main[indice_melhor_caminho]))
        print("Menor distancia: " + str(valor_menor_rota(valor_rota)))

    print("Menor valor de rota: " + str(min(distancia_geracoes)))
    print(populacao_Main[indice_melhor_caminho])

if __name__ == '__main__':
    main()
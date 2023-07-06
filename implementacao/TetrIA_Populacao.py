# Trabalho final da Disciplina INF 420
# Objetivos: Desenvolvimento de um sistema de inteligência artificial para obter altas pontuações no Tetris utilizando algoritmo genético
# Criado por Rafael Zardo (ES105468) e Pedro Fiorio (ES105475) em 15/06/2023

import pygame
import sys
import copy
import time
from Tabuleiro import Tabuleiro
from Blocos import *
from Jogo import Jogo
from Individuo import Individuo
from Populacao import Populacao
import re

def getParametrosPopulacao():
    arquivoEntrada = './inputs/populacao.txt'
    parametros = []
    cont = 0

    # Expressão regular para extrair os valores numéricos
    expressaoRegular = r'[-+]?\d*\.\d+|\d+'

    with open(arquivoEntrada, 'r') as arquivo:
        for linha in arquivo:
            if cont == 3:
                valores = re.findall(expressaoRegular, linha) # Procura por valores numéricos na linha utilizando expressão regular
                for valor in valores:
                    parametros.append(float(valor))
            else:
                valores = re.findall(expressaoRegular, linha) # Procura por valores numéricos na linha utilizando expressão regular
                for valor in valores:
                    parametros.append(int(valor))
            cont += 1

    return parametros

# Definido a população
parametros = getParametrosPopulacao()

# Tratamento de excessão
if parametros[0] <= 2:
    sys.stderr.write("ERRO: o tamanho da população deve ser maior que 2.\n")
    sys.exit()

populacao = Populacao(parametros[0], parametros[1], parametros[2], parametros[3])

pygame.init()

# Craição de fontes de texto
fonteTitulo = pygame.font.Font("./fontes/NEONLEDLight.otf",35)
fonteGenes = pygame.font.Font("./fontes/NEONLEDLight.otf",25)
textoPontos = fonteTitulo.render("Pontos", True, (255,255,255))
textoGeracao = fonteTitulo.render("Geração", True, (255,255,255))
textoIndividuo = fonteTitulo.render("Indivíduo", True, (255,255,255))
textoJogo = fonteTitulo.render("Jogo", True, (255,255,255))
textoGenes = fonteTitulo.render("Genes", True, (255,255,255))
textoTempo = fonteTitulo.render("Delay", True, (255,255,255))

# Música
pygame.mixer.music.load("./musica/musicaPrincipal.mp3")
pygame.mixer.music.play(-1)

# Definições globais do jogo
screen = pygame.display.set_mode((550,620)) # no caso do pygame, canto superior esquerdo e o 0,0
pygame.display.set_caption("TetrIA")
clock = pygame.time.Clock() 
FPS = 60
ESPERA = 1000

# Estilização de cores do display
fundo = (0,65,89)
fundoTexto = (224, 224, 224)
corTexto = (224, 224, 224)

# Inicialização do jogo
TetrIA = Jogo()

def floodFill(matriz, linha, coluna, celulaAlvo = 0, celulaNova= -1):
    # Verifica se as coordenadas estão dentro dos limites da matriz
    if linha < 0 or linha >= len(matriz) or coluna < 0 or coluna >= len(matriz[0]):
        return
    
    # Verifica se a célula atual tem o valor alvo
    if matriz[linha][coluna] != celulaAlvo:
        return
    
    matriz[linha][coluna] = celulaNova
    
    # Chamada recursiva para os vizinhos (cima, baixo, esquerda, direita)
    floodFill(matriz, linha - 1, coluna)
    floodFill(matriz, linha + 1, coluna)
    floodFill(matriz, linha, coluna - 1)
    floodFill(matriz, linha, coluna + 1)

# Retorna o número de buracos do tabuleiro
def getNumBuracos(tabuleiro):
    tempTabuleiro = tabuleiro.tabuleiro
    numBuracos = 0

    floodFill(tempTabuleiro, 0, 3)
    
    for linha in range(tabuleiro.numLinhas):
        for coluna in range(tabuleiro.numColunas):
            if tempTabuleiro[linha][coluna] == 0: numBuracos += 1

    return numBuracos

# Retorna a soma das diferenças de alturas entre as colunas
def getRugosidade(tabuleiro):
    tempTabuleiro = tabuleiro.tabuleiro
    alturas = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    rugosidade = 0

    for coluna in range(tabuleiro.numColunas):
        for linha in range(tabuleiro.numLinhas):
            if (tempTabuleiro[linha][coluna] != 0):
                alturas[coluna] = (20 - linha)
                break

    for i in range(len(alturas)-1):
        rugosidade += abs(alturas[i]-alturas[i+1])

    return rugosidade

# Retorna maior altura do tabuleiro
def getAltura(tabuleiro):
    tempTabuleiro = tabuleiro.tabuleiro
    alturas = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    for coluna in range(tabuleiro.numColunas):
        for linha in range(tabuleiro.numLinhas):
            if (tempTabuleiro[linha][coluna] != 0):
                alturas[coluna] = (20 - linha)
                break
    return max(alturas)


# Retorna a soma dos número de posições vazias abaixo da posição preenchida mais alta de cada coluna
def getNumSombras(tabuleiro):
    tempTabuleiro = tabuleiro.tabuleiro
    profundidade = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
    numSombras = 0
    
    for coluna in range(tabuleiro.numColunas):
        for linha in range(tabuleiro.numLinhas):
            if (tempTabuleiro[linha][coluna] != 0):
                profundidade[coluna] = linha
                break

    for coluna in range(tabuleiro.numColunas):
        for linha in range(profundidade[coluna], tabuleiro.numLinhas):
            if (tempTabuleiro[linha][coluna] == 0):
                numSombras += 1

    return numSombras
    
# Retorna um valor para um tabuleiro sendo aplicados os pesos do indivíduo
def funcaoAvaliacao(tabuleiro, pontosAntigo, pontosNovo, individuo):
    rugosidade = getRugosidade(tabuleiro)
    altura = getAltura(tabuleiro)
    numLinhasLimpasTopo = pontosNovo[1] - pontosAntigo[1] 
    numLinhasLimpasEmbaixo = pontosNovo[0] - pontosAntigo[0] 
    tempNumSombras = getNumSombras(tabuleiro)
    numBuracos = getNumBuracos(tabuleiro)
    numSombras = tempNumSombras - numBuracos

    return (numLinhasLimpasTopo * individuo.pesoLinhasLimpasTopo) + (numLinhasLimpasEmbaixo * individuo.pesoLinhasLimpasEmbaixo) - (numBuracos * individuo.pesoNumBuracos) - (rugosidade * individuo.pesoRugosidade) - (altura*individuo.pesoAltura) - (numSombras*individuo.pesoSombras)

# Algoritmo genético e visualização do jogo
for geracao in range(populacao.numGeracoes):
    numIndividuo = 1

    for individuo in populacao.getPopulacao():
        pontos = []
        numJogo = 1

        for i in range(populacao.numJogosIndividuo):

            # Loop principal do jogo
            while True:
                # O indivíduo testa suas jogadas possíveis
                jogadas = []
                tempTetrIA = copy.deepcopy(TetrIA)

                for estadoDeRotacao in range(4):
                    pontosAntigos = (tempTetrIA.pontosBaixo, tempTetrIA.pontosCima)

                    if (estadoDeRotacao != 0): tempTetrIA.rotacionar()
                    
                    for coluna in range(TetrIA.tabuleiro.numColunas):
                        temp2TetrIA = copy.deepcopy(tempTetrIA)

                        for i in range(5):
                            temp2TetrIA.moverParaEsquerda()

                        for i in range(coluna):
                            temp2TetrIA.moverParaDireita()

                        for moverBaixo in range(20):
                            posicao = temp2TetrIA.moverParaBaixoTreinamento()

                        temp2TetrIA.moverParaBaixo()

                        pontosNovos = (temp2TetrIA.pontosBaixo, temp2TetrIA.pontosCima)
                        avaliacao = funcaoAvaliacao(temp2TetrIA.tabuleiro, pontosAntigos, pontosNovos, individuo)

                        jogadas.append([avaliacao, posicao, estadoDeRotacao])

                # Escolhe a jogada com melhor função de avaliação e reproduz suas características
                melhorJogada = max(jogadas, key=lambda jogada: jogada[0])

                for rotacao in range(melhorJogada[2]):
                    TetrIA.blocoAtual.rotacionar()

                for i in range(5):
                    TetrIA.moverParaEsquerda()
                
                while True:
                    if TetrIA.blocoAtual.deslocamentoDaColuna == melhorJogada[1][1]:
                        break
                    TetrIA.moverParaDireita()   
                        
                for linha in range(melhorJogada[1][0]):
                    TetrIA.moverParaBaixoTreinamento()

                # Efetiva a jogada
                TetrIA.moverParaBaixo()

                # Trata das nossas interações com o jogo
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if TetrIA.fimDeJogo:
                            TetrIA.fimDeJogo = False
                            TetrIA.reiniciar()
                        
                        if event.key == pygame.K_DOWN and TetrIA.fimDeJogo == False:
                            ESPERA -= 100
                            if ESPERA < 0:
                                ESPERA = 0

                        if event.key == pygame.K_UP and TetrIA.fimDeJogo == False:
                            ESPERA += 100
                
                # Escreve as estatísticas na tela
                screen.fill(fundo)
                screen.blit(textoPontos, (340,20,50,50))
                textoPontosObtidos = fonteTitulo.render(str(TetrIA.pontos), True, (0,0,0))
                screen.blit(textoPontosObtidos, (340,50,50,50))

                screen.blit(textoGeracao, (340,100,50,50))
                textoNumGeracao = fonteTitulo.render(str(geracao+1)+"/"+str(populacao.numGeracoes), True, (0,0,0))
                screen.blit(textoNumGeracao, (340,130,50,50))

                screen.blit(textoIndividuo, (340,180,50,50))
                textoNumIndividuo = fonteTitulo.render(str(numIndividuo)+"/"+str(len(populacao.populacao)), True, (0,0,0))
                screen.blit(textoNumIndividuo, (340,210,50,50))

                screen.blit(textoJogo, (340,260,50,50))
                textoNumJogo = fonteTitulo.render(str(numJogo)+"/"+str(populacao.numJogosIndividuo), True, (0,0,0))
                screen.blit(textoNumJogo, (340,290,50,50))

                screen.blit(textoGenes, (340,340,50,50))
                textoValorGene1 = fonteGenes.render("Nb: " + str(round(individuo.pesoNumBuracos, 8)), True, (0,0,0))
                screen.blit(textoValorGene1, (340,370,50,50))

                textoValorGene2 = fonteGenes.render("Rg: " + str(round(individuo.pesoRugosidade, 8)), True, (0,0,0))
                screen.blit(textoValorGene2, (340,395,50,50))

                textoValorGene3 = fonteGenes.render("Lt: " + str(round(individuo.pesoLinhasLimpasTopo, 8)), True, (0,0,0))
                screen.blit(textoValorGene3, (340,420,50,50))

                textoValorGene4 = fonteGenes.render("Le: " + str(round(individuo.pesoLinhasLimpasEmbaixo, 8)), True, (0,0,0))
                screen.blit(textoValorGene4, (340,445,50,50))

                textoValorGene5 = fonteGenes.render("Al: " + str(round(individuo.pesoAltura, 8)), True, (0,0,0))
                screen.blit(textoValorGene5, (340,470,50,50))

                textoValorGene6 = fonteGenes.render("Sb: " + str(round(individuo.pesoSombras, 8)), True, (0,0,0))
                screen.blit(textoValorGene6, (340,495,50,50))

                screen.blit(textoTempo, (340,550,50,50))
                textoValorTempo = fonteTitulo.render(str(ESPERA/1000) + "s", True, (0,0,0))
                screen.blit(textoValorTempo, (340,580,50,50))

                # Verifica fim de jogo
                if (TetrIA.fimDeJogo == True): 
                    TetrIA.fimDeJogo = False
                    pontos.append(TetrIA.pontos)
                    TetrIA.reiniciar()
                    break

                # Atualiza todas as mudancas feitas no display
                TetrIA.desenhar(screen)
                pygame.display.update() 
                clock.tick(FPS)

                # Espera por TEMPO milissegundos
                pygame.time.wait(ESPERA)

            numJogo += 1  

        media = sum(pontos) / populacao.numJogosIndividuo
        individuo.pontos = media
        numIndividuo += 1

    # Funções auxiliares da população
    populacao.gravarResultados(geracao+1)
    populacao.encontrarMelhoresIndividuos()
    populacao.gerarFilhos()
    populacao.gerarNovaPopulacao()
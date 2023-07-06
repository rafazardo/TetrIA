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

def getPesosIndividuo():
    arquivoEntrada = './inputs/individuo.txt'
    pesos = []

    # Expressão regular para extrair os valores numéricos
    expressaoRegular = r'[-+]?\d*\.\d+|\d+'

    with open(arquivoEntrada, 'r') as arquivo:
        for linha in arquivo:
            valores = re.findall(expressaoRegular, linha) # Procura por valores numéricos na linha utilizando expressão regular
            
            for valor in valores:
                pesos.append(float(valor))

    return pesos

# Capturando características do player
pesos = getPesosIndividuo()
player = Individuo(pesos[0], pesos[1], pesos[2], pesos[3], pesos[4], pesos[5])

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
    
    # Verifica se a célula atual tem a célula alvo
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
def funcaoAvaliacao(tabuleiro, pontosAntigo, pontosNovo):
    rugosidade = getRugosidade(tabuleiro)
    altura = getAltura(tabuleiro)
    numLinhasLimpasTopo = pontosNovo[1] - pontosAntigo[1] 
    numLinhasLimpasEmbaixo = pontosNovo[0] - pontosAntigo[0] 
    tempNumSombras = getNumSombras(tabuleiro)
    numBuracos = getNumBuracos(tabuleiro)
    numSombras = tempNumSombras - numBuracos

    return (numLinhasLimpasTopo * player.pesoLinhasLimpasTopo) + (numLinhasLimpasEmbaixo * player.pesoLinhasLimpasEmbaixo) - (numBuracos * player.pesoNumBuracos) - (rugosidade * player.pesoRugosidade) - (altura * player.pesoAltura) - (numSombras * player.pesoSombras)

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
            avaliacao = funcaoAvaliacao(temp2TetrIA.tabuleiro, pontosAntigos, pontosNovos)

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

    screen.blit(textoGenes, (340,150,50,50))
    textoValorGene1 = fonteGenes.render("Nb: " + str(round(pesos[0], 8)), True, (0,0,0))
    screen.blit(textoValorGene1, (340,185,50,50))

    textoValorGene2 = fonteGenes.render("Rg: " + str(round(pesos[1], 8)), True, (0,0,0))
    screen.blit(textoValorGene2, (340,210,50,50))

    textoValorGene3 = fonteGenes.render("Lt: " + str(round(pesos[2], 8)), True, (0,0,0))
    screen.blit(textoValorGene3, (340,235,50,50))

    textoValorGene4 = fonteGenes.render("Le: " + str(round(pesos[3], 8)), True, (0,0,0))
    screen.blit(textoValorGene4, (340,260,50,50))

    textoValorGene5 = fonteGenes.render("Al: " + str(round(pesos[4], 8)), True, (0,0,0))
    screen.blit(textoValorGene5, (340,285,50,50))

    textoValorGene6 = fonteGenes.render("Sb: " + str(round(pesos[5], 8)), True, (0,0,0))
    screen.blit(textoValorGene6, (340,310,50,50))

    screen.blit(textoTempo, (340,550,50,50))
    textoValorTempo = fonteTitulo.render(str(ESPERA/1000) + "s", True, (0,0,0))
    screen.blit(textoValorTempo, (340,580,50,50))

    # Verifica fim de jogo
    if (TetrIA.fimDeJogo == True): 
        TetrIA.fimDeJogo = False
        TetrIA.reiniciar()
        break

    # Atualiza todas as mudancas feitas no display
    TetrIA.desenhar(screen)
    pygame.display.update() 
    clock.tick(FPS)

    # Espera por ESPERA milissegundos
    pygame.time.wait(ESPERA)
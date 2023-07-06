# Descição da classe:
# Essa classe é responsável por gerenciar os eventos e interações que ocorrem no jogo, desde movimentação
# de blocos, até modificações no tabuleiro

from Tabuleiro import Tabuleiro
from Blocos import *
import random

class Jogo:
    def __init__(self):
        self.tabuleiro = Tabuleiro()
        self.blocos = [BlocoI(), BlocoJ(), BlocoL(), BlocoO(), BlocoS(), BlocoT(), BlocoZ()]
        self.blocoAtual = self.getBlocoAleatorio()
        self.proximoBloco = self.getBlocoAleatorio()
        self.fimDeJogo = False
        self.pontos = 0
        self.pontosCima = 0
        self.pontosBaixo = 0     
        self.numBlocos = 0

    def getBlocoAleatorio(self):
        if (len(self.blocos) == 0):
            self.blocos = [BlocoI(), BlocoJ(), BlocoL(), BlocoO(), BlocoS(), BlocoT(), BlocoZ()]

        bloco = random.choice(self.blocos)
        self.blocos.remove(bloco)

        return bloco
    
    def desenhar(self, screen):
        self.tabuleiro.desenhar(screen)
        self.blocoAtual.desenhar(screen)

    def moverParaDireita(self):
        self.blocoAtual.mover(0,1)

        if (self.blocoEstaDentro() == False or self.blocoEncaixa() == False):
            self.blocoAtual.mover(0,-1)
            # self.travarBloco()

    def moverParaEsquerda(self):
        self.blocoAtual.mover(0,-1)

        if (self.blocoEstaDentro() == False or self.blocoEncaixa() == False):
            self.blocoAtual.mover(0,1)
            # self.travarBloco()

    def moverParaBaixo(self):
        self.blocoAtual.mover(1,0)

        if (self.blocoEstaDentro() == False or self.blocoEncaixa() == False):
            self.blocoAtual.mover(-1,0)    
            self.travarBloco()   

    def moverParaBaixoTreinamento(self):
        self.blocoAtual.mover(1,0)

        if (self.blocoEstaDentro() == False or self.blocoEncaixa() == False):
            self.blocoAtual.mover(-1,0)    
            return (self.blocoAtual.deslocamentoDaLinha, self.blocoAtual.deslocamentoDaColuna)     

        return (0,0)

    def rotacionar(self):
        self.blocoAtual.rotacionar()

        if (self.blocoEstaDentro() == False or self.blocoEncaixa() == False): self.blocoAtual.desfazerRotacao()

    def blocoEstaDentro(self):
        tiles = self.blocoAtual.getPosicoesCelulas()

        for tile in tiles: # Verifica se o bloco saio do tabuleiro
            if (self.tabuleiro.estaDentro(tile.linha, tile.coluna) == False):
                return False
            
        return True
    
    def travarBloco(self):
        tiles = self.blocoAtual.getPosicoesCelulas()

        for posicao in tiles:
            self.tabuleiro.tabuleiro[posicao.linha][posicao.coluna] = self.blocoAtual.id # Prenchendo os tiles com o id do bloco, para prende-la

        self.blocoAtual = self.proximoBloco
        self.proximoBloco = self.getBlocoAleatorio()

        numLinhasCompletadas, linhasCheias = self.tabuleiro.limparLinhasCheias()
        self.atualizarPontos(numLinhasCompletadas, linhasCheias)

        if self.blocoEncaixa() == False:
            self.fimDeJogo = True

        self.numBlocos += 1

    def blocoEncaixa(self):
        tiles = self.blocoAtual.getPosicoesCelulas()

        for tile in tiles:
            if (self.tabuleiro.estaVazio(tile.linha, tile.coluna) == False):
                return False
            
        return True
    
    def reiniciar(self):
        self.tabuleiro.resetar()
        self.blocos = [BlocoI(), BlocoJ(), BlocoL(), BlocoO(), BlocoS(), BlocoT(), BlocoZ()]
        self.blocoAtual = self.getBlocoAleatorio()
        self.proximoBloco = self.getBlocoAleatorio()
        self.pontos = 0
        self.numBlocos = 0

    def atualizarPontos(self, numLinhasCompletadas, linhasCheias):
        if numLinhasCompletadas == 1:
            self.pontos += 100
        elif numLinhasCompletadas == 2:
            self.pontos += 250
        elif numLinhasCompletadas == 3:
            self.pontos += 400      
        elif numLinhasCompletadas == 4:
            self.pontos += 1000                     
    
        for linha in linhasCheias:
            if linha <= 9:
                self.pontosCima += 1
            else:
                self.pontosBaixo += 1


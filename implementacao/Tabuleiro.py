# Descrição da classe:
# Concentra os métodos utilizados para verificações de eventos que ocorrem no tabuleiro
# durante o jogo

import pygame
from Cores import Cores

class Tabuleiro:
    def __init__(self):
        self.numLinhas = 20
        self.numColunas = 10
        self.tamanhoCelula = 30
        self.tabuleiro = list()
        self.cores = Cores().getCores()

        for i in range(self.numLinhas):
            linha = list()

            for j in range(self.numColunas):
                linha.append(0)

            self.tabuleiro.append(linha)
    
    def printTabuleiro(self):
        for linha in self.tabuleiro:
            print(linha)

    def desenhar(self, screen):
        for linha in range(self.numLinhas):
            for coluna in range(self.numColunas):
                valorCelula = self.tabuleiro[linha][coluna]
                rectCelula = pygame.Rect(coluna*self.tamanhoCelula + 11, linha*self.tamanhoCelula + 11, self.tamanhoCelula - 1, self.tamanhoCelula - 1)
                pygame.draw.rect(screen, self.cores[valorCelula],rectCelula)


    def estaDentro(self, linha, coluna):
        if (linha >= 0 and linha < self.numLinhas and coluna >= 0 and coluna < self.numColunas):
            return True
        
        return False

    def estaVazio(self, linha, coluna):
        if (self.tabuleiro[linha][coluna] == 0): return True
        
        return False

    def linhaCheia(self, linha):
        for coluna in range(self.numColunas):
            if self.tabuleiro[linha][coluna] == 0:
                return False
            
        return True

    def limparLinha(self, linha):
        for coluna in range(self.numColunas):
            self.tabuleiro[linha][coluna] = 0

    def abaixarLinha(self, linha, numLinhas):
        for coluna in range(self.numColunas):
            self.tabuleiro[linha+numLinhas][coluna] = self.tabuleiro[linha][coluna] 
            self.tabuleiro[linha][coluna] = 0

    def limparLinhasCheias(self):
        numLinhasCompletas = 0
        linhasCheias = []

        for linha in range(self.numLinhas-1, 0, -1):
            if self.linhaCheia(linha):
                self.limparLinha(linha)
                numLinhasCompletas += 1
                linhasCheias.append(linha)

            elif numLinhasCompletas > 0:
                self.abaixarLinha(linha, numLinhasCompletas)
        
        return numLinhasCompletas, linhasCheias
    
    def resetar(self):
        for linha in range(self.numLinhas):
            for coluna in range(self.numColunas):
                self.tabuleiro[linha][coluna] = 0

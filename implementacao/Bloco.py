# Descição da classe:
# Em resumo, a classe Bloco encapsula a lógica relacionada aos blocos do jogo Tetris, incluindo 
# movimento, rotação e manipulação das posições das células do bloco.

import pygame
from Cores import Cores
from Posicao import Posicao

class Bloco:
    def __init__(self, id):
        self.id = id
        self.celulas = dict() # Armazena os estados de rotação
        self.tamanhoCelula = 30
        self.estadoDeRotacao = 0
        self.cores = Cores().getCores()
        self.deslocamentoDaLinha = 0
        self.deslocamentoDaColuna = 0

    def desenhar(self, screen):
        tiles = self.getPosicoesCelulas()

        for tile in tiles:
            tileRect = pygame.Rect(tile.coluna*self.tamanhoCelula + 11, tile.linha*self.tamanhoCelula + 11, self.tamanhoCelula - 1, self.tamanhoCelula - 1)
            pygame.draw.rect(screen, self.cores[self.id], tileRect)

    def mover(self, linhas, colunas):
        self.deslocamentoDaLinha += linhas
        self.deslocamentoDaColuna += colunas

    def rotacionar(self):
        self.estadoDeRotacao += 1

        if (self.estadoDeRotacao == len(self.celulas)): self.estadoDeRotacao = 0

    def desfazerRotacao(self):
        self.estadoDeRotacao -= 1

        if (self.estadoDeRotacao == -1): self.estadoDeRotacao = len(self.celulas) - 1

    def getPosicoesCelulas(self):
        tiles = self.celulas[self.estadoDeRotacao]
        tilesMovidos = list()

        for posicao in tiles:
            posicao = Posicao(posicao.linha + self.deslocamentoDaLinha, posicao.coluna + self.deslocamentoDaColuna)
            tilesMovidos.append(posicao)

        return tilesMovidos
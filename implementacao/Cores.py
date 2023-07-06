# Descrição da classe:
# Classe auxiliar para coloração dos blocos

class Cores:
    def __init__(self):
        cinza = (20, 20, 20)
        verde = (0, 255, 0)
        roxo = (153, 0, 153)
        vermelho = (255,0,0)
        amarelo = (255, 255, 0)
        laranja = (255, 116, 32)
        azulClaro = (0, 255, 255)
        azulEscuro = (0, 0, 255)
        azulMarinho = (0, 65, 89)

        self.cores = [cinza, laranja, azulEscuro, azulClaro, amarelo, verde, roxo, vermelho, azulMarinho]

    def getCores(self): 
        return self.cores
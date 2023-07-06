# Descrição da classe:
# Representa um dos indivíduos que populam as gerações

class Individuo:
    def __init__(self, pesoNumBuracos, pesoRugosidade, pesoLinhasLimpasTopo, pesoLinhasLimpasEmbaixo, pesoAltura, pesoSombras):
        self.pesoNumBuracos = pesoNumBuracos
        self.pesoRugosidade = pesoRugosidade
        self.pesoLinhasLimpasTopo = pesoLinhasLimpasTopo
        self.pesoLinhasLimpasEmbaixo = pesoLinhasLimpasEmbaixo
        self.pesoAltura = pesoAltura
        self.pesoSombras = pesoSombras
        self.pontos = 0

    def getCaracteristicas(self):
        print("PesoNumBuracos: ", self.pesoNumBuracos)
        print("PesoRugosidade: ", self.pesoRugosidade)
        print("PesoLinhasLimpasTopo: ", self.pesoLinhasLimpasTopo)
        print("PesoLinhasLimpasEmbaixo: ", self.pesoLinhasLimpasEmbaixo)
        print("PesoAltura: ", self.pesoAltura)
        print("PesoSombras: ", self.pesoSombras)
        print("Pontos (média): ", self.pontos)

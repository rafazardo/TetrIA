# Descrição da classe:
# Essa classe funciona como representação da população de indivíduos que compõem
# as gerações do algoritmo genético

import random
from Individuo import Individuo

class Populacao:
    def __init__(self, tamanho, numJogosIndividuo, numGeracoes, taxaMutacao):
        self.populacao = []
        self.populacaoDeMelhoresIndividuos = []
        self.populacaoFilhos = []
        self.melhoresDeCadaGeracao = []
        self.numJogosIndividuo = numJogosIndividuo
        self.taxaMutacao = taxaMutacao
        self.numGeracoes = numGeracoes
        
        self.gerarPopulacao(tamanho)
        self.limparResultados()

    def gerarPopulacao(self, tamanho):
        self.populacao = []
        for i in range(tamanho):
            individuo = Individuo(random.random(), random.random(), random.random(), random.random(), random.random(), random.random())
            self.populacao.append(individuo)

    def getPopulacao(self):
        return self.populacao
    
    def getStatusPopulacao(self):
        numIndividuo = 1
        
        print("Populacao Completa")
        
        for individuo in self.populacao:
            print("Indivíduo ", numIndividuo)
            individuo.getCaracteristicas()
            print("\n")
            numIndividuo += 1
        
    def getStatusPopulacaoDeMelhoresIndividuos(self):
        numIndividuo = 1

        print("Populacao Melhorada")
        
        for individuo in self.populacaoDeMelhoresIndividuos:
            print("Indivíduo ", numIndividuo)
            individuo.getCaracteristicas()
            print("\n")
            numIndividuo += 1     

    def getStatusFilhos(self):
        numIndividuo = 1

        print("Populacao Filhos")
        
        for individuo in self.populacaoFilhos:
            print("Indivíduo ", numIndividuo)
            individuo.getCaracteristicas()
            print("\n")
            numIndividuo += 1           

    
    def encontrarMelhoresIndividuos(self):
        ordenado = sorted(self.populacao, key=lambda x: x.pontos, reverse=True)
        tamanhoMetade = len(ordenado)//2

        self.populacaoDeMelhoresIndividuos = ordenado[:tamanhoMetade]   

    def gerarReproducao(self, pai, mae):
        escolha = ["pai", "mae"]
        filho = Individuo(0, 0, 0, 0, 0, 0)

        if (random.choice(escolha) == "pai"):
            filho.pesoNumBuracos = pai.pesoNumBuracos
        else:
            filho.pesoNumBuracos = mae.pesoNumBuracos

        if (random.choice(escolha) == "pai"):
            filho.pesoRugosidade = pai.pesoRugosidade
        else:
            filho.pesoRugosidade = mae.pesoRugosidade            

        if (random.choice(escolha) == "pai"):
            filho.pesoLinhasLimpasTopo = pai.pesoLinhasLimpasTopo
        else:
            filho.pesoLinhasLimpasTopo = mae.pesoLinhasLimpasTopo       

        if (random.choice(escolha) == "pai"):
            filho.pesoLinhasLimpasEmbaixo = pai.pesoLinhasLimpasEmbaixo
        else:
            filho.pesoLinhasLimpasEmbaixo = mae.pesoLinhasLimpasEmbaixo        

        if (random.choice(escolha) == "pai"):
            filho.pesoAltura = pai.pesoAltura
        else:
            filho.pesoAltura = mae.pesoAltura        

        if (random.choice(escolha) == "pai"):
            filho.pesoSombras = pai.pesoSombras
        else:
            filho.pesoSombras = mae.pesoSombras               

        return filho                       
    
    def gerarMutacao(self, individuo):
        if random.random() <= self.taxaMutacao:
            individuo.pesoNumBuracos = random.random()
            
        if random.random() <= self.taxaMutacao:           
            individuo.pesoRugosidade = random.random()  

        if random.random() <= self.taxaMutacao:          
            individuo.pesoLinhasLimpasTopo = random.random()   

        if random.random() <= self.taxaMutacao:        
            individuo.pesoLinhasLimpasEmbaixo = random.random()          

        if random.random() <= self.taxaMutacao:       
            individuo.pesoAltura = random.random()      

        if random.random() <= self.taxaMutacao:       
            individuo.pesoSombras = random.random()                                      

    def gerarFilhos(self):
        for individuo in self.populacaoDeMelhoresIndividuos:
            while True:
                individuoAleatorio = random.choice(self.populacaoDeMelhoresIndividuos)
                if (individuoAleatorio != individuo): break

            filho = self.gerarReproducao(individuo, individuoAleatorio)

            self.gerarMutacao(filho)

            self.populacaoFilhos.append(filho)

    def gerarNovaPopulacao(self):
        self.populacao = self.populacaoDeMelhoresIndividuos + self.populacaoFilhos
        self.populacaoDeMelhoresIndividuos = []
        self.populacaoFilhos = []

    def gravarResultados(self, numGeracao):
        melhorIndividuoGeracao = max(self.populacao, key=lambda individuo: individuo.pontos)

        # Abrir o arquivo em modo de escrita (append)
        with open('./outputs/resultados.txt', 'a') as arquivo:
            arquivo.write("Geração: {}\n".format(numGeracao))
            arquivo.write("PesoNumBuracos: {}\n".format(melhorIndividuoGeracao.pesoNumBuracos))
            arquivo.write("PesoRugosidade: {}\n".format(melhorIndividuoGeracao.pesoRugosidade))
            arquivo.write("PesoLinhasLimpasTopo: {}\n".format(melhorIndividuoGeracao.pesoLinhasLimpasTopo))
            arquivo.write("PesoLinhasLimpasEmbaixo: {}\n".format(melhorIndividuoGeracao.pesoLinhasLimpasEmbaixo))
            arquivo.write("PesoAltura: {}\n".format(melhorIndividuoGeracao.pesoAltura))
            arquivo.write("PesoSombras: {}\n".format(melhorIndividuoGeracao.pesoSombras))
            arquivo.write("Pontos (média): {}\n".format(melhorIndividuoGeracao.pontos))
            arquivo.write("\n")   

    def limparResultados(self):
        with open('./outputs/resultados.txt', 'w') as arquivo:
            arquivo.write("")  # Limpar o conteúdo do arquivo
        

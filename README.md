# TetrIA
O objetivo deste projeto foi desenvolver um sistema autônomo capaz de jogar o videogame Tetris com alto desempenho e obter altas pontuações. Para isso, foi implementada uma inteligência artificial baseada em Algoritmos Genéticos.

Este repositório contém o projeto final apresentado na disciplina de Inteligência Artificial I (INF 420), ministrada pelo professor Julio C. S. Reis. O projeto foi desenvolvido como requisito parcial para aprovação na disciplina.

# Detalhes do Algoritmo Genético
Para uma explicação mais detalhada, recomendamos que você visite o artigo elaborado sobre o projeto. O artigo pode ser acessado no seguinte link: [Artigo sobre o Projeto](https://github.com/rafazardo/TetrIA/blob/main/Desenvolvimento_de_um_sistema_de_inteligencia_artificial_para_obter_altas_pontuacoes_no_Tetris_utilizando_algoritmo_genetico.pdf).

# Como executar
Logo abaixo será apresentando o passo a passo para utilizar a implementação de forma correta. Sinta-se à vontade para explorar o repositório e utilizar as implementações disponíveis. Se tiver alguma dúvida ou precisar de mais informações, não hesite em entrar em contato.

## Dependências
O desenvolvimento do projeto foi feito utilizando a biblioteca Pygame. Certifique-se de instalar as dependências necessárias executando o comando "pip install pygame" ou de acordo com sua preferência.

## Executáveis
Existem dois arquivos executáveis: "TetrIA_Individuo.py" e "TetrIA_População.py".

### Instruções para executar o "TetrIA_Individuo.py":
Nesta implementação, você tem a capacidade de escolher os pesos que o indivíduo utilizará para avaliar suas jogadas. Isso permite ajustar o desempenho do sistema de acordo com suas preferências e estratégias desejadas. Ao definir os pesos, você pode influenciar o comportamento do jogo e observar como diferentes combinações afetam o desempenho e as pontuações alcançadas. Experimente diferentes valores para os pesos e veja como isso impacta o desempenho do jogo. Sinta-se à vontade para explorar e ajustar os pesos de acordo com suas necessidades.

1. Acesse a pasta "inputs" e abra o arquivo "individuo.txt".
2. Insira os valores desejados referentes aos pesos do indivíduo, conforme exemplo abaixo: <br>
```
Peso para o Número de Buracos: 0.5764343247818454
Peso para a Rugosidade: 0.09973954062855961
Peso para as Linhas Limpas no Topo: 0.7934715772414589
Peso para as Linhas Limpas na Base: 0.16871021668664132
Peso para a Altura: 0.03334951194142333
Peso para as Sombras: 0.951676843485697
```
3. Execute o programa com o comando "python TetrIA_Individuo.py".

### Instruções para executar o "TetrIA_Populacao.py":
Nesta implementação, você pode ver o algoritmo genético em ação. Ele evolui uma população de indivíduos do jogo Tetris ao longo de várias gerações. Durante a execução, você pode configurar parâmetros como o tamanho da população, o número de jogos por indivíduo e o número de gerações. O algoritmo seleciona os melhores indivíduos de cada geração para reprodução, aplicando cruzamento e mutação. Ao final da execução, os resultados são registrados em um arquivo chamado "resultados.txt". Experimente diferentes configurações para ver como o desempenho evolui ao longo do tempo.

1. Acesse a pasta "inputs" e abra o arquivo "populacao.txt".
2. Insira os valores desejados referentes aos parâmetros do algoritmo genético, conforme exemplo abaixo: <br>
```
Tamanho da população: 20
Número de jogos do indivíduo: 10
Número de gerações: 5
Taxa de mutação: 0.1
```
3. Execute o programa com o comando "python TetrIA_Populacao.py".
4. Um arquivo "resultados.txt" contendo os melhores indivíduos de cada geração será salvo na pasta "outputs".

# Contribuidores:

[Pedro Baldotto](https://github.com/PedroFiorio) <br>
[Rafael Zardo](https://github.com/rafazardo)

Agradecimentos especiais ao professor Julio C. S. Reis pela orientação e suporte durante o desenvolvimento do projeto.

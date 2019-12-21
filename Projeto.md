# Projeto Inteligência Artificial

## Perguntas

### Pergunta 1 - Quantos quartos não estão ocupados?

+ criação de uma objeto AGENTE que contem um array de objetos QUARTO dos quais cada tem um contador do numero de pessoas encontradas a ocupá-los;
+ incrementar o contador do respetivo quarto sempre que se encontre uma pessoa num quarto;
+ contar o número de quartos encontrados dos quais foram encontradas pessoas no interior.

### Pergunta 2 - Quantas Suites foram encontradas até agora?

+ Utilizar as coordenadas fornecidas pelo ROS para determinar a posição do agente no mundo e perceber se se encontra num corredor ou num quarto;
+ Utilizar um incrementador para contar o número de quartos visitados.

### Pergunta 3 - É mais provável encontrar pessoas nos corredores ou dentro dos quartos?

Com o conhecimento do número de pessoas observadas até ao momento tanto nos quartos como nos corredores, calcular as probabilidades de encontrar pessoas em quartos vs nos corredores e devolver aquele que for mais provável;

### Pergunta 4 - Se queremos encontrar um computador, para que tipo de quarto devemos ir?

Utilizar o conhecimento a priori dos quartos que contêm computadores para determinar uma correlação entre um tipo de quarto e os quartos onde já foram encontrados computadores;

### Pergunta 5 - Qual é o número do quarto singular mais próximo?

+ Conhecendo os quartos *single*: determinar a distância da posição do agente aos quartos *single* conhecidos;
+ Desconhecendo qualquer quarto(ínicio do programa): ???

### Pergunta 6 - Como é que podemos ir do atual quarto para o elevador?

+ Ponto de partida: Posição do agente;
+ Ponto de chegada: Posição (estática) do elevador;
+ Se o agente se encontrar dentro de um quarto, informar para se sair do quarto para o corredor;
+ Do corredor, informar a direção/sentido que o agente deve seguir para atingir o corredor on pode encontrar o elevador;
+ No corredor do elevador informar a direção/sentido que o agente deve seguir para atingir o elevador;

### Pergunta 7 - Quantos livros estimamos encontrar nos próximos dois minutos?

Utilizando o conhecimento do número de livros encontrados até agora e os instantes de tempo em que se encontrou cada livro:
Calcular uma previsão para o número de livros que podem ainda vir a ser encontrados nos próximos 2 minutos;

### Pergunta 8 - Qual é a probabilidade de encontrar uma mesa num quarto sem livros mas que tem pelo menos uma cadeira?

Utilizando o conhecimento prévio das mesas encontradas, dos livros encontrados e das cadeiras encontradas calcular uma probabilidade condicional;
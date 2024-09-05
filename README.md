# Campo Minado - Pygame

Este projeto é uma implementação do clássico jogo Campo Minado (Minesweeper) utilizando a biblioteca Pygame em Python. O jogo permite ao usuário jogar em diferentes níveis de dificuldade e inclui uma interface gráfica para uma melhor experiência.

## Índice

1. [Introdução](#introdução)
2. [Instalação](#instalação)
3. [Como Executar](#como-executar)
4. [Funcionalidades](#funcionalidades)
5. [Screenshots](#screenshots)
6. [Tecnologias Utilizadas](#tecnologias-utilizadas)
7. [Como Jogar](#como-jogar)
8. [Contribuição](#contribuição)
9. [Licença](#licença)

## Introdução

Este projeto é uma implementação do jogo Campo Minado usando a biblioteca Pygame. O jogo permite que o usuário selecione o nível de dificuldade e jogue contra o computador. Inclui gráficos e uma interface de usuário simples.

## Instalação

### Pré-requisitos

Certifique-se de ter o Python instalado em seu sistema. Você pode baixá-lo em: https://www.python.org/downloads/

Além disso, você precisará instalar a biblioteca Pygame. Para isso, use o seguinte comando no terminal:

```bash
pip install pygame
```

## Clonar o Repositório
```bash
git clone https://github.com/enricomalta/campo-minado.git
cd campo-minado
```

## Como Executar
```bash
python campo_minado.py
```

## Funcionalidades
Jogo Campo Minado com diferentes níveis de dificuldade.
Interface gráfica com botões para selecionar a dificuldade.
Contador de minas marcadas e tempo decorrido.
Gráficos para minas, bandeiras e tempo.

## Screenshots
![image](https://github.com/user-attachments/assets/43eb547e-59df-4e92-982d-1c34509169bd)
![image](https://github.com/user-attachments/assets/0e78d6df-327c-48df-b120-d1b94181f23d)


## Tecnologias Utilizadas
Python 3.x
Pygame
NumPy

## Como Jogar
Controles
Clique com o botão esquerdo do mouse para revelar uma célula.
Clique com o botão direito do mouse para marcar ou desmarcar uma célula com uma bandeira.

## Regras
Revele todas as células sem tocar em uma mina para vencer o jogo.
O número exibido em uma célula indica o número de minas adjacentes.
Marque as células que você suspeita conter minas com bandeiras.

## Seleção de Dificuldade
Ao iniciar o jogo, você pode selecionar a dificuldade através do menu:
Fácil: 10x10 células, 10 minas
Médio: 15x15 células, 45 minas
Difícil: 20x20 células, 200 minas

## Contribuição
Sinta-se à vontade para contribuir com melhorias para este projeto. Faça um fork do repositório, crie uma branch com suas alterações e envie um pull request.

import pygame
import random
import numpy as np
import time

# INICIALIZAÇÃO DO PYGAME
menu_ativo = True  # FLAG
pygame.init()
pygame.font.init()

# CORES
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (192, 192, 192)
AZUL = (0, 0, 128)
VERDE = (0, 128, 0)
VERMELHO = (128, 0, 0)

# DISPLAY
LARGURA_CELULA = 30  
ALTURA_TOPO = 50     
LARGURA_BOTAO = 80
ALTURA_BOTAO = 40
FONTE = pygame.font.SysFont('Arial', 15)
largura_janela_menu = 400
altura_janela_menu = 300
janela_menu = pygame.display.set_mode((largura_janela_menu, altura_janela_menu))


# MARCAÇÃO IMG
BOMBA_IMAGEM = pygame.image.load('assets/bomb.png').convert_alpha()
BOMBA_IMAGEM = pygame.transform.smoothscale(BOMBA_IMAGEM, (LARGURA_CELULA - 2, LARGURA_CELULA - 2))
BANDEIRA_IMAGEM = pygame.image.load('assets/flag.png').convert_alpha()
BANDEIRA_IMAGEM = pygame.transform.smoothscale(BANDEIRA_IMAGEM, (LARGURA_CELULA - 2, LARGURA_CELULA - 2))

# ICON STATUS IMG
FLAG_ICON = pygame.image.load('assets/flag.png').convert_alpha()
FLAG_ICON = pygame.transform.smoothscale(FLAG_ICON, (20, 20))
BOMB_ICON = pygame.image.load('assets/bomb.png').convert_alpha()
BOMB_ICON = pygame.transform.smoothscale(BOMB_ICON, (20, 20))
CLOCK_ICON = pygame.image.load('assets/clock.png').convert_alpha()
CLOCK_ICON = pygame.transform.smoothscale(CLOCK_ICON, (20, 20))

class CampoMinado:
    def __init__(self, tamanho, num_minas):
        self.tamanho = tamanho
        self.num_minas = num_minas 
        self.tabuleiro = np.zeros((tamanho, tamanho), dtype=int)
        self.visivel = np.zeros((tamanho, tamanho), dtype=bool)
        self.marcado = np.zeros((tamanho, tamanho), dtype=bool)
        self.minas_colocadas = False
        self.num_marcacoes = 0

    def contar_minas_vizinhas(self, x, y):
        contador = 0
        for i in range(max(0, x-1), min(self.tamanho, x+2)):
            for j in range(max(0, y-1), min(self.tamanho, y+2)):
                if self.tabuleiro[i, j] == -1:
                    contador += 1
        return contador

    def colocar_minas(self, inicial_x, inicial_y):
        minas_colocadas = 0
        while minas_colocadas < self.num_minas:  # SE FALTAR MINAR
            x, y = random.randint(0, self.tamanho - 1), random.randint(0, self.tamanho - 1)  # POSIÇÃO MINA ALEATORIA
            if self.tabuleiro[x, y] != -1 and (x != inicial_x or y != inicial_y): # RASTREIA 1º JOGADA
                self.tabuleiro[x, y] = -1
                minas_colocadas += 1  # COLOCA MINA

    def calcular_numeros(self):
        for x in range(self.tamanho):
            for y in range(self.tamanho):
                if self.tabuleiro[x, y] == -1:
                    continue
                self.tabuleiro[x, y] = self.contar_minas_vizinhas(x, y) # CONTA MINA

    def revelar_celula(self, x, y):
        if not self.minas_colocadas:
            self.colocar_minas(x, y)
            self.calcular_numeros()
            self.minas_colocadas = True

        if self.tabuleiro[x, y] == -1 and not self.marcado[x, y]:
            self.visivel[:, :] = True
            return False
        self.revelar_recursivo(x, y)
        return True
    
    def revelar_recursivo(self, x, y):
        if not (0 <= x < self.tamanho and 0 <= y < self.tamanho):
            return
        if self.visivel[x, y]:
            return
        self.visivel[x, y] = True
        if self.tabuleiro[x, y] == 0:
            for i in range(max(0, x-1), min(self.tamanho, x+2)):
                for j in range(max(0, y-1), min(self.tamanho, y+2)):
                    self.revelar_recursivo(i, j)

    def contar_marcacoes(self):
        return self.num_marcacoes

    def marcar_celula(self, x, y):
        if not self.visivel[x, y]:
            if self.marcado[x, y]:
                self.marcado[x, y] = False
                self.num_marcacoes -= 1
            elif self.num_marcacoes < self.num_minas:
                self.marcado[x, y] = True
                self.num_marcacoes += 1

    def desenhar(self, janela):
        for x in range(self.tamanho):
            for y in range(self.tamanho):
                rect = pygame.Rect(y * LARGURA_CELULA, x * LARGURA_CELULA + ALTURA_TOPO, LARGURA_CELULA, LARGURA_CELULA)
                if self.visivel[x, y]:
                    pygame.draw.rect(janela, BRANCO, rect)
                    if self.tabuleiro[x, y] > 0:
                        if self.tabuleiro[x, y] == 1:
                            cor_numero = AZUL
                        elif self.tabuleiro[x, y] == 2:
                            cor_numero = VERDE
                        else:
                            cor_numero = VERMELHO
                        texto = FONTE.render(str(self.tabuleiro[x, y]), True, cor_numero)
                        janela.blit(texto, (y * LARGURA_CELULA + (LARGURA_CELULA - texto.get_width()) // 2, 
                                            x * LARGURA_CELULA + ALTURA_TOPO + (LARGURA_CELULA - texto.get_height()) // 2))
                    if self.tabuleiro[x, y] == -1:
                        janela.blit(BOMBA_IMAGEM, (rect.x + (LARGURA_CELULA - BOMBA_IMAGEM.get_width()) // 2, 
                                                rect.y + (LARGURA_CELULA - BOMBA_IMAGEM.get_height()) // 2))
                else:
                    pygame.draw.rect(janela, CINZA, rect)
                    if self.marcado[x, y]:
                        janela.blit(BANDEIRA_IMAGEM, (rect.x + (LARGURA_CELULA - BANDEIRA_IMAGEM.get_width()) // 2, 
                                                    rect.y + (LARGURA_CELULA - BANDEIRA_IMAGEM.get_height()) // 2))
                pygame.draw.rect(janela, PRETO, rect, 1)

    def contar_restantes(self):
        return self.tamanho * self.tamanho - np.sum(self.visivel)

    def verificar_vitoria(self):
        for x in range(self.tamanho):
            for y in range(self.tamanho):
                if self.tabuleiro[x, y] == -1:
                    if not self.marcado[x, y]:
                        return False
                elif self.marcado[x, y]:
                    return False
        return True

def desenhar_botao(janela, texto, x, y, largura, altura, cor_normal, cor_hover):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    botao_retangulo = pygame.Rect(x, y, largura, altura)
    FONTE = pygame.font.SysFont('Arial', 12)
    # RASTREIA MOUSE NO BOTÃO
    if botao_retangulo.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(janela, cor_hover, botao_retangulo)
    else:
        pygame.draw.rect(janela, cor_normal, botao_retangulo)

    texto_surface = FONTE.render(texto, True, BRANCO)
    
    texto_rect = texto_surface.get_rect(center=botao_retangulo.center)
    janela.blit(texto_surface, texto_rect)    

def mostrar_menu():
    global menu_ativo
    largura_janela = 500
    altura_janela = 403
    janela_menu = pygame.display.set_mode((largura_janela, altura_janela))
    rodando = True
    dificuldade = None
    
    while rodando:
        janela_menu.fill(BRANCO)
        desenhar_botao(janela_menu, '1. Fácil', largura_janela // 2 - LARGURA_BOTAO // 2, 50, LARGURA_BOTAO, ALTURA_BOTAO, PRETO, CINZA)
        desenhar_botao(janela_menu, '2. Médio', largura_janela // 2 - LARGURA_BOTAO // 2, 120, LARGURA_BOTAO, ALTURA_BOTAO, PRETO, CINZA)
        desenhar_botao(janela_menu, '3. Difícil', largura_janela // 2 - LARGURA_BOTAO // 2, 190, LARGURA_BOTAO, ALTURA_BOTAO, PRETO, CINZA)
        desenhar_botao(janela_menu, '4. Sair', largura_janela // 2 - LARGURA_BOTAO // 2, 260, LARGURA_BOTAO, ALTURA_BOTAO, PRETO, CINZA)
        pygame.display.set_caption("Campo Minado - Menu Principal")
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.MOUSEBUTTONDOWN and pygame.KEYDOWN:
                x, y = evento.pos
                # RASTREIA CLICK
                if largura_janela // 2 - LARGURA_BOTAO // 2 <= x <= largura_janela // 2 + LARGURA_BOTAO // 2:
                    if 50 <= y <= 50 + ALTURA_BOTAO:
                        dificuldade = (10, 10)  # FÁCIL 10% Mina
                        pygame.display.set_caption("Campo Minado - Fácil")
                    elif 120 <= y <= 120 + ALTURA_BOTAO:
                        dificuldade = (15, 45)  # MÉDIO 20% Mina
                        pygame.display.set_caption("Campo Minado - Medio")
                    elif 190 <= y <= 190 + ALTURA_BOTAO:
                        dificuldade = (20, 200)  # DIFÍCIL 50% Mina
                        pygame.display.set_caption("Campo Minado - Dificil")
                    elif 260 <= y <= 260 + ALTURA_BOTAO:
                        rodando = False  # SAIR DO JOGO
                        pygame.quit()
            
            # RASTREIA BOTÃO
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    dificuldade = (10, 10) # FÁCIL 10% Mina
                    pygame.display.set_caption("Campo Minado - Fácil")
                if evento.key == pygame.K_2:
                    dificuldade = (15, 45) # MÉDIO 20% Mina
                    pygame.display.set_caption("Campo Minado - Medio")
                if evento.key == pygame.K_3:
                    dificuldade = (20, 200) # DIFÍCIL 50% Mina
                    pygame.display.set_caption("Campo Minado - Dificil")
                if evento.key == pygame.K_4:
                    rodando = False # SAIR DO JOGO
                    pygame.quit() 
        
        if dificuldade:
            rodando = False
    
    return dificuldade

def main():
    while True:
        dificuldade = mostrar_menu()
        if not dificuldade:
            pygame.quit()
            return
        
        tamanho, num_minas = dificuldade
        largura_janela = tamanho * LARGURA_CELULA
        altura_janela = tamanho * LARGURA_CELULA + ALTURA_TOPO
        janela_jogo = pygame.display.set_mode((largura_janela, altura_janela))


        global menu_ativo
        campo_minado = CampoMinado(tamanho, num_minas)
        rodando = True
        game_over = False
        tempo_inicio = time.time()

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                if evento.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    x, y = pygame.mouse.get_pos()
                    if y > ALTURA_TOPO:
                        x, y = (y - ALTURA_TOPO) // LARGURA_CELULA, x // LARGURA_CELULA
                        if evento.button == 1:  # CLIQUE ESQUERDO
                            if not campo_minado.visivel[x, y] and not campo_minado.marcado[x, y]:
                                if not campo_minado.revelar_celula(x, y):
                                    game_over = True
                        if evento.button == 3:  # CLIQUE DIREITO
                            if not campo_minado.visivel[x, y]:
                                campo_minado.marcar_celula(x, y)
                    
            # ATUALIZAR DISPLAY
            marcacoes = campo_minado.contar_marcacoes()
            tempo_decorrido = int(time.time() - tempo_inicio)
            
            janela_jogo.fill(CINZA)
            
            janela_jogo.blit(FLAG_ICON, (10, 7))
            texto_marcacoes = FONTE.render(f' {marcacoes}', True, PRETO)
            janela_jogo.blit(texto_marcacoes, (35, 7))
            
            
            janela_jogo.blit(CLOCK_ICON, (220, 7))
            texto_tempo = FONTE.render(f' {tempo_decorrido}s', True, PRETO)
            janela_jogo.blit(texto_tempo, (245, 7))

            campo_minado.desenhar(janela_jogo)

            pygame.display.flip()

            if game_over:
                print("Você atingiu uma mina! Fim de jogo.")
                time.sleep(2.5)
                rodando = False
                mostrar_menu()
            if not menu_ativo and campo_minado.verificar_vitoria():
                print("Parabéns! Você venceu!")
                time.sleep(2.5)
                campo_minado = CampoMinado(tamanho, num_minas)
                tempo_inicio = time.time()
                game_over = False
                rodando = False
                mostrar_menu()

        rodando = True

if __name__ == "__main__":
    main()

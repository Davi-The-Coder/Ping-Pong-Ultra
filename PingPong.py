import pygame
import random
#iniciar o modulo
pygame.init()
#criar a janela e batizar ela
LarguraTela = 900
AlturaTela = 600
tela = pygame.display.set_mode((LarguraTela, AlturaTela))
pygame.display.set_caption("Ping Pong Ultra")
tempo = pygame.time.Clock()   #relogio do jogo

#FILTRO NA TELA
filtro = pygame.Surface((LarguraTela, AlturaTela))
filtro.fill((255, 255, 255)) # Cor branca 
filtro.set_alpha(0)    # Transparência: 0 (invisível) a 255 (visivel)

#jogadores
# Sintaxe: pygame.Rect(x, y, largura, altura)
jogador1 = pygame.Rect(0, 0, 20, 100)
jogador1.topleft = (50, 200)

#PONTOS DOS JOGADORES
ponto1 = 0
ponto2 = 0

jogador2 = pygame.Rect(0, 0, 20, 100)
jogador2.right = (LarguraTela-50)
jogador2.y = 200

#coisas pras abilidades do jogador
MexeuBaixo1 = False
MexeuBaixo2 = False


#ABILIDADES
#dash player 1
dashFrame = 0
dashdirecao = 0
cooldown = False
dashtime = 0
canDash = False

#dash player2
dashFrame2 = 0
cooldown2 = False
dashtime2 = 0
canDash2 = False

#Soco
canPunch = False
powerpunch = False
punchFrame = 0
punchedOnce = False

#soco player 2
canPunch2 = False
powerpunch2 = False
punchFrame2 = 0
punchedOnce2 = False


#SONS DO JOGO
Parry = pygame.mixer.Sound("parry.mp3") #carrega o som
acerto = pygame.mixer.Sound("wallhit.mp3") #carrega o som
ponto = pygame.mixer.Sound("point.mp3") #carrega o som
perder = pygame.mixer.Sound("lose.mp3") #carrega o som
impulso = pygame.mixer.Sound("dash.mp3") #carrega o som

#bolinha
velocidadeincial = 0
bola = pygame.Rect(LarguraTela/2,AlturaTela/2, 20, 20)  #a posicao inicial dela (posicao x, posicao y,Tamanho dela no x, Tamanho dela no y)

#direcoes random
xrandom = random.randint(-2,2)
while xrandom == 0:  #NAO POde PEGAR 0 SE pegar 0 troca
    if xrandom == 0:
       xrandom = random.randint(-2,2)
yrandom = xrandom

ativo = True
velocidadeincial = xrandom
while ativo:
    tela.fill((0,0,0))
    
    velocidade = str(abs(xrandom)) #transformar a velocidade em string
    velocidade = velocidade[:4]  #Cortar a velocidade em 2 casas decimais pra nao ficar numero enorme na tela
    
    #O texto agora
    fonte = pygame.font.SysFont("Arial", 50, bold=True)  #carrega a fonte peguei a basica mesmo
    fonte2 = pygame.font.SysFont("Arial", 15, bold=True)  #carrega a fonte peguei a basica mesmo
    texto_aparencia = fonte.render(f"{str(ponto1)} - {str(ponto2)}", True, (255, 255, 255))   # Renderiza o texto (Texto, Antialias, Cor)
    texto_aparencia2 = fonte2.render("Jogador 1: Dash = Shift Esquerdo ; Soco = Tecla D  |  Jogador 2: Dash = Shift Direito; Soco = Setinha da Esquerda", True, (255, 255, 255))   # Renderiza o texto (Texto, Antialias, Cor)
    texto_aparencia3 = fonte2.render(f"Velocidade da bola: {velocidade}x", True, (255, 255, 255))   # Renderiza o texto (Texto, Antialias, Cor)
    # Antialias == True deixa as bordas do texto bonitinha
    # O 'f' antes das aspas permite colocar variáveis dentro de {} na string pro texto

    texto_rect = texto_aparencia.get_rect(center=(LarguraTela // 2, 40))
    texto_rect2 = texto_aparencia2.get_rect(center=(LarguraTela // 2, AlturaTela-20))
    texto_rect3 = texto_aparencia3.get_rect(center=(LarguraTela // 2, AlturaTela/2))
    
    tela.blit(texto_aparencia, texto_rect)  # texto que pega a posicao do quadrado -- copia o texto e cola ele na tela
    tela.blit(texto_aparencia2, texto_rect2)  # texto que pega a posicao do quadrado -- copia o texto e cola ele na tela
    tela.blit(texto_aparencia3, texto_rect3)  # texto que pega a posicao do quadrado -- copia o texto e cola ele na tela
    
    
    TempoDeAgora = pygame.time.get_ticks()  #PEGAR O TEMPO ATUAL
    
    pygame.draw.rect(tela, "cyan", jogador1)  #DESENHAR OS JOGADORES E A BOLA NA TELA
    pygame.draw.rect(tela, "red", jogador2)
    pygame.draw.rect(tela, "magenta", bola)
    
    
    filtro.set_alpha(0)    # Transparência: 0 (invisível) a 255 (visivel)
    #DASH PLAYER 1
    if dashFrame > 0:
        jogador1.move_ip(0, dashdirecao)
        dashFrame = dashFrame-1
    if dashFrame == 0:
        cooldown = False 
    
    if TempoDeAgora - dashtime < 1000:  #COOLDOWN
        canDash = False
    else:
        canDash = True
    #DASH PLAYER 2
    if dashFrame2 > 0:
        jogador2.move_ip(0, dashdirecao)
        dashFrame2 = dashFrame2-1
    if dashFrame2 == 0:
        cooldown2 = False 
    
    if TempoDeAgora - dashtime2 < 1000:  #COOLDOWN
        canDash2 = False
    else:
        canDash2 = True
    
    #POWER PUNCH player1
    if punchFrame > 0:
        jogador1.move_ip(dashdirecao, 0)
        punchFrame = punchFrame-1
    if punchFrame == 0:
        cooldown = False 
        powerpunch = False
        jogador1.x = 50
    
    if TempoDeAgora - dashtime < 3000:  #COOLDOWN
        canPunch = False
    else:
        canPunch = True
        
    #POWER PUNCH player2
    if punchFrame2 > 0:
        jogador2.move_ip(-dashdirecao, 0)
        punchFrame2 = punchFrame2-1
    if punchFrame2 == 0:
        cooldown2 = False 
        powerpunch2 = False
        jogador2.x = LarguraTela-50
    #COOLDOWN PRA N SPAMMAR
    if TempoDeAgora - dashtime2 < 3000:  #COOLDOWN
        canPunch2 = False
    else:
        canPunch2 = True    
    
    tecla = pygame.key.get_pressed()   #MOVIMENTACAO DOS JOGADORES
    if cooldown == False:  
        if tecla[pygame.K_w]:   #PLAYER 1
            MexeuBaixo1 = False
            jogador1.move_ip(0,-5)
        if tecla[pygame.K_s]:
            MexeuBaixo1 = True
            jogador1.move_ip(0,5)
        if tecla[pygame.K_UP]:    #PLAYER 2
            MexeuBaixo2 = False
            jogador2.move_ip(0,-5)
        if tecla[pygame.K_DOWN]:
            MexeuBaixo2 = True
            jogador2.move_ip(0,5)
    
    #COLISAO
    jogador1.clamp_ip(tela.get_rect())
    jogador2.clamp_ip(tela.get_rect())
    
    #colisao da bola com coisas
    if bola.colliderect(jogador2):
        Parry.play()
        filtro.set_alpha(150)    # Transparência: 0 (invisível) a 255 (visivel)
        if powerpunch2 == True:   #powerpunch
            if punchedOnce2 == True:
                xrandom = xrandom*1.1
                yrandom = yrandom*1.1
                
            else:
                xrandom = xrandom*-1.1
                yrandom = yrandom*1.1
                punchedOnce2 = True
            
        else:
            if abs(xrandom) <= 20:
                xrandom = xrandom*-1.1
                yrandom = yrandom*1.1
                punchedOnce2 = True
            else:
                xrandom = xrandom*-1
                punchedOnce2 = True
        bola.x = jogador2.x-20
        tela.blit(filtro, (0, 0))
        pygame.display.update()    # Mostra na tela imediatamente
        pygame.time.wait(500)   #congela tudo por 0.5 secs ou seja 500 milisecs
        filtro.set_alpha(0)    #tira dps do freeze
        print("velocidade no x:",xrandom,"velocidade no y:",yrandom)
    if bola.colliderect(jogador1):
        Parry.play()
        filtro.set_alpha(150)    # Transparência: 0 (invisível) a 255 (visivel)
        if powerpunch == True:   #powerpunch
            if punchedOnce == True:
                xrandom = xrandom*1.1
                yrandom = yrandom*1.1
                
            else:
                xrandom = xrandom*-1.1
                yrandom = yrandom*1.1
                punchedOnce = True
            
        else:
            if abs(xrandom) <= 20:
                xrandom = xrandom*-1.1
                yrandom = yrandom*1.1
                punchedOnce = True
            else:
                xrandom = xrandom*-1
                punchedOnce = True
        tela.blit(filtro, (0, 0))
        pygame.display.update()    # Mostra na tela imediatamente
        pygame.time.wait(500)    #congela a tela por 0.5 secs
        filtro.set_alpha(0)      #dps do freeze tira o filtro branco
        bola.x = jogador1.x+20   #colocar a bola um pouco a frente do jogador pra ela n entrar dentro dele ou so sumir 
        print("velocidade no x:",xrandom,"velocidade no y:",yrandom)
        
    
    #colisao com cima e baixo da tela
    if bola.y <= 0:
        acerto.play()
        yrandom = yrandom*-1
        bola.y = 0
        print("velocidade no x:",xrandom,"velocidade no y:",yrandom)
    if bola.y >= AlturaTela:
        acerto.play()
        yrandom = yrandom*-1
        bola.y = AlturaTela
        print("velocidade no x:",xrandom,"velocidade no y:",yrandom)
    
    #COLISAO NAS BORDAS (GAME OVER)
    if bola.x >= LarguraTela or bola.x <= 0:  #TUDO VOLTA PRO INICIO
        #PONTOS A SEREM GANHOS
        if bola.x >= LarguraTela:
            ponto1 = ponto1+1
        if bola.x <= 0:
            ponto2 = ponto2+1
        #REPOCISIONAMENTO DAS COISAS
        perder.play()   #toca o som de perder
        pygame.time.wait(1000)    #congela a tela por 1 sec
        bola.x = LarguraTela/2
        bola.y = AlturaTela/2
        xrandom = velocidadeincial
        yrandom = velocidadeincial
        jogador1.topleft = (50, 200)
        jogador2.right = (LarguraTela-50)
        jogador2.y = 200
        ponto.play()
        
    
    #movimento da bola

    
    bola.move_ip(xrandom, yrandom)
    if bola.y == AlturaTela or bola.y == 0:   #inverter e aumentar a velocidade da bola ao bater em cima da tela ou em baixo com limite de 10x de velocidade
        if abs(xrandom) and abs(yrandom) <= 10:
            yrandom = yrandom*-1.1
            xrandom = xrandom*1.1
        else:
            yrandom = yrandom*-1
            
        
      
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ativo = False
        else:
            if event.type == pygame.KEYDOWN:
                #Abilidades Especiais pros jogadores
                #DASH player 1
                if event.key == pygame.K_LSHIFT and cooldown == False and canDash == True and punchFrame == 0:
                    dashtime = TempoDeAgora
                    impulso.play()
                    cooldown = True
                    dashFrame = 15
                    if MexeuBaixo1 == True:   #decide se o dash vai pra cima ou pra baixo
                        dashdirecao = 10
                    else:
                        dashdirecao = -10
                #PUNCH PLAYER 1
                elif event.key == pygame.K_d and cooldown == False and canPunch == True and punchFrame == 0:
                    dashtime = TempoDeAgora
                    impulso.play()
                    punchedOnce = False
                    cooldown = True
                    powerpunch = True
                    punchFrame = 15
                    dashdirecao = 15
                #Dash player 2
                if event.key == pygame.K_RSHIFT and cooldown2 == False and canDash2 == True and punchFrame2 == 0:
                    dashtime2 = TempoDeAgora
                    impulso.play()
                    cooldown2 = True
                    dashFrame2 = 15
                    if MexeuBaixo2 == True:   #Decide se o dash vai pra cima ou pra baixo
                        dashdirecao = 10
                    else:
                        dashdirecao = -10
                #PUNCH PLAYER 2
                elif event.key == pygame.K_LEFT and cooldown2 == False and canPunch2 == True and punchFrame2 == 0:
                    dashtime2 = TempoDeAgora
                    impulso.play()
                    punchedOnce2 = False
                    cooldown2 = True
                    powerpunch2 = True
                    punchFrame2 = 15
                    dashdirecao = 15
    pygame.display.update() #atualizar a cada ciclo em outra maneira de dizer (fps) - Frames por segundo
    tempo.tick(60) #limitar a 60 fps pra nao bugar tudo
pygame.quit()   #Fecha o jogo

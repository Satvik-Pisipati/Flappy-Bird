import random 
import sys 
import pygame
from pygame.locals import * 

FPS = 36
S_width = 289
S_height = 511
SCREEN = pygame.display.set_mode((S_width, S_height))
gro__und= S_height * 0.10
s_g_pics = {}
game_bgm_s = {}
ply = 'gallery/sprites/bird.png'
bcg = 'gallery/sprites/bcg.png'
PIPE = 'gallery/sprites/pipe.png'

def W_s():
    """
    Shows welcome images on the screen
    """

    plyx = int(S_width/5)
    plyy = int((S_height - s_g_pics['ply'].get_height())/2)
    messagex = int((S_width - s_g_pics['message'].get_width())/2)
    messagey = int(S_height*0.15)
    basex = 0
    while True:
        for event in pygame.event.get():
           
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(s_g_pics['bcg'], (0, 0))    
                SCREEN.blit(s_g_pics['ply'], (plyx, plyy))    
                SCREEN.blit(s_g_pics['message'], (messagex,messagey ))    
                SCREEN.blit(s_g_pics['base'], (basex, GROUNDY))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    plyx = int(S_width/5)
    plyy = int(S_width/2)
    basex = 0

    
    newPipe1 = G_R_P()
    newPipe2 = G_R_P()

   
    UPP_PIPEs = [
        {'x': S_width+200, 'y':newPipe1[0]['y']},
        {'x': S_width+200+(S_width/2), 'y':newPipe2[0]['y']},
    ]
    
    LOW_PIPE = [
        {'x': S_width+200, 'y':newPipe1[1]['y']},
        {'x': S_width+200+(S_width/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    plyVelY = -9
    plyMaxVelY = 10
    plyMinVelY = -8
    plyAccY = 1

    plyFlapAccv = -8 
    plyFlapped = False 


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if plyy > 0:
                    plyVelY = plyFlapAccv
                    plyFlapped = False
                    game_bgm_s['wing'].play()


        crashTest = I_C(plyx, plyy, UPP_PIPEs, LOW_PIPE) 
        if crashTest:
            return     

      
        plyMidPos = plyx + s_g_pics['ply'].get_width()/2
        for pipe in UPP_PIPEs:
            pipeMidPos = pipe['x'] + s_g_pics['pipe'][0].get_width()/2
            if pipeMidPos<= plyMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                game_bgm_s['point'].play()


        if plyVelY <plyMaxVelY and not plyFlapped:
            plyVelY += plyAccY

        if plyFlapped:
            plyFlapped = False            
        plyHeight = s_g_pics['ply'].get_height()
        plyy = plyy + min(plyVelY, gro__und- plyy - plyHeight)

       
        for UPP_PIPE , lowerPipe in zip(UPP_PIPEs, LOW_PIPE):
            UPP_PIPE['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

       
        if 0<UPP_PIPEs[0]['x']<5:
            newpipe = G_R_P()
            UPP_PIPEs.append(newpipe[0])
            LOW_PIPE.append(newpipe[1])

        
        if UPP_PIPEs[0]['x'] < -s_g_pics['pipe'][0].get_width():
            UPP_PIPEs.pop(0)
            LOW_PIPE.pop(0)
        
       
        SCREEN.blit(s_g_pics['bcg'], (0, 0))
        for UPP_PIPE, lowerPipe in zip(UPP_PIPEs, LOW_PIPE):
            SCREEN.blit(s_g_pics['pipe'][0], (UPP_PIPE['x'], UPP_PIPE['y']))
            SCREEN.blit(s_g_pics['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(s_g_pics['base'], (basex, GROUNDY))
        SCREEN.blit(s_g_pics['ply'], (plyx, plyy))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += s_g_pics['numbers'][digit].get_width()
        Xoffset = (S_width - width)/2

        for digit in myDigits:
            SCREEN.blit(s_g_pics['numbers'][digit], (Xoffset, SH*0.12))
            Xoffset += s_g_pics['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def I_C(plyx, plyy, UPP_PIPEs, LOW_PIPE):
    if plyy> gro__und- 25  or plyy<0:
        game_bgm_s['touch'].play()
        return True
    
    for pipe in UPP_PIPEs:
        pipeHeight = s_g_pics['pipe'][0].get_height()
        if(plyy < pipeHeight + pipe['y'] and abs(plyx - pipe['x']) < s_g_pics['pipe'][0].get_width()):
            game_bgm_s['touch'].play()
            return True

    for pipe in LOW_PIPE:
        if (plyy + s_g_pics['ply'].get_height() > pipe['y']) and abs(plyx - pipe['x']) < s_g_pics['pipe'][0].get_width():
            game_bgm_s['touch'].play()
            return True

    return False

def G_R_P():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = s_g_pics['pipe'][0].get_height()
    offset = S_height/3
    y2 = offset + random.randrange(0, int(S_height - s_g_pics['base'].get_height()  - 1.2 *offset))
    pipeX = S_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, 
        {'x': pipeX, 'y': y2} 
    ]
    return pipe


  



if __name__ == "__main__":
   
    pygame.init() 
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Code_bro')
    s_g_pics['numbers'] = ( 
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    s_g_pics['message'] =pygame.image.load('gallery/sprites/Untitled.png').convert_alpha()
    s_g_pics['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
    s_g_pics['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )

    
    game_bgm_s['dead'] = pygame.mixer.Sound('gallery/audio/dead.wav')
    game_bgm_s['touch'] = pygame.mixer.Sound('gallery/audio/touch.wav')
    game_bgm_s['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    game_bgm_s['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    game_bgm_s['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    s_g_pics['bcg'] = pygame.image.load(bcg).convert()
    s_g_pics['ply'] = pygame.image.load(ply).convert_alpha()

    while True:
        W_s() 
        mainGame() 

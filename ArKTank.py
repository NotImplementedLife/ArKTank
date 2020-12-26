"""
    ArKTank - 0.1
"""
from math import *
from random import random

try:
    import pygame
except:
    print("Hey, where is the pygame module?")
    exit(1)

def blend(color1,color2,percent):
    if(0<=percent and percent<=1):
        return(color1[0]*percent+color2[0]*(1-percent),
               color1[1]*percent+color2[1]*(1-percent),
               color1[2]*percent+color2[2]*(1-percent))
    else:
        return (0,0,0)

main_result=0

def game_restart():
    global main_result
    main_result=1
def game_quit():
    global main_result
    main_result=-1

game_action_1=game_restart
game_action_2=game_quit

first=False

def main():
    global main_result
    global first
    pygame.init()
    pygame.display.set_caption("ArKTank")
    pygame.font.init()
    font=pygame.font.SysFont('Comic Sans MS',30)
    screen = pygame.display.set_mode((400, 300))
    done = False

    #_player position
    x = 80
    y = 80
    angle=pi
    speed=1

    generate=True
    percent=0
    perDown=False

    #_player data
    level=1
    mana=20
    manamax=20
    xp=0
    key_list=[]
    gameover=False

    #_check for mana
    def use_mana(m):
        nonlocal mana
        if(mana>=m):
            mana-=m
            return True
        return False

    #_check for special move
    def semiluna():   
        global key_list
        if len(key_list)>=3:
            l=len(key_list)
            return (key_list[l-3]=='Z' and key_list[l-2]=='J' and key_list[l-1]=='J');

        
    class bullet :
        x=0
        y=0
        a=0
        dmg=1
        def __init__(self,x,y,a,dmg=1):
            self.x=x
            self.y=y
            self.a=a
            self.dmg=dmg
        def go(self):
            self.x+=5*cos(self.a)
            self.y+=5*sin(self.a)
        def draw(self):
            pygame.draw.circle(screen, (255,255,255), (int(self.x),int(self.y)),5)
        def time_to_die(self):
            return self.x<-50 or self.x>450 or self.y<-50 or self.y>350


    class enemy :
        x=0
        y=0
        a=0
        speed=1
        color=(0,255,0)
        radius=15
        hp=10
        mxhp=10
        def __init__(self,x,y,a,hp=10,r=15):
            self.x=x
            self.y=y
            self.a=a
            self.radius=r
            self.hp=hp
            self.mxhp=hp
        def go(self):
            self.x+=self.speed*cos(self.a)
            self.y+=self.speed*sin(self.a)
            if(self.x>375): self.a+=pi/2+self.a%(pi/2)
            if(self.y>275): self.a+=pi/2+self.a%(pi/2)
            if(self.x<25) : self.a+=pi/2+self.a%(pi/2)
            if(self.y<25) : self.a+=pi/2+self.a%(pi/2)
            self.color=(0,255,0)
        def draw(self):
            px=int(self.x)
            py=int(self.y)
            pygame.draw.circle(screen, self.color, (px,py),self.radius)
            pygame.draw.line(screen,(255,0,0),(px-self.radius,py),(px-self.radius+int(self.hp/self.mxhp*(2*self.radius)),py))
        def hit(self,bullet):
            return (self.x-bullet.x)**2+(self.y-bullet.y)**2 <= self.radius**2
        def gethit(self,bullets):
            _hit=False
            for i in bullets:
                _hit=_hit or self.hit(i)
                if _hit :
                    if(self.hp>0): self.hp-=i.dmg
                    break
            return _hit
        def time_to_die(self):
            return self.hp<=0


    class option:
        text=""
        render=None
        color=[255,255,255]
        bounds=(0,0,0,0)
        top=0
        left=0
        width=0
        height=0
        execute=None
        def __init__(self,text,action=None):
            self.text=text
            self.render=font.render(text,False,self.color)
            self.width=self.render.get_width()
            self.height=self.render.get_height()
            self.execute=action
        def draw(self,cx,cy,center="X"):
            _x=cx
            if "X" in center: _x-=self.render.get_width()/2
            _y=cy
            if "Y" in center: _y-=self.render.get_height()/2
            screen.blit(self.render,(_x,_y))
            self.render=font.render(self.text,False,self.color)
            pygame.draw.line(screen,self.color,(_x,_y),(_x+self.render.get_width(),_y))
            self.left=_x
            self.top=_y
        def mouse_in_range(self):
            mx=pygame.mouse.get_pos()[0]
            my=pygame.mouse.get_pos()[1]
            return self.left<=mx and mx<=self.left+self.width and self.top <=my and my<=self.top +self.height
        def hover(self):
            temp=[255,255,255]
            hovered=False
            if  self.mouse_in_range():
                temp=[255,255,0]
                hovered=True
            for i in range(0,3): self.color[i]=temp[i]
            return hovered
        def selected(self):
            if(self.hover()):
                if(pygame.mouse.get_pressed()[0]):
                    if self.execute!=None:
                        self.execute()

    bullets=[]
    enemies=[]

    go_options=[option("Restart",game_action_1),option("Quit",game_action_2)]

    clock = pygame.time.Clock()
    start = pygame.time.get_ticks()
    clear_time=start

    while not done:
        timer=pygame.time.get_ticks()-start
        if(timer<5000 and not first):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        main_result=-1
            title=font.render("ArKTank",True,(255,255,255))
            sfont=pygame.font.SysFont("Comic Sans MS",20)
            subtitle=sfont.render("Created by N•I•L",True,(255,255,255))
            sub2=sfont.render("~ 2018 ~",True,(255,255,255));
            screen.fill((0,0,0));
            screen.blit(title,((400-title.get_width())/2,(300-title.get_height())/2-timer/80))
            screen.blit(subtitle,((400-subtitle.get_width())/2,(300-subtitle.get_height())/2+40-timer/80))
            screen.blit(sub2,((400-sub2.get_width())/2,(300-sub2.get_height())/2+80-timer/80))
            pygame.draw.line(screen,(255,255,255),(0,2),(400*timer/5000,2),8)
            pygame.display.flip()
        else:
            first=True
            if not gameover:
                if timer-clear_time>1000:
                    key_list=[]
                if(key_list==[]): clear_time=timer
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        main_result=-1
                            
                if event.type == pygame.KEYDOWN:
                    # SPACE = SPEED
                    if event.key == pygame.K_SPACE:
                        speed*=3
                    # S = Shoot
                    if event.key == pygame.K_s:
                        key_list.append("S");
                        bullets.append(bullet(x+15*cos(angle),y+15*sin(angle),angle))
                    # Z = [Special] Circle
                    if event.key == pygame.K_z:
                        if(use_mana(50)):
                            key_list.append("Z");
                            _a=0
                            while(_a<=2*pi):
                                bullets.append(bullet(x+15*cos(angle),y+15*sin(angle),_a))
                                _a+=pi/72
                            _a=0
                    # J = [Special] Clone
                    if event.key == pygame.K_j:
                        if(len(key_list)!=0):
                            if(use_mana(20)):
                                key_list.append("J");
                                new_bul = []
                                for i in bullets:
                                    new_bul.append(bullet(i.x,i.y,i.a-i.a/2,6));
                                    new_bul.append(bullet(i.x,i.y,i.a+i.a/2,6));
                                bullets=new_bul;
                    if event.key == pygame.K_F5:
                        main_result=1
                        
                if event.type == pygame.KEYUP:
                    # Reset speed
                    if event.key == pygame.K_SPACE:
                           speed//=3

            #   Spawn enemies   #
            if(generate) :
                if(len(enemies)<(level//5+1 if level//5+1<10 else 10)):
                    spawnx=int(50+random()*300)
                    spawny=int(50+random()*200)
                    while((x-spawnx)**2+(y-spawny)**2<30):
                        spawnx=int(50+random()*300)
                        spawny=int(50+random()*200)
                    enemies.append(enemy(spawnx,spawny,random()*2*pi,15+level//3,15+level//25))
                else:
                    generate=False


            #   Key preseed #
            pressed = pygame.key.get_pressed()
            if not gameover:
                    ## Move control ##
                if pressed[pygame.K_UP]: y -= 3*speed
                if pressed[pygame.K_DOWN]: y += 3*speed
                if pressed[pygame.K_LEFT]: x -= 3*speed
                if pressed[pygame.K_RIGHT]: x += 3*speed
                    ## Angle control ##
                if pressed[pygame.K_a]: angle+=pi/90*speed*2
                if pressed[pygame.K_d]: angle-=pi/90*speed*2
                    ## Attack control ##
                if pressed[pygame.K_x]: #Automatic
                    if(timer%3==0):
                        if(use_mana(1)):
                            bullets.append(bullet(x+15*cos(angle),y+15*sin(angle),angle))
                if pressed[pygame.K_c]: #Cardinal
                    if(timer%3==0):
                        if(use_mana(2)):
                            _a=0
                            while(_a<=2*pi):
                                bullets.append(bullet(x+15*cos(angle),y+15*sin(angle),_a))
                                _a+=pi/2   
                angle%=2*pi
                if(x>400): x=0
                if(x<0): x=390
                if(y>300): y=0
                if(y<0): y=290
                        
            screen.fill(blend((255,0,0),(0,0,255),percent/100))

            #   Draw player #
            color = blend((255,255,0),(0,255,255),percent/100)
            pygame.draw.circle(screen, color, (x,y),10)
            pygame.draw.line(screen,color,(x,y),(x+15*cos(angle),y+15*sin(angle)),3)
                
            #   Render bullets  #
            index=0
            deleter=[]
            for i in bullets:
                i.go()
                i.draw()
                if(i.time_to_die()): deleter.append(index)
                index+=1
            index=0
            for i in deleter:
                bullets.pop(i-index)
                index+=1

            #   Render enemies  #
            entity_del=[]
            index=0
            for i in enemies:
                if not gameover: i.go()
                i.draw()
                if not gameover:
                    i.gethit(bullets)
                    if(i.time_to_die()):
                        entity_del.append(index)
                        xp+=1
                        # Level up :)
                        if xp==(level//5+1 if level//5+1<10 else 10):
                            bullets=[]
                            generate=True
                            mana+=30
                            if(mana>manamax): mana=manamax
                            if level<100:
                                level+=1
                                manamax=20+level//10*30
                                if manamax>100: manamax=100
                                xp=0
                            else:
                                xp=0
                    #Check for colision
                    if (x-i.x)**2+(y-i.y)**2<=i.radius+15:
                        gameover=True
                index+=1
            index=0
            for i in entity_del:
                enemies.pop(i-index)
                index+=1

            #   Render Text #
            if not gameover:
                lvltext=font.render('Level:'+str(level),False,(255,255,255))
                screen.blit(lvltext,(0,0))
                manatext=font.render('Mana:'+str(mana),False,(255,255,255));
                screen.blit(manatext,(250,250));
            if gameover:
                gotext=font.render('Game over',False,(255,255,255))
                screen.blit(gotext,((400-gotext.get_width())/2,10))

                h=50
                for i in go_options:
                    i.selected()
                    i.draw(200,h)
                    h+=45
            pygame.display.flip()
            clock.tick(60)
            if percent==100 : perDown=True
            if percent==0   : perDown=False
            if not perDown : percent+=1
            else: percent-=1

            if(main_result!=0): done=1        
            if done: pygame.quit()

while(1):
    main_result=0
    main()
    if(main_result<0): break

import pygame as pg
import sys,time
from pygame import mixer
from random import randint
pg.init()
mixer.init()
jump=pg.mixer.Sound("cartoon-jump-6462.mp3")
mixer.music.load("boom.mp3")
mixer.music.set_volume(1)
sizing=1.4
width=550
pillar_up=0
pillar_down=0
height=749
fps=pg.time.Clock()
class Bird:
    def __init__(self):
        self.image=(pg.image.load("image-removebg-preview_optimized_1_optimized_optimized_1_optimized.png").convert_alpha())
        self.yspeed=0
        self.gravity_on=True
        self.gameon=True
        self.gravity=10
        self.speed=300
        self.birdieRect=self.image.get_rect(center=(100,400))
    # gravity implementation
    def G_force(self,dt):
        if self.gameon:
            # to prevent birdie to fly above
            if self.birdieRect.y<0 :
                self.birdieRect.y=0
                self.speed=0
            # aadfdscc
            elif self.birdieRect.y>0 and self.speed==0:#dsfff
                self.speed=250 
        if self.gravity_on:
                self.yspeed+=self.gravity*dt
                self.birdieRect.y+=self.yspeed          
    def jump(self,dt):
        self.yspeed=-self.speed*dt

#to be edited
class pillar:
    def __init__(self,sizing,move_speed):
        self.move_speed=move_speed
        self.up_pillar=pg.transform.scale_by(pg.image.load("PngItem_1668203 (1).png").convert_alpha(),sizing)
        self.down_pillar=pg.transform.scale_by(pg.image.load("PngItem_1668203 (1).png").convert_alpha(),sizing)
        self.pillar_upRect=self.up_pillar.get_rect()
        self.pillar_downRect=self.down_pillar.get_rect()
        self.pillar_upRect.y=randint(290,510)
        self.pillar_upRect.x=1000
        self.pillar_downRect.y=self.pillar_upRect.y - 200 - self.pillar_upRect.height
        self.pillar_downRect.x=1000
        pillar_up=self.pillar_upRect
        pillar_down=self.pillar_downRect
    def createpillar(self,win):
        win.blit(self.up_pillar,self.pillar_upRect)
        win.blit(self.down_pillar,self.pillar_downRect)
    def update(self,dt):
        self.pillar_upRect.x-=int(self.move_speed*dt)
        self.pillar_downRect.x-=int(self.move_speed*dt)




class Game:
    def __init__(self):
        #initialising game dimensions
        pg.display.set_caption('Flappy Bird NINJA')
        self.score=0
        self.notcrash=True
        self.t=False
        self.exp=False
        self.start=False
        self.x=True
        self.firstime=True
        self.win=pg.display.set_mode((width,height))
        self.pipes=[]
        self.pipe_generate_counter=81
        #speed of the bird
        self.movingspeed=300
        self.birdie=Bird()
        #setting up the images for the game
        self.win=pg.display.set_mode((width,height))
        self.explosion=pg.image.load("explode_optimized.png")
        self.bgImg=pg.transform.scale_by(pg.image.load("bg.png").convert(),sizing)
        self.zameeno1=pg.transform.scale_by(pg.image.load("ground.png").convert(),sizing)
        self.zameeno1=pg.transform.scale_by(pg.image.load("ground.png").convert(),sizing)
        #intialising rect
        self.ground1Rect=self.zameeno1.get_rect()
        self.ground2Rect=self.zameeno1.get_rect()
        self.ground1Rect.x=0
        self.ground2Rect.x=self.ground1Rect.right
        self.ground1Rect.y=650
        self.ground2Rect.y=650
        self.gameRun()



    def gameRun(self):
        self.secure=True
        prevTime=time.time()
        n=False
        self.font=pg.font.Font(None,74)
        self.text=self.font.render(str(self.score),True,(0,0,0))
        self.textRect=self.text.get_rect(center=(275,40))
        while True:
            nextTime=time.time()
            dt=nextTime-prevTime
            prevTime=nextTime
            for i in pg.event.get():
                if i.type==pg.QUIT:
                    pg.quit()
                    sys.exit()
                self.collision()
                if i.type==pg.KEYDOWN:
                    if i.key==pg.K_RETURN and self.x:
                        self.start=True
                    if i.key==pg.K_SPACE and self.start:   
                        jump.play()                 
                        self.birdie.jump(dt)  
                        
            self.ifscore()
            self.collision()
            self.blit()
            self.motions(dt)
            pg.display.update()
            fps.tick(60)
    
    #intilises motion for the game

                
                

    
    def motions(self,dt):
        if self.start:
            #ground ki speed
            self.ground1Rect.x-=int(self.movingspeed*dt)
            self.ground2Rect.x-=int(self.movingspeed*dt)
            #agar pehle ground khtm to doosra lgado
            if self.ground1Rect.right<0:
                self.ground1Rect.x=self.ground2Rect.right
            if self.ground2Rect.right<0:
                self.ground2Rect.x=self.ground1Rect.right
            #iske baad pillar lgalu
            if self.pipe_generate_counter>80:
                self.pipes.append(pillar(sizing,self.movingspeed))
                self.pipe_generate_counter=0
            self.pipe_generate_counter+=1
            
            for i in self.pipes:
                i.update(dt)   

            if len(self.pipes)!=0:
                if self.pipes[0].pillar_upRect.right<0:
                    self.pipes.pop(0)
            self.birdie.G_force(dt)
        if self.start==False and self.t==True:
            self.birdie.G_force(dt)

    def ifscore(self):
        if self.firstime:
            self.score=-1
            self.firstime=False
        self.exit=True
        self.enter=False
        if len(self.pipes)>0:
            #entry
            if(self.birdie.birdieRect.left>self.pipes[0].pillar_downRect.left and self.exit==True):
                self.enter=True
            if(self.birdie.birdieRect.right-10>self.pipes[0].pillar_downRect.right and self.enter==True):
                self.exit=True
                self.score+=1
                self.font=pg.font.Font(None,74)
            
            if(self.notcrash):
                self.text=self.font.render(str(self.score//29 +1),True,(0,0,0))
                self.textRect=self.text.get_rect(center=(275,40))    
            #jab enter aur exit dono kra tb score+=1
            #aur entry tbhi hogi jb exit hui
    
    def blit(self):
        self.win.blit(self.bgImg,(0,-200))
        for i in self.pipes:
            i.createpillar(self.win)
        self.win.blit(self.zameeno1,self.ground1Rect)
        self.win.blit(self.text,self.textRect)
        self.win.blit(self.zameeno1,self.ground2Rect)
        self.win.blit(self.birdie.image,self.birdie.birdieRect)
        if (self.birdie.birdieRect.y>612 and self.exp==False ):
            self.win.blit(self.explosion,(self.birdie.birdieRect.x-38,570))
        elif len(self.pipes):
            if self.birdie.birdieRect.colliderect(self.pipes[0].pillar_downRect) or self.birdie.birdieRect.colliderect(self.pipes[0].pillar_upRect):
                self.exp=True 
                self.win.blit(self.explosion,(self.birdie.birdieRect.x-38,self.birdie.birdieRect.y-33))
        
        if(self.exp==True):
            self.win.blit(self.explosion,(self.birdie.birdieRect.x-38,self.birdie.birdieRect.y-33))

#fixed the biggest crap but can; make bird go down

    def collision(self):
        if self.secure:
            if len(self.pipes):
                print(self.birdie.birdieRect.y)
                if (self.birdie.birdieRect.y>619):
                    self.birdie.birdieRect.y=615
                    mixer.music.play()
                    self.birdie.gravity_on=False
                    self.start=False
                    self.x=False
                    self.secure=False
                elif self.birdie.birdieRect.colliderect(self.pipes[0].pillar_downRect) or self.birdie.birdieRect.colliderect(self.pipes[0].pillar_upRect): 
                    mixer.music.play()
                    self.notcrash=False
                    self.x=False
                    self.boom=False
                    self.t=True
                    self.start=False
            

    
game=Game()


        
import pygame
import random
import sys
import math

class Proton:
    def __init__(self,position):
        self.radius = 8
        self.colour = (255,0,0)
        self.thickness = 0
        self.position = position
        
class Electron:
    def __init__(self, position):
        self.radius = 5
        self.colour = (0,0,255)
        self.thickness = 0
        self.position = position
        
class Atom:
    def __init__(self,position):
        self.ID = random.uniform (1,100)
        self.state = 1
        self.orbitRadius= 30
        self.orbitVelocity= 10
        self.position = position
        self.orbitAngle = 0
        self.proton=Proton(self.position)
        self.electron=Electron((self.position[0],self.position[1]+50))
        self.proton.position=self.position
        self.centre = self.position
        self.excitedTimer = 0
        
    def orbit(self):
        self.orbitAngle+=self.orbitVelocity
        x=self.position[0]+self.orbitRadius*math.sin(math.radians(self.orbitAngle))
        y=self.position[1]+self.orbitRadius*math.cos(math.radians(self.orbitAngle))
        self.electron.position=(x,y)
    
        
    def draw(self,screen):
        self.orbit()
        pygame.draw.circle(screen,self.proton.colour,self.proton.position,self.proton.radius,self.proton.thickness)
        pygame.draw.circle(screen,(255,255,255),self.position,self.orbitRadius,1)
        pygame.draw.circle(screen,self.electron.colour,self.electron.position,self.electron.radius,self.electron.thickness)

class Wave:
    def __init__(self,position,ID):
        self.ID = ID
        self.frequency = demonstrate()                                                                               
        self.amplitude = 10
        self.position = position
        self.x = self.position[0]
        self.y = self.position[1]
        self.origin = position
        self.phase = 0
        self.speed = 5
        self.tip = (0,0)
        self.angle = random.uniform(0,6.283)
        self.exist = True
        self.colour = (255,255,0)
        self.edgeHit = False
        
        
    def create(self):
        points = []
        times=100
        for i in range (times):
            pointX=self.x+i
            pointY=self.y+self.amplitude*(math.sin(self.frequency*(self.x+i)-self.phase))
            translatedX=pointX-self.origin[0]
            translatedY=pointY-self.origin[1]
            rotatedTranslatedX= translatedX*math.cos(self.angle) - translatedY*math.sin(self.angle)
            rotatedTranslatedY= translatedX*math.sin(self.angle) + translatedY*math.cos(self.angle)
            finalX=self.origin[0]+rotatedTranslatedX
            finalY=self.origin[1]+rotatedTranslatedY
            finalPoint=(finalX,finalY)
            points.append(finalPoint)
        if (points[0][0]>1200) or (points[0][1]>700) or (points[0][0]<0) or (points[0][1]<0):
            self.edgeHit=True
            self.exist=False
        self.tip = points[times-1]
        return points
    
    def draw(self,screen):
        self.phase+=0.001
        self.x+=self.speed
        pygame.draw.lines(screen, self.colour, False, self.create(), 2)
        
def demonstrate():
    choose=random.randint(1,3)
    lst=[0.05,0.1,0.15]
    choice=lst[choose-1]
    return choice
        
def excitedChecker(atom,wave):
    if atom.state == 1:
        
        if wave.frequency == 0.05:
            atom.state = 2
            wave.exist = False
            atom.orbitRadius = 40
        if wave.frequency == 0.15:
            atom.state = 3
            wave.exist = False
            atom.orbitRadius = 55
    if atom.state == 2:
        
        if wave.frequency == 0.1:
            atom.state = 3
            wave.exist = False
            atom.orbitRadius = 55
            
def relax(atoms):
    waves=[]
    for atom in atoms:
        if atom.state != 1:
            chance=random.randint(1,10)
            if chance == 1:
                if atom.state == 3:
                    wave=Wave(atom.position,atom.ID)
                    chance2 = random.randint(1,100)
                    if chance2>22:
                        wave.frequency = 0.1
                        atom.state = 2
                        atom.orbitRadius = 40
                    else:
                        wave.frequency=0.15
                        atom.state=1
                        atom.orbitRadius=30
                    waves.append(wave)
                        
                if atom.state == 2:
                    wave=Wave(atom.position,atom.ID)
                    wave.frequency = 0.05
                    waves.append(wave)
                    atom.state = 1
                    atom.orbitRadius = 30
    return waves
    
    
    
    
    
            
def collisionChecker(waves,atoms):
    for wave in waves:
        for atom in atoms:
            distanceX = wave.tip[0]-atom.position[0]
            distanceY = wave.tip[1]-atom.position[1]
            if (distanceX*distanceX + distanceY*distanceY <= atom.orbitRadius*atom.orbitRadius) and wave.ID != atom.ID:
                excitedChecker(atom,wave)
                

    

                
def main():
    pygame.init()
    width, height = 1200, 700
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Waves")
    clock = pygame.time.Clock()
    waves=[]
    atoms=[]
    emissions=[]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clickPosition = event.pos
                    for i in range (10):
                        waves.append(Wave(clickPosition,0))
                if event.button == 3:
                    clickPosition = event.pos
                    atoms.append(Atom(clickPosition))
            
            
                
        
        screen.fill((0, 0, 0))
        collisionChecker(waves,atoms)
        moreWaves=relax(atoms)
        for newWave in moreWaves:
            waves.append(newWave)
        for atom in atoms:
            atom.draw(screen)
        for wave in waves[:]:
            if wave.edgeHit == True:
                emissions.append(wave.frequency)
            if wave.exist == False:
                waves.remove(wave)
            else:
                wave.draw(screen)
                
                
        pygame.display.flip() 
        clock.tick(60)
    

main()

        

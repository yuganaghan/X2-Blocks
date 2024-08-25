import random
import pygame
pygame.font.init()
startMatrix = [2,4,8,16,32,64]
class Block:
    startMatrix = []
    font = pygame.font.SysFont('Fixedsys', 27, 1, False)
    def __init__(self,x,y,value,blockes,colors) :
        self.x = x
        self.y = y
        self.Board_x = y*50
        self.Board_y = x*50+50
        self.value = value
        self.level = 7
        self.colors = colors
        self.Blocks = blockes
    
    def draw(self,display):
        if self.value not in self.colors.keys():
            self.genratecolor()
        color = self.colors[self.value]
        text = self.font.render(self.ChageApperance(), True, (0, 0, 0))
        pygame.draw.rect(display, color, (self.Board_x, self.Board_y, 50, 50), 0, 5)
        pygame.draw.rect(display, (0, 0, 0), (self.Board_x, self.Board_y, 50, 50), 1, 5)
        display.blit(text, (self.Board_x+2, self.Board_y+3))

    def UpadteCorrdinates(self):
        self.Board_x = self.y*50
        self.Board_y = self.x*50+50


    def ChageApperance(self):
        x = str(self.value)
        top =-1
        while len(x)>4:
            x = x[0:len(x)-3]
            top+=1
        if top ==0:
            x+="k"
        elif top == 1:
            x+="m"
        elif top>1:
            x += chr(65+(top-2))
        return x
    def genratecolor(self):
        color = (random.randint(10, 45) * 5, random.randint(10, 45) * 5, random.randint(10, 45) * 5)
        while color in self.colors.values():
            color = (random.randint(0, 25) * 10, random.randint(0, 25) * 10, random.randint(0, 25) * 10)
        self.colors[self.value] = color

        
 
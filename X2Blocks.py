import pygame
import time
import copy 
from GameBoard import gameBoard
pygame.font.init()
pygame.init()

class X2Block():
    def __init__(self) -> None:
        self.display = pygame.display.set_mode((250, 530))
        self.font = pygame.font.SysFont('Fixedsys', 27, 1, False)
        self.run = True
        self.Animate = True
        self.RunAgain = False
        self.CurentBlock= None
        self.Clock = pygame.time.Clock()
        self.GameBoard = gameBoard()
        self.GameOverFont =pygame.font.SysFont('Fixesys',50,1,1)
        self.gameOver = self.GameOverFont.render("GameOver",True,(255,255,255))
        self.Score = self.GameOverFont.render("Score",True,(255,255,255))
        self.ScoreFont = pygame.font.SysFont("Fixesys",40,1,1)

    def main(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN and ~self.Animate:        
                    self.Animate = True
                    x,y = pygame.mouse.get_pos()
                    if 50<y<400 and ~self.GameBoard.GameOver:
                        self.CurentBlock = None
                        self.Update(x//50)
            self.draw()
            self.Clock.tick(30)
            pygame.display.update()
        pygame.quit()


    def draw(self):
        text = self.ScoreFont.render("Score "+str(self.GameBoard.Score),True,(255,255,255))
        self.display.fill((0,0,0))
        pygame.draw.rect(self.display, (255, 255, 255), (0, 50, 250, 350))
        pygame.draw.rect(self.display, (0, 0, 0), (0, 50, 250, 350), 2)
        pygame.draw.rect(self.display, (255, 255, 255), (100, 50 + 380, 50, 50))
        pygame.draw.rect(self.display, (255, 255, 255), (47, 50 + 400, 50, 50))
        self.GameBoard.DrawBottomBlocks(self.display)
        self.GameBoard.ShowBoard(self.display)
        self.display.blit(text,(30,10))
        # Vertical line
        for i in range(5):
            pygame.draw.line(self.display, (0, 0, 0), (50 * i, 50), (50 * i, 350 + 50))
        # Horizontal Lines
        for i in range(7):
            pygame.draw.line(self.display, (0, 0, 0), (0, 50 + (50 * i)), (325, 50 + (i * 50)))

        if self.GameBoard.GameOver:
            self.ShowGameOver()
        
    def ShowGameOver(self):
        width = 200
        height = 300
        ScoreInt = self.GameOverFont.render(str(self.GameBoard.Score),True,(255,255,255))
        pygame.draw.rect(self.display,(0,0,0),((250-width)//2,(530-height)//2,width,height),0,15)
        pygame.draw.rect(self.display,(255,0,255),((250-width)//2-3,(530-height)//2-3,width+6,height+6),3,20)
        self.display.blit(self.gameOver,((250-width-15),(180)))
        self.display.blit(self.Score,((250-width-15),(240)))
        self.display.blit(ScoreInt,((250-width-15),(280)))

    def Update(self,x):
        self.GameBoard.CheckCurrentLine(x)
        if self.GameBoard.Top !=-1:
            self.GameBoard.ChageBottomBlocks()
            self.linearanimation([x*50,350],[x*50,50+self.GameBoard.Top*50],self.GameBoard.MovingBlock)
            self.GameBoard.Board[self.GameBoard.Top][x] = copy.copy(self.GameBoard.MovingBlock)
            self.GameBoard.MovingBlock = copy.copy(self.GameBoard.CurrentBlock)
            self.CurentBlock = [self.GameBoard.Top,x]
            self.GameBoard.Score+=2
            self.MeargeBlock()
            while self.RunAgain:
                self.MeargeBlock()
            self.HandleNewBlock()
        else:
            self.GameBoard.Board[6][x].value = self.GameBoard.CurrentBlock.value
            self.GameBoard.Board[6][x].value *=2 
        self.GameBoard.CheckGameOver()
            

    def MeargeBlock(self):
        self.RunAgain = False
        mearginBlocks = self.GameBoard.MeargeBlocks(self.CurentBlock)
        if mearginBlocks["change"] == 0:
            return
        if mearginBlocks["Right"] !=-1:
            time.sleep(0.2)
            self.RunAgain =True
            x,y = mearginBlocks["Right"]
            self.Animate =True
            self.torightanimation([y*50,x*50+50],[self.CurentBlock[1]*50,self.CurentBlock[0]*50+50],self.GameBoard.Board[x][y])
            self.GameBoard.UpdateBoard(self.CurentBlock,{"Right":mearginBlocks["Right"]},"Right")


        if mearginBlocks["Left"] !=-1:
            time.sleep(0.2)
            self.RunAgain =True
            x,y = mearginBlocks["Left"]
            self.Animate =True
            self.toleftanimation([y*50,x*50+50],[self.CurentBlock[1]*50,self.CurentBlock[0]*50+50],self.GameBoard.Board[x][y])
            self.GameBoard.UpdateBoard(self.CurentBlock,{"Left":mearginBlocks["Left"]},"Left")


        if mearginBlocks["UP"] !=-1:
            time.sleep(0.2)
            self.RunAgain = True
            x,y = mearginBlocks["UP"]
            self.Animate =True
            self.linearanimation([self.CurentBlock[1]*50,self.CurentBlock[0]*50+50],[y*50,x*50+50],self.GameBoard.Board[self.CurentBlock[0]][self.CurentBlock[1]])
            self.GameBoard.UpdateBoard(self.CurentBlock,{"UP":mearginBlocks["UP"]},"UP")
            self.CurentBlock = [x,y]
            self.GameBoard.SetBoard()
        
        self.FillEmptyPlace()
        
    def FillEmptyPlace(self):
        moving = False
        for i in range(5):
            movingPieces = []
            j=6
            moving = False
            while j>0:
                if self.GameBoard.Board[j][i] !=0:
                    movingPieces.append([j,i])
                    if self.GameBoard.Board[j-1][i] ==0:
                        i-=1
                        moving = True
                        self.Animate = True
                        break
                j-=1
            if moving:
                movingPieces.reverse()
                for k in movingPieces:
                    self.Animate = True
                    time.sleep(0.2)
                    self.linearanimation([k[1]*50,k[0]*50+50], [k[1]*50, k[0]*50],self.GameBoard.Board[k[0]][k[1]])
                    self.GameBoard.Board[k[0]-1][k[1]] = self.GameBoard.Board[k[0]][k[1]]
                    self.GameBoard.Board[k[0]-1][k[1]].x,self.GameBoard.Board[k[0]-1][k[1]].y = k[0]-1,k[1]
                    self.GameBoard.Board[k[0]][k[1]] = 0


    def HandleNewBlock(self):
        self.GameBoard.AddNewBlock()
        temp = self.MoivngEveryBlock()
        while temp:
            temp = self.MoivngEveryBlock()

    
    def MoivngEveryBlock(self):
        RunAgain = False
        left = self.CurentBlock[1]-1
        right = self.CurentBlock[1]+1
        self.FillEmptyPlace()
        while left >-1:
            last = 6
            while last>-1:
                if self.GameBoard.Board[last][left] !=0:
                    self.CurentBlock = [last,left]
                    meargingBlocks = self.GameBoard.MeargeBlocks(self.CurentBlock)
                    if meargingBlocks["change"] >0:
                        RunAgain = False
                        self.MeargeBlock()
                        while self.RunAgain:
                            self.MeargeBlock()
                last-=1
            left-=1
        while right <5 :
            last = 6
            while last > -1:
                if self.GameBoard.Board[last][right] !=0:
                    self.CurentBlock = [last,right]
                    meargingBlocks = self.GameBoard.MeargeBlocks(self.CurentBlock)
                    if meargingBlocks["change"] >0:
                        RunAgain = False
                        self.MeargeBlock()
                        while self.RunAgain:
                            self.MeargeBlock()
                last-=1
            right += 1
        return RunAgain
                        


    def linearanimation(self,first, last, piece):
        if self.Animate:
            if first == last:
                piece.Board_x=first[0]
                piece.Board_y=first[1]
            while first[1] > last[1]:
                piece.Board_x = first[0]
                piece.Board_y = first[1]
                first[1] -= 2
                self.draw()
                self.GameBoard.ShowBoard(self.display)
                piece.draw(self.display)
                pygame.display.update()
            piece.x,piece.y = (last[1]-50)//50,last[0]//50 
            self.Animate = False

    def toleftanimation(self,first, last, piece):
        if self.Animate:
            while first[0] > last[0]:
                piece.Board_x = first[0]
                piece.Board_y = first[1]
                first[0] -= 1
                self.draw()
                self.GameBoard.ShowBoard(self.display)
                piece.draw(self.display)
                pygame.display.update()
            self.Animate = False

    def torightanimation(self,first, last, piece):
        if self.Animate:
            while first[0] <= last[0]:
                piece.Board_x = first[0]
                piece.Board_y = first[1]
                first[0] += 1
                self.draw()
                self.GameBoard.ShowBoard(self.display)
                piece.draw(self.display)
                pygame.display.update()
            self.Animate = False

    def todownanimation(self,first, last, piece):
        if self.Animate:
            while first[1] <= last[1]:
                piece.Board_y = first[1]
                first[1] += 1
                self.draw()
                self.GameBoard.ShowBoard(self.display)
                piece.draw(self.display)
                pygame.display.update()
            self.Animate = False


main = X2Block()
if __name__ == "__main__":
    main.main()
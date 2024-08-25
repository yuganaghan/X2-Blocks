from Blocks import Block
import random
import copy
class gameBoard:
    def __init__(self) -> None:
        self.level = 7
        self.Top =-1
        self.colors = {
        2:(255,0,0),
        4:(0,255,0),
        8:(0,0,255),
        16:(255,0,255),
        32:(255,255,0),
        64:(0,255,255)
    }
        self.Blocks = [2,4,8,16,32,64]
        self.CurrentBlocks = [2,4,8,16,32,64,128]
        self.Board = [[0 for _ in range (5)] for _ in range(7)]
        self.CurrentBlock = Block(7.6,2,self.Blocks[(random.randint(0,100))%6],self.CurrentBlocks,self.colors)
        self.NextBlock = Block(8,0.94,self.Blocks[(random.randint(0,100))%6],self.CurrentBlocks,self.colors)
        self.MovingBlock = copy.copy(self.CurrentBlock)
        self.DeletBlock = []
        self.MaxBlock = 128
        self.GameOver = False
        self.Score = 0

    def DrawBottomBlocks(self,display):
        self.CurrentBlock.draw(display)
        self.NextBlock.draw(display)

    def ChageBottomBlocks(self):
        self.CurrentBlock.value = self.NextBlock.value
        self.NextBlock.value = self.Blocks[random.randint(0,100)%6]

    def CheckCurrentLine(self,x):
        i=6
        while(i>-1):
            if self.Board[i][x] ==0:
                i-=1
            else:
                break
        self.Top = i+1 if (i+1)!=7 else -1

    def SetBoard(self):
        for i in self.Board:
            for j in i:
                if j!=0:
                    j.UpadteCorrdinates()


    def ShowBoard(self,display):
        for i in self.Board:
            for j in i:
                if j!= 0:
                    j.draw(display)
    
    def printC(self):
        for i in self.Board:
            print([j if j == 0 else j.value for j in i])
        print("\n")
    
    def printXandY(self):
        for i in self.Board:
            print([(-1,-1) if j == 0 else (j.x,j.y) for j in i])
        print("\n")

    def MeargeBlocks(self,position):
        x,y =position
        meargeBlock={
            "UP" :-1,
            "Left" :-1,
            "Right" :-1,
            "change":0
        }
        if self.Board[x][y] != 0:
            value = self.Board[x][y].value
            if x>0:
                if self.Board[x-1][y] != 0 and self.Board[x-1][y].value == value:
                    meargeBlock["UP"]= (x-1,y)
                    meargeBlock["change"]+=1
            if y>0:
                if self.Board[x][y-1] != 0 and self.Board[x][y-1].value == value:
                    meargeBlock["Right"] = (x,y-1)
                    meargeBlock["change"]+=1
            if y<4:
                if self.Board[x][y+1] != 0 and self.Board[x][y+1].value == value:
                    meargeBlock["Left"]=(x,y+1)
                    meargeBlock["change"]+=1
        self.Score += 2* meargeBlock["change"]
        return meargeBlock
    
    def UpdateBoard(self,Position,changing,key):
        x,y = Position
        x1,y1 = changing[key] 
        self.Board[x][y].value *=2
        self.Board[x1][y1] = 0
        if key == "UP": 
            self.Board[x1][y1] = self.Board[x][y]
            self.Board[x][y] = 0
            self.Board[x1][y1].x=x1
            self.Board[x1][y1].y=y1
            self.Board[x1][y1].UpadteCorrdinates()
    

    def AddNewBlock(self):
        FindMax =0
        for i in self.Board:
            for j in i:
                if j!=0:
                    FindMax = max(FindMax,j.value)
        while FindMax not in self.CurrentBlocks:
            self.CurrentBlocks.append(FindMax)
            FindMax /=2
        self.CurrentBlocks.sort()
        self.HandleRemovingBlock()



    def HandleRemovingBlock(self):
        Division = self.CurrentBlocks[-1]/self.MaxBlock 
        while Division> 4:
            Division/=8
            temp = self.Blocks.pop(0)
            self.Blocks.append(self.Blocks[-1]*2)
            self.CurrentBlocks.remove(temp)
            self.MaxBlock = self.CurrentBlocks[self.CurrentBlocks.index(self.MaxBlock)+3]
            self.DeletBlock.append(temp)
        if len(self.DeletBlock)>0:
            self.DeleteBlocks()
    
    def DeleteBlocks(self):
        if len(self.DeletBlock)>0:
            for i in self.DeletBlock:
                self.colors.pop(i)
                for j in range(7):
                    for k in range(5):
                        if self.Board[j][k] !=0:
                            if self.Board[j][k].value == i:
                                self.Board[j][k] = 0
            if self.CurrentBlock.value in self.DeletBlock:
                self.CurrentBlock.value == self.Blocks[random.randint(0,100)%6]
            if self.NextBlock.value in self.DeletBlock:
                self.NextBlock.value == self.Blocks[random.randint(0,100)%6]
        self.DeletBlock = []
    
    def CheckGameOver(self):
        self.GameOver = False
        values = []
        for i in range(5):
            if self.Board[6][i] !=0:
                values.append(self.Board[6][i].value)
            else:
                return
        if self.CurrentBlock.value not in values:
            self.GameOver = True
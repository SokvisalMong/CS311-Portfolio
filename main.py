import pygame
import random

pygame.init()

# Setting Initial colors
bg_color = (192, 192, 192)
grid_color = (128, 128, 128)

# The size of the minesweeper field
boardWidth = 15
boardHeight = 15

# Duh
numMines = 9

# The size of the icons used as sprites
# but since they are all squares, then
# we don't need a height
iconWidth = 32

# Padding for the top for text
topBorder = 16
# Padding for left, right and bottom for looks
otherBorder = 100

# The size of the screen itself
displayWidth = iconWidth * boardWidth + topBorder * 2
displayHeight = iconWidth * boardHeight + topBorder + otherBorder

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
timer = pygame.time.Clock()
pygame.display.set_caption("Minesweeper")

# This is such a shit way to implement this
# But I am running on 0 hours of sleep for the past 30 hours
# Take it or leave it
spriteEmpty = pygame.image.load("Sprites/empty.png")
spriteFlag = pygame.image.load("Sprites/flag.png")
spriteGrid = pygame.image.load("Sprites/grid.png")
spriteGrid1 = pygame.image.load("Sprites/grid1.png")
spriteGrid2 = pygame.image.load("Sprites/grid2.png")
spriteGrid3 = pygame.image.load("Sprites/grid3.png")
spriteGrid4 = pygame.image.load("Sprites/grid4.png")
spriteGrid5 = pygame.image.load("Sprites/grid5.png")
spriteGrid6 = pygame.image.load("Sprites/grid6.png")
spriteGrid7 = pygame.image.load("Sprites/grid7.png")
spriteGrid8 = pygame.image.load("Sprites/grid8.png")
spriteMine = pygame.image.load("Sprites/mine.png")
spriteMineClicked = pygame.image.load("Sprites/mineClicked.png")
spriteMineFalse = pygame.image.load("Sprites/mineFalse.png")


fieldGrid = []  # The main grid
minesPos = []  # Pos of the mines


# Text popup function
def drawText(text, size, yOffset = 0):
    popUpText = pygame.font.SysFont("comicsans", size, True).render(text, True, (0, 0, 0))
    rect = popUpText.get_rect()
    rect.center = (boardWidth * iconWidth / 2 + topBorder, boardHeight * iconWidth / 2 + otherBorder + yOffset)
    gameDisplay.blit(popUpText, rect)


# Create class grid
class Grid:
    def __init__(self, xGrid, yGrid, mines):
        # Remapping the positions
        self.xGrid = xGrid
        self.yGrid = yGrid 

        self.clicked = False 
        self.mineClicked = False 
        self.mineFalse = False  
        self.flag = False 

        # Create rectObject to handle drawing and collisions
        self.rect = pygame.Rect(topBorder + self.xGrid * iconWidth, otherBorder + self.yGrid * iconWidth, iconWidth, iconWidth)
        
        # mines here can be a value from -1 to 8
        # -1 being that it is a mine
        # 0 - 8 is the number of mines near that grid
        self.val = mines

    def drawGrid(self):
        # Draw the grid according to bool variables and value of grid
        if self.mineFalse:
            gameDisplay.blit(spriteMineFalse, self.rect)

        # I'm going to commit arson at the nearest controlled forest fire
        else:
            if self.clicked:
                if self.val == -1:
                    if self.mineClicked:
                        gameDisplay.blit(spriteMineClicked, self.rect)
                    else:
                        gameDisplay.blit(spriteMine, self.rect)
                else:
                    if self.val == 0:
                        gameDisplay.blit(spriteEmpty, self.rect)
                    elif self.val == 1:
                        gameDisplay.blit(spriteGrid1, self.rect)
                    elif self.val == 2:
                        gameDisplay.blit(spriteGrid2, self.rect)
                    elif self.val == 3:
                        gameDisplay.blit(spriteGrid3, self.rect)
                    elif self.val == 4:
                        gameDisplay.blit(spriteGrid4, self.rect)
                    elif self.val == 5:
                        gameDisplay.blit(spriteGrid5, self.rect)
                    elif self.val == 6:
                        gameDisplay.blit(spriteGrid6, self.rect)
                    elif self.val == 7:
                        gameDisplay.blit(spriteGrid7, self.rect)
                    elif self.val == 8:
                        gameDisplay.blit(spriteGrid8, self.rect)

            else:
                if self.flag:
                    gameDisplay.blit(spriteFlag, self.rect)
                else:
                    gameDisplay.blit(spriteGrid, self.rect)

    def revealGrid(self):
        self.clicked = True

        if self.val == 0:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < boardWidth:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < boardHeight:
                            if not fieldGrid[self.yGrid + y][self.xGrid + x].clicked:
                                fieldGrid[self.yGrid + y][self.xGrid + x].revealGrid()
        elif self.val == -1:
            for m in minesPos:
                if not fieldGrid[m[1]][m[0]].clicked:
                    fieldGrid[m[1]][m[0]].revealGrid()

    def updateValue(self):
        if self.val != -1:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < boardWidth:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < boardHeight:
                            if fieldGrid[self.yGrid + y][self.xGrid + x].val == -1:
                                self.val += 1


def gameLoop():
    gameState = "Playing" 
    minesLeft = numMines 
    global fieldGrid  
    fieldGrid = []
    global minesPos
    t = 0 # Set the timer to 0

    # Generate mines
    minesPos = [[random.randrange(0, boardWidth),
              random.randrange(0, boardHeight)]]

    for c in range(numMines - 1):
        pos = [random.randrange(0, boardWidth),
               random.randrange(0, boardHeight)]
        same = True
        while same:
            for i in range(len(minesPos)):
                if pos == minesPos[i]:
                    pos = [random.randrange(0, boardWidth), random.randrange(0, boardHeight)]
                    break
                if i == len(minesPos) - 1:
                    same = False
        minesPos.append(pos)

    # Generate the grid
    for j in range(boardHeight):
        line = []
        for i in range(boardWidth):
            if [i, j] in minesPos:
                line.append(Grid(i, j, -1))
            else:
                line.append(Grid(i, j, 0))
        fieldGrid.append(line)

    # Update the grid
    for i in fieldGrid:
        for j in i:
            j.updateValue()

    # Main Loop
    while gameState != "Exit":
        # Reset screen
        gameDisplay.fill(bg_color)

        # User inputs
        for event in pygame.event.get():
            # Check if player close window
            if event.type == pygame.QUIT:
                gameState = "Exit"
            # Check if play restart
            if gameState == "Game Over" or gameState == "Win":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        gameLoop()
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    for i in fieldGrid:
                        for j in i:
                            if j.rect.collidepoint(event.pos):
                                if event.button == 1:
                                    # If player left clicked of the grid
                                    j.revealGrid()
                                    # Toggle flag off
                                    if j.flag:
                                        minesLeft += 1
                                        j.falg = False
                                    # If it's a mine
                                    if j.val == -1:
                                        gameState = "Game Over"
                                        j.mineClicked = True
                                elif event.button == 3:
                                    # If the player right clicked
                                    if not j.clicked:
                                        if j.flag:
                                            j.flag = False
                                            minesLeft += 1
                                        else:
                                            j.flag = True
                                            minesLeft -= 1

        # Check if won
        w = True
        for i in fieldGrid:
            for j in i:
                j.drawGrid()
                if j.val != -1 and not j.clicked:
                    w = False
        if w and gameState != "Exit":
            gameState = "Win"

        # Draw Texts
        if gameState != "Game Over" and gameState != "Win":
            t += 1
        elif gameState == "Game Over":
            drawText("Game Over!", 50)
            drawText("R to restart", 35, 50)
            for i in fieldGrid:
                for j in i:
                    if j.flag and j.val != -1:
                        j.mineFalse = True
        else:
            drawText("You WON!", 50)
            drawText("R to restart", 35, 50)
        # Draw time
        s = str(t // 15)
        screen_text = pygame.font.SysFont("comicsans", 50).render(s, True, (0, 0, 0))
        gameDisplay.blit(screen_text, (topBorder, topBorder))
        # Draw mine left
        screen_text = pygame.font.SysFont("comicsans", 50).render(minesLeft.__str__(), True, (0, 0, 0))
        gameDisplay.blit(screen_text, (displayWidth - topBorder - 50, topBorder))

        pygame.display.update()  # Update screen

        timer.tick(15)  # Tick fps


gameLoop()
pygame.quit()
quit()

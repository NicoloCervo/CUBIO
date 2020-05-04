import pygame
from Skeleton import Skeleton
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_WHITE, FONT_COLOR, BOX_PLAYER1_X, WIDTH_BOX_PLAYER2, WIDTH_ROBOT_PLAYER2, BOX_PLAYER2_X, BOX_PLAYER_Y, ROBOT1_X, ROBOT2_X, ROBOT_Y, FONT_PLAYER1_X, FONT_PLAYER1_Y, FONT_PLAYER2_X, FONT_PLAYER2_Y, BOARD_POSITION_X, BOARD_POSITION_Y, FPS

#Loads all the images needed for drawing the game board
pygame.display.init()
pygame.font.init()
pygame.mixer.quit()

#Loads all the images
logo = pygame.image.load('images/myLogo.png')
background = pygame.image.load('images/background.jpg')
front = pygame.image.load('images/front.png')
frontB = pygame.image.load('images/frontBlue.png')
frontR = pygame.image.load('images/frontRed.png')
top = pygame.image.load('images/top.png')
topB = pygame.image.load('images/topBlue.png')
topR = pygame.image.load('images/topRed.png')
side = pygame.image.load('images/side.png')
sideB = pygame.image.load('images/sideBlue.png')
sideR = pygame.image.load('images/sideRed.png')
boxPlayer1 = pygame.image.load('images/tabPl1.png')
boxPlayer2 = pygame.image.load('images/tabPl2.png')
robotPlayer1 = pygame.image.load('images/robot1.png')
robotPlayer1_ACTIVE = pygame.image.load('images/robot1Active.png')
robotPlayer2 = pygame.image.load('images/robot2.png')
robotPlayer2_ACTIVE = pygame.image.load('images/robot2Active.png')
turnText = pygame.image.load('images/turn.png')
delName = pygame.image.load('images/coverName.png')
delTurn = pygame.image.load('images/coverTurn.png')
#layer = pygame.image.load('images/game_over_layer.png')

#Loads font
font = pygame.font.Font("fonts/playerFont.ttf", 25)
win_font = pygame.font.Font("fonts/winnerFont.ttf", 40)

class UserInterface:

    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.fill(COLOR_WHITE)
        pygame.display.set_caption("CUBIO")
        pygame.display.set_icon(logo)
        self.screen.blit(background,(0,0))
        self.turn = 0
        self.clicked = []
        self.player1Names = ['Player 1']
        self.player2Names = ['Player 2']
        self.freezedBox1 = [False]
        self.freezedBox2 = [False]
        self.game_over = False


    def drawBoard(self, screen):

        #Finds the relevant dimensions of the tiles
        self.fWidth = pygame.Surface.get_width(front)-1
        self.sWidth = pygame.Surface.get_width(side)-1
        self.tHeight = pygame.Surface.get_height(top)-1

        """	Creates a dictionary in which the keys will denote the unique integer identifier of a tile
            and the values will consist of tuple determining its position. This will be useful when drawing
            the board, when coloring each tile, and when determining if the user clicked on a tile
        """
        self.tilePos = {}
        identifier = 0
        number_cubes = 3

        """	The board is drawn in a upward vertical direction for the front and top faces of each cube. The
            lateral face is drawn in a horizontal direction. The loops start by drawing the bottom left tile
            of the front face.
        """
        for k in range(number_cubes):
            #These two loops draw the front and top portion of the face of the cube
            for j in range(3):
                for i in range(6):
                    #Checks if we are currently traversing the front face
                    if i in (0,1,2):
                        x_coor = BOARD_POSITION_X+(3*k+j)*self.fWidth
                        y_coor = BOARD_POSITION_Y+(3*k-i)*self.fWidth
                        #The front tile is drawn on position (x_coor, y_coor)
                        self.screen.blit(front, (x_coor, y_coor))
                        #The position of the tile is stored with its unique identifier
                        self.tilePos[identifier] = (x_coor,y_coor) 
                        #Sets the identifier of the next tile
                        identifier = identifier+1
                        #These coordinates are used as an anchor point when drawing the first lateral tile
                        x = x_coor
                        y = y_coor
                    else:
                        x_coor += int((i-2)/2)*self.sWidth
                        y_coor -= self.tHeight
                        self.screen.blit(top, (x_coor, y_coor))
                        self.tilePos[identifier] = (x_coor,y_coor)
                        identifier = identifier+1
            #This for loop draws the lateral portion of the face of the cube
            for i in range (9):
                x_c = x+self.fWidth+self.sWidth*(i%3)
                y_c = y-(i%3+1)*self.tHeight+int(i/3)*self.fWidth
                self.screen.blit(side, (x_c, y_c))
                self.tilePos[identifier] = (x_c,y_c)
                identifier = identifier+1

    def isClicked(self,p,obj):

        for i in range(81):
            """	Creates a mapping from the set of identifier to the faces of the cubes. 
                j=2: lateral face
                j=1: top face
                j=0: front face
            """
            if (int(int(i/3)/3)-2)%3 == 0:
                j = 2
            elif (int(i/3)-int(int(i/3)/9))%2 != 0:
                j = 1
            else:
                j = 0

            #Checks if the tile was previously clicked, if so, no changes will be made
            if (i not in self.clicked):
                #Checks if the mouse click lies inside one of the lateral tiles of each cube
                if (abs(2*(p[0]-self.tilePos[i][0])-13)<13 and abs(p[1]+(16/13)*(p[0]-self.tilePos[i][0])-self.tilePos[i][1]-33)<16) and j == 2:
                    #Checks the turn of the player and colors the tiles accoridngly
                    if self.turn%2 == 0: 
                        self.colorTile(i,sideB,1,2,obj) 
                    else: 
                        self.colorTile(i,sideR,1,1,obj)

                elif (abs(2*(p[1]-self.tilePos[i][1])-16)<16 and abs(p[0]+(12/17)*(p[1]-self.tilePos[i][1])-self.tilePos[i][0]-29)<16) and j == 1:
                    if self.turn%2 == 0: 
                        self.colorTile(i,topB,2,2,obj) 
                    else:
                        self.colorTile(i,topR,2,1,obj)

                elif (abs(2*(p[0]-self.tilePos[i][0])-34)<34 and abs(2*(p[1]-self.tilePos[i][1])-34)<34) and j == 0:
                    if self.turn%2 == 0: 
                        self.colorTile(i,frontB,2,2,obj) 
                    else: 
                        self.colorTile(i,frontR,2,1,obj)

    def colorTile(self, index, tile_color, tile_type, player, obj):

        """	args:
                index: identifier of the tile
                tile_color: colored tile
                tyle_type: integer that is either 1 or 2. Needed to determine which mapping 
                           to use from identefier to its corrisponding matrix position
                player: Marks the game matrix with either 1 (player 1) or 2 (player 2)
        """
        #Colors the tile with blue
        self.screen.blit(tile_color, (self.tilePos[index][0],self.tilePos[index][1]))
        #Freezes the current tile
        self.clicked.append(index)
        #Passes the turn to the other player
        self.turn = self.turn + 1
        if tile_type == 1:
            #Updates the game matrix
            obj.mark(int(index/3)-3*(int(int(index/3)/9)+1),index%3+3,player)
        else:
            obj.mark(int((index+3*int(int(index/3)/9))/6)+int(int(index/3)/9),(index+3*int(int(index/3)/9))%6,player)

    def playerBox(self,fontX,fontY,robot,robotX,robotY,box,boxX,boxY,p,clickedBox,nameList,obj):

        char_max = 13
        active = True
        text_box = pygame.Rect((boxX,boxY,pygame.Surface.get_width(box),pygame.Surface.get_height(box)))
        name = nameList[-1]
        count_chars = len(name)
        clicked_away = False

        if text_box.collidepoint(p):
            self.screen.blit(robot, (robotX, robotY))
            pygame.display.update() 
            while active:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit(0) #maybe replace with return and check in game loop?
                    elif event.type == pygame.KEYDOWN and not clicked_away:
                        if event.key == pygame.K_BACKSPACE and count_chars>0:
                            self.screen.blit(delName,(fontX-1,fontY))
                            count_chars -= 1
                            name = name[:-1]
                            self.screen.blit(font.render(name, True, FONT_COLOR),(fontX,fontY))
                            pygame.display.update() 

                        elif (event.unicode.isalnum() or event.key == pygame.K_SPACE) and count_chars <= char_max:
                            name += event.unicode
                            self.screen.blit(font.render(name, True, FONT_COLOR),(fontX,fontY))	
                            pygame.display.update() 		 				
                            count_chars += 1
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if text_box.collidepoint(pygame.mouse.get_pos()):
                            clicked_away = False		
                        else:
                            clicked_away = True
                            nameList.append(name)
                            self.isClicked(pygame.mouse.get_pos(),obj)
                            self.printTurn()
                            if len(self.clicked)!=0:
                                clickedBox.append(True)
                                active = False
    def printTurn(self):
        if self.turn%2 != 0:
            self.screen.blit(delTurn,(BOX_PLAYER2_X+20,BOX_PLAYER_Y-15))
            self.screen.blit(turnText,(BOX_PLAYER1_X+pygame.Surface.get_width(boxPlayer2)/2+20,BOX_PLAYER_Y-15))
        else:
            self.screen.blit(delTurn,(BOX_PLAYER1_X+pygame.Surface.get_width(boxPlayer2)/2+20,BOX_PLAYER_Y-15))
            self.screen.blit(turnText,(BOX_PLAYER2_X+20,BOX_PLAYER_Y-15))

    def gameOver(self,inst):
        if inst.result == 1 or inst.result == 2:
                self.screen.blit(delTurn,(BOX_PLAYER2_X+20,BOX_PLAYER_Y-15))
                self.screen.blit(delTurn,(BOX_PLAYER1_X+pygame.Surface.get_width(boxPlayer2)/2+20,BOX_PLAYER_Y-15))
                if inst.result == 1:
                    self.screen.blit(robotPlayer2,(ROBOT2_X,ROBOT_Y))
                    self.screen.blit(font.render(self.player1Names[-1].upper()+' WINS!', True, COLOR_WHITE),(350,50))
                else:
                    self.screen.blit(robotPlayer1,(ROBOT1_X,ROBOT_Y))
                    self.screen.blit(font.render(self.player2Names[-1].upper()+' WINS!', True, COLOR_WHITE),(350,50))
                self.game_over = True
                #self.screen.blit(layer,(0,0))

    def gameLoop(self):

        clock = pygame.time.Clock()
        running = True

        game = Skeleton()
        self.drawBoard(self.screen)
    
        self.screen.blit(boxPlayer1,(BOX_PLAYER1_X,BOX_PLAYER_Y))
        self.screen.blit(robotPlayer1,(ROBOT1_X,ROBOT_Y))
        self.screen.blit(font.render(self.player1Names[0], True, FONT_COLOR),(FONT_PLAYER1_X,FONT_PLAYER1_Y))

        self.screen.blit(boxPlayer2,(BOX_PLAYER2_X,BOX_PLAYER_Y))
        self.screen.blit(robotPlayer2,(ROBOT2_X,ROBOT_Y))
        self.screen.blit(font.render(self.player2Names[0], True, FONT_COLOR),(FONT_PLAYER2_X,FONT_PLAYER2_Y))
        self.screen.blit(turnText,(BOX_PLAYER2_X+20,BOX_PLAYER_Y-15))

 
        while running:	
            #Loops through all the events of the game
            for event in pygame.event.get():
                #Checks whether the user exited the window 
                if event.type == pygame.QUIT:
                    running = False
                if not self.game_over:
                    #Checks whether the user clicked anywhere on the screen
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        #The position of the mouse click is stored
                        pos = pygame.mouse.get_pos()
                        if self.freezedBox1[-1] and self.freezedBox2[-1]:
                            self.isClicked(pos,game)
                            self.printTurn()
                        if not self.freezedBox1[-1] or not self.freezedBox2[-1]:
                            if not self.freezedBox1[-1] and self.freezedBox2[-1]:
                                self.playerBox(FONT_PLAYER1_X,FONT_PLAYER1_Y,robotPlayer1_ACTIVE,ROBOT1_X,ROBOT_Y,boxPlayer1,BOX_PLAYER1_X,BOX_PLAYER_Y,pos,self.freezedBox1,self.player1Names,game)
                            if not self.freezedBox2[-1]:
                                self.playerBox(FONT_PLAYER2_X,FONT_PLAYER2_Y,robotPlayer2_ACTIVE,ROBOT2_X,ROBOT_Y,boxPlayer2,BOX_PLAYER2_X,BOX_PLAYER_Y,pos,self.freezedBox2,self.player2Names,game)
            self.gameOver(game)
            #Updates the screen
            pygame.display.update() 
            #Restricts the game to run on a specifed number of FPS
            clock.tick(FPS) #does this need to be insie the loop? seems weird.
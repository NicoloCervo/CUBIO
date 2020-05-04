import pygame, os
from Skeleton import Skeleton
import constants as const

pygame.init() 

#Loads images
logo = pygame.image.load('images/myLogo.png')
background = pygame.image.load('images/background.jpg') 
grid = pygame.image.load('images/grid.png')
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
robotPlayer1_DEAD = pygame.image.load('images/robot1Dead.png')
robotPlayer2 = pygame.image.load('images/robot2.png')
robotPlayer2_ACTIVE = pygame.image.load('images/robot2Active.png')
robotPlayer2_DEAD = pygame.image.load('images/robot2Dead.png')
turnText = pygame.image.load('images/turn.png')
layer = pygame.image.load('images/game_over_layer.png')
newGame_Box = pygame.image.load('images/newGameBar.png')
newGame_button = pygame.image.load('images/newGameBUTTON.png')
newGame_buttonA = pygame.image.load('images/newGameHover.png')

#Loads fonts
font = pygame.font.Font("fonts/playerFont.ttf", 25)
win_font = pygame.font.Font("fonts/winnerFont.ttf", 40)

#Loads sounds
click_sound = pygame.mixer.Sound("sounds/tile_click.wav")
robotACTIVE_sound = pygame.mixer.Sound("sounds/robot_activation.wav")
background_sound = pygame.mixer.Sound("sounds/background_sound.wav")

#Sets the position of the game window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (const.WINDOW_X, const.WINDOW_Y)

class UserInterface:

    def __init__(self):

        #Creates the game window
        self.screen = pygame.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))
        self.screen.fill(const.COLOR_WHITE)
        pygame.display.set_caption("CUBIO")
        pygame.display.set_icon(logo)

        #Keeps track of the turns
        self.turn = 0

        #Number of wins for player 1 and 2
        self.winsp1 = 0
        self.winsp2 = 0

        #List containing all the clicked tiles
        self.clicked = []

        #Name of player 1 and 2
        self.player1Name = ['Player 1']
        self.player2Name = ['Player 2']

        #Describes the state of the robots for each player
        self.inactive_robot1 = [True]
        self.inactive_robot2 = [True]

        #Needed to make the boxes permanently inactive when the game begins
        self.player1_first_move = [False]
        self.player2_first_move = [False]

        #Needed to make the boxes temporarly inactive when player clicks away
        self.box1_active = [False]
        self.box2_active = [False]

        #A dictionary which has as key a tuple containing the identefier of a tile and
        #an integer which indicates the face it appears on. The value in an integer denoting 
        #player 1 or player 2
        self.colored_tiles = {}

        #Game state
        self.game_over = False

    def drawBoard(self, screen):

        #Finds the relevant dimensions of the tiles
        self.fWidth = pygame.Surface.get_width(front)-1
        self.sWidth = pygame.Surface.get_width(side)-1
        self.tHeight = pygame.Surface.get_height(top)-1

        """	Creates a dictionary in which the keys will denote the unique integer identifier of a tile
            and the values will consist of tuples determining its position. This will be useful when drawing
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
            #The first two loops draw the front and top portions of the face of the cube
            for j in range(3):
                for i in range(6):
                    #Checks if we are currently traversing the front face
                    if i in (0,1,2):
            
                        x_coor = const.BOARD_POSITION_X + (3*k+j)*self.fWidth
                        y_coor = const.BOARD_POSITION_Y + (3*k-i)*self.fWidth

                        #Checks if any tiles in the front face have been colored
                        if (identifier, 0) in self.colored_tiles:
                            #Checks if player 1 colored the tile
                            if self.colored_tiles[(identifier, 0)] == 1:
                                #Colors the tile red
                                self.screen.blit(frontR, (x_coor, y_coor))

                            #If player 1 did not click the tile, then player 2 did
                            else:
                                #Colors the tile blue
                                self.screen.blit(frontB, (x_coor, y_coor))

                        #If no tiles have been colored, draw empty ones
                        else:
                            #The front tile is drawn on position (x_coor, y_coor)
                            self.screen.blit(front, (x_coor, y_coor))

                        #The position of the tile is stored with its unique identifier
                        self.tilePos[identifier] = (x_coor, y_coor) 

                        #Sets the identifier of the next tile
                        identifier = identifier + 1

                        #These coordinates are used as an anchor point when drawing the first lateral tile
                        x = x_coor
                        y = y_coor

                    #Traversing the top face
                    else: 

                        x_coor += int((i-2)/2)*self.sWidth
                        y_coor -= self.tHeight
                        
                        #Checks if any tiles in the top face have been colored
                        if (identifier, 1) in self.colored_tiles:
                            if self.colored_tiles[(identifier, 1)] == 1:
                                self.screen.blit(topR,(x_coor, y_coor))
                            else:
                                self.screen.blit(topB,(x_coor, y_coor))
                        else:
                            self.screen.blit(top, (x_coor, y_coor))
                        
                        self.tilePos[identifier] = (x_coor, y_coor)
                        identifier = identifier + 1

            #This for loop draws the lateral portion of the face of the cube
            for i in range (9):

                x_c = x + self.fWidth + (i%3)*self.sWidth
                y_c =  y - (i%3+1)*self.tHeight + int(i/3)*self.fWidth

                #Checks if any tiles in the lateral face have been colored
                if (identifier, 2) in self.colored_tiles:
                    if self.colored_tiles[(identifier, 2)] == 1:
                        self.screen.blit(sideR,(x_c, y_c))
                    else:
                        self.screen.blit(sideB,(x_c, y_c))
                else:
                    self.screen.blit(side, (x_c, y_c))
                
                self.tilePos[identifier] = (x_c, y_c)
                identifier = identifier + 1

    def handle_click(self, mouse_pos, obj):

        for i in range(81):

            """	Creates a mapping from the set of identifiers to the faces of the cubes. 
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
            if i not in self.clicked:
                #Checks if the mouse click lies inside one of the lateral tiles of each cube
                if (abs(2*(mouse_pos[0]-self.tilePos[i][0])-13)<13 and abs(mouse_pos[1]+(16/13)*(mouse_pos[0]-self.tilePos[i][0])-self.tilePos[i][1]-33)<16) and j == 2:
                    #Checks the turn of the player
                    if self.turn%2 == 0: 
                        #Plays a sound when the tile is clicked
                        click_sound.play()
                        #Handles the updatig of colored_tiles and clicked for player 1
                        self.colorTile(i, j, 1, obj) 
                    else: 
                        click_sound.play()
                        #Handles it for player 2
                        self.colorTile(i, j, 2, obj)
                
                #Checks if the mouse click lies inside one of the top tiles of each cube
                elif (abs(2*(mouse_pos[1]-self.tilePos[i][1])-16)<16 and abs(mouse_pos[0]+(12/17)*(mouse_pos[1]-self.tilePos[i][1])-self.tilePos[i][0]-29)<16) and j == 1:
                    if self.turn%2 == 0: 
                        click_sound.play()
                        self.colorTile(i, j, 1, obj)
                    else: 
                        click_sound.play()
                        self.colorTile(i, j, 2, obj)
                
                #Checks if the mouse click lies inside one of the front tiles of each cube
                elif (abs(2*(mouse_pos[0]-self.tilePos[i][0])-34)<34 and abs(2*(mouse_pos[1]-self.tilePos[i][1])-34)<34) and j == 0:
                    if self.turn%2 == 0: 
                        click_sound.play()
                        self.colorTile(i, j, 1, obj) 
                    else: 
                        click_sound.play()
                        self.colorTile(i, j, 2, obj)

    def colorTile(self, index, tile_type, player, obj):

        """	args:
                index: identifier of the tile
                tile_color: colored tile
                tyle_type: integer that is either 0, 1 or 2. Needed to determine which mapping 
                           to use from identefier to its corrisponding matrix position
                player: Marks the game matrix with either 1 (player 1) or 2 (player 2)
        """
        #Updates colored_tiles with all the relevant information of tile
        self.colored_tiles[(index, tile_type)] = player

        #Freezes the current tile
        self.clicked.append(index)

        #Passes the turn to the other player
        self.turn = self.turn + 1

        #Checks if the current tile lies on the lateral face of one of the three cubes
        if tile_type == 2:
            #Updates the game matrix accordingly
            obj.mark(int(index/3)-3*(int(int(index/3)/9)+1),index%3+3,player)
        else:
            obj.mark(int((index+3*int(int(index/3)/9))/6)+int(int(index/3)/9),(index+3*int(int(index/3)/9))%6,player)

    def activateNameBox(self, mouse_pos, box, boxX, boxY, activate_box, inactive_robot, first_move, player, obj):

        """	args:
                mouse_pos: a tuple containing the x and y coordinates of the mouse click
                box: loads the player box
                boxX: x coordinate of the player box
                boxY: y coordinate of the player box
                activate_box: a boolean that is needed to check if the box is temporarly active or inactive
                inactive_robot: a boolean that is needed to check if the corresponding robot is active or inactive
                first_move: a boolean that is needed to check if the player made the first move
                player: integer that is either 1 (player 1) or 2 (player 2)
        """
        #Creates a Rect object needed to manipulate the area in which the name of the player will appear
        text_box = pygame.Rect((boxX,boxY,pygame.Surface.get_width(box),pygame.Surface.get_height(box)))

        #Checks whether the player clicked on his name box
        if text_box.collidepoint(mouse_pos):
            #Activates the robot
            inactive_robot.append(False)
            #Checks whether the box is inactive
            if not activate_box[-1]:
                #Makes the box active
                activate_box.append(True)
                robotACTIVE_sound.play()

        #If the player clicks away
        else:
            #Make the box inactive
            activate_box.append(False)
            #Checks whether the player's robot is active
            if not inactive_robot[-1]:
                #If that is the case, the player may start the game
                self.handle_click(mouse_pos, obj)

            #Checks if the player made his first move
            if len(self.clicked) == player: 
                first_move.append(True)
            

    def updateName(self, event, updated_name, obj):

        """	args:
                event: pygame event which may consist in a mouseclick, keyboard press
                updated_name: current name of the player
        """

        #Maximum length of the player name
        char_max = 10

        #Extrapolates the most recent name update
        name = updated_name[-1]

        #Current length of the name
        count_chars = len(name)

        #Checks whether a key was pressed
        if event.type == pygame.KEYDOWN:
            #Checks whether the player tried deleting a character of his name
            if event.key == pygame.K_BACKSPACE and count_chars > 0:
                count_chars -= 1
                name = name[:-1]
                #Updates the name accordingly
                updated_name.append(name)

            #Checks whether the player pressed a valid key (a backspace or an alpha-numeric character) 
            #and if the length of the name satisfies the constraint
            elif (event.unicode.isalnum() or event.key == pygame.K_SPACE) and count_chars <= char_max:
                count_chars += 1
                name += event.unicode		 				
                updated_name.append(name)
    
    def newGame(self, mouse_pos, obj):
        
        #Checks whether the  user clicked on top of the YES button
        if abs(2*(mouse_pos[0]-const.BUTTON_YES_X)-const.BUTTON_YES_WIDTH)<const.BUTTON_YES_WIDTH and abs(2*(mouse_pos[1]-const.BUTTON_YES_Y)-const.BUTTON_YES_HEIGHT)<const.BUTTON_YES_HEIGHT:
            #Resets the clicked tiles
            self.clicked = []
            #Resets the colored tiles
            self.colored_tiles = {}
            #Begins a new game
            self.game_over = False
            #The winner begins the match
            self.turn += 1
            #The board is cleared
            obj.reset()
            #The winning sequence is cleared
            obj.seq_list = []
            #The winner is set to none
            obj.result = 0
            #The game is still going, thus return True
            return True

        elif abs(2*(mouse_pos[0]-const.BUTTON_NO_X)-const.BUTTON_NO_WIDTH)<const.BUTTON_NO_WIDTH and abs(2*(mouse_pos[1]-const.BUTTON_NO_Y)-const.BUTTON_NO_HEIGHT)<const.BUTTON_NO_HEIGHT:
            #The user clicked quit, therefore the game is not running
            return False
        else:
            #If the user clicks anywhere else, the game is still running
            return True

    def drawNewGame(self):

        #Draws the skeleton of the box
        self.screen.blit(newGame_Box, (const.NEW_GAME_X, const.NEW_GAME_Y))

        #Obtains the current position of the mous
        mouse_pos = pygame.mouse.get_pos()

        #Checks if the mouse is currently hovering above the YES button
        if abs(2*(mouse_pos[0]-const.BUTTON_YES_X)-const.BUTTON_YES_WIDTH)<const.BUTTON_YES_WIDTH and abs(2*(mouse_pos[1]-const.BUTTON_YES_Y)-const.BUTTON_YES_HEIGHT)<const.BUTTON_YES_HEIGHT:
            #Activates the eyes of the button
            self.screen.blit(newGame_buttonA, (const.BUTTON_YES_X, const.BUTTON_YES_Y))
            #The NO button remains as is
            self.screen.blit(newGame_button, (const.BUTTON_NO_X, const.BUTTON_NO_Y))
                   
        elif abs(2*(mouse_pos[0]-const.BUTTON_NO_X)-const.BUTTON_NO_WIDTH)<const.BUTTON_NO_WIDTH and abs(2*(mouse_pos[1]-const.BUTTON_NO_Y)-const.BUTTON_NO_HEIGHT)<const.BUTTON_NO_HEIGHT:
            self.screen.blit(newGame_button, (const.BUTTON_YES_X, const.BUTTON_YES_Y))
            self.screen.blit(newGame_buttonA, (const.BUTTON_NO_X, const.BUTTON_NO_Y))
        
        #If the user is not hovering over any of the two buttons, leave them inecative
        else:
            self.screen.blit(newGame_button, (const.BUTTON_YES_X, const.BUTTON_YES_Y))
            self.screen.blit(newGame_button, (const.BUTTON_NO_X, const.BUTTON_NO_Y))


    def gameOver(self, obj):

        #Checks if there is a winner
        if obj.result == 1 or obj.result == 2:

                if obj.result == 1:

                    #Deactivates the loser's robot
                    self.screen.blit(robotPlayer2_DEAD, (const.ROBOT2_X, const.ROBOT_Y))

                    #Checks whether the game is over
                    if self.game_over == False:
                        #Increments the points of player 1
                        self.winsp1 += 1

                    #Dimmens the background light
                    self.screen.blit(layer, const.ORIGIN)

                    #Congratulates the winner
                    self.screen.blit(font.render(self.player1Name[-1].upper() + ' WINS!', True, const.COLOR_WHITE), (const.WINNER_CONGRATS_X, const.WINNER_CONGRATS_Y))

                    #Draws the new game request box
                    self.drawNewGame()

                    #Highlights the winning sequence for player 1
                    for idx in range(4):

                        #Extracts the matrix coordinates of one of the winning tiles
                        i = obj.seq_list[idx]['pos'][0]
                        j = obj.seq_list[idx]['pos'][1]

                        #Maps the coordinates to its corresponding identifier
                        identifier = 6*i + j - 3*((int(i/3)-2)%2)*(1+i%3) - 9*int(i/6)

                        #Finds the face the tiles lives on, using the same mapping as in handle_click(), and colors the tile
                        if (int(int(identifier/3)/3)-2)%3 == 0: 
                            self.screen.blit(sideR, self.tilePos[identifier])

                        elif (int(identifier/3)-int(int(identifier/3)/9))%2 != 0: 
                            self.screen.blit(topR, self.tilePos[identifier])

                        else: 
                            self.screen.blit(frontR, self.tilePos[identifier])

                else:
                    self.screen.blit(robotPlayer1_DEAD, (const.ROBOT1_X, const.ROBOT_Y))

                    if self.game_over == False:
                        self.winsp2 += 1
                    
                    self.screen.blit(layer, const.ORIGIN)
                    self.screen.blit(font.render(self.player2Name[-1].upper() + ' WINS!', True, const.COLOR_WHITE), (const.WINNER_CONGRATS_X, const.WINNER_CONGRATS_Y))
                    self.drawNewGame()
                    
                    for idx in range(4):

                        i = obj.seq_list[idx]['pos'][0]
                        j = obj.seq_list[idx]['pos'][1]

                        identifier = 6*i + j - 3*((int(i/3)-2)%2)*(1+i%3) - 9*int(i/6)

                        if (int(int(identifier/3)/3)-2)%3 == 0: 
                            self.screen.blit(sideB, self.tilePos[identifier])

                        elif (int(identifier/3)-int(int(identifier/3)/9))%2 != 0: 
                            self.screen.blit(topB, self.tilePos[identifier])

                        else: 
                            self.screen.blit(frontB, self.tilePos[identifier])

                #Changes the game state to over
                self.game_over = True
        
        #Checks whether the game has ended in a draw
        elif obj.result == 0 and len(self.clicked) == 81:

            self.screen.blit(font.render('IT IS A DRAW!', True, const.COLOR_WHITE), (const.WINNER_CONGRATS_X, const.WINNER_CONGRATS_Y))
            self.screen.blit(robotPlayer2_DEAD, (const.ROBOT2_X, const.ROBOT_Y))
            self.screen.blit(robotPlayer1_DEAD, (const.ROBOT1_X, const.ROBOT_Y))
            self.game_over = True
            self.screen.blit(layer, const.ORIGIN)
            self.drawNewGame()


    def updateScreen(self, inactiveR1, inactiveR2, delta_y):

        """	args:
            inactiveR1: loads robot of player 1
            inactiveR2: loads robot of player 2
            delta_y: float needed to determine the vertical grid displacement 
        """
        
        #Draws the background of the game
        self.screen.blit(background, const.ORIGIN)
        #Draws the grid
        self.screen.blit(grid, (const.GRID_X, const.GRID_Y + delta_y*(const.GRID_DISPLACEMENT/const.FPS)))
        #Draws the game board
        self.drawBoard(self.screen)
        #Draws the player box for player 1
        self.screen.blit(boxPlayer1, (const.BOX_PLAYER1_X, const.BOX_PLAYER_Y))
        #Displays the name of player 1
        self.screen.blit(font.render(self.player1Name[-1], True, const.FONT_COLOR), (const.FONT_PLAYER1_X, const.FONT_PLAYER1_Y))
        #Displays the number of wins of player 1
        self.screen.blit(font.render(str(self.winsp1), True, const.FONT_COLOR), (const.WINS_PLAYER1_X , const.WINS_PLAYER1_Y))

        #Checks whether the robot is inactive
        if inactiveR1[-1]:
            #Draws inactive robot of player 1
            self.screen.blit(robotPlayer1, (const.ROBOT1_X, const.ROBOT_Y))
        else:
            #Draws active robot of player 1
            self.screen.blit(robotPlayer1_ACTIVE, (const.ROBOT1_X, const.ROBOT_Y))

        #Draws all the above, but for player 2
        self.screen.blit(boxPlayer2, (const.BOX_PLAYER2_X, const.BOX_PLAYER_Y))
        self.screen.blit(font.render(self.player2Name[-1], True, const.FONT_COLOR), (const.FONT_PLAYER2_X, const.FONT_PLAYER2_Y))
        self.screen.blit(font.render(str(self.winsp2), True, const.FONT_COLOR), (const.WINS_PLAYER2_X, const.WINS_PLAYER2_Y))

        if inactiveR2[-1]:
            self.screen.blit(robotPlayer2,(const.ROBOT2_X, const.ROBOT_Y))
        else:
            self.screen.blit(robotPlayer2_ACTIVE, (const.ROBOT2_X, const.ROBOT_Y))
        
        if not self.game_over:
            #Checks whether it is player's 1 turn 
            if self.turn%2 == 0:
                #Dispays notification that tells it is player's 1 turn
                self.screen.blit(turnText, (const.TURN_TEXT1_X, const.TURN_TEXT1_Y))
            else:
                #Dispays notification that tells it is player's 2 turn
                self.screen.blit(turnText, (const.TURN_TEXT2_X, const.TURN_TEXT2_Y))
        
    
    def gameLoop(self):
        
        #Needed to increment the displacement of the grid
        i = 0

        #Needed to check if the grid is moving upwards or downwards
        state = "DECREASING"

        clock = pygame.time.Clock()

        running = True

        game = Skeleton()
        background_sound.play(-1)
 
        while running:
            
            #Draws the screen
            self.updateScreen(self.inactive_robot1, self.inactive_robot2,i)

            #Checks whether the screen is moving downwards
            if i == 0 or state == "DECREASING": 
                i += 1
                #Checks to see if the grid reached the maximum downward displacement
                if i == const.FPS:
                    #Makes the grid move upwards
                    state = "INCREASING"
            else:
                i -= 1
                if i == 0:
                    state = "DECREASING"

            #Loops through all the events of the game
            for event in pygame.event.get():
                #Checks whether the user exited the window 
                if event.type == pygame.QUIT:
                     running = False

                if self.game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        running = self.newGame(pos, game) 
                else:
                    #Checks whether the user clicked anywhere on the screen
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        #The position of the mouse click is stored
                        pos = pygame.mouse.get_pos()
                        #Checks whether both players made their first move
                        if	self.player1_first_move[-1] and self.player2_first_move[-1]:
                            self.handle_click(pos,game)
                        else:
                            #Checks whether player 1 has made his first move
                            if not self.player1_first_move[-1]:
                                #waits for player 1 to activate his box in order to start playing the game
                                self.activateNameBox(pos, boxPlayer1, const.BOX_PLAYER1_X, const.BOX_PLAYER_Y, self.box1_active, self.inactive_robot1, self.player1_first_move, 1, game)
                            else:
                                self.activateNameBox(pos, boxPlayer2, const.BOX_PLAYER2_X, const.BOX_PLAYER_Y, self.box2_active, self.inactive_robot2, self.player2_first_move, 2, game)
                    
                    #Checks whether player 1 currently clicked on his box 
                    if self.box1_active[-1]:
                        #Updating of player's 1 name
                        self.updateName(event,self.player1Name, game)
                    if self.box2_active[-1]:
                        self.updateName(event,self.player2Name, game)    

            self.gameOver(game) 

            pygame.display.update() 

            #Restricts the game to run on a specifed number of FPS
            clock.tick(const.FPS)
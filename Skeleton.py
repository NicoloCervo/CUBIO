from constants import WIDTH, HEIGHT, WIN_LEN

class Skeleton:
    """ basic game object with logic, operations on the board and winner detection
    """
    def __init__(self):

        self.board = [[0 for col in range(WIDTH)] for row in range(HEIGHT)]
        self.result = 0
        self.seq_list=[]

    def show(self):
        """	prints the board to cmd
        """
        for row in range(HEIGHT):
            if row%3 == 0:
                print()
            print(self.board[row])

    def reset(self):
        """	resets the board to all 0
        """
        self.board = [[0 for col in range(WIDTH)] for row in range(HEIGHT)]

    def mark(self, row, col, symbol):
        """	Sets the tile at (row,col) to symbol
            >>>AS SOON AS THIS METHOD RETURNS A VALUE != 0 THE GAME SHOULD END<<<
            args:
                row,col: column and line of a tile
                symbol: character to insert in the tile
            returns: 0 if nobody won or the list of the dict containing symbols 
            and positions of the winning sequence winning_symbol,
            [{'pos':(x,y),'symb':symbol},{...},{...},{...}]
        """
        self.board[row][col] = symbol
        # for the 3 leftmost columns
        if col < 3:
            # mark also in the rotated support 3x3 squares
            self.board[WIDTH*int(row/WIDTH)+5-col][row-WIDTH*int(row/WIDTH)] = symbol

        self.show()
        self.result, self.seq_list = self.check(row, col)

        return self.result, self.seq_list

    def check(self, row, col):
        """	Checks the board for winning states 
            ( 4 aligned tiles with the same symbol, only checks 1 row, 1 col and the diagonal ).
            args: coordinates of the last mark
            returns: 0 if nobody won or the list of the dict containing symbols
            and positions of the winning sequence winning_symbol,
            [{'pos':(x,y),'symb':symbol},{...},{...},{...}]
        """
        # check the [col] column for sequnces of 4 only if [col]>2 (then it is a valid column)
        if col > 2:
            #list of same sequential symbols encountered adiacent to the current
            # position with corresponding position
            current_sequence = []
            #iterate through every row
            for i in range(HEIGHT):
                #get the value of the tile we are currently looking at
                current_tile = self.board[i][col]

                #current tile empty => no sequence
                if current_tile == 0:
                    current_sequence = []
                #empty sequence or symbol in sequence => append symbol
                elif len(current_sequence) == 0 or current_sequence[0]['symb'] == current_tile:
                    current_sequence.append({'pos' : (col, i), 'symb' : current_tile})
                #otherwise => sequence contains only current symbol
                else:
                    current_sequence = [{'pos' : (col, i), 'symb' : current_tile}]

                #as soon as the list contains 4 symbols somebody won
                if len(current_sequence) == WIN_LEN:
                    #return the winning symbol
                    return current_sequence[0]['symb'], current_sequence

        # checks the [row] row for sequences of 4
        current_sequence = []
        #run check also on the row where the support tile is changed, if it if changed
        for check in range(2):
            for j in range(WIDTH):
                current_tile = self.board[row][j]

                #current tile empty => no sequence
                if current_tile == 0:
                    current_sequence = []
                #empty sequence or symbol in sequence => append symbol
                elif len(current_sequence) == 0 or current_sequence[0]['symb'] == current_tile:
                    current_sequence.append({'pos' : (j, row), 'symb' : current_tile})
                #otherwise => sequence contains only current symbol
                else:
                    current_sequence = [{'pos' : (j, row), 'symb' : current_tile}]

                if len(current_sequence) == WIN_LEN:
                    # change support tiles to original coordinates before returning the list
                    for element in current_sequence:
                        if element['pos'][0] <= 2 and element['pos'][1]%6 >= 2:
                            element['pos']=(5-element['pos'][1]%6, element['pos'][0]+int(element['pos'][1]/6))
                    print(current_sequence)
                    return current_sequence[0]['symb'],current_sequence

            current_sequence = []
            #auxiliary row check condition, aux rows are used only for tiles in the first 3 cols
            if col < 3:
                row = 5-col+6*int(row/6)
            else:
                break

        # check the diagonal
        for i in range(3):
            for j in range(3):
                current_tile = self.board[j+WIDTH*i][2-j]
                if current_tile != 0:
                    if len(current_sequence) == 0 or current_sequence[0]['symb'] == current_tile:
                        current_sequence.append({'pos' : (j+WIDTH*i,2-j), 'symb' : current_tile})
                    else:
                        current_sequence = []
                if len(current_sequence) == WIN_LEN:
                    return current_sequence[0]['symb'], current_sequence
        return 0,[]
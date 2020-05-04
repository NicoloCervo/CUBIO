from math import inf, isinf
from constants import WIDTH, HEIGHT, WIN_LEN
import copy

class PvE:
    """ methods for automated moves
    """
    def __init__(self, max_depth, cpu_symbol):
        self.max_depth = max_depth
        self.symbol= cpu_symbol

    def find_best_move(self, board):
        """ tries minmax on every possible move on the board and
            returns the one with the highest evaluation
        """
        possible_moves = []
        for col in range(3, 6):
            for row in range(18):
                if (col > 2 or row%6 < 3) and board[col, row] == 0:
                    possible_moves.append({'coords':[col, row], 'score':-inf})

        for move in possible_moves:
            poss_board = copy.deepcopy(board)
            self.mark(poss_board, move['coords'][0], move['coords'][1], self.symbol)

    def evaluate_state(self, board):
        """returns an indicator of the quality of the state of he board, -INF for losing state 
           and +INF for winning state, values in between indicate which outcome is "closer"
        """

        return 0

    def minimax(self, board, depth, is_maximizing_player):
        """recursive minmax implementation
        """

        board_state_eval = self.evaluate_state(board)
        if isinf(board_state_eval) or depth == self.max_depth:
            return board_state_eval
        """
        if is_maximizing_player :
            best_val = -INFINITY 
            for each move in board :
                mark
                value = minimax(board, depth+1, false)
                unmark
                best_val = max( best_val, value) 
            return best_val

        else :
            best_val = +INFINITY 
            for each move in board :
                mark
                value = minimax(board, depth+1, true)
                unmark
                best_val = min( best_val, value) 
            return best_val
        """
    def mark(self, board, row, col, symbol):

        board[row][col] = symbol
        # for the 3 leftmost columns
        if col < 3:
            # mark also in the rotated support 3x3 squares
            board[WIDTH*int(row/WIDTH)+5-col][row-WIDTH*int(row/WIDTH)] = symbol

    def check(self, row, col):
        # check the [col] column for sequnces of 4 only if [col]>2 (then it is a valid column)
        if col > 2:
            #list of same sequential symbols encountered adiacent to the current
            # position with corresponding position
            current_sequence = []
            #iterate through every row
            for i in range(HEIGHT):
                #get the value of the tile we are currently looking at
                current_tile = board[i][col]

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
                current_tile = board[row][j]

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
                current_tile = board[j+WIDTH*i][2-j]
                if current_tile != 0:
                    if len(current_sequence) == 0 or current_sequence[0]['symb'] == current_tile:
                        current_sequence.append({'pos' : (j+WIDTH*i, 2-j), 'symb' : current_tile})
                    else:
                        current_sequence = []
                if len(current_sequence) == WIN_LEN:
                    return current_sequence[0]['symb'], current_sequence
        return 0, []

import sys
import copy

EXPLORED = []


class Piece:
    def __init__(self, name):
        self.name = name
        if name == "b":
            self.value = -1
            self.team = "black"
        elif name == "B":
            self.value = -2
            self.team = "black"
        elif name == "r":
            self.value = 1
            self.team = "red"
        else:
            self.value = 2
            self.team = "red"


def configure(file):
    """Read from input file and return a board.
       The board is a dictionary with keys = (row, column) and values = either "b" or "B" or "r" or "R" """
    r = 0
    board = {}
    while r != 8:
        c = 0
        while c != 8:
            if file[r][c] == "b":
                board[(r, c)] = Piece("b")
            elif file[r][c] == "B":
                board[(r, c)] = Piece("B")
            elif file[r][c] == "r":
                board[(r, c)] = Piece("r")
            elif file[r][c] == "R":
                board[(r, c)] = Piece("R")
            c += 1
        r += 1
    return board


def u_sum(board):
    """calculate the net utility of the board by summing up all the pieces' values"""
    s = 0
    for key in board:
        s += board[key].value
    return s


def check_king(board, piece):
    """ check if the current piece is in the first row or the last row. change to a king if the condition is
    satisfied. Pieces will be either "r" or "b" """
    if board[piece].name == "r":
        if piece[0] == 0:
            board[piece] = Piece("R")
    elif board[piece].name == "b":
        if piece[0] == 7:
            board[piece] = Piece("R")
    return board


def check_surrounding(board, piece):
    """return a list of potential boards that switch the current piece with nearby empties.
        piece = (r,c)"""
    empty = []
    if board[piece].name == "r":
        if not (piece[0] - 1, piece[1] - 1) in board: #not in board, check for border
            if piece[0] - 1 >= 0 and piece[1] - 1 >= 0:
                pointer = copy.deepcopy(board)
                pointer[(piece[0] - 1, piece[1] - 1)] = pointer[piece]
                pointer.pop(piece)
                pointer = check_king(pointer, (piece[0] - 1,piece[1] - 1))
                if check_explored(pointer):
                    EXPLORED.append((pointer, u_sum(pointer)))
                    empty.append(pointer)
        if not (piece[0] - 1,piece[1] + 1) in board: #not in board, check for border
            if piece[0] - 1 >= 0 and piece[1] + 1 < 8:
                pointer = copy.deepcopy(board)
                pointer[(piece[0] - 1, piece[1] + 1)] = pointer[piece]
                pointer.pop(piece)
                pointer = check_king(pointer, (piece[0] - 1, piece[1] + 1))
                if check_explored(pointer):
                    EXPLORED.append((pointer, u_sum(pointer)))
                    empty.append(pointer)
    elif board[piece].name == "b":
        if not (piece[0] + 1,piece[1] + 1) in board: #not in board, check for border
            if piece[0] + 1 < 8 and piece[1] + 1 < 8:
                pointer = copy.deepcopy(board)
                pointer[(piece[0] + 1,piece[1] + 1)] = pointer[piece]
                pointer.pop(piece)
                pointer = check_king(pointer, (piece[0] + 1, piece[1] + 1))
                if check_explored(pointer):
                    EXPLORED.append((pointer, u_sum(pointer)))
                    empty.append(pointer)
        if not (piece[0] + 1,piece[1] - 1) in board: #not in board, check for border
            if piece[0] + 1 < 8 and piece[1] - 1 >= 0:
                pointer = copy.deepcopy(board)
                pointer[(piece[0] + 1,piece[1] - 1)] = pointer[piece]
                pointer.pop(piece)
                pointer = check_king(pointer, (piece[0] + 1, piece[1] - 1))
                if check_explored(pointer):
                    EXPLORED.append((pointer, u_sum(pointer)))
                    empty.append(pointer)
    else: # the kings
        if not (piece[0] + 1, piece[1] + 1)in board: #not in board, check for border
            if piece[0] + 1 < 8 and piece[1] + 1 < 8:
                pointer = copy.deepcopy(board)
                pointer[(piece[0] + 1,piece[1] + 1)] = pointer[piece]
                pointer.pop(piece)
                if check_explored(pointer):
                    EXPLORED.append((pointer, u_sum(pointer)))
                    empty.append(pointer)
        if not (piece[0] - 1,piece[1] - 1) in board: #not in board, check for border
            if piece[0] - 1 >= 0 and piece[1] - 1 > 0:
                pointer = copy.deepcopy(board)
                pointer[(piece[0] - 1,piece[1] - 1)] = pointer[piece]
                pointer.pop(piece)
                if check_explored(pointer):
                    EXPLORED.append((pointer, u_sum(pointer)))
                    empty.append(pointer)
        if not (piece[0] - 1,piece[1] + 1) in board: #not in board, check for border
            if piece[0] - 1 >= 0 and piece[1] + 1 < 8:
                pointer = copy.deepcopy(board)
                pointer[(piece[0] - 1,piece[1] + 1)] = pointer[piece]
                pointer.pop(piece)
                if check_explored(pointer):
                    EXPLORED.append((pointer, u_sum(pointer)))
                    empty.append(pointer)
        if not (piece[0] + 1,piece[1] - 1) in board: #not in board, check for border
            if piece[0] + 1 < 8 and piece[1] - 1 >= 0:
                pointer = copy.deepcopy(board)
                pointer[(piece[0] + 1,piece[1] - 1)] = pointer[piece]
                pointer.pop(piece)
                if check_explored(pointer):
                    EXPLORED.append((pointer, u_sum(pointer)))
                    empty.append(pointer)
    return empty


def check_capture(board, piece):
    """Check if the piece can move two spaces and capture the opposite piece. if true, switch them and record the
    potential board. return a list of possible moves."""
    capture = []
    if board[piece].name == "r":
        if not (piece[0] - 2, piece[1] - 2) in board:  # not in board, check for boundaries
            neighbor_r = piece[0] - 1
            neighbor_c = piece[1] - 1
            if neighbor_r > piece[0] - 2 >= 0 and neighbor_c > piece[1] - 2 >= 0:  # all within bound
                if (neighbor_r, neighbor_c) in board and board[(neighbor_r, neighbor_c)].team != board[piece].team:
                    # if neighbor is not empty and it is an enemy
                    pointer = copy.deepcopy(board)
                    pointer.pop((neighbor_r, neighbor_c))
                    pointer[(piece[0] - 2, piece[1] - 2)] = pointer[piece]
                    pointer.pop(piece)
                    pointer = check_king(pointer, (piece[0] - 2, piece[1] - 2))
                    capture.append((pointer, (piece[0] - 2, piece[1] - 2)))
        if not (piece[0] - 2, piece[1] + 2) in board:  # not in board, check for boundaries
            neighbor_r = piece[0] - 1
            neighbor_c = piece[1] + 1
            if neighbor_r > piece[0] - 2 >= 0 and neighbor_c < piece[1] + 2 < 8:  # all within bound
                if (neighbor_r, neighbor_c) in board and board[(neighbor_r, neighbor_c)].team != board[piece].team:
                    # if neighbor is not empty and it is an enemy
                    pointer = copy.deepcopy(board)
                    pointer.pop((neighbor_r, neighbor_c))
                    pointer[(piece[0] - 2, piece[1] + 2)] = pointer[piece]
                    pointer.pop(piece)
                    pointer = check_king(pointer, (piece[0] - 2, piece[1] + 2))
                    capture.append((pointer, (piece[0] - 2, piece[1] + 2)))
    elif board[piece].name == "b":
        if not (piece[0] + 2, piece[1] + 2) in board:  # not in board, check for boundaries
            neighbor_r = piece[0] + 1
            neighbor_c = piece[1] + 1
            if neighbor_r < piece[0] + 2 < 8 and neighbor_c < piece[1] + 2 < 8:  # all within bound
                if (neighbor_r, neighbor_c) in board and board[(neighbor_r, neighbor_c)].team != board[piece].team:
                    # if neighbor is not empty and it is an enemy
                    pointer = copy.deepcopy(board)
                    pointer.pop((neighbor_r, neighbor_c))
                    pointer[(piece[0] + 2, piece[1] + 2)] = pointer[piece]
                    pointer.pop(piece)
                    pointer = check_king(pointer, (piece[0] + 2, piece[1] + 2))
                    capture.append((pointer, (piece[0] + 2, piece[1] + 2)))
        if not (piece[0] + 2, piece[1] - 2) in board:  # not in board, check for boundaries
            neighbor_r = piece[0] + 1
            neighbor_c = piece[1] - 1
            if neighbor_r < piece[0] + 2 < 8 and neighbor_c > piece[1] - 2 >= 0:  # all within bound
                if (neighbor_r, neighbor_c) in board and board[(neighbor_r, neighbor_c)].team != board[piece].team:
                    # if neighbor is not empty and it is an enemy
                    pointer = copy.deepcopy(board)
                    pointer.pop((neighbor_r, neighbor_c))
                    pointer[(piece[0] + 2, piece[1] - 2)] = pointer[piece]
                    pointer.pop(piece)
                    pointer = check_king(pointer, (piece[0] + 2, piece[1] - 2))
                    capture.append((pointer, (piece[0] + 2, piece[1] - 2)))
    else:
        if not (piece[0] + 2, piece[1] + 2) in board:  # not in board, check for boundaries
            neighbor_r = piece[0] + 1
            neighbor_c = piece[1] + 1
            if neighbor_r < piece[0] + 2 < 8 and neighbor_c < piece[1] + 2 < 8:    # all within bound
                if (neighbor_r, neighbor_c) in board and board[(neighbor_r,neighbor_c)].team != board[piece].team:
                    # if neighbor is not empty and it is an enemy
                    pointer = copy.deepcopy(board)
                    pointer.pop((neighbor_r, neighbor_c))
                    pointer[(piece[0] + 2, piece[1] + 2)] = pointer[piece]
                    pointer.pop(piece)
                    capture.append((pointer, (piece[0] + 2, piece[1] + 2)))
        if not (piece[0] - 2, piece[1] - 2) in board:  # not in board, check for boundaries
            neighbor_r = piece[0] - 1
            neighbor_c = piece[1] - 1
            if neighbor_r > piece[0] - 2 >= 0 and neighbor_c > piece[1] - 2 >= 0:  # all within bound
                if (neighbor_r, neighbor_c) in board and board[(neighbor_r, neighbor_c)].team != board[piece].team:
                    # if neighbor is not empty and it is an enemy
                    pointer = copy.deepcopy(board)
                    pointer.pop((neighbor_r, neighbor_c))
                    pointer[(piece[0] - 2, piece[1] - 2)] = pointer[piece]
                    pointer.pop(piece)
                    capture.append((pointer, (piece[0] - 2, piece[1] - 2)))
        if not (piece[0] - 2, piece[1] + 2) in board:  # not in board, check for boundaries
            neighbor_r = piece[0] - 1
            neighbor_c = piece[1] + 1
            if neighbor_r > piece[0] - 2 >= 0 and neighbor_c < piece[1] + 2 < 8:  # all within bound
                if (neighbor_r, neighbor_c) in board and board[(neighbor_r, neighbor_c)].team != board[piece].team:
                    # if neighbor is not empty and it is an enemy
                    pointer = copy.deepcopy(board)
                    pointer.pop((neighbor_r, neighbor_c))
                    pointer[(piece[0] - 2, piece[1] + 2)] = pointer[piece]
                    pointer.pop(piece)
                    capture.append((pointer, (piece[0] - 2, piece[1] + 2)))
        if not (piece[0] + 2, piece[1] - 2) in board:  # not in board, check for boundaries
            neighbor_r = piece[0] + 1
            neighbor_c = piece[1] - 1
            if neighbor_r < piece[0] + 2 < 8 and neighbor_c > piece[1] - 2 >= 0:  # all within bound
                if (neighbor_r, neighbor_c) in board and board[(neighbor_r, neighbor_c)].team != board[piece].team:
                    # if neighbor is not empty and it is an enemy
                    pointer = copy.deepcopy(board)
                    pointer.pop((neighbor_r, neighbor_c))
                    pointer[(piece[0] + 2, piece[1] - 2)] = pointer[piece]
                    pointer.pop(piece)
                    capture.append((pointer, (piece[0] + 2, piece[1] - 2)))
    return capture


def check_multi_capture(more_capture):
    """ check recursively for multi-capture moves"""
    recur = check_capture(more_capture[0], more_capture[1])
    multi = []
    if len(recur) == 0:
        return [more_capture]
    else:
        for item in recur:
            more = check_multi_capture(item)
            multi = multi + more
    return multi


def check_explored(board):
    """check if a board is already explored, prevent moving back and forth"""
    if board in EXPLORED:
        return False
    return True


def successor(board, player):
    """ given player, "red", or "black"
        return a list of successors of the current board. i.e. return a list of dictionaries.
        sorted from highest to lowest utility"""
    capture_move = []
    single_move = []
    entry_count = 0
    for key in board:      # want to max value for player red, min value for player black
        if board[key].team == player:
            first = check_capture(board, key)
            second = check_surrounding(board, key)
            for each in first: # record the utility of capture move and the move itself
                if check_explored((each[0], u_sum(each[0]))): # if true == have not explored
                    EXPLORED.append((each[0], u_sum(each[0])))
                    multi_cap = check_multi_capture(each) # list of tuples (dict, key) representing multi capture
                    for item in multi_cap:
                        capture_move.append((u_sum(item[0]), board[key].value, entry_count, item[0]))
                        EXPLORED.append((item[0], u_sum(item[0])))
                        entry_count -= 1
            for each in second:  # record the utility of next move and the move itself
                if check_explored((each, key)):
                    single_move.append((u_sum(each), board[key].value, entry_count, each))
                    EXPLORED.append((each, u_sum(each)))
                    entry_count -= 1
    capture_move = sorted(capture_move) # order from smallest to biggest
    single_move = sorted(single_move) # order by 1.utility function, 2. king > normal, 3. entry
    c_result = []
    s_result = []
    for i in range(0, len(capture_move)):
        if player == "red":
            c_result.append(capture_move[-i - 1][3])
        else:
            c_result.append(capture_move[i][3])
    for j in range(0, len(single_move)):
        if player == "red":
            s_result.append(single_move[-j - 1][3])
        else:
            s_result.append(single_move[j][3])
    return c_result, s_result     # if both are empty list, no moves is available, end


def check_goal(board, player):
    """ check if the opposite player has no piece left on board. True if no piece is left"""
    remaining = 0
    for key in board:
        if board[key].team == player:
            remaining += 1
    return remaining == 0


def minimax_max(board, depth):
    """call this when player is red
        return value """
    best_move = None
    if check_goal(board, "black") or depth == 0: # check if opponent has piece left or reach depth limit
        return u_sum(board), best_move
    suc_capture, suc_single = successor(board, "red")
    if not suc_capture and not suc_single: # if no possible moves
        return u_sum(board), best_move
    value = -float("infinity")
    if suc_capture: # search capture first, if no capture moves, search single moves
        for each in suc_capture:
            next_value, next_move = minimax_min(each, depth-1)
            if value < next_value:
                value = next_value
                best_move = each
        return value, best_move
    for each in suc_single:
        next_value, next_move = minimax_min(each, depth-1)
        if value < next_value:
            value = next_value
            best_move = each
    return value, best_move


def minimax_min(board, depth):
    """call this when player is black"""
    best_move = None
    if check_goal(board, "red") or depth == 0: # check if opponent has piece left or reach depth limit
        return u_sum(board), best_move
    suc_capture, suc_single = successor(board, "black")
    if not suc_capture and not suc_single:  # if no possible moves
        return u_sum(board), best_move
    value = float("infinity")
    if suc_capture:  # search capture first, if no capture moves, search single moves
        for each in suc_capture:
            next_value, next_move = minimax_max(each, depth - 1)
            if value > next_value:
                value = next_value
                best_move = each
        return value, best_move
    for each in suc_single:
        next_value, next_move = minimax_max(each, depth-1)
        if value > next_value:
            value = next_value
            best_move = each
    return value, best_move


def alpha_beta_max(board, alpha, beta, depth):
    """call this when player is red
            return value """
    best_move = None
    if check_goal(board, "black") or depth == 0:  # check if opponent has piece left or reach depth limit
        return u_sum(board), best_move
    suc_capture, suc_single = successor(board, "red")
    if not suc_capture and not suc_single:  # if no possible moves
        return u_sum(board), best_move
    value = -float("infinity")
    if suc_capture:  # search capture first, if no capture moves, search single moves
        for each in suc_capture:
            next_value, next_move = alpha_beta_min(each, alpha, beta, depth-1)
            if value < next_value:
                value = next_value
                best_move = each
            if value >= beta:
                return value, best_move
            alpha = max(alpha, value)
        return value, best_move
    for each in suc_single:
        next_value, next_move = alpha_beta_min(each, alpha, beta, depth-1)
        if value < next_value:
            value = next_value
            best_move = each
        if value >= beta:
            return value, best_move
        alpha = max(alpha, value)
    return value, best_move


def alpha_beta_min(board, alpha, beta, depth):
    """call this when player is black"""
    best_move = None
    if check_goal(board, "red") or depth == 0:  # check if opponent has piece left or reach depth limit
        return u_sum(board), best_move
    suc_capture, suc_single = successor(board, "black")
    if not suc_capture and not suc_single:  # if no possible moves
        return u_sum(board), best_move
    value = float("infinity")
    if suc_capture:  # search capture first, if no capture moves, search single moves
        for each in suc_capture:
            next_value, next_move = alpha_beta_max(each, alpha, beta, depth-1)
            if value > next_value:
                value = next_value
                best_move = each
            if value <= alpha:
                return value, best_move
            beta = min(beta, value)
        return value, best_move
    for each in suc_single:
        next_value, next_move = alpha_beta_max(each, alpha, beta, depth-1)
        if value > next_value:
            value = next_value
            best_move = each
        if value <= alpha:
            return value, best_move
        beta = min(beta, value)
    return value, best_move


def alpha_beta(board):
    """perform alpha-beta pruning search;
        red always start first, so we start with max
        return the best next move and value"""
    value, best_move = alpha_beta_max(board, -float("inf"), float("inf"), 8)
    return value, best_move


def convert_output(board):
    """convert board to output file
    return a list of list"""
    lst = []
    for i in range(0,8):
        lst.append([])
        for j in range(0,8):
            lst[i].append(".")
    for key in board:
        lst[key[0]][key[1]] = board[key].name
    return lst


if __name__ == '__main__':
    filename = sys.argv[1]
    # store in list of list; first list = first line of file
    f = open(filename, "r")
    counter = 0
    inputfile = []
    while counter != 8:
        line = f.readline()
        inputfile.append([x for x in line.strip()])
        counter += 1
    f.close()
    start = configure(inputfile)
    v, result = alpha_beta(start)
    convert = convert_output(result)
    filename = sys.argv[2]
    f = open(filename, "w")
    for row in convert:
        for column in row:
            f.write(column)
        f.write("\n")
    f.close()

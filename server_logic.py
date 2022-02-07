import random

def generate_possible_moves(head: dict) -> dict:
    """ Calculates where the head will be for each of the possible moves """

    x, y = head["x"], head["y"]
    return {
        "up": {"x": x, "y": y+1},
        "down": {"x": x, "y": y-1},
        "left": {"x": x-1, "y": y},
        "right": {"x": x+1, "y": y}
    }

def avoid_walls(possible_moves: dict, width: int, height: int):
    """ Removes the moves that will collide with walls """
    moves_to_remove = []
    for move in possible_moves:
        if not (0 <= possible_moves[move]["x"] < width and 0 <= possible_moves[move]["y"] < height):
            moves_to_remove.append(move)

    for move in moves_to_remove:
        del possible_moves[move]

    return possible_moves

def avoid_body(possible_moves: dict, body: list):
    """ Removes the moves that will collide with self """
    moves_to_remove = []
    for move in possible_moves:
        if possible_moves[move] in body:
            moves_to_remove.append(move)

    for move in moves_to_remove:
        del possible_moves[move]

    return possible_moves

def avoid_snakes(possible_moves: dict, snakes: dict):
    """ Removes the moves that will collide with other snakes """
    moves_to_remove = []
    for snake in snakes:
        for move in possible_moves:
            if possible_moves[move] in snake["body"]:
                moves_to_remove.append(move)

    for move in moves_to_remove:
        del possible_moves[move]

    return possible_moves

def create_board(snakes, width, height):
    """ Create a board representation """
    board = [[1 for _ in range(width)] for _ in range(height)]
    for snake in snakes:
        for body in snake["body"]:
            board[height - body["y"] - 1][body["x"]] = 1
    return board
    
def get_closer_to_food(possible_moves: dict, food: list, board: list):
    """ Find the move that gets the snake closest to food """
    stack, added = [], []
    food = [(f["x"], f["y"]) for f in food]
    for move in possible_moves:
        stack.append((possible_moves[move]["x"], possible_moves[move]["y"], move))

    while stack:
        current_x, current_y, initial_dir = stack.pop(0)
        if (current_x, current_y) in food: return initial_dir
        for x, y in [(1,0), (-1,0), (0,1), (0,-1)]:
            dx = current_x + x
            dy = current_y + y

            if (dx, dy) in food: return initial_dir
            if not(0 <= dx < len(board[0]) and 0 <= dy < len(board)): continue

            if board[dy][dx] and (dx, dy) not in added:
                added.append((dx,dy))
                stack.append((dx, dy, initial_dir))

def choose_move(data: dict) -> str:
    """
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request
    """

    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves = generate_possible_moves(my_head)

    board_width = data["board"]["width"]
    board_height = data["board"]["height"]
    snakes = data["board"]["snakes"]
    food = data["board"]["food"]

    board = create_board(snakes, board_width, board_height)

    possible_moves = avoid_walls(possible_moves, board_width, board_height)
    possible_moves = avoid_body(possible_moves, my_body)
    possible_moves = avoid_snakes(possible_moves, snakes)

    move = get_closer_to_food(possible_moves, food, board)

    if move == None:
        move = "up"
        if len(possible_moves) > 0:
            move = random.choice(list(possible_moves.keys()))

    return move

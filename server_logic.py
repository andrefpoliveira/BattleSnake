import random

def convert_coordinates_wrapped_mode(coordinates: dict, width: int, height: int, gamemode: str) -> dict:
    """ Convert coordinates outside of board to inside if playing wrapped """
    if gamemode != "wrapped": return coordinates
    x, y = coordinates["x"], coordinates["y"]
    return {"x": x % width, "y": y % height}

def generate_possible_moves(head: dict, gamemode: str, width: int, height: int) -> dict:
    """ Calculates where the head will be for each of the possible moves """
    x, y = head["x"], head["y"]
    return {
        "up": convert_coordinates_wrapped_mode({"x": x, "y": y+1}, width, height, gamemode),
        "down": convert_coordinates_wrapped_mode({"x": x, "y": y-1}, width, height, gamemode),
        "left": convert_coordinates_wrapped_mode({"x": x-1, "y": y}, width, height, gamemode),
        "right": convert_coordinates_wrapped_mode({"x": x+1, "y": y}, width, height, gamemode)
    }

def avoid_walls(possible_moves: dict, width: int, height: int):
    """ Removes the moves that will collide with walls """
    moves_to_remove = []
    for move in possible_moves:
        if not (0 <= possible_moves[move]["x"] < width and 0 <= possible_moves[move]["y"] < height):
            moves_to_remove.append(move)

    for move in moves_to_remove:
        if move in possible_moves:
            del possible_moves[move]

    return possible_moves

def avoid_body(possible_moves: dict, body: list):
    """ Removes the moves that will collide with self """
    moves_to_remove = []
    for move in possible_moves:
        if possible_moves[move] in body:
            moves_to_remove.append(move)

    for move in moves_to_remove:
        if move in possible_moves:
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
        if move in possible_moves:
            del possible_moves[move]

    return possible_moves

def create_board(snakes, width, height):
    """ Create a board representation """
    board = [[1 for _ in range(width)] for _ in range(height)]
    for snake in snakes:
        for body in snake["body"]:
            board[height - body["y"] - 1][body["x"]] = 0
    return board
    
def print_board(board):
    print("---")
    for row in board:
        print(''.join([str(x) for x in row]))
    print("---")

def get_closer_to_food(possible_moves: dict, food: list, board: list, gamemode: str):
    """ Find the move that gets the snake closest to food """
    width, height = len(board[0]), len(board)
    stack, added = [], []
    food = [(f["x"], f["y"]) for f in food]
    for move in possible_moves:
        stack.append((possible_moves[move]["x"], possible_moves[move]["y"], move))

    while stack:
        current_x, current_y, initial_dir = stack.pop(0)
        if (current_x, current_y) in food: return initial_dir
        for x, y in [(1,0), (-1,0), (0,1), (0,-1)]:

            coordinates = convert_coordinates_wrapped_mode({"x": current_x + x, "y": current_y + y}, width, height, gamemode)
            dx, dy = coordinates["x"], coordinates["y"]

            if (dx, dy) in food: return initial_dir
            if not(0 <= dx < width and 0 <= dy < height): continue
            if board[height-1-dy][dx] and (dx, dy) not in added:
                added.append((dx,dy))
                stack.append((dx, dy, initial_dir))

def avoid_head_to_head(possible_moves: dict, snakes: list, length: int, id: str, gamemode: str, width: int, height: int):
    """ Avoids the collision head to head with stronger snakes """
    moves_to_remove = []
    for move in possible_moves:
        for snake in snakes:
            if snake["id"] == id: continue
            if snake["length"] < length: continue
            poss_moves_snake = generate_possible_moves(snake["head"], gamemode, width, height)
            for s_move in poss_moves_snake:
                if possible_moves[move] == poss_moves_snake[s_move]:
                    moves_to_remove.append(move)

    for move in moves_to_remove:
        if move in possible_moves:
            del possible_moves[move]

    return possible_moves

def choose_move(data: dict) -> str:
    """
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request
    """
    
    gamemode = data["game"]["ruleset"]["name"]

    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    my_length = data["you"]["length"]
    my_id = data["you"]["id"]
    
    board_width = data["board"]["width"]
    board_height = data["board"]["height"]
    snakes = data["board"]["snakes"]
    food = data["board"]["food"]
    
    possible_moves = generate_possible_moves(my_head, gamemode, board_width, board_height)

    board = create_board(snakes, board_width, board_height)

    if gamemode != "wrapped":
        possible_moves = avoid_walls(possible_moves, board_width, board_height)
    
    possible_moves = avoid_body(possible_moves, my_body)
    possible_moves = avoid_snakes(possible_moves, snakes)
    
    possible_moves = avoid_head_to_head(possible_moves, snakes, my_length, my_id, gamemode, board_width, board_height)

    move = get_closer_to_food(possible_moves, food, board, gamemode)

    if move == None:
        move = "up"
        if len(possible_moves) > 0:
            move = random.choice(list(possible_moves.keys()))

    return move
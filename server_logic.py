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

def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """

    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves = generate_possible_moves(my_head)

    board_width = data["board"]["width"]
    board_height = data["board"]["height"]
    snakes = data["board"]["snakes"]

    possible_moves = avoid_walls(possible_moves, board_width, board_height)
    possible_moves = avoid_body(possible_moves, my_body)
    possible_moves = avoid_snakes(possible_moves, snakes)

    move = random.choice(list(possible_moves.keys()))

    return move

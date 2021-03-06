"""
Starter Unit Tests using the built-in Python unittest library.
See https://docs.python.org/3/library/unittest.html

You can expand these to cover more cases!

To run the unit tests, use the following command in your terminal,
in the folder where this file exists:

    python tests.py -v

"""
import unittest

import server_logic

class ConvertCoordinatesWrappedTest(unittest.TestCase):
    def test_other_mode(self):
        """ Should ignore the conversion """

        # Arrange
        width, height = 11, 11
        test_coordinates = {"x": -1, "y": 4}
        gamemode = "standard"

        # Act
        coordinates = server_logic.convert_coordinates_wrapped_mode(test_coordinates, width, height, gamemode)

        # Assert
        self.assertEqual(coordinates, test_coordinates)

    def test_wrapped_outside_left(self):
        """ Should convert to the other side """

        # Arrange
        width, height = 11, 11
        test_coordinates = {"x": -1, "y": 4}
        gamemode = "wrapped"

        # Act
        coordinates = server_logic.convert_coordinates_wrapped_mode(test_coordinates, width, height, gamemode)

        # Assert
        self.assertEqual(coordinates, {"x": width - 1, "y": 4})

    def test_wrapped_outside_right(self):
        """ Should convert to the other side """

        # Arrange
        width, height = 11, 11
        test_coordinates = {"x": width, "y": 4}
        gamemode = "wrapped"

        # Act
        coordinates = server_logic.convert_coordinates_wrapped_mode(test_coordinates, width, height, gamemode)

        # Assert
        self.assertEqual(coordinates, {"x": 0, "y": 4})

    def test_wrapped_outside_up(self):
        """ Should convert to the down side """

        # Arrange
        width, height = 11, 11
        test_coordinates = {"x": 4, "y": height}
        gamemode = "wrapped"

        # Act
        coordinates = server_logic.convert_coordinates_wrapped_mode(test_coordinates, width, height, gamemode)

        # Assert
        self.assertEqual(coordinates, {"x": 4, "y": 0})

    def test_wrapped_outside_down(self):
        """ Should convert to the upper side """

        # Arrange
        width, height = 11, 11
        test_coordinates = {"x": 4, "y": -1}
        gamemode = "wrapped"

        # Act
        coordinates = server_logic.convert_coordinates_wrapped_mode(test_coordinates, width, height, gamemode)

        # Assert
        self.assertEqual(coordinates, {"x": 4, "y": height-1})

class GeneratePossibleMoves(unittest.TestCase):
    def test_generate_moves(self):
        """ Should generate 4 moves """

        # Arrange
        test_head = {"x": 4, "y": 4}
        width, height = 11, 11
        gamemode = "standard"

        # Act
        possible_moves = server_logic.generate_possible_moves(test_head, gamemode, width, height)

        # Assert
        self.assertEqual(len(possible_moves), 4)
        self.assertEqual(possible_moves["up"], {"x": 4, "y": 5})
        self.assertEqual(possible_moves["down"], {"x": 4, "y": 3})
        self.assertEqual(possible_moves["left"], {"x": 3, "y": 4})
        self.assertEqual(possible_moves["right"], {"x": 5, "y": 4})

class AvoidWallsTest(unittest.TestCase):
    def test_no_walls(self):
        """ In the middle of the board, should have 4 moves"""

        # Arrange
        width = 11
        height = 11
        test_head = {"x": 4, "y": 4}
        gamemode = "standard"
        
        possible_moves = server_logic.generate_possible_moves(test_head, gamemode, width, height)

        # Act
        possible_moves = server_logic.avoid_walls(possible_moves, width, height)

        # Assert
        self.assertEqual(len(possible_moves), 4)
        self.assertTrue("up" in possible_moves)
        self.assertTrue("down" in possible_moves)
        self.assertTrue("left" in possible_moves)
        self.assertTrue("right" in possible_moves)

    def test_upper_wall(self):
        """ Against the upper wall, should not have 'up' option """

        # Arrange
        width = 11
        height = 11
        test_head = {"x": 4, "y": height-1}
        gamemode = "standard"

        possible_moves = server_logic.generate_possible_moves(test_head, gamemode, width, height)

        # Act
        possible_moves = server_logic.avoid_walls(possible_moves, width, height)

        # Assert
        self.assertEqual(len(possible_moves), 3)
        self.assertTrue("up" not in possible_moves)
        self.assertTrue("down" in possible_moves)
        self.assertTrue("left" in possible_moves)
        self.assertTrue("right" in possible_moves)

    def test_down_wall(self):
        """ Against the down wall, should not have 'down' option """

        # Arrange
        width = 11
        height = 11
        test_head = {"x": 4, "y": 0}
        gamemode = "standard"
        possible_moves = server_logic.generate_possible_moves(test_head, gamemode, width, height)

        # Act
        possible_moves = server_logic.avoid_walls(possible_moves, width, height)

        # Assert
        self.assertEqual(len(possible_moves), 3)
        self.assertTrue("up" in possible_moves)
        self.assertTrue("down" not in possible_moves)
        self.assertTrue("left" in possible_moves)
        self.assertTrue("right" in possible_moves)

    def test_left_wall(self):
        """ Against the left wall, should not have 'left' option """

        # Arrange
        width = 11
        height = 11
        test_head = {"x": 0, "y": 4}
        gamemode = "standard"

        possible_moves = server_logic.generate_possible_moves(test_head, gamemode, width, height)

        # Act
        possible_moves = server_logic.avoid_walls(possible_moves, width, height)

        # Assert
        self.assertEqual(len(possible_moves), 3)
        self.assertTrue("up" in possible_moves)
        self.assertTrue("down" in possible_moves)
        self.assertTrue("left" not in possible_moves)
        self.assertTrue("right" in possible_moves)

    def test_right_wall(self):
        """ Against the right wall, should not have 'right' option """

        # Arrange
        width = 11
        height = 11
        test_head = {"x": width-1, "y": 4}
        gamemode = "standard"

        possible_moves = server_logic.generate_possible_moves(test_head, gamemode, width, height)

        # Act
        possible_moves = server_logic.avoid_walls(possible_moves, width, height)

        # Assert
        self.assertEqual(len(possible_moves), 3)
        self.assertTrue("up" in possible_moves)
        self.assertTrue("down" in possible_moves)
        self.assertTrue("left" in possible_moves)
        self.assertTrue("right" not in possible_moves)

    def test_upper_left_corner(self):
        """ Against the upper left corner, should not have 'up' neither 'left' option """

        # Arrange
        width = 11
        height = 11
        test_head = {"x": 0, "y": height-1}
        gamemode = "standard"

        possible_moves = server_logic.generate_possible_moves(test_head, gamemode, width, height)

        # Act
        possible_moves = server_logic.avoid_walls(possible_moves, width, height)

        # Assert
        self.assertEqual(len(possible_moves), 2)
        self.assertTrue("up" not in possible_moves)
        self.assertTrue("down" in possible_moves)
        self.assertTrue("left" not in possible_moves)
        self.assertTrue("right" in possible_moves)

    def test_upper_right_corner(self):
        """ Against the upper right corner, should not have 'up' neither 'right' option """

        # Arrange
        width = 11
        height = 11
        test_head = {"x": width-1, "y": height-1}
        gamemode = "standard"

        possible_moves = server_logic.generate_possible_moves(test_head, gamemode, width, height)

        # Act
        possible_moves = server_logic.avoid_walls(possible_moves, width, height)

        # Assert
        self.assertEqual(len(possible_moves), 2)
        self.assertTrue("up" not in possible_moves)
        self.assertTrue("down" in possible_moves)
        self.assertTrue("left" in possible_moves)
        self.assertTrue("right" not in possible_moves)

    def test_down_left_corner(self):
        """ Against the down left corner, should not have 'down' neither 'left' option """

        # Arrange
        width = 11
        height = 11
        test_head = {"x": 0, "y": 0}
        gamemode = "standard"

        possible_moves = server_logic.generate_possible_moves(test_head, gamemode, width, height)

        # Act
        possible_moves = server_logic.avoid_walls(possible_moves, width, height)

        # Assert
        self.assertEqual(len(possible_moves), 2)
        self.assertTrue("up" in possible_moves)
        self.assertTrue("down" not in possible_moves)
        self.assertTrue("left" not in possible_moves)
        self.assertTrue("right" in possible_moves)

    def test_down_right_corner(self):
        """ Against the down right corner, should not have 'down' neither 'right' option """

        # Arrange
        width = 11
        height = 11
        test_head = {"x": width-1, "y": 0}
        gamemode = "standard"

        possible_moves = server_logic.generate_possible_moves(test_head, gamemode, width, height)

        # Act
        possible_moves = server_logic.avoid_walls(possible_moves, width, height)

        # Assert
        self.assertEqual(len(possible_moves), 2)
        self.assertTrue("up" in possible_moves)
        self.assertTrue("down" not in possible_moves)
        self.assertTrue("left" in possible_moves)
        self.assertTrue("right" not in possible_moves)

class AvoidBodyTest(unittest.TestCase):
    def test_avoid_neck(self):
        """ It should not be able to move back """

        # Arrange
        test_head = {"x": 4, "y": 4}
        test_body = [{"x": 3, "y": 4}, {"x": 2, "y": 4}]
        gamemode = "standard"
        width, height = 11, 11

        possible_moves = server_logic.generate_possible_moves(test_head, gamemode, width, height)

        # Act
        possible_moves = server_logic.avoid_body(possible_moves, test_body)

        # Assert
        self.assertEqual(len(possible_moves), 3)
        self.assertTrue("up" in possible_moves)
        self.assertTrue("down" in possible_moves)
        self.assertTrue("left" not in possible_moves)
        self.assertTrue("right" in possible_moves)

    def test_avoid_rest_body(self):
        """ Should avoid the rest of the body aswell """

        # Arrange
        test_head = {"x": 4, "y": 4}
        test_body = [{"x": 3, "y": 4}, {"x": 3, "y": 3}, {"x": 4, "y": 3}]
        gamemode = "standard"
        width, height = 11, 11

        possible_moves = server_logic.generate_possible_moves(test_head, gamemode, width, height)

        # Act
        possible_moves = server_logic.avoid_body(possible_moves, test_body)

        # Assert
        self.assertEqual(len(possible_moves), 2)
        self.assertTrue("up" in possible_moves)
        self.assertTrue("down" not in possible_moves)
        self.assertTrue("left" not in possible_moves)
        self.assertTrue("right" in possible_moves)

class AvoidSnakesTest(unittest.TestCase):
    def test_avoid_snake(self):
        """ It should not be able to move into the snake """

        # Arrange
        test_head = {"x": 4, "y": 4}
        test_snakes = [{"body": [{"x": 3, "y": 4}, {"x": 3, "y": 3}, {"x": 4, "y": 3}]}]
        gamemode = "standard"
        width, height = 11, 11
        
        possible_moves = server_logic.generate_possible_moves(test_head, gamemode, width, height)

        # Act
        possible_moves = server_logic.avoid_snakes(possible_moves, test_snakes)

        # Assert
        self.assertEqual(len(possible_moves), 2)
        self.assertTrue("up" in possible_moves)
        self.assertTrue("down" not in possible_moves)
        self.assertTrue("left" not in possible_moves)
        self.assertTrue("right" in possible_moves)

class AvoidSnakesHead(unittest.TestCase):
    def test_avoid_collision(self):
        """ It should not move to square in the middle """

        # Arrange
        test_head = {"x": 4, "y": 4}
        test_snake = [{"id": "2", "head": {"x": 2, "y": 4}, "length": 3}]
        #test_snakes = [{"body": [{"x": 3, "y": 4}, {"x": 3, "y": 3}, {"x": 4, "y": 3}]}]
        gamemode = "standard"
        width, height = 11, 11
        
        possible_moves = server_logic.generate_possible_moves(test_head, gamemode, width, height)

        # Act
        possible_moves = server_logic.avoid_head_to_head(possible_moves, test_snake, 3, "1", gamemode, width, height)

        # Assert
        self.assertEqual(len(possible_moves), 3)
        self.assertTrue("up" in possible_moves)
        self.assertTrue("down" in possible_moves)
        self.assertTrue("left" not in possible_moves)
        self.assertTrue("right" in possible_moves)

    def test_dont_avoid_collision(self):
        """ It should be able to move to square in the middle """

        # Arrange
        test_head = {"x": 4, "y": 4}
        test_snake = [{"id": "2", "head": {"x": 2, "y": 4}, "length": 3}]
        #test_snakes = [{"body": [{"x": 3, "y": 4}, {"x": 3, "y": 3}, {"x": 4, "y": 3}]}]
        gamemode = "standard"
        width, height = 11, 11
        
        possible_moves = server_logic.generate_possible_moves(test_head, gamemode, width, height)

        # Act
        possible_moves = server_logic.avoid_head_to_head(possible_moves, test_snake, 4, "1", gamemode, width, height)

        # Assert
        self.assertEqual(len(possible_moves), 4)
        self.assertTrue("up" in possible_moves)
        self.assertTrue("down" in possible_moves)
        self.assertTrue("left" in possible_moves)
        self.assertTrue("right" in possible_moves)

if __name__ == "__main__":
    unittest.main()

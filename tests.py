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

class GeneratePossibleMoves(unittest.TestCase):
    def test_generate_moves(self):
        """ Should generate 4 moves """

        # Arrange
        test_head = {"x": 4, "y": 4}

        # Act
        possible_moves = server_logic.generate_possible_moves(test_head)

        # Assert
        self.assertEqual(len(possible_moves), 4)
        self.assertEqual(possible_moves["up"], {"x": 4, "y": 3})
        self.assertEqual(possible_moves["down"], {"x": 4, "y": 5})
        self.assertEqual(possible_moves["left"], {"x": 3, "y": 4})
        self.assertEqual(possible_moves["right"], {"x": 5, "y": 4})

class AvoidWallsTest(unittest.TestCase):
    def test_no_walls(self):
        """ In the middle of the board, should have 4 moves"""

        # Arrange
        width = 11
        height = 11
        test_head = {"x": 4, "y": 4}
        possible_moves = server_logic.generate_possible_moves(test_head)

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
        test_head = {"x": 4, "y": 0}
        possible_moves = server_logic.generate_possible_moves(test_head)

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
        test_head = {"x": 4, "y": height-1}
        possible_moves = server_logic.generate_possible_moves(test_head)

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
        possible_moves = server_logic.generate_possible_moves(test_head)

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
        possible_moves = server_logic.generate_possible_moves(test_head)

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
        test_head = {"x": 0, "y": 0}
        possible_moves = server_logic.generate_possible_moves(test_head)

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
        test_head = {"x": width-1, "y": 0}
        possible_moves = server_logic.generate_possible_moves(test_head)

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
        test_head = {"x": 0, "y": height-1}
        possible_moves = server_logic.generate_possible_moves(test_head)

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
        test_head = {"x": width-1, "y": height-1}
        possible_moves = server_logic.generate_possible_moves(test_head)

        # Act
        possible_moves = server_logic.avoid_walls(possible_moves, width, height)

        # Assert
        self.assertEqual(len(possible_moves), 2)
        self.assertTrue("up" in possible_moves)
        self.assertTrue("down" not in possible_moves)
        self.assertTrue("left" in possible_moves)
        self.assertTrue("right" not in possible_moves)

if __name__ == "__main__":
    unittest.main()

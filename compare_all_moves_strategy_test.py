import unittest

from colour import Colour
from compare_all_moves_strategy import CompareAllMoves
from test_board_base import TestBoardBase, Contains


class TestCompareAllMovesStrategy(TestBoardBase):

    def test_pieces_will_double_up(self):

        self.add_many_pieces(1, Colour.WHITE, 1)
        self.add_many_pieces(1, Colour.WHITE, 3)

        strategy = CompareAllMoves()
        strategy.move(self.board, Colour.WHITE, [6, 4])

        self.assert_location(7, Contains(2).pieces())

    def test_will_form_wall(self):

        self.add_many_pieces(2, Colour.WHITE, 20)
        self.add_many_pieces(1, Colour.WHITE, 16)
        self.add_many_pieces(1, Colour.WHITE, 17)
        self.add_many_pieces(1, Colour.WHITE, 18)

        strategy = CompareAllMoves()
        strategy.move(self.board, Colour.WHITE, [3, 4])

        self.assert_location(21, Contains(2).pieces())
        self.assert_location(20, Contains(2).pieces())
        self.assert_location(16, Contains(1).pieces())


class TestCompareAllMovesValidity(TestBoardBase):

    def test_make_single_move_to_win(self):

        self.add_many_pieces(1, Colour.WHITE, 23)

        strategy = CompareAllMoves()
        strategy.move(self.board, Colour.WHITE, [6, 4])

        self.assert_location(23, Contains(0).pieces())

    def test_can_use_second_roll_without_first(self):
        self.add_many_pieces(2, Colour.WHITE, 0)
        self.add_many_pieces(2, Colour.BLACK, 3)

        strategy = CompareAllMoves()
        strategy.move(self.board, Colour.WHITE, [3, 4])

        self.assert_location(4, Contains(1).pieces())
        self.assert_location(0, Contains(1).pieces())

    def test_can_use_not_all_dice(self):
        self.add_many_pieces(3, Colour.WHITE, 18)
        self.add_many_pieces(1, Colour.WHITE, 12)
        self.add_many_pieces(2, Colour.BLACK, 17)

        strategy = CompareAllMoves()
        strategy.move(self.board, Colour.WHITE, [5, 5, 5, 5])

        self.assert_location(23, Contains(3).pieces())
        self.assert_location(12, Contains(1).pieces())


if __name__ == '__main__':
    unittest.main()

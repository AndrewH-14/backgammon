from colour import Colour
from piece import Piece


class Board:
    def __init__(self):
        self.__pieces = []
        self.setup_pieces()

    def setup_pieces(self):
        self.add_many_pieces(2, Colour.WHITE, 1)
        self.add_many_pieces(5, Colour.BLACK, 6)
        self.add_many_pieces(3, Colour.BLACK, 8)
        self.add_many_pieces(5, Colour.WHITE, 12)
        self.add_many_pieces(5, Colour.BLACK, 13)
        self.add_many_pieces(3, Colour.WHITE, 17)
        self.add_many_pieces(5, Colour.WHITE, 19)
        self.add_many_pieces(2, Colour.BLACK, 24)

    def add_many_pieces(self, number_of_pieces, colour, location):
        for i in range(number_of_pieces):
            self.__pieces.append(Piece(colour, location))

    def is_move_possible(self, piece, die_roll):
        if len(self.pieces_at(self.taken_location(piece.colour))) > 0:
            if piece.location != self.taken_location(piece.colour):
                return False
        if piece.colour == Colour.BLACK:
            die_roll = -die_roll
        new_location = piece.location + die_roll
        if new_location <= 0 or new_location >= 25:
            return self.can_move_off(piece.colour)
        pieces_at_new_location = self.pieces_at(new_location)
        if len(pieces_at_new_location) == 0 or len(pieces_at_new_location) == 1:
            return True
        if self.pieces_at(new_location)[0].colour == piece.colour:
            return True
        return False

    def can_move_off(self, colour):
        return all(x.spaces_to_home() <= 6 for x in self.get_pieces(colour))

    def move_piece(self, piece, die_roll):
        if not self.is_move_possible(piece, die_roll):
            raise Exception('You cannot make this move')
        if piece.colour == Colour.BLACK:
            die_roll = -die_roll

        new_location = piece.location + die_roll
        if new_location <= 0 or new_location >= 25:
            self.remove_piece(piece)

        pieces_at_new_location = self.pieces_at(new_location)

        if len(pieces_at_new_location) == 1 and pieces_at_new_location[0].colour != piece.colour:
            piece_to_take = pieces_at_new_location[0]
            piece_to_take.location = self.taken_location(piece_to_take.colour)

        piece.location = new_location

    def taken_location(self, colour):
        if colour == Colour.WHITE:
            return 0
        else:
            return 25

    def pieces_at(self, location):
        return [x for x in self.__pieces if x.location == location]

    def get_pieces(self, colour):
        return [x for x in self.__pieces if x.colour == colour]

    def pieces_at_text(self, location):
        pieces = self.pieces_at(location)
        if len(pieces) == 0:
            return " .  "
        if pieces[0].colour == Colour.WHITE:
            return " %sW " % (len(pieces))
        else:
            return " %sB " % (len(pieces))

    def print_board(self):
        print("---------------------------------------------------")
        line = "|"
        for i in range(13, 18 + 1):
            line = line + self.pieces_at_text(i)
        line = line + "|"
        for i in range(19, 24 + 1):
            line = line + self.pieces_at_text(i)
        line = line + "|"
        line = line + self.pieces_at_text(self.taken_location(Colour.BLACK))
        print(line)
        print("|                        |                        |")
        line = "|"
        for i in reversed(range(7, 12+1)):
            line = line + self.pieces_at_text(i)
        line = line + "|"
        for i in reversed(range(1, 6+1)):
            line = line + self.pieces_at_text(i)
        line = line + "|"
        line = line + self.pieces_at_text(self.taken_location(Colour.WHITE))
        print(line)
        print("---------------------------------------------------")

    def remove_piece(self, piece):
        self.__pieces.remove(piece)


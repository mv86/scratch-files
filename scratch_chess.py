from collections import defaultdict

from src.game_enums import Color, Direction
from src.scratch_game import Coords, Game

from src.game_pieces.bishop import Bishop
from src.game_pieces.king import King
from src.game_pieces.knight import Knight
from src.game_pieces.pawn import Pawn
from src.game_pieces.queen import Queen
from src.game_pieces.rook import Rook


class Chess(Game):
    """temp"""
    def __init__(self):
        super().__init__()
        self.playing_color = Color.WHITE
        self.opponent_color = Color.BLACK
        self.pieces = {
            Color.WHITE: defaultdict(int),
            Color.BLACK: defaultdict(int)
        }
        self.valid_piece_names = {'Bishop', 'King', 'Knight', 'Pawn', 'Queen', 'Rook'}
        self.valid_piece_colors = {Color.WHITE, Color.BLACK}
        self.king_coords = {
            Color.WHITE: None,
            Color.BLACK: None
        }
        self.from_coords = None
        self.to_coords = None
        self.from_board_positon = None
        self.to_board_position = None
        self.check_mate = False

    def new_setup():
        """Return dictionary of new chess game default piece postitions.

        Dictionary is in following format:
        key = str representation of game coordinates xy
        value = chess GamePiece
        e.g '00': Rook(Color.WHITE)
        """
        white_pieces = chess_pieces(Color.WHITE, y_idxs=[0, 1])
        black_pieces = chess_pieces(Color.BLACK, y_idxs=[7, 6])
        return dict(white_pieces + black_pieces)

    def move(self, from_coords, to_coords):
        """temp"""
        self.validate_coords(from_coords, to_coords)
        self._set_move_attibutes(from_coords, to_coords)
        # move_type = _move_type(from_coords, to_coords)
        is_legal_move, move_ = self._move_type()
        if is_legal_move(self.board, from_coords, to_coords):
            move_(self.board, from_coords, to_coords)

    def _set_move_attibutes(self, from_coords, to_coords):
        self.from_coords, self.to_coords = from_coords, to_coords
        self.playing_piece = self.board[from_coords.x][from_coords.y]
        self.from_board_positon = self.board[from_coords.x][from_coords.y]
        self.to_board_positon = self.board[to_coords.x][to_coords.y]

    def _move_type(self):
        if self._is_castle_move():
            return self._is_legal_castle, self._castle_move_type()
        if self._is_prawn_promotion():
            return self.playing_piece.valid_move, self._promote_pawn
        if self._is_attack_move():
            return self.playing_piece.valid_attack, self._attack
        return self.playing_piece.valid_move, self._move

    def is_piece_blocking(self):
        """Check if any piece blocking move from_coords to_coords. Return bool."""
        if self.move_direction(self.from_coords, self.to_coords) != Direction.NON_LINEAR:
            # Only Knights move non_linear and they can jump over pieces
            for coords in self.coords_between(self.from_coords, self.to_coords):
                if self.board[coords.x][coords.y] is not None:
                    return True
        return False

    def _promote_pawn(self):
        self.from_board_positon = None
        # Defaults to Queen as most players want this
        # TODO Add functionality to choose promotion piece
        self.to_board_positon = Queen(self.playing_color)

    def _move(self):
        self.from_board_positon = None
        self.to_board_position = self.playing_piece

    def _attack(self):
        self.from_board_positon = None
        captured_piece = self.to_board_position
        captured_piece.coords = None
        self.pieces[captured_piece.color][captured_piece.name] -= 1
        self.to_board_position = self.playing_piece

    def _is_castle_move(self):
        if self.playing_piece.type == 'King' and self.playing_piece.color == Color.WHITE:
            if (self.from_coords == Coords(4, 0)
                    and self.to_coords in (Coords(2, 0), Coords(6, 0))):
                return True
        if self.playing_piece.type == 'King' and self.playing_piece.color == Color.BLACK:
            if (self.from_coords == Coords(4, 7)
                    and self.to_coords in (Coords(2, 7), Coords(6, 7))):
                return True
        return False

    def _castle_move_type(self):
        if self.to_coords.y == 0:
            if self.to_coords.x == 2:
                return self._white_castle_queen_side
            return self._white_castle_king_side
        if self.to_coords.y == 7:
            if self.to_coords.x == 2:
                return self._black_castle_queen_side
            return self._black_castle_king_side

    def _is_prawn_promotion(self):
        return self.playing_piece.type == 'Pawn' and self.to_coords.y in (0, 7)

    def _is_legal_castle(self, board, from_coords, to_coords):
        # check king and rook not moved
        # check king not in check
        # check rook and king in right positions
        # check no piece blocking
        # check king not in check for thru and to move
        pass

    def _is_legal_en_passant(self):
        # check last move was opponent pawn moving 2 spaces

    def _white_castle_king_side(self):
        self.board[4][0], self.board[7][0] = None, None
        self.board[6][0], self.board[5][0] = self._king_rook_castled_pieces(Color.WHITE)

    def _white_castle_queen_side(self):
        self.board[4][0], self.board[0][0] = None, None
        self.board[2][0], self.board[3][0] = self._king_rook_castled_pieces(Color.WHITE)

    def _black_castle_king_side(self):
        self.board[4][7], self.board[7][7] = None, None
        self.board[6][7], self.board[5][7] = self._king_rook_castled_pieces(Color.BLACK)

    def _black_castle_queen_side(self):
        self.board[4][7], self.board[0][7] = None, None
        self.board[2][7], self.board[3][7] = self._king_rook_castled_pieces(Color.BLACK)

    @staticmethod
    def _king_rook_castled_pieces(playing_color):
        king, rook = King(playing_color), Rook(playing_color)
        king.moved = True
        rook.moved = True
        return king, rook

    def _is_attack_move(self):
        return self.to_board_position is not None or self._is_en_passant()

    def _is_en_passant(self):
        if (self.playing_piece.type == 'Pawn' and self.playing_piece.valid_capture()
                and self.to_board_positon is None):
            if self.playing_piece.color == Color.WHITE and self.to_coords.y == 5:
                return self.board[self.to_coords.x][self.to_coords.y - 1] == Pawn(Color.BLACK)
            if self.playing_piece.color == Color.BLACK and self.to_coords.y == 2:
                return self.board[self.to_coords.x][self.to_coords.y + 1] == Pawn(Color.WHITE)
        return False


def chess_pieces(color, *, y_idxs=None):
    """Helper method for new_chess_setup."""
    coords = [f'{x_idx}{y_idx}' for y_idx in y_idxs for x_idx in range(8)]
    pieces = [
        Rook(color),
        Knight(color),
        Bishop(color),
        Queen(color),
        King(color),
        Bishop(color),
        Knight(color),
        Rook(color),
        Pawn(color),
        Pawn(color),
        Pawn(color),
        Pawn(color),
        Pawn(color),
        Pawn(color),
        Pawn(color),
        Pawn(color)
    ]
    return list(zip(coords, pieces))
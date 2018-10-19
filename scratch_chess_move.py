# from src.scratch_game import Coords
# from src. game_enums import Color

# class ChessMove:
#     def __init__(self):
#         self.to_coords = None
#         self.from_coords = None



#     def is_castle_move(self, piece, from_coords, to_coords):
#         if piece.type == 'King' and piece.color == Color.WHITE:
#             if (from_coords == Coords(4, 0)
#                     and to_coords in (Coords(2, 0), Coords(6, 0))):
#                 return True
#         if piece.type == 'King' and piece.color == Color.BLACK:
#             if (from_coords == Coords(4, 7)
#                     and to_coords in (Coords(2, 7), Coords(6, 7))):
#                 return True
#         return False

#     def castle_move_type(self, to_coords):
#         if to_coords.y == 0:
#             if to_coords.x == 2:
#                 return self.white_castle_queen_side
#             return self.white_castle_king_side
#         if to_coords.y == 7:
#             if to_coords.x == 2:
#                 return self.black_castle_queen_side
#             return self.black_castle_king_side

#     def is_prawn_promotion(self, piece, to_coords):
#         return piece.type == 'Pawn' and to_coords.y in (0, 7)

#     def is_legal_castle(self, board, from_coords, to_coords):
#         # check king and rook not moved
#         # check king not in check
#         # check rook and king in right positions
#         # check no piece blocking
#         # check king not in check for thru and to move
#         pass

#     # def is_legal_promotion(self, board)

#     def white_castle_king_side(self, board, from_coords, to_coords):
#         board[4][0], board[7][0] = None, None
#         board[6][0] = King(Color.WHITE)
#         board[5][0] = Rook(Color.WHITE)

#     def white_castle_queen_side(self, board, from_coords, to_coords):
#         board[4][0], board[0][0] = None, None
#         board[2][0] = King(Color.WHITE)
#         board[3][0] = Rook(Color.WHITE)

#     def black_castle_king_side(self, board, from_coords, to_coords):
#         board[4][7], board[7][7] = None, None
#         board[6][7] = King(Color.BLACK)
#         board[5][7] = Rook(Color.BLACK)

#     def black_castle_queen_side(self, board, from_coords, to_coords):
#         board[4][7], board[0][7] = None, None
#         board[2][7] = King(Color.BLACK)
#         board[3][7] = Rook(Color.BLACK)


#     def attack(self):
#         if


#     def is_attack_move(self, board, from_coords, to_coords):
#         if board[to_coords.x, to_coords.y] is not None
#                 or self.is_en_passant(*args):
#             return True
#         return False

#     def is_en_passant(self, board, piece, from_coords, to_coords):
#         if (piece.type == 'Pawn' and piece.valid_capture()
#                 and board[from_coords.x][from_coords.y] == None):
#             if piece.color == Color.WHITE and to_coords.y == 5:
#                 return board[to_coords.x][to_coords.y - 1] == Pawn(Color.BLACK)
#             if piece.color == Color.BLACK and to_coords.y == 2:
#                 return board[to_coords.x][to_coords.y + 1] == Pawn(Color.WHITE)
#         return False

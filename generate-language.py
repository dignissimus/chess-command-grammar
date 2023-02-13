from language import String, Union, Enumeration

File = Enumeration("A", "B", "C", "D", "E", "F", "G", "H")
Rank = Enumeration("One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight")
Square = File + Rank

Takes = (String("Takes") + ~String("On")) | String("X")
CommandPrefix = String("Move") + ~String("The")

PieceName = Enumeration("Rook", "Knight", "Bishop", "Queen", "King", "Pawn")
PieceAbbreviation = Enumeration("R", "N", "B", "Q", "K", "P")
Piece = PieceName | PieceAbbreviation


Promotes = String("Promotes") + ~String("To") | String("Equals")
PromotionSuffix = ~Promotes + Piece

# Pawn moves
## For example, e4
SimplePawnMove = Square
## Examples: e4-e5, h3 to h4, d-d4, d to d4, d-e
ComplexPawnMove = (File | Square) + ~String("To") + (File | Square)
## Examples: e takes d5, e4 takes d5, exd5, exd
PawnTakes = (File | Square) + Takes + (File | Square)
## Examples, exd8=Q, e takes f8 promotes to queen, d8=Q
PawnMove = (SimplePawnMove | ComplexPawnMove | PawnTakes) + ~PromotionSuffix


# Examples: Rook e4, Pawn to e4, Bishop to f8, Bf8, B to f8
SimplePieceMove = Piece + ~String("To") + Square
# Examples: Rook on e f8, Rook on b5 to g5
ComplexPieceMove = (
    Piece + ~String("On") + (Square | File | Rank) + ~String("To") + Square
)
# Examples: Move the rook on e4 to e8, Move the rook to d6
PieceMove = ~CommandPrefix + (SimplePieceMove | ComplexPieceMove)

Castle = String("Castle")
CastleLocation = String("Short") | String("Long")
CastleLocationFirst = Castle + CastleLocation
CastleLocationSecond = CastleLocation + Castle
CastlingMove = Castle | CastleLocationFirst | CastleLocationSecond

Move = (PieceMove | PawnMove | CastlingMove) + ~String("Check")

InterfaceCommand = Enumeration(
    "next",
    "continue",
    "next puzzle",
    "clock",
    "draw",
    "offer draw",
    "accept draw",
    "resign",
    "resign",
    "up vote",
    "down vote",
)

Command = Move | InterfaceCommand

with open("language.txt", "w") as file:
    file.writelines("\n".join(Command.lower()))

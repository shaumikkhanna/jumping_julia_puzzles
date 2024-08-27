import random


class Chessboard:
    def __init__(self):
        self.board = [['?' for _ in range(8)] for _ in range(8)]
        self.path = []


    def __str__(self):
        return "\n".join(" ".join(f'{cell: <5}' for cell in row) for row in self.board)


    def check_valid(self):
        """Checks if the board is valid."""
        
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece in ['p', 'k', 'X']:
                    continue
                elif piece[0] in ['r', 'q', 'b'] and piece[1] in ['1', '2', '3', '4', '5', '6']:
                    continue
                else:
                    return False
                
        return True


    def neighbors(self, square, piece=None, difficulty_bias=1):
        x, y = square
        if piece is None:
            piece = self.board[x][y]

        # Pawn movement
        if piece[0] == 'p':
            if random.random() < difficulty_bias:
                out = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            else:
                out = [(x + 1, y), (x, y + 1)]

        # Knight movement
        elif piece[0] == 'k':
            if random.random() < difficulty_bias:
                out = [(x + 1, y + 2), (x - 1, y + 2), (x + 1, y - 2), (x - 1, y - 2), (x + 2, y + 1), (x - 2, y + 1), (x + 2, y - 1), (x - 2, y - 1)]
            else:
                out = [(x + 1, y + 2), (x - 1, y + 2), (x + 2, y + 1), (x + 2, y - 1)]
        
        # Rook movement
        elif piece[0] == 'r':
            stride = int(piece[1])
            if random.random() < difficulty_bias:
                out = [(x + stride, y), (x - stride, y), (x, y + stride), (x, y - stride)]
            else:
                out = [(x + stride, y), (x, y + stride)]

        # Bishop movement
        elif piece[0] == 'b':
            stride = int(piece[1])
            if random.random() < difficulty_bias:
                out = [(x + stride, y + stride), (x - stride, y - stride), (x + stride, y - stride), (x - stride, y + stride)]
            else:
                out = [(x + stride, y + stride)]
        
        # Queen movement
        elif piece[0] == 'q':
            stride = int(piece[1])
            if random.random() < difficulty_bias:
                out = [(x + stride, y), (x - stride, y), (x, y + stride), (x, y - stride), (x + stride, y + stride), (x - stride, y - stride), (x + stride, y - stride), (x - stride, y + stride)]
            else:
                out = [(x + stride, y), (x + stride, y + stride), (x, y + stride)]
        
        # Removing invalid moves
        return [(i, j) for i, j in out if 0 <= i < 8 and 0 <= j < 8]
        

    def all_neighbors_and_pieces(self, square, shuffled=True, difficulty_bias=1):
        """
        Returns a list of all possible neighbors of a cell along with what piece that 
        square will have to be to get that neighbor.
        """
        
        x, y = square

        out = [
            ((x + 1, y), ['p', 'r1', 'q1']), # Right 1
            ((x, y + 1), ['p', 'r1', 'q1']), # Down 1
            ((x + 1, y + 1), ['p', 'b1', 'q1']), # Right 1, Down 1
            ((x + 1, y + 2), ['k']), # Right 1, Down 2
            ((x + 2, y + 1), ['k']), # Right 2, Down 1
            ((x - 1, y + 2), ['k']), # Left 1, Down 2
            ((x + 2, y - 1), ['k']), # Right 2, Up 1
        ]   
        maybe = [
            ((x - 1, y), ['p', 'r1', 'q1']), # Left 1
            ((x, y - 1), ['p', 'r1', 'q1']), # Up 1
            ((x - 1, y - 1), ['p', 'b1', 'q1']), # Left 1, Up 1
            ((x + 1, y - 1), ['p', 'b1', 'q1']), # Right 1, Up 1
            ((x - 1, y + 1), ['p', 'b1', 'q1']), # Left 1, Down 1
            ((x - 2, y + 1), ['k']), # Left 2, Down 1
            ((x + 1, y - 2), ['k']), # Right 1, Up 2
            ((x - 1, y - 2), ['k']), # Left 1, Up 2
            ((x - 2, y - 1), ['k']), # Left 2, Up 1
        ]

        for stride in range(2, 7):
            out.extend([
                ((x + stride, y), ['r' + str(stride), 'q' + str(stride)]), # Right stride
                ((x, y + stride), ['r' + str(stride), 'q' + str(stride)]), # Down stride
                ((x + stride, y + stride), ['b' + str(stride), 'q' + str(stride)]), # Right stride, Down stride
            ])

            maybe.extend([
                ((x - stride, y), ['r' + str(stride), 'q' + str(stride)]), # Left stride
                ((x, y - stride), ['r' + str(stride), 'q' + str(stride)]), # Up stride
                ((x - stride, y - stride), ['b' + str(stride), 'q' + str(stride)]), # Left stride, Up stride
                ((x + stride, y - stride), ['b' + str(stride), 'q' + str(stride)]), # Right stride, Up stride
                ((x - stride, y + stride), ['b' + str(stride), 'q' + str(stride)]), # Left stride, Down stride
            ])

        for move in maybe:
            if random.random() < difficulty_bias:
                out.append(move)

        # Removing invalid moves
        out = [(n, p) for n, p in out if 0 <= n[0] < 8 and 0 <= n[1] < 8]

        if shuffled:
            random.shuffle(out)

        return out


    def create_random_path(self, difficulty_bias=0.25):
        self.path = [(0, 0)]
        path_pieces = []

        current_square = (0, 0)
        bad_squares = []
        affected_squares = []

        while current_square != (7, 7):
            print(f'Path: {self.path}\nCurrent Square: {current_square}\nAffected Squares: {affected_squares}\nBad Squares: {bad_squares}\nPath Pieces: {path_pieces}\n')
            for neighbor, pieces in self.all_neighbors_and_pieces(current_square, difficulty_bias=difficulty_bias):
                
                # Found next square if it is 
                # 1) A new square ie not in the path
                # 2) Not a bad square ie has neighbors that are not in the path
                # 3) Does not touch the path with a certain distance
                if neighbor not in bad_squares and all(neighbor not in as_ for as_ in affected_squares):
                    next_square = neighbor
                    next_to_piece = random.choice(pieces)
                    bad_squares = []
                    break

            else:
                if not path_pieces:
                    return self.create_random_path(difficulty_bias=difficulty_bias)

                bad_squares.append(current_square)
                current_square = self.path.pop()
                affected_squares.pop()
                path_pieces.pop()
                continue

            self.path.append(next_square)
            affected_squares.append(self.neighbors(current_square, next_to_piece))
            path_pieces.append(next_to_piece)
            current_square = next_square

        # Mark all the squares in the path
        for square, piece in zip(self.path, path_pieces):
            self.board[square[0]][square[1]] = piece


cb = Chessboard()
cb.create_random_path()
print(cb)
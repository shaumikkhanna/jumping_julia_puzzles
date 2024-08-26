class Chessboard:
    def __init__(self, board):
        self.board = board
        self.paths = set()

    def neighbors(self, square):
        x, y = square
        piece = self.board[x][y]

        if piece[0] == 'p':
            out = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        elif piece[0] == 'k':
            out = [(x + 1, y + 2), (x - 1, y + 2), (x + 1, y - 2), (x - 1, y - 2), (x + 2, y + 1), (x - 2, y + 1), (x + 2, y - 1), (x - 2, y - 1)]
        elif piece[0] == 'r':
            stride = int(piece[1])
            out = [(x + stride, y), (x - stride, y), (x, y + stride), (x, y - stride)]
        elif piece[0] == 'b':
            stride = int(piece[1])
            out = [(x + stride, y + stride), (x - stride, y - stride), (x + stride, y - stride), (x - stride, y + stride)]
        elif piece[0] == 'q':
            stride = int(piece[1])
            out = [(x + stride, y), (x - stride, y), (x, y + stride), (x, y - stride), (x + stride, y + stride), (x - stride, y - stride), (x + stride, y - stride), (x - stride, y + stride)]
        
        return [(i, j) for i, j in out if 0 <= i < 8 and 0 <= j < 8]
    

    def find_paths_from_u(self, u, visited, path):
        """Finds all paths from square u to the end using a recursive DFS approach."""

        visited[u[0]][u[1]] = True
        path.append(u)

        if u == (7, 7):
            self.paths.add(str(path))
            print(path)
        else:
            for neighbor in self.neighbors(u):
                if not visited[neighbor[0]][neighbor[1]]:
                    self.find_paths_from_u(neighbor, visited, path)
        
        path.pop()
        visited[u[0]][u[1]] = False


    def find_paths_from_start(self):
        visited = [[False for _ in range(8)] for _ in range(8)]
        path = []
        self.find_paths_from_u((0, 0), visited, path)
    


original = [
        ['p', 'q3', 'p', 'b2', 'p', 'r4', 'k', 'q6'],
        ['k', 'p', 'r3', 'k', 'r1', 'p', 'b2', 'p'],
        ['r2', 'p', 'b2', 'r4', 'p', 'r1', 'q5', 'k'],
        ['b4', 'r3', 'p', 'q5', 'r3', 'b2', 'k', 'p'],
        ['q5', 'p', 'k', 'b4', 'q2', 'r2', 'p', 'b2'],
        ['b1', 'p', 'k', 'p', 'r1', 'q3', 'k', 'r5'],
        ['p', 'q1', 'r3', 'k', 'p', 'q4', 'p', 'k'],
        ['k', 'q3', 'p', 'b1', 'r2', 'b5', 'b5', 'X']
]

b = [
        ['p', 'q3', 'p', 'b2', 'p', 'r4', 'k', 'q6'],
        ['k', 'p', 'r3', 'k', 'r1', 'p', 'b2', 'p'],
        ['r2', 'p', 'b2', 'r4', 'p', 'r1', 'q5', 'k'],
        ['b4', 'r3', 'p', 'q5', 'r3', 'b2', 'k', 'p'],
        ['q5', 'p', 'k', 'b4', 'q2', 'r2', 'p', 'b2'],
        ['b1', 'p', 'k', 'p', 'r1', 'q3', 'k', 'r5'],
        ['p', 'q1', 'r3', 'k', 'p', 'q4', 'p', 'k'],
        ['k', 'q3', 'p', 'b1', 'r2', 'r2', 'b5', 'X']
]


if __name__ == '__main__':
    cb = Chessboard(original)
    paths = cb.find_paths_from_start()
    print(paths)
    print(len(paths))
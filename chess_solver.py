from collections import deque


class Chessboard:
    def __init__(self, board):
        self.board = board


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
    

    def find_all_paths(self): #TODO
        start = (0, 0)
        end = (7, 7)

        queue = [[start]]
        paths = []
        visited = set()

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node == end:
                paths.append(path)
            else:
                for neighbor in self.neighbors(node):
                    if neighbor not in visited:
                        new_path = list(path)
                        new_path.append(neighbor)
                        queue.append(new_path)
                        visited.add(neighbor)

        return paths
    
    def find_paths_iterative(self): #TODO
        """Finds all paths from top-left (0, 0) to bottom-right (7, 7) using an iterative BFS approach."""
        start = (0, 0)
        end = (7, 7)
        
        # Queue to store the paths to explore
        queue = deque([([start], {start})])
        all_paths = []

        while queue:
            path, visited = queue.popleft()
            current = path[-1]
            
            if current == end:
                all_paths.append(path)
            else:
                for neighbor in self.neighbors(current):
                    if neighbor not in visited:  # Check if neighbor is visited
                        new_visited = visited.copy()
                        new_visited.add(neighbor)
                        new_path = path + [neighbor]
                        queue.append((new_path, new_visited))

        return all_paths
    


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
    cb = Chessboard(b)
    paths = cb.find_paths_iterative()
    print(paths)
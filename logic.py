import random
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont
# import numpy as np
from matplotlib import colormaps
from matplotlib.colors import Normalize


class Board:
    def __init__(self, m, n, max_distance=None):
        self.m = m
        self.n = n
        self.board = [[0 for _ in range(n)] for _ in range(m)]
        self.path = []
        if max_distance is None:
            self.max_distance = (m + n) // 2 - 2
        else:
            self.max_distance = max_distance

    def __str__(self):
        return "\n".join(" ".join(f'{cell: <5}' for cell in row) for row in self.board)

    def neighbors(self, square, distance, difficulty_bias=1):
        """
        List of neighbors of a square at an exact certain distance.
        """
        neighbors = []

        assert 0 < distance <= max(self.m, self.n), "Distance must be between 1 and the maximum of m and n"

        if random.random() < difficulty_bias:
            if 0 <= square[0] - distance < self.m: # Left
                neighbors.append((square[0] - distance, square[1]))
            if 0 <= square[1] - distance < self.n: # Up
                neighbors.append((square[0], square[1] - distance))

        if 0 <= square[0] + distance < self.m: # Right
                neighbors.append((square[0] + distance, square[1]))
        if 0 <= square[1] + distance < self.n: # Down
                neighbors.append((square[0], square[1] + distance))
        
        
        return neighbors
    
    def all_neighbors_and_distances(self, square, shuffled=True, difficulty_bias=1):
        """
        Returns a list of all neighbors of a square at all possible 
        distances. In the format- (distance:int, neighbor:tup)
        """

        possible_distances = range(1, self.max_distance + 1)
        possible_neighbors = []

        for distance in possible_distances:
            for neighbor in self.neighbors(square, distance, difficulty_bias=difficulty_bias):
                possible_neighbors.append(
                    (distance, neighbor)
                )

        if shuffled:
            random.shuffle(possible_neighbors)

        return possible_neighbors


    def create_random_path(self, difficulty_bias=0.25):
        self.path = [(0, 0)]
        distances = []

        current_square = (0, 0)
        bad_squares = [] # Squares that have no neighbors that are not in the path.
        affected_squares = [] # Squares that are reachable from the path.

        while current_square != (self.m - 1, self.n - 1):
            
            # Pick a random neighbor that is not in the path.
            possible_neighbors = self.all_neighbors_and_distances(current_square, difficulty_bias=difficulty_bias)
            for distance, neighbor in possible_neighbors:

                # Found next square if it is 
                # 1) A new square ie not in the path
                # 2) Not a bad square ie has neighbors that are not in the path
                # 3) Does not touch the path with a certain distance
                if neighbor not in self.path + bad_squares and all(neighbor not in as_ for as_ in affected_squares):
                    next_square = neighbor
                    next_to_distance = distance
                    bad_squares = []
                    break
            
            # If no new square is found, undo the last step in the path.
            else:
                if not distances:
                    return self.create_random_path(difficulty_bias=difficulty_bias) 

                bad_squares.append(current_square)
                current_square = self.path.pop()
                affected_squares.pop()
                distances.pop()
                continue

            self.path.append(next_square)
            affected_squares.append(self.neighbors(current_square, next_to_distance))
            distances.append(next_to_distance)
            current_square = next_square

        # Mark all the squares in the path
        for square, distance in zip(self.path, distances):
            self.board[square[0]][square[1]] = distance

        
    def fill_remaining_squares(self, show_duds=False):
        self.board[self.m - 1][self.n - 1] = 'X'

        dud_squares = []
        for i in range(self.m):
            for j in range(self.n):
                if self.board[i][j] == 0:
                    dud_squares.append((i, j))

        possible_distances = list(range(1, self.max_distance + 1))
        while dud_squares:
            random.shuffle(possible_distances)
            i, j = dud_squares.pop()
            
            for distance in possible_distances:
                if all(neighbor not in self.path for neighbor in self.neighbors((i, j), distance)):
                    self.board[i][j] = f'{distance}X' if show_duds else distance
                    break                    


    def all_possible_paths(self): #TODO
        """
        Returns all possible paths from the start to the end.
        """
        queue = [((0, 0), None)] # In the format (square, parent)
        seen = []

        while queue:
            current_square, parent = queue.pop(0)
            if current_square == (self.m - 1, self.n - 1):
                path = []
                while current_square:
                    path.append(current_square)
                    current_square = parent
                yield path[::-1]

            for neighbor in self.neighbors(current_square, self.board[current_square[0]][current_square[1]]):
                if neighbor not in seen:
                    queue.append((neighbor, current_square))
                    seen.append(neighbor)


    def number_to_color(self, number):
        if type(number) == str:
            number = -1
        
        norm = Normalize(vmin=-1, vmax=self.max_distance + 1)
        colormap = colormaps['PuBu']  # Try different colormaps here
        rgba = colormap(norm(number))
        return '#{:02x}{:02x}{:02x}'.format(int(rgba[0]*255), int(rgba[1]*255), int(rgba[2]*255))


    def create_board_image(self, filename="jumping_julia_board.png", show_path=False):
        cell_size = 100  # Size of each cell in pixels
        img_size = (self.n * cell_size, self.m * cell_size)
        
        img = Image.new('RGB', img_size, color='white')
        draw = ImageDraw.Draw(img)
        
        # font = ImageFont.load_default()  # Use default font
        font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", size=30)
        small_font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", size=20)
        
        for i in range(self.m):
            for j in range(self.n):
                
                number = self.board[i][j]
                color = self.number_to_color(number)
                
                top_left_corner = (j * cell_size, i * cell_size)
                bottom_right_corner = ((j + 1) * cell_size, (i + 1) * cell_size)
                draw.rectangle([top_left_corner, bottom_right_corner], fill=color)
                text_position = (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2)
                draw.text(text_position, str(number), fill="black", font=font, anchor="mm")

        if show_path:
            for index, (x, y) in enumerate(self.path):

                top_left_corner = (y * cell_size, x * cell_size)  # Note: (x, y) -> (row, column)
                bottom_right_corner = ((y + 1) * cell_size, (x + 1) * cell_size)
                draw.rectangle([top_left_corner, bottom_right_corner], outline="yellow", width=5)
        
                # Draw the sequential number in the top-right corner of each square
                number_position = (y * cell_size + cell_size - 25, x * cell_size + 15)
                draw.text(number_position, str(index + 1), fill="yellow", font=small_font, anchor="mm")
    
        
        # img.show()  # For preview
        img.save(filename)  # Save the image as a file


    def create_path_text_file(self, filename="jumping_julia_path.txt"):
        with open(filename, 'w') as f:
            for x in self.path:
                f.write(f'{x[0]} {x[1]}\n')


    def create_board_text_file(self, filename="jumping_julia_board.txt"):
        with open(filename, 'w') as f:
            for row in self.board:
                f.write(" ".join(str(x) for x in row) + '\n')




# print(b)

concerns = []

if __name__ == "__main__":

    # for index in range(1, 36):
    # for index in concerns:
    #     b = Board(4, 4, max_distance=3)
    #     b.create_random_path(difficulty_bias=0.15 + 0.1*(index/30))
    #     b.fill_remaining_squares(show_duds=False)
    #     b.create_board_text_file(filename=f"boards/4x4/jumping_julia_board_{index}.txt")
    #     b.create_path_text_file(filename=f"boards/4x4/jumping_julia_path_{index}.txt")
    #     b.create_board_image(filename=f"boards/4x4/jumping_julia_board_{index}.png")
    #     b.create_board_image(filename=f"boards/4x4/jumping_julia_solution_{index}.png", show_path=True)
    #     print(f'Board {index} created. (4x4)')

    # for index in range(1, 36):
    # for index in concerns:
    #     b = Board(6, 6)
    #     b.create_random_path(difficulty_bias=0.15 + 0.1*(index/30))
    #     b.fill_remaining_squares(show_duds=False)
    #     b.create_board_text_file(filename=f"boards/6x6/jumping_julia_board_{index}.txt")
    #     b.create_path_text_file(filename=f"boards/6x6/jumping_julia_path_{index}.txt")
    #     b.create_board_image(filename=f"boards/6x6/jumping_julia_board_{index}.png")
    #     b.create_board_image(filename=f"boards/6x6/jumping_julia_solution_{index}.png", show_path=True)
    #     print(f'Board {index} created. (6x6)')

    for index in range(1, 36):
        b = Board(8, 8)
        b.create_random_path(difficulty_bias=0.15 + 0.1*(index/30))
        b.fill_remaining_squares(show_duds=False)
        b.create_board_text_file(filename=f"boards/8x8/jumping_julia_board_{index}.txt")
        b.create_path_text_file(filename=f"boards/8x8/jumping_julia_path_{index}.txt")
        b.create_board_image(filename=f"boards/8x8/jumping_julia_board_{index}.png")
        b.create_board_image(filename=f"boards/8x8/jumping_julia_solution_{index}.png", show_path=True)
        print(f'Board {index} created. (8x8)')


import random
# import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont, ImageFilter
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
    
    @classmethod
    def from_file(cls, board_filename, path_filename=None):
        out = []
        with open(board_filename) as f:
            for line in f.readlines():
                out.append([int(x) if x.isdigit() else x for x in line.split()])

        new_board = cls(len(out), len(out[0]))
        new_board.board = out

        if path_filename is not None:
            out = []
            with open(path_filename) as f:
                for line in f.readlines():
                    out.append(tuple(map(int, line.split())))
            new_board.path = out

        return new_board

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
        # These will be updated when there is a permanant change in the path.
        # self.path[i] will have the number distances[i] in the grid. Meaning, distances[i] = self.path[i+1] - self.path[i]
        self.path = []
        distances = []

        current_square = (0, 0) # Working current square.

        bad_squares = [] # Squares that have no neighbors that are not in the path.
        affected_squares = [] # Squares that are reachable from the path.

        while current_square != (self.m - 1, self.n - 1):
            # Debugging print line
            # print(f'Path: {self.path}\nCurrent square: {current_square}\nBad squares: {bad_squares}\nAffected squares: {affected_squares}\nDistances: {distances}\n\n')
            
            # Pick a random neighbor that is not in the path.
            possible_neighbors = self.all_neighbors_and_distances(current_square, difficulty_bias=difficulty_bias)
            for distance, neighbor in possible_neighbors:

                # Found next square if it is 
                # 1) Not a bad square. That is, it has not been tried before.
                # 2) Not an affected square. That is, It is not reachable from an earlier point in the path.
                # 3) Not be the same distance as the goal but not be the goal. That is, must not create a shortcut.
                
                # For 1) and 2)
                if neighbor not in bad_squares and all(neighbor not in as_ for as_ in affected_squares):
                    
                    # For 3)
                    if neighbor != (self.m - 1, self.n - 1) and distance == (abs(current_square[0] - (self.m - 1)) + abs(current_square[1] - (self.n - 1))):
                        continue
                    
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

            self.path.append(current_square)
            affected_squares.append(self.neighbors(current_square, next_to_distance))
            distances.append(next_to_distance)
            current_square = next_square

        # Mark all the squares in the path
        self.path.append((self.m - 1, self.n - 1))
        for square, distance in zip(self.path, distances):
            self.board[square[0]][square[1]] = distance

        
    def fill_remaining_squares(self, show_duds=False, restart_for_zeros=False):
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
            else:
                if restart_for_zeros:
                    self.board = [[0 for _ in range(self.n)] for _ in range(self.m)]
                    self.create_random_path()
                    self.fill_remaining_squares(show_duds=show_duds, restart_for_zeros=restart_for_zeros)
                    return


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
            number = 0
        
        norm = Normalize(vmin=0, vmax=self.max_distance + 1)
        colormap = colormaps['Blues']  # Try different colormaps here
        rgba = colormap(norm(number))
        return '#{:02x}{:02x}{:02x}'.format(int(rgba[0]*255), int(rgba[1]*255), int(rgba[2]*255))


    @staticmethod
    def add_drop_shadow(image, offset=(5, 5), background_color=0xffffff, shadow_color=0x000000, border=10, iterations=5):
        total_width = image.width + abs(offset[0]) + 2 * border
        total_height = image.height + abs(offset[1]) + 2 * border
        shadow = Image.new(image.mode, (total_width, total_height), background_color)
        
        shadow_left = border + max(offset[0], 0)
        shadow_top = border + max(offset[1], 0)
        
        shadow.paste(shadow_color, [shadow_left, shadow_top, shadow_left + image.width, shadow_top + image.height])
        
        for _ in range(iterations):
            shadow = shadow.filter(ImageFilter.BLUR)
        
        img = Image.new(image.mode, (total_width, total_height), background_color)
        img.paste(shadow, (0, 0))
        img.paste(image, (border, border))
        
        return img


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
                x0, y0 = top_left_corner
                x1, y1 = bottom_right_corner
    
                # Determine if the cell is part of the path
                if show_path and (i, j) in self.path:
                    outline_color = "yellow"
                    outline_width = 5
                else:
                    outline_color = "black"
                    outline_width = 2

                # Draw the rounded rectangle with an outline for path cells
                draw.rounded_rectangle([x0, y0, x1, y1], radius=20, fill=color, outline=outline_color, width=outline_width)
                
                text_position = (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2)
                draw.text(text_position, str(number), fill="black", font=font, anchor="mm")

        if show_path:
            for index, (x, y) in enumerate(self.path):                
                # Draw the sequential number in the top-right corner of each square
                number_position = (y * cell_size + cell_size - 25, x * cell_size + 15)
                draw.text(number_position, str(index + 1), fill="yellow", font=small_font, anchor="mm")
    
        img = Board.add_drop_shadow(img, offset=(10, 10), shadow_color="black", border=20)
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

concerns = [16]

if __name__ == "__main__":


    # DEBUGGING BOARDS

    for seed in range(1, 31):
    # for seed in concerns:
        random.seed(42 + seed)
        b = Board(7, 7, max_distance=6)
        b.create_random_path(difficulty_bias=0.25)
        b.fill_remaining_squares(show_duds=False, restart_for_zeros=False)
        b.create_board_image(filename=f"debugging_boards/{seed}.png", show_path=True)
        # print(b)
        print(f'Board {seed} created.')



    # RECOLORING BOARDS

    # for board_index in range(1, 36):
    #     difficulty = 'hard'
    #     b = Board.from_file(
    #         board_filename=f"boards/{difficulty}/jumping_julia_board_{board_index}.txt", 
    #         path_filename=f"boards/{difficulty}/jumping_julia_path_{board_index}.txt"
    #     )
    #     b.create_board_image(filename=f"boards/{difficulty}/jumping_julia_board_{board_index}.png")
    #     b.create_board_image(filename=f"boards/{difficulty}/jumping_julia_solution_{board_index}.png", show_path=True)
    #     print(f'Board {board_index} created. ({difficulty})')


    
    # CREATING BOARDS

    # for board_index in range(1, 36):
    # for board_index in concerns:
    #     b = Board(8, 8)
    #     b.create_random_path(difficulty_bias=0.15 + 0.1*(board_index/30))
    #     b.fill_remaining_squares(show_duds=False, restart_for_zeros=True)
    #     b.create_board_text_file(filename=f"boards/hard/jumping_julia_board_{board_index}.txt")
    #     b.create_path_text_file(filename=f"boards/hard/jumping_julia_path_{board_index}.txt")
    #     b.create_board_image(filename=f"boards/hard/jumping_julia_board_{board_index}.png")
    #     b.create_board_image(filename=f"boards/hard/jumping_julia_solution_{board_index}.png", show_path=True)
    #     print(f'Board {board_index} created. (hard)')


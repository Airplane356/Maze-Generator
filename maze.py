import pygame
import random 
pygame.init()

CELL = 24
COLS = 20
ROWS = 20
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL

class Cell: 
    """
    Represents a cell and its four walls in the grid

    Attributes: 
        column (integer): column count of the cell
        row (integer): row count of the cell
        walls (dict): track status of cell walls
    """
    def __init__(self, column, row):
        """
        Initializes a cell object

        Args: 
            column (integer): column count of the cell
            row (integer): row count of the cell
        """
        self.column = column
        self.row = row
        self.walls = {"RIGHT": True,
                    "LEFT": True,
                    "TOP": True,
                    "BOTTOM": True}
        self.visited = False
    
    def x(self): 
        """
        x-coordinate of top-left corner of cell

        returns: top-left corner x-coord
        """
        return self.column * CELL
    
    def y(self):
        """
        y-coord of top-left corner of cell

        returns: top-left corner y-coord
        """
        return self.row * CELL
            
def draw_cell(screen, cell: Cell):  
    """
    draws each individual cell

    args: 
        screen (Surface): PyGame screen to draw cell on 
        cell (Cell): Cell object to draw
    """

    x = cell.x()
    y = cell.y()

    if cell.visited: 
        pygame.draw.rect(screen, "#5732D4", (x,y,24, 24))
    if cell.walls["TOP"] == True: 
        pygame.draw.line(screen, (25,25,25), (x, y), (x + CELL, y), 2) 
    if cell.walls["BOTTOM"] == True: 
        pygame.draw.line(screen, (25,25,25), (x, y + CELL), (x + CELL, y + CELL), 2) 
    if cell.walls["RIGHT"] == True: 
        pygame.draw.line(screen, (25,25,25), (x + CELL, y + CELL), (x + CELL, y), 2) 
    if cell.walls["LEFT"] == True: 
        pygame.draw.line(screen, (25,25,25), (x, y + CELL), (x, y), 2) 
    
def create_grid():
    """
    creates a 2d array of Cell objects

    returns: 2d arr of Cell objects in the form of [rows][cols]
    """
    return [[Cell(c, r) for c in range(COLS)] for r in range(ROWS)]

def draw_grid(screen, grid): 
    """
    draws all cells 

    args: 
        screen (Surface): PyGame Surface to draw on 
        grid (arr): grid of Cell objects to draw [rows][cols]
    """
    screen.fill((255, 255, 255))
    for r in range(ROWS): 
        for c in range(COLS): 
            draw_cell(screen, grid[r][c])

def get_neighbours(grid, r, c): 
    """
    gets unvisited neighbours

    args: 
        grid (arr): grid of Cell objects to draw [rows][cols]
        r (int): row count 
        c (int): column count
    """
    available_neighbours = []

    if r > 0 and grid[r-1][c].visited == False: 
        available_neighbours.append("TOP")
    if c < COLS-1 and grid[r][c+1].visited == False:
        available_neighbours.append("RIGHT")
    if r < ROWS-1 and grid[r+1][c].visited == False: 
        available_neighbours.append("BOTTOM")
    if c > 0 and grid[r][c-1].visited == False: 
        available_neighbours.append("LEFT")
    
    return available_neighbours

def break_wall(grid, r, c, stack, side):
    """
    breaks given wall of a given cell 

    args: 
        grid (arr): grid of Cell objects to draw [rows][cols]
        r (int): row count 
        c (int): column count
        stack (arr): list of visited cells
        side (string): side to break
    """
    if side == "TOP": 
        grid[r-1][c].walls["BOTTOM"] = False
        grid[r][c].walls["TOP"] = False
        grid[r-1][c].visited = True
        stack.insert(0, grid[r][c])   
        return [r-1, c]
    if side == "RIGHT": 
        grid[r][c+1].walls["LEFT"] = False
        grid[r][c].walls["RIGHT"] = False
        grid[r][c+1].visited = True
        stack.insert(0, grid[r][c])   
        return [r, c+1]
    if side == "BOTTOM":
        grid[r+1][c].walls["TOP"] = False
        grid[r][c].walls["BOTTOM"] = False
        grid[r+1][c].visited = True
        stack.insert(0, grid[r][c])   
        return [r+1, c]
    if side == "LEFT": 
        grid[r][c-1].walls["RIGHT"] = False
        grid[r][c].walls["LEFT"] = False
        grid[r][c-1].visited = True
        stack.insert(0, grid[r][c])   
        return [r, c-1]
    
def dfs_step(grid, current, stack): 
    """
    move into unvisited neighbour, otherwise backtrack if all neighbours have been visited

    args: 
        grid (arr): grid of Cell objects to draw [rows][cols]
        current (arr): current position [row][column] 
        stack (arr): list of visited cells
    """
    r = current[0]
    c = current[1]
    
    available_neighbours = get_neighbours(grid, r, c)
    
    if len(available_neighbours) != 0: 
        side = random.choice(available_neighbours)
        return break_wall(grid, r, c, stack, side)
    else: 
        for cell in stack: 
            if len(get_neighbours(grid, cell.row, cell.column)) != 0: 
                stack.pop(0)
                return [cell.row, cell.column] 

    return current

def main():
    """
    mainline logic
    """

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Generation")
    clock = pygame.time.Clock()

    running = True
    grid = create_grid()
    current = [0, 0]
    stack = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        current = dfs_step(grid, current, stack)
        draw_grid(screen, grid)
        
        pygame.display.flip()

        clock.tick(80)

    pygame.quit()

main()
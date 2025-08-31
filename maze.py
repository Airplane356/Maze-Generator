import pygame
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

    if cell.walls["TOP"] == True: 
        pygame.draw.line(screen, (25,25,25), (x, y), (x + CELL, y), 2) 
    if cell.walls["BOTTOM"] == True: 
        pygame.draw.line(screen, (25,25,25), (x, y + CELL), (x + CELL, y + CELL), 2) 
    if cell.walls["RIGHT"] == True: 
        pygame.draw.line(screen, (25,25,25), (x + CELL, y + CELL), (x + CELL, y), 2) 
    if cell.walls["TOP"] == True: 
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

def main():
    """
    mainline logic
    """

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Generation")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        draw_grid(screen, create_grid())
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

main()
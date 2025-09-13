import pygame
import sys
from collections import deque

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 900, 700
GRID_SIZE = 30
GRID_WIDTH = 22
GRID_HEIGHT = 23
SIDEBAR_WIDTH = 250

# Colors
BACKGROUND = (40, 44, 52)
GRID_LINES = (30, 34, 42)
SIDEBAR_BG = (50, 54, 62)
BUTTON_COLOR = (86, 182, 194)
BUTTON_HOVER = (102, 217, 232)
BUTTON_TEXT = (25, 29, 35)
TEXT_COLOR = (220, 220, 220)
START_COLOR = (92, 184, 92)
END_COLOR = (217, 83, 79)
WALL_COLOR = (60, 64, 72)
VISITED_COLOR = (66, 135, 245)
PATH_COLOR = (255, 221, 89)
GRID_BG = (45, 49, 57)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BFS Visualization")

# Font
font = pygame.font.SysFont("Arial", 18)
title_font = pygame.font.SysFont("Arial", 24, bold=True)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = BUTTON_COLOR
        self.hover_color = BUTTON_HOVER
        self.text_color = BUTTON_TEXT
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (70, 74, 82), self.rect, 2, border_radius=5)
        
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def check_click(self, pos):
        return self.rect.collidepoint(pos)

class Grid:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.cells = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.start = (5, 5)
        self.end = (19, 12)
        self.cells[self.start[1]][self.start[0]] = 1  
        self.cells[self.end[1]][self.end[0]] = 2      
        self.walls = set()
        self.visited = set()
        self.path = []
        self.bfs_completed = False
        
    def toggle_wall(self, x, y):
        if (x, y) == self.start or (x, y) == self.end:
            return
            
        if self.cells[y][x] == 3:
            self.cells[y][x] = 0
            if (x, y) in self.walls:
                self.walls.remove((x, y))
        else:
            self.cells[y][x] = 3
            self.walls.add((x, y))
            
    def move_point(self, x, y, point_type):
        # point_type: 1 for start, 2 for end
        old_x, old_y = self.start if point_type == 1 else self.end
        self.cells[old_y][old_x] = 0
        
        if point_type == 1:
            self.start = (x, y)
        else:
            self.end = (x, y)
            
        self.cells[y][x] = point_type
        
    def bfs(self):
        if not self.start or not self.end:
            return
            
        self.visited = set()
        self.path = []
        self.bfs_completed = False
        
        queue = deque([(self.start, [])])
        visited = set([self.start])
        
        while queue:
            # Check for events to keep the window responsive
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            current, path = queue.popleft()
            
            if current == self.end:
                self.path = path + [current]
                self.bfs_completed = True
                return
                
            x, y = current
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                    if (nx, ny) not in visited and self.cells[ny][nx] != 3:
                        visited.add((nx, ny))
                        queue.append(((nx, ny), path + [current]))
                        
                        # Add to visited for visualization
                        if (nx, ny) != self.end:
                            self.visited.add((nx, ny))
                        
                        # Draw the current state
                        self.draw(screen)
                        pygame.display.flip()
                        pygame.time.delay(50)
        
        self.bfs_completed = True
        
    def draw(self, surface):
        # Draw grid background
        grid_rect = pygame.Rect(0, 0, GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE)
        pygame.draw.rect(surface, GRID_BG, grid_rect)
        
        # Draw grid lines
        for x in range(0, GRID_WIDTH * GRID_SIZE, GRID_SIZE):
            pygame.draw.line(surface, GRID_LINES, (x, 0), (x, GRID_HEIGHT * GRID_SIZE))
        for y in range(0, GRID_HEIGHT * GRID_SIZE, GRID_SIZE):
            pygame.draw.line(surface, GRID_LINES, (0, y), (GRID_WIDTH * GRID_SIZE, y))
            
        # Draw visited cells
        for x, y in self.visited:
            if (x, y) != self.start and (x, y) != self.end:
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(surface, VISITED_COLOR, rect)
                
        # Draw path
        for x, y in self.path:
            if (x, y) != self.start and (x, y) != self.end:
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(surface, PATH_COLOR, rect)
                
        # Draw walls
        for x, y in self.walls:
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, WALL_COLOR, rect)
            
        # Draw start and end points
        start_rect = pygame.Rect(self.start[0] * GRID_SIZE, self.start[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        end_rect = pygame.Rect(self.end[0] * GRID_SIZE, self.end[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, START_COLOR, start_rect)
        pygame.draw.rect(surface, END_COLOR, end_rect)
        
        # Add labels to start and end
        start_text = font.render("S", True, (255, 255, 255))
        end_text = font.render("E", True, (255, 255, 255))
        screen.blit(start_text, (self.start[0] * GRID_SIZE + 10, self.start[1] * GRID_SIZE + 7))
        screen.blit(end_text, (self.end[0] * GRID_SIZE + 10, self.end[1] * GRID_SIZE + 7))

# Create grid and buttons
grid = Grid()
start_button = Button(WIDTH - SIDEBAR_WIDTH + 20, 100, SIDEBAR_WIDTH - 40, 40, "Start BFS")
reset_button = Button(WIDTH - SIDEBAR_WIDTH + 20, 160, SIDEBAR_WIDTH - 40, 40, "Reset Grid")
clear_walls_button = Button(WIDTH - SIDEBAR_WIDTH + 20, 220, SIDEBAR_WIDTH - 40, 40, "Clear Walls")

buttons = [start_button, reset_button, clear_walls_button]

# Main game loop
clock = pygame.time.Clock()
dragging = None

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if click is in grid area
            if mouse_pos[0] < GRID_WIDTH * GRID_SIZE and mouse_pos[1] < GRID_HEIGHT * GRID_SIZE:
                grid_x, grid_y = mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE
                
                # Check if clicking on start or end point
                if (grid_x, grid_y) == grid.start:
                    dragging = "start"
                elif (grid_x, grid_y) == grid.end:
                    dragging = "end"
                else:
                    grid.toggle_wall(grid_x, grid_y)
            
            # Check button clicks
            for button in buttons:
                if button.check_click(mouse_pos):
                    if button == start_button:
                        grid.bfs()
                    elif button == reset_button:
                        grid.reset()
                    elif button == clear_walls_button:
                        grid.walls.clear()
                        for y in range(GRID_HEIGHT):
                            for x in range(GRID_WIDTH):
                                if grid.cells[y][x] == 3:
                                    grid.cells[y][x] = 0
        
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = None
            
        if event.type == pygame.MOUSEMOTION and dragging:
            if mouse_pos[0] < GRID_WIDTH * GRID_SIZE and mouse_pos[1] < GRID_HEIGHT * GRID_SIZE:
                grid_x, grid_y = mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE
                if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                    if grid.cells[grid_y][grid_x] != 3:  # Don't move to wall
                        if dragging == "start":
                            grid.move_point(grid_x, grid_y, 1)
                        elif dragging == "end":
                            grid.move_point(grid_x, grid_y, 2)
    
    # Update button hover states
    for button in buttons:
        button.check_hover(mouse_pos)
    
    # Draw everything
    screen.fill(BACKGROUND)
    
    # Draw sidebar
    sidebar_rect = pygame.Rect(WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT)
    pygame.draw.rect(screen, SIDEBAR_BG, sidebar_rect)
    
    # Draw title
    title_text = title_font.render("BFS Pathfinding", True, TEXT_COLOR)
    screen.blit(title_text, (WIDTH - SIDEBAR_WIDTH + 20, 30))
    
    # Draw instructions
    instructions = [
        "INSTRUCTIONS:",
        "- Click to place walls",
        "- Again click on that wall to remove",
        "- Drag start (S) or end (E) points",
        "- Click Start BFS to visualize",
        "- Click Reset to clear everything"
    ]
    
    for i, line in enumerate(instructions):
        text = font.render(line, True, TEXT_COLOR)
        screen.blit(text, (WIDTH - SIDEBAR_WIDTH + 20, 300 + i * 30))
    
    # Draw legend
    legend_title = font.render("LEGEND:", True, TEXT_COLOR)
    screen.blit(legend_title, (WIDTH - SIDEBAR_WIDTH + 20, 480))
    
    legend_items = [
        (START_COLOR, "Start point"),
        (END_COLOR, "End point"),
        (WALL_COLOR, "Wall/Obstacle"),
        (VISITED_COLOR, "Visited nodes"),
        (PATH_COLOR, "Path")
    ]
    
    for i, (color, text) in enumerate(legend_items):
        pygame.draw.rect(screen, color, (WIDTH - SIDEBAR_WIDTH + 20, 510 + i * 30, 20, 20))
        text_surf = font.render(text, True, TEXT_COLOR)
        screen.blit(text_surf, (WIDTH - SIDEBAR_WIDTH + 50, 510 + i * 30))
    
    # Draw buttons
    for button in buttons:
        button.draw(screen)
    
    # Draw grid
    grid.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
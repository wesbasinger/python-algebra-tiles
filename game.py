#!/usr/bin/env python3
 
#
# pygame (simple) template - by furas
#
# https://github.com/furas/my-python-codes/tree/master/pygame/__template__/
#
 
# ---------------------------------------------------------------------
 
__author__  = 'Bartlomiej "furas" Burek'
__webpage__ = 'http://blog.furas.pl'
 
# ---------------------------------------------------------------------
 
import pygame
 
# === CONSTANS === (UPPER_CASE names)
 
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
 
BLOCK_SIZE = 25

# Set the boundaries for the rectangles
BOUNDARY_LEFT = 25
BOUNDARY_RIGHT = 800
BOUNDARY_TOP = 25
BOUNDARY_BOTTOM = 600
 
# === CLASSES === (CamelCase names)
 
class GuidedRect(pygame.Rect):

    def __init__(self, left, top, width, height, target_coords):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

        self.target_coords = target_coords

    def move(self, x, y):

        if abs(x - self.target_coords[0]) < 10 and abs(y - self.target_coords[1]) < 10:

            self.left = self.target_coords[0]
            self.top = self.target_coords[1]

        else:

            self.left = x
            self.top = y

# === FUNCTIONS === (lower_case names)
 
    # empty
   
# === MAIN === (lower_case names)
 
# --- (global) variables ---
 
# --- init ---
 
pygame.init()
 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()
 
# --- objects ---
 
'''
button = Button(...)
'''

perimeter_rects = [
    pygame.Rect(0,BLOCK_SIZE,BLOCK_SIZE, BLOCK_SIZE*5),
    pygame.Rect(BLOCK_SIZE,0, BLOCK_SIZE*5, BLOCK_SIZE),
    pygame.Rect(BLOCK_SIZE*6, 0, BLOCK_SIZE, BLOCK_SIZE),
    pygame.Rect(0, BLOCK_SIZE*6, BLOCK_SIZE, BLOCK_SIZE)
]

solution_rects = [
    GuidedRect(100, 100, BLOCK_SIZE*5, BLOCK_SIZE*5, (BLOCK_SIZE, BLOCK_SIZE)), # X2
    GuidedRect(200,200,BLOCK_SIZE*5, BLOCK_SIZE, (BLOCK_SIZE, BLOCK_SIZE*6)), # x_horiz
    GuidedRect(300, 300, BLOCK_SIZE, BLOCK_SIZE*5, (BLOCK_SIZE*6, BLOCK_SIZE)), #x_vert
    GuidedRect(400, 400, BLOCK_SIZE, BLOCK_SIZE, (BLOCK_SIZE*6, BLOCK_SIZE*6))
]


 
dragging = False
   
# --- mainloop ---
 
clock = pygame.time.Clock()
is_running = True
active_rect = None
 
while is_running:
 
    # --- events ---
   
    for event in pygame.event.get():
 
        # --- global events ---
       
        if event.type == pygame.QUIT:
            is_running = False
 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
 
        elif event.type == pygame.MOUSEBUTTONDOWN:

            for main_rect in solution_rects:
                if main_rect.collidepoint(event.pos):
                    dragging = True
                    active_rect = main_rect
                    selected_offset_x = main_rect.x - event.pos[0]
                    selected_offset_y = main_rect.y - event.pos[1]
               
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
               
        elif event.type == pygame.MOUSEMOTION:
            if dragging: # selected can be `0` so `is not None` is required
                # move object

                active_rect.move(event.pos[0] + selected_offset_x, event.pos[1] + selected_offset_y)
               
        # --- objects events ---
 
        '''
       button.handle_event(event)
       '''
       
    # --- updates ---
 
        # empty
       
    # --- draws ---
   
    screen.fill('Black')
 
    '''
    button.draw(screen)    
    '''

    colors = ['Yellow', 'Orange', 'Blue', 'Gray']

    color_iter = 0
   
    # draw rect
    for r in perimeter_rects:
        pygame.draw.rect(screen, 'Red', r, 1)

    for r in solution_rects:
        pygame.draw.rect(screen, colors[color_iter], r)
        color_iter += 1
       
    pygame.display.update()
 
    # --- FPS ---
 
    clock.tick(25)
 
# --- the end ---
   
pygame.quit()
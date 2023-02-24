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
from random import randint
from time import sleep
import os
 
# === CONSTANS === (UPPER_CASE names)
 
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
 
BLOCK_SIZE = 25

ORIGIN = (0,0)

# Set the spawn boundaries
BOUNDARY_LEFT = 25
BOUNDARY_RIGHT = 800
BOUNDARY_TOP = 25
BOUNDARY_BOTTOM = 600

# === CLASSES === (CamelCase names)

class BinomialPair():

    def __init__(self, a,c,b,d):

        self.a = a
        self.c = c
        self.b = b
        self.d = d

        self.bounding_horizontal_rects = []

        self.bounding_vertical_rects = []

        self.solution_rects = []

        self.all_snap_points = []

        self.solved = False
        
        self._generate_bounding_rects()

        self._generate_solutions_rects()

        for solution_rect in self.solution_rects:

            solution_rect.set_snap_points(solution_rect.tag, self.all_snap_points)

    def is_solved(self):

        for rect in solution_rects:

            if not rect.locked:

                return False

        return True

    def _generate_bounding_rects(self):

        #generate horizontal rects

        curr_x = BLOCK_SIZE

        for i in range(self.a):

            self.bounding_horizontal_rects.append(pygame.Rect(curr_x, ORIGIN[1], BLOCK_SIZE*5,BLOCK_SIZE))

            curr_x += BLOCK_SIZE*5

        for i in range(self.c):

            self.bounding_horizontal_rects.append(pygame.Rect(curr_x, ORIGIN[1], BLOCK_SIZE, BLOCK_SIZE))

            curr_x += BLOCK_SIZE

        #generate vertical rects

        curr_y = BLOCK_SIZE

        for i in range(self.b):

            self.bounding_vertical_rects.append(pygame.Rect(ORIGIN[0], curr_y, BLOCK_SIZE, BLOCK_SIZE*5))

            curr_y += BLOCK_SIZE*5

        for i in range(self.d):

            self.bounding_vertical_rects.append(pygame.Rect(ORIGIN[0], curr_y, BLOCK_SIZE, BLOCK_SIZE))
            
            curr_y += BLOCK_SIZE

    def _generate_solutions_rects(self):

        # target x coord comes from horizonal bounding origin
        # target y coord comes from vertical bounding origin
        # width is from the horizontal bounding rect
        # height is from the vertical bounding rect

        for horizontal_rect in self.bounding_horizontal_rects:

            for vertical_rect in self.bounding_vertical_rects:

                if horizontal_rect.width == BLOCK_SIZE*5 and vertical_rect.height == BLOCK_SIZE*5:

                    self.solution_rects.append(FiveByFive())

                    self.all_snap_points.append(('5x5', horizontal_rect.left, vertical_rect.top))

                elif horizontal_rect.width == BLOCK_SIZE*5 and vertical_rect.height == BLOCK_SIZE:

                    self.solution_rects.append(FiveByOne())

                    self.all_snap_points.append(('5x1', horizontal_rect.left, vertical_rect.top))

                elif horizontal_rect.width == BLOCK_SIZE and vertical_rect.height == BLOCK_SIZE*5:

                    self.solution_rects.append(OneByFive())

                    self.all_snap_points.append(('1x5', horizontal_rect.left, vertical_rect.top))

                else:

                    self.solution_rects.append(OneByOne())

                    self.all_snap_points.append(('1x1', horizontal_rect.left, vertical_rect.top))

class Tile(pygame.Rect):

    def __init__(self):

        spawn_point = self._generate_spawn_point()

        self.left = spawn_point[0]
        self.top = spawn_point[1]

        self.snap_points = []

        self.locked = False

        self.final_coords = None

    def move(self, x, y):

        for snap_point in self.snap_points:

            if abs(x - snap_point[1]) < 10 and abs(y - snap_point[2]) < 10:

                self.final_coords = (snap_point[1], snap_point[2])

                self.x = self.final_coords[0]
                self.y = self.final_coords[1]

                self.locked = True
        else:

            self.left = x
            self.top = y

    def kill_snap_point(self, snap_point):

        if snap_point in self.snap_points:

            self.snap_points.remove(snap_point)

    def _generate_spawn_point(self):

        return (randint(BOUNDARY_LEFT,BOUNDARY_RIGHT), randint(BOUNDARY_TOP, BOUNDARY_BOTTOM))

    def set_snap_points(self, tag, all_snap_points):

        for result in filter(lambda snap_point : snap_point[0] == tag, all_snap_points):

            self.snap_points.append(result)

class FiveByFive(Tile):

    def __init__(self):

        super().__init__()

        self.width = BLOCK_SIZE*5
        self.height = BLOCK_SIZE*5
        self.tag = "5x5"

class FiveByOne(Tile):

    def __init__(self):

        super().__init__()

        self.width = BLOCK_SIZE*5
        self.height = BLOCK_SIZE
        self.tag = "5x1"

class OneByFive(Tile):

    def __init__(self):

        super().__init__()

        self.width = BLOCK_SIZE
        self.height = BLOCK_SIZE*5
        self.tag = "1x5"

class OneByOne(Tile):

    def __init__(self):

        super().__init__()

        self.width = BLOCK_SIZE
        self.height = BLOCK_SIZE
        self.tag = "1x1"



# === FUNCTIONS === (lower_case names)
 
    # empty
   
# === MAIN === (lower_case names)
 
# --- (global) variables ---
 
# --- init ---
 
pygame.init()
 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()

score = 0
 
# --- objects ---

five_by_five_img = pygame.image.load(os.path.join('graphics', '5x5.png'))

one_by_one_img = pygame.image.load(os.path.join('graphics', '1x1.png'))

five_by_one_img = pygame.image.load(os.path.join('graphics', '5x1.png'))

one_by_five_img = pygame.image.load(os.path.join('graphics', '1x5.png'))

binomial_pair = BinomialPair(1,1,1,1)

horizontal_rects = binomial_pair.bounding_horizontal_rects
vertical_rects = binomial_pair.bounding_vertical_rects

perimeter_rects = horizontal_rects + vertical_rects

solution_rects = binomial_pair.solution_rects
 
dragging = False
   
# --- mainloop ---
 
clock = pygame.time.Clock()
is_running = True
active_rect = None
 
while is_running:

    # create a font object.
    # 1st parameter is the font file
    # which is present in pygame.
    # 2nd parameter is size of the font
    font = pygame.font.Font('freesansbold.ttf', 32)
    
    # create a text surface object,
    # on which text is drawn on it.
    text = font.render('Score:' + str(score), True, 'Green', 'Blue')
    
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
    
    # set the center of the rectangular object.
    textRect.center = (700, 50)

    if binomial_pair.is_solved():

        score += 1

        dragging = False

        binomial_pair = BinomialPair(randint(1,2), randint(1,3), randint(1,1), randint(1,2))

        horizontal_rects = binomial_pair.bounding_horizontal_rects
        vertical_rects = binomial_pair.bounding_vertical_rects

        perimeter_rects = horizontal_rects + vertical_rects

        solution_rects = binomial_pair.solution_rects
 
 
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
                if not active_rect.locked:
                    active_rect.move(event.pos[0] + selected_offset_x, event.pos[1] + selected_offset_y)
                else:
                    active_rect.move(active_rect.final_coords[0], active_rect.final_coords[1])
                    for rect in solution_rects:

                        rect.kill_snap_point((active_rect.tag, active_rect.final_coords[0], active_rect.final_coords[1]))

               
        # --- objects events ---
 
        '''
       '''
       
    # --- updates ---
 
        # empty
       
    # --- draws ---
   
    screen.fill('Black')

    screen.blit(text, textRect)
 
    '''
    button.draw(screen)    
    '''
   
    # draw rect
    for r in perimeter_rects:
        pygame.draw.rect(screen, 'Red', r, 1)

    for r in solution_rects:
        if r.tag == "5x5":
            screen.blit(five_by_five_img, (r.left, r.top))
        elif r.tag == "1x1":
            screen.blit(one_by_one_img, (r.left, r.top))
        elif r.tag == "1x5":
            screen.blit(one_by_five_img, (r.left, r.top))
        elif r.tag == "5x1":
            screen.blit(five_by_one_img, (r.left, r.top))
       
    pygame.display.update()
 
    # --- FPS ---
 
    clock.tick(25)
 
# --- the end ---
   
pygame.quit()
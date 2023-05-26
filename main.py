import pygame
import random

board = []
num_bombs = 0
num_marked_correctly = 0
first_click_made = False



class Cube(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.location = (y // 20) * 20 + (x // 20)
        self.number = 0
        self.bomb_tile = False
        self.clicked = False
        self.marked = False
        self.starter_cube = False

    def draw(self, surface, color, num=None):
        # Draw outer rectangle as the border
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, 20, 20))

        # Draw inner rectangle as the cube
        pygame.draw.rect(surface, color, (self.x + 1, self.y + 1, 18, 18))

        if num is not None:
            font = pygame.font.SysFont(None, 24)
            text_surface = font.render(str(num), True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.x + 10, self.y + 10))
            surface.blit(text_surface, text_rect)

    def mark(self, surface):
        global num_marked_correctly
        if self.get_starter():
            self.marked = True
            pygame.draw.circle(surface, (255, 0, 0), (self.x + 10, self.y + 10), 4)
            if self.is_bomb():
                num_marked_correctly += 1

    def unmark(self, surface):
        global num_marked_correctly
        self.marked = False
        pygame.draw.circle(surface, (144, 238, 144), (self.x + 10, self.y + 10), 4)
        if self.is_bomb():
            num_marked_correctly -= 1

    


    def bombs_adjacent(self):
        direction = [1, -1, 20, -20, 19, -19, 21, -21]
        self.number = 0  # Reset the number of adjacent bombs
        for i in direction:
            adjacent_location = int(self.location) + i

            # Ignore adjacent cubes on the next row if the current cube is on the left edge
            if self.location % 20 == 0 and i in [-21, -1, 19]:
                continue

            # Ignore adjacent cubes on the next row if the current cube is on the right edge
            if (self.location + 1) % 20 == 0 and i in [-19, 1, 21]:
                continue

            if 0 <= adjacent_location < len(board) and board[adjacent_location].is_bomb():
                self.number += 1
        return self.number


    def create_bomb(self):
        self.bomb_tile = True

    def is_bomb(self):
        return self.bomb_tile

    def is_clicked(self):
        return self.clicked

    def set_clicked(self, clicked):
        self.clicked = clicked

    def set_starter(self, param):
        self.starter_cube = param

    def get_starter(self):
        return self.starter_cube
    
    def get_marked(self):
        return self.marked


def handle_click(cube):
    direction = [1, -1, 20, -20, 19, -19, 21, -21]

    if not cube.is_clicked():
        cube.set_clicked(True)
        if cube.is_bomb():
            print("You clicked on a bomb!")
        else:
            if cube.bombs_adjacent() == 0:
                for i in direction:
                    adjacent_location = cube.location + i
                    if 0 <= adjacent_location < len(board):
                        adjacent_cube = board[adjacent_location]
                        if not adjacent_cube.is_clicked():
                            handle_click(adjacent_cube)
                cube.draw(screen, (255, 198, 153))  # Update color of the clicked and revealed cube
                cube.set_starter(False)
            else:
                cube.draw(screen, (255, 198, 153), cube.bombs_adjacent())  # Update color and display number of adjacent bombs
                cube.set_starter(False)



pygame.init()
screen = pygame.display.set_mode((400, 400))
done = False

for y in range(0, 400, 20):
    for x in range(0, 400, 20):
        cube = Cube(x, y)
        cube.set_starter(True)
        rand_num = random.randrange(1, 10)
        if rand_num > 8:
            cube.create_bomb()
            num_bombs += 1
        board.append(cube)

for cube in board:
    bombs = cube.bombs_adjacent()
    if cube.get_starter():
        cube.draw(screen, (144, 238, 144))

print(num_bombs)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not first_click_made:  # Left mouse button and first click
                mouse_pos = pygame.mouse.get_pos()
                for cube in board:
                    if cube.x <= mouse_pos[0] <= cube.x + 20 and cube.y <= mouse_pos[1] <= cube.y + 20:
                        if cube.is_bomb() or cube.bombs_adjacent() != 0:  # If the first click is a bomb or adjacent to a bomb
                            # Regenerate the board
                            board = []  # Clear the existing board
                            num_bombs = 0  # Reset the number of bombs
                            num_marked_correctly = 0  # Reset the number of marked bombs
                            for y in range(0, 400, 20):  # Recreate the board
                                for x in range(0, 400, 20):
                                    new_cube = Cube(x, y)
                                    new_cube.set_starter(True)
                                    rand_num = random.randrange(1, 10)
                                    if rand_num > 8:
                                        new_cube.create_bomb()
                                        num_bombs += 1
                                    board.append(new_cube)
                            # Reset the first click flag
                            first_click_made = False
                            # Exit the loop to prevent further processing of the click event
                            break
                        else:
                            handle_click(cube)
                            first_click_made = True
                            break
            elif event.button == 1:  # Left mouse button (after the first click)
                mouse_pos = pygame.mouse.get_pos()
                for cube in board:
                    if cube.x <= mouse_pos[0] <= cube.x + 20 and cube.y <= mouse_pos[1] <= cube.y + 20:
                        handle_click(cube)
            if event.button == 3:  # Right mouse button
                mouse_pos = pygame.mouse.get_pos()
                for cube in board:
                    if cube.x <= mouse_pos[0] <= cube.x + 20 and cube.y <= mouse_pos[1] <= cube.y + 20:
                        if cube.marked:
                            cube.unmark(screen)
                        else:
                            cube.mark(screen)

    if num_bombs == num_marked_correctly:
        font = pygame.font.SysFont(None, 48)
        text = font.render("You Win!", True, (255, 255, 255))
        # Fill the screen with black color
        screen.fill((0, 0, 0))

        # Blit the text to the center of the screen
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)

        # Update the display
        pygame.display.update()

    pygame.display.flip()


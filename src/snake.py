import pygame
import random
from enum import Enum
from collections import namedtuple


# initialize pygame
pygame.init()
font = pygame.font.Font('F:\\Snake-Game\\assets\\KnightWarrior.otf', 20)


# direction
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# rgb color
WHITE = (232, 249, 253)
BLACK = (25, 40, 47)
RED = (179, 48, 48)
GREEN1 = (66, 133, 91)
GREEN2 = (161, 181, 125)

# object
BLOCK_SIZE = 20
SPEED = 10

# difficulty


# reset
# reward
# play(action) --> direction
# game_iteration
# is_collision
class SnakeGame:

    def __init__(self, width=800, height=600):
        # init display
        self.w = width
        self.h = height
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')

        # init game state
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT

        self.head = Point(self.w // 2, self.h // 2)
        self.snake = [self.head,
                      Point(self.head[0] - BLOCK_SIZE, self.head[1]),
                      Point(self.head[0] - 2 * BLOCK_SIZE, self.head[1])]
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        food_x = random.randint(0, (self.w - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        food_y = random.randint(0, (self.h - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(food_x, food_y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # 2. move
        self._move(self.direction)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, GREEN2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)


if __name__ == '__main__':
    game = SnakeGame()

    # game loop
    while True:
        _game_over, score = game.play_step()

        if _game_over:
            break

    print('Final Score', score)

    pygame.quit()

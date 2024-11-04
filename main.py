import pygame
import time
import random

# 初始化 pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 游戏窗口的宽度和高度
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 10

# 创建游戏窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('贪吃蛇')

# 时钟
clock = pygame.time.Clock()

# 蛇类
class Snake:
    def __init__(self):
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = 'RIGHT'
        self.grow = False

    def move(self):
        head = self.body[0].copy()
        if self.direction == 'UP':
            head[1] -= BLOCK_SIZE
        elif self.direction == 'DOWN':
            head[1] += BLOCK_SIZE
        elif self.direction == 'LEFT':
            head[0] -= BLOCK_SIZE
        elif self.direction == 'RIGHT':
            head[0] += BLOCK_SIZE

        self.body.insert(0, head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_direction):
        # 防止反向移动
        opposites = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_direction != opposites[self.direction]:
            self.direction = new_direction

    def grow_snake(self):
        self.grow = True

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

# 食物类
class Food:
    def __init__(self):
        self.position = [random.randrange(1, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                         random.randrange(1, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]

    def spawn_food(self):
        self.position = [random.randrange(1, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                         random.randrange(1, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]

    def draw(self):
        pygame.draw.rect(screen, RED, pygame.Rect(self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

# 游戏主循环
def game_loop():
    snake = Snake()
    food = Food()
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction('UP')
                elif event.key == pygame.K_DOWN:
                    snake.change_direction('DOWN')
                elif event.key == pygame.K_LEFT:
                    snake.change_direction('LEFT')
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction('RIGHT')

        snake.move()

        # 检查食物是否被吃掉
        if snake.body[0] == food.position:
            snake.grow_snake()
            food.spawn_food()
            score += 1

        # 检查边界和自身碰撞
        if (snake.body[0][0] < 0 or snake.body[0][0] >= WIDTH or
                snake.body[0][1] < 0 or snake.body[0][1] >= HEIGHT or
                snake.body[0] in snake.body[1:]):
            running = False

        # 清屏并绘制
        screen.fill(BLACK)
        snake.draw()
        food.draw()

        pygame.display.flip()
        clock.tick(15)

    pygame.quit()
    print(f'游戏结束！你的得分是: {score}')

if __name__ == "__main__":
    game_loop()
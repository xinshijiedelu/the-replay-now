import pygame
import random

# 游戏窗口设置
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLS, ROWS = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE

# 颜色定义
COLORS = [
    (0, 0, 0),  # 背景
    (255, 0, 0),  # 红色
    (0, 255, 0),  # 绿色
    (0, 0, 255),  # 蓝色
    (255, 255, 0),  # 黄色
    (255, 165, 0),  # 橙色
    (128, 0, 128),  # 紫色
    (0, 255, 255)  # 青色
]

# 俄罗斯方块形状
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
]


class Tetris:
    def __init__(self):
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.current_shape = None
        self.current_position = [0, 0]
        self.spawn_shape()

    def spawn_shape(self):
        self.current_shape = random.choice(SHAPES)
        self.current_position = [0, COLS // 2 - len(self.current_shape[0]) // 2]

    def rotate_shape(self):
        self.current_shape = [list(row) for row in zip(*self.current_shape[::-1])]

    def valid_move(self, offset):
        for r, row in enumerate(self.current_shape):
            for c, cell in enumerate(row):
                if cell:
                    new_r = self.current_position[0] + r + offset[0]
                    new_c = self.current_position[1] + c + offset[1]
                    if (new_r < 0 or new_r >= ROWS or
                            new_c < 0 or new_c >= COLS or
                            self.board[new_r][new_c]):
                        return False
        return True

    def freeze_shape(self):
        for r, row in enumerate(self.current_shape):
            for c, cell in enumerate(row):
                if cell:
                    self.board[self.current_position[0] + r][self.current_position[1] + c] = 1
        self.clear_lines()
        self.spawn_shape()
        if not self.valid_move((0, 0)):
            raise Exception("Game Over")

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = ROWS - len(new_board)
        self.board = [[0] * COLS for _ in range(lines_cleared)] + new_board

    def move(self, direction):
        if self.valid_move(direction):
            self.current_position[0] += direction[0]
            self.current_position[1] += direction[1]

    def drop(self):
        if self.valid_move((1, 0)):
            self.current_position[0] += 1
        else:
            self.freeze_shape()


def draw_board(screen, board):
    for r in range(ROWS):
        for c in range(COLS):
            color = COLORS[board[r][c]]
            pygame.draw.rect(screen, color, (c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, (200, 200, 200), (c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Tetris()
    running = True

    while running:
        screen.fill(COLORS[0])
        draw_board(screen, game.board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move((0, -1))
                elif event.key == pygame.K_RIGHT:
                    game.move((0, 1))
                elif event.key == pygame.K_DOWN:
                    game.drop()
                elif event.key == pygame.K_UP:
                    game.rotate_shape()

        game.drop()
        pygame.display.flip()
        clock.tick(5)

    pygame.quit()


if __name__ == "__main__":
    main()
import pygame
import random

pygame.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Colorful Pong")

FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_PURPLE = (48, 25, 52)
BALL_COLOR = (255, 255, 0)
PADDLE_LEFT_COLOR = (0, 255, 255)
PADDLE_RIGHT_COLOR = (255, 0, 255)
MIDLINE_COLOR = (200, 200, 255)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont("comicsans", 50, bold=True)
MENU_FONT = pygame.font.SysFont("comicsans", 40, bold=True)
WINNING_SCORE = 10


class Paddle:
    VEL = 6

    def __init__(self, x, y, width, height, color):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), border_radius=10)

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    MAX_VEL = 5

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL * random.choice((-1, 1))
        self.y_vel = 0
        self.color = BALL_COLOR

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel = self.MAX_VEL * random.choice((-1, 1))


def draw_background(win):
    win.fill(DARK_PURPLE)
    for i in range(10, HEIGHT, 30):
        pygame.draw.rect(win, MIDLINE_COLOR, (WIDTH // 2 - 2, i, 4, 15), border_radius=2)


def draw(win, paddles, ball, left_score, right_score):
    draw_background(win)

    left_score_text = SCORE_FONT.render(f"{left_score}", True, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", True, WHITE)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))

    for paddle in paddles:
        paddle.draw(win)

    ball.draw(win)
    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                middle_y = left_paddle.y + left_paddle.height / 2
                diff_y = middle_y - ball.y
                ball.y_vel = -diff_y / ((left_paddle.height / 2) / ball.MAX_VEL)

    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                middle_y = right_paddle.y + right_paddle.height / 2
                diff_y = middle_y - ball.y
                ball.y_vel = -diff_y / ((right_paddle.height / 2) / ball.MAX_VEL)


def handle_paddle_movement(keys, left_paddle, right_paddle, game_mode, ball=None, difficulty=None):
    if game_mode == "player_vs_player":
        if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
            left_paddle.move(True)
        if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
            left_paddle.move(False)

        if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
            right_paddle.move(True)
        if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
            right_paddle.move(False)
    elif game_mode == "player_vs_ai":
        if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
            left_paddle.move(True)
        if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
            left_paddle.move(False)

        if ball and difficulty:
            if difficulty == "easy":
                if ball.y > right_paddle.y + right_paddle.height / 2 and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
                    right_paddle.y += right_paddle.VEL * 0.5
                elif ball.y < right_paddle.y + right_paddle.height / 2 and right_paddle.y - right_paddle.VEL >= 0:
                    right_paddle.y -= right_paddle.VEL * 0.5
            elif difficulty == "medium":
                if ball.y > right_paddle.y + right_paddle.height / 2 and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
                    right_paddle.y += right_paddle.VEL * 0.8
                elif ball.y < right_paddle.y + right_paddle.height / 2 and right_paddle.y - right_paddle.VEL >= 0:
                    right_paddle.y -= right_paddle.VEL * 0.8
            elif difficulty == "hard":
                if ball.y > right_paddle.y + right_paddle.height / 2 and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
                    right_paddle.y += right_paddle.VEL
                elif ball.y < right_paddle.y + right_paddle.height / 2 and right_paddle.y - right_paddle.VEL >= 0:
                    right_paddle.y -= right_paddle.VEL


def main_game_loop(game_mode, difficulty=None):
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_LEFT_COLOR)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT,
                          PADDLE_RIGHT_COLOR)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle, game_mode, ball, difficulty)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        win_text = None
        if left_score >= WINNING_SCORE:
            win_text = "Left Player Wins!" if game_mode == "player_vs_player" else "You Win!"
        elif right_score >= WINNING_SCORE:
            win_text = "Right Player Wins!" if game_mode == "player_vs_player" else "AI Wins!"

        if win_text:
            win_label = SCORE_FONT.render(win_text, True, WHITE)
            WIN.blit(win_label, (WIDTH // 2 - win_label.get_width() // 2, HEIGHT // 2 - win_label.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(4000)
            return "menu"


def main_menu():
    run = True
    while run:
        WIN.fill(DARK_PURPLE)

        title_text = MENU_FONT.render("Colorful Pong", True, WHITE)
        play_text = MENU_FONT.render("1. Player vs Player", True, WHITE)
        ai_text = MENU_FONT.render("2. Player vs AI", True, WHITE)
        quit_text = MENU_FONT.render("Q. Quit", True, WHITE)

        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        WIN.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, 150))
        WIN.blit(ai_text, (WIDTH // 2 - ai_text.get_width() // 2, 200))
        WIN.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 250))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_state = main_game_loop("player_vs_player")
                    if game_state == "quit":
                        run = False
                elif event.key == pygame.K_2:
                    difficulty = difficulty_menu()
                    if difficulty:
                        game_state = main_game_loop("player_vs_ai", difficulty)
                        if game_state == "quit":
                            run = False
                elif event.key == pygame.K_q:
                    run = False


def difficulty_menu():
    selecting = True
    while selecting:
        WIN.fill(DARK_PURPLE)
        title_text = MENU_FONT.render("Select Difficulty", True, WHITE)
        easy_text = MENU_FONT.render("1. Easy", True, WHITE)
        medium_text = MENU_FONT.render("2. Medium", True, WHITE)
        hard_text = MENU_FONT.render("3. Hard", True, WHITE)
        back_text = MENU_FONT.render("B. Back", True, WHITE)

        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        WIN.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, 150))
        WIN.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, 200))
        WIN.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, 250))
        WIN.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, 300))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "easy"
                elif event.key == pygame.K_2:
                    return "medium"
                elif event.key == pygame.K_3:
                    return "hard"
                elif event.key == pygame.K_b:
                    return None


if __name__ == "__main__":
    main_menu()
    pygame.quit()
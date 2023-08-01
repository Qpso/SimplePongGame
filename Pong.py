import pygame
import sys

pygame.init()

# Constants for the game window
WINDOW_WIDTH, WINDOW_HEIGHT = 640, 480
WINDOW_TITLE = "Pong Game"

# Colors
WHITE = (255, 255, 255)

# Create window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 80)

    def draw(self, window):
        pygame.draw.rect(window, WHITE, self.rect)

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.speed_x = 7
        self.speed_y = 7

    def draw(self, window):
        pygame.draw.rect(window, WHITE, self.rect)

def display_score(window, font, player_score, opponent_score):
    score_text = font.render(f"{player_score} - {opponent_score}", True, WHITE)
    window.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 20))

def main():
    clock = pygame.time.Clock()

    # Create paddles and ball
    player_paddle = Paddle(50, WINDOW_HEIGHT // 2 - 40)
    opponent_paddle = Paddle(WINDOW_WIDTH - 50, WINDOW_HEIGHT // 2 - 40)
    ball = Ball(WINDOW_WIDTH // 2 - 7, WINDOW_HEIGHT // 2 - 7)

    # Load a font for displaying the score
    font = pygame.font.Font(None, 50)

    # scores for both players
    player_score = 0
    opponent_score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_paddle.rect.y -= 7
        if keys[pygame.K_s]:
            player_paddle.rect.y += 7

        # Ensure paddles stay within the window boundaries
        player_paddle.rect.y = max(0, player_paddle.rect.y)
        player_paddle.rect.y = min(WINDOW_HEIGHT - player_paddle.rect.height, player_paddle.rect.y)

        # AI opponent movement
        if opponent_paddle.rect.centery < ball.rect.centery:
            opponent_paddle.rect.y += 5
        if opponent_paddle.rect.centery > ball.rect.centery:
            opponent_paddle.rect.y -= 5

        # Ensure the opponent's paddle stays within the window boundaries
        opponent_paddle.rect.y = max(0, opponent_paddle.rect.y)
        opponent_paddle.rect.y = min(WINDOW_HEIGHT - opponent_paddle.rect.height, opponent_paddle.rect.y)

        # Ball movement
        ball.rect.x += ball.speed_x
        ball.rect.y += ball.speed_y

        # Ball collisions with walls
        if ball.rect.top <= 0 or ball.rect.bottom >= WINDOW_HEIGHT:
            ball.speed_y *= -1

        # Ball collisions with paddles
        if ball.rect.colliderect(player_paddle.rect) or ball.rect.colliderect(opponent_paddle.rect):
            ball.speed_x *= -1

        # Reset ball when out of screen
        if ball.rect.left <= 0:
            opponent_score += 1
            ball.rect.x = WINDOW_WIDTH // 2 - 7
            ball.rect.y = WINDOW_HEIGHT // 2 - 7
            ball.speed_x *= -1

        if ball.rect.right >= WINDOW_WIDTH:
            player_score += 1
            ball.rect.x = WINDOW_WIDTH // 2 - 7
            ball.rect.y = WINDOW_HEIGHT // 2 - 7
            ball.speed_x *= -1

        # Draw 
        window.fill((0, 0, 0))
        player_paddle.draw(window)
        opponent_paddle.draw(window)
        ball.draw(window)
        display_score(window, font, player_score, opponent_score)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()

import pygame
import sys
import time
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        self.game_over = False
        self.winner_text = ""
        self.max_score = 5  # Default to "best of 5" (first to 5)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.game_over:
            return  # Stop updates if game is over

        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        # Scoring logic
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x + self.ball.width >= self.width:
            self.player_score += 1
            self.ball.reset()

        # AI tracking
        self.ai.auto_track(self.ball, self.height)

        # Check for game over condition
        self.check_game_over()

    def check_game_over(self):
        """Check if either player reached max_score and handle replay screen."""
        if self.player_score >= self.max_score:
            self.winner_text = "Player Wins!"
            self.game_over = True
        elif self.ai_score >= self.max_score:
            self.winner_text = "AI Wins!"
            self.game_over = True

        if self.game_over:
            self.show_game_over_screen()

    def show_game_over_screen(self):
        """Display winner message and replay options."""
        screen = pygame.display.get_surface()
        screen.fill(BLACK)

        # Winner message
        winner_font = pygame.font.SysFont("Arial", 60, bold=True)
        text = winner_font.render(self.winner_text, True, WHITE)
        screen.blit(text, (self.width // 2 - text.get_width() // 2,
                           self.height // 3))

        # Options
        option_font = pygame.font.SysFont("Arial", 30)
        options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit"
        ]
        for i, opt in enumerate(options):
            t = option_font.render(opt, True, WHITE)
            screen.blit(t, (self.width // 2 - t.get_width() // 2,
                            self.height // 2 + i * 40))

        pygame.display.flip()

        # Wait for input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_3:
                        self.max_score = 2  # best of 3
                        waiting = False
                    elif event.key == pygame.K_5:
                        self.max_score = 3  # best of 5
                        waiting = False
                    elif event.key == pygame.K_7:
                        self.max_score = 4  # best of 7
                        waiting = False

        # Reset everything for replay
        self.reset_game_state()

    def reset_game_state(self):
        """Reset scores, ball, and state for replay."""
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.game_over = False
        self.winner_text = ""

    def render(self, screen):
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

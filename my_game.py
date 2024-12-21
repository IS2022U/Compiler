import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions (increased size)
WIDTH, HEIGHT = 1280, 768  # Increased width
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Compiler Learning Game - Lexical Analyzer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)
YELLOW = (255, 255, 100)

# Fonts
FONT = pygame.font.Font(None, 36)
LARGE_FONT = pygame.font.Font(None, 60)

# Token categories
CATEGORIES = ["Keyword", "Identifier", "Operator"]

# Token templates for each category
TOKEN_TEMPLATES = {
    "Keyword": ["int", "float", "double", "if", "else", "while"],
    "Identifier": ["x", "y", "z", "counter", "sum", "average"],
    "Operator": ["=", "+", "-", "*", "/", ";"]
}

# Drop zones for categories
drop_zones = {
    "Keyword": pygame.Rect(50, HEIGHT - 150, 200, 100),
    "Identifier": pygame.Rect(300, HEIGHT - 150, 200, 100),
    "Operator": pygame.Rect(550, HEIGHT - 150, 200, 100)
}

# Game variables
score = 0
level = 1
time_limit = 30  # Initial time limit
start_time = None
tokens = []
game_over = False
win = False
dragging_token = None

# Levels Configuration
LEVELS = [
    {"time_limit": 30, "tokens_per_category": 2, "token_size": (100, 50)},
    {"time_limit": 25, "tokens_per_category": 3, "token_size": (80, 40)},
    {"time_limit": 20, "tokens_per_category": 4, "token_size": (70, 35)},
    {"time_limit": 15, "tokens_per_category": 5, "token_size": (60, 30)}
]

def generate_tokens(level_config):
    """Generate tokens based on the level configuration."""
    tokens = []
    for category in CATEGORIES:
        for _ in range(level_config["tokens_per_category"]):
            text = random.choice(TOKEN_TEMPLATES[category])
            x = random.randint(50, WIDTH - 150)
            y = random.randint(50, HEIGHT - 200)
            tokens.append(Token(text, category, x, y, level_config["token_size"]))
    random.shuffle(tokens)
    return tokens

class Token:
    def __init__(self, text, category, x, y, size):
        self.text = text
        self.category = category
        self.rect = pygame.Rect(x, y, *size)
        self.dragging = False

def draw_text(text, x, y, color=BLACK, font=FONT):
    """Helper function to draw text on the screen."""
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def draw_confetti():
    """Draw confetti animation."""
    for _ in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        color = random.choice([RED, GREEN, BLUE, YELLOW])
        pygame.draw.circle(screen, color, (x, y), 5)

def new_game(level=1):
    """Reset the game variables for a new session or level."""
    global tokens, score, start_time, game_over, win, time_limit
    level_config = LEVELS[level - 1]
    tokens = generate_tokens(level_config)
    score = 0
    start_time = time.time()
    game_over = False
    win = False
    time_limit = level_config["time_limit"]

def show_instructions():
    """Display instructions at the start of the game."""
    screen.fill(WHITE)
    draw_text("Welcome to the Compiler Learning Game!", WIDTH // 2 - 250, HEIGHT // 4, BLUE, LARGE_FONT)
    
    draw_text("What are these terms?", WIDTH // 2 - 150, HEIGHT // 2 - 100, BLACK, FONT)
    draw_text("- Keyword: A special word in programming like 'int' or 'if'.", WIDTH // 2 - 250, HEIGHT // 2 - 50, BLACK, FONT)
    draw_text("- Operator: Symbols like '=', '+', or '*' that perform actions.", WIDTH // 2 - 250, HEIGHT // 2, BLACK, FONT)
    draw_text("- Identifier: Names for variables or functions like 'counter' or 'sum'.", WIDTH // 2 - 250, HEIGHT // 2 + 50, BLACK, FONT)
    
    draw_text("Your Task: Drag each term into the correct category.", WIDTH // 2 - 250, HEIGHT // 2 + 150, BLACK, FONT)
    
    # Draw "Start Game" button
    pygame.draw.rect(screen, BLACK, (300, HEIGHT - 150, 200, 50))
    draw_text("Start Game", 330, HEIGHT - 140, WHITE)

def main():
    global score, game_over, win, level, dragging_token
    clock = pygame.time.Clock()

    # Show instructions before starting the game
    show_instructions()

    # Wait for the user to click on "Start Game"
    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if "Start Game" is clicked
                if 300 <= event.pos[0] <= 500 and HEIGHT - 150 <= event.pos[1] <= HEIGHT - 100:
                    new_game(level)  # Start the game
                    waiting_for_start = False
                    break

        # Update the display
        pygame.display.flip()
        clock.tick(30)

    # Main game loop
    while True:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Start dragging a token
                if not game_over:
                    for token in tokens:
                        if token.rect.collidepoint(event.pos):
                            token.dragging = True
                            dragging_token = token
                            break

            elif event.type == pygame.MOUSEBUTTONUP:
                # Drop the token
                if dragging_token:
                    token = dragging_token
                    token.dragging = False

                    # Check if token is dropped in the correct drop zone
                    for category, zone in drop_zones.items():
                        if token.rect.colliderect(zone):
                            if token.category == category:
                                score += 1
                                tokens.remove(token)  # Remove token from the game
                            break
                    dragging_token = None

            elif event.type == pygame.MOUSEMOTION:
                # Dragging a token
                if dragging_token:
                    token = dragging_token
                    token.rect.x += event.rel[0]
                    token.rect.y += event.rel[1]

        # Timer logic
        elapsed_time = time.time() - start_time if start_time else 0
        remaining_time = max(0, int(time_limit - elapsed_time))
        if remaining_time == 0 and not game_over:
            game_over = True
            win = False

        # Draw drop zones
        for category, zone in drop_zones.items():
            pygame.draw.rect(screen, GRAY, zone)
            draw_text(category, zone.x + 50, zone.y + 35)

        # Draw tokens
        if not game_over:
            for token in tokens:
                pygame.draw.rect(screen, BLUE, token.rect)
                draw_text(token.text, token.rect.x + 10, token.rect.y + 10, WHITE)

        # Draw score, timer, and level
        draw_text(f"Score: {score}/{len(tokens) + score}", 10, 10)
        draw_text(f"Time: {remaining_time}s", WIDTH - 150, 10)
        draw_text(f"Level: {level}", WIDTH // 2 - 50, 10)
        
        # End game condition
        if not tokens and not game_over:
            if level < len(LEVELS):
                level += 1
                new_game(level)
            else:
                game_over = True
                win = True
         
        # Draw game over screen
        if game_over:
            if win:
                draw_text("You Win!", WIDTH // 2 - 100, HEIGHT // 2 - 50, GREEN, LARGE_FONT)
                draw_confetti()
            else:
                draw_text("You Lost!", WIDTH // 2 - 100, HEIGHT // 2 - 50, RED, LARGE_FONT)

            # Draw "New Game" button
            new_game_button_rect = pygame.Rect(400, HEIGHT // 2 + 50, 200, 50)  # Adjusted position and size
            pygame.draw.rect(screen, BLACK, new_game_button_rect)
            draw_text("New Game", new_game_button_rect.x + 50, new_game_button_rect.y + 10, WHITE)

            # Check if "New Game" button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN and new_game_button_rect.collidepoint(event.pos):
                new_game(level)

        # Update display
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()

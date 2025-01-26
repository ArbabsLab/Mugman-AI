import pygame
import os

# Initialize Pygame
pygame.init()

# Set up the game window
WIN_WIDTH, WIN_HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Mugman Animation Test")

# Load the spritesheet
SPRITESHEET = pygame.image.load(os.path.join("assets", "mugman_spritesheet.png")).convert_alpha()

# Function to extract sprites
def extract_sprites(sheet, sprite_width, sprite_height, start_x=0, start_y=0, columns=1, rows=1, spacing_x=0, spacing_y=0):
    frames = []
    for row in range(rows):
        for col in range(columns):
            x = start_x + col * (sprite_width + spacing_x) + 1
            y = start_y + row * (sprite_height + spacing_y)
            sprite = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            sprite.blit(sheet, (0, 0), (x, y, sprite_width, sprite_height))
            frames.append(sprite)
    return frames

# Extract animations for Mugman
MUGMAN_RUN_FRAMES = extract_sprites(SPRITESHEET, 24, 24, start_x=25, start_y=10, columns=3, rows=1)
MUGMAN_JUMP_FRAMES = extract_sprites(SPRITESHEET, 32, 24, start_x=33, start_y=35, columns=1, rows=1)
MUGMAN_DUCK_FRAMES = extract_sprites(SPRITESHEET, 24, 24, start_x=220, start_y=10, columns=1, rows=1)

# Test variables
clock = pygame.time.Clock()
run = True
frame_index = 0
current_frames = MUGMAN_RUN_FRAMES  # Default animation
last_frames = current_frames  # Keep track of the previous animation

# Main loop
while run:
    WIN.fill((255, 255, 255))  # Clear screen with white

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Handle key inputs to switch animations
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        current_frames = MUGMAN_JUMP_FRAMES
    elif keys[pygame.K_DOWN]:
        current_frames = MUGMAN_DUCK_FRAMES
    else:
        current_frames = MUGMAN_RUN_FRAMES

    # Reset frame index if the animation changes
    if current_frames != last_frames:
        frame_index = 0
        last_frames = current_frames

    # Draw the current frame
    sprite_x = (WIN_WIDTH // 2) - 12  # Adjust horizontal position
    sprite_y = 300  # Fixed vertical position for better ground alignment
    WIN.blit(current_frames[frame_index], (sprite_x, sprite_y))

    # Update the frame index to animate
    frame_index += 1
    if frame_index >= len(current_frames):  # Loop back to the first frame
        frame_index = 0

    pygame.display.update()
    clock.tick(10)  # Control the frame rate (10 FPS)

pygame.quit()

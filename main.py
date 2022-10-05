import pygame
import os
pygame.init()
pygame.mixer.init()
pygame.font.init()

BLAZE_VEL = 5
COLOR_VEL = 5

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Deagle Showdown - Blaze VS Blue - ")

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
BULLET_VEL = 7
MAX_BULLETS = 3

BLAZE_HIT = pygame.USEREVENT + 1

COLOR_HIT = pygame.USEREVENT + 2

BLAZE_WIDTH, BLAZE_HEIGHT = 190, 100
BLAZE_GUN_IMAGE = pygame.image.load(os.path.join('Assets', 'dablaze.png'))
BLAZE_GUN = pygame.transform.scale(BLAZE_GUN_IMAGE, (BLAZE_WIDTH, BLAZE_HEIGHT))

COLOR_WIDTH, COLOR_HEIGHT = 160, 85
COLOR_GUN_IMAGE = pygame.image.load(os.path.join('Assets', 'purple.png'))
COLOR_GUN = pygame.transform.scale(COLOR_GUN_IMAGE, (COLOR_WIDTH, COLOR_HEIGHT))

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'sand.png')), (WIDTH, HEIGHT))


# draw_function will draw the game on the screen
def draw_window(color, blaze, color_bullets, blaze_bullets, color_health, blaze_health):
   WIN.blit(SPACE, (0, 0))
   pygame.draw.rect(WIN, BLACK, BORDER)
   color_health_text = HEALTH_FONT.render(
       "Health: " + str(color_health), 1, WHITE)
   blaze_health_text = HEALTH_FONT.render(
       "Health: " + str(blaze_health), 1, WHITE)
   WIN.blit(blaze_health_text, (WIDTH - blaze_health_text.get_width() - 10, 10))
   WIN.blit(color_health_text, (10, 10))
   # each image is drawn at the point that is created via input while main runs
   # this change allows the input to effect the actual position of the guns
   WIN.blit(BLAZE_GUN, (blaze.x, blaze.y))
   WIN.blit(COLOR_GUN, (color.x, color.y))
   for bullet in color_bullets:
       pygame.draw.rect(WIN, BLUE, bullet)
   for bullet in blaze_bullets:
       pygame.draw.rect(WIN, YELLOW, bullet)
   pygame.display.update()


def color_handle_movement(keys_pressed, color):
   if keys_pressed[pygame.K_LEFT] and color.x - COLOR_VEL > BORDER.x + BORDER.width - 15:
       color.x -= COLOR_VEL
   if keys_pressed[pygame.K_RIGHT] and color.x + COLOR_VEL + color.width < WIDTH + 35:
       color.x += COLOR_VEL
   if keys_pressed[pygame.K_UP] and color.y - COLOR_VEL > -30:
       color.y -= COLOR_VEL
   if keys_pressed[pygame.K_DOWN] and color.y + COLOR_VEL + color.height < HEIGHT + 50:
       color.y += COLOR_VEL


def blaze_handle_movement(keys_pressed, blaze):
   #                           for this -70; the lower, the larger the range to the left
   if keys_pressed[pygame.K_a] and blaze.x - BLAZE_VEL > -70:  # LEFT
       blaze.x -= BLAZE_VEL
   if keys_pressed[pygame.K_d] and blaze.x + BLAZE_VEL + blaze.width < BORDER.x + 15.2:  # RIGHT
       blaze.x += BLAZE_VEL
   if keys_pressed[pygame.K_w] and blaze.y - BLAZE_VEL > -30:  # UP
       blaze.y -= BLAZE_VEL
   if keys_pressed[pygame.K_s] and blaze.y + BLAZE_VEL + blaze.height < HEIGHT + 70:  # DOWN
       blaze.y += BLAZE_VEL


def handle_bullets(blaze_bullets, color_bullets, blaze, color):
   # so this means whenever the bullet is made, it will be sent out, and check for collisions
   for bullet in blaze_bullets:
       bullet.x += BULLET_VEL
       if color.colliderect(bullet):
           pygame.event.post(pygame.event.Event(COLOR_HIT))
           blaze_bullets.remove(bullet)
       elif bullet.x > WIDTH:
           blaze_bullets.remove(bullet)
   for bullet in color_bullets:
       bullet.x -= BULLET_VEL
       if blaze.colliderect(bullet):
           pygame.event.post(pygame.event.Event(BLAZE_HIT))
           color_bullets.remove(bullet)
       elif bullet.x < 0:
           color_bullets.remove(bullet)


def draw_winner(text):
   draw_text = WINNER_FONT.render(text, 1, WHITE)
   WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
   pygame.display.update()
   pygame.time.delay(5000)


def main():
   color_health = 10
   blaze_health = 10
   color = pygame.Rect(700, 300, COLOR_WIDTH, COLOR_HEIGHT)
   blaze = pygame.Rect(100, 300, BLAZE_WIDTH, BLAZE_HEIGHT)
   clock = pygame.time.Clock()

   color_bullets = []
   blaze_bullets = []

   run = True
   while run:
       #       makes the game tick at int FPS
       clock.tick(FPS)
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               run = False
               pygame.quit()
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_LCTRL and len(blaze_bullets) < MAX_BULLETS:
                   bullet = pygame.Rect(
                       blaze.x + blaze.width, blaze.y + blaze.height // 2 - 28, 15, 7.5)
                   blaze_bullets.append(bullet)
                   pygame.mixer.music.set_volume(0.3)
                   BULLET_FIRE_SOUND.play()

               if event.key == pygame.K_SPACE and len(color_bullets) < MAX_BULLETS:
                   bullet = pygame.Rect(
                   color.x, color.y + color.height // 2 - 28, 15, 7.5)
                   color_bullets.append(bullet)
                   pygame.mixer.music.set_volume(0.3)
                   BULLET_FIRE_SOUND.play()

           if event.type == COLOR_HIT:
               # here the blaze halth is lowered for the imapct of the buklet to make ana ffect on the health omf
               blaze_health -= 1
               pygame.mixer.music.set_volume(0.3)
               BULLET_HIT_SOUND.play()
           if event.type == BLAZE_HIT:
               color_health -= 1
               pygame.mixer.music.set_volume(0.3)
               BULLET_HIT_SOUND.play()

       winner_text = ""
       if color_health <= 0:
           winner_text = "Blue Wins"

       if blaze_health <= 0:
           winner_text = "Blaze Wins"

       if winner_text != "":
           draw_winner(winner_text)
           break # someone won,

       keys_pressed = pygame.key.get_pressed()

       blaze_handle_movement(keys_pressed, blaze)
       color_handle_movement(keys_pressed, color)

       handle_bullets(blaze_bullets, color_bullets, blaze, color)
       #       everytime that the main loops runs;
       #       so does the window loop!
       #       main takes controls / input
       #       draw_window makes it appear on the surface.
       draw_window(color, blaze, color_bullets, blaze_bullets, color_health, blaze_health)

   main()


if __name__ == "__main__":
   main()


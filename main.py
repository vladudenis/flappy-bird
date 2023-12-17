import pygame

import assets
import configs
from objects.background import Background
from objects.bird import Bird
from objects.column import Column
from objects.floor import Floor
from objects.game_over_msg import GameOverMessage
from objects.game_start_msg import GameStartMessage
from objects.score import Score

pygame.init()
assets.load_sprites()
assets.load_audios()
sprites = pygame.sprite.LayeredUpdates()


def create_sprites():
    Background(0, sprites)
    Background(1, sprites)
    Floor(0, sprites)
    Floor(1, sprites)
    Column(sprites)

    return Bird(sprites), GameStartMessage(sprites), Score(0, sprites)


screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running = True
game_over = False
game_started = False

bird, game_start_msg, score = create_sprites()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == column_create_event:
            Column(sprites)
        if event.type == pygame.KEYDOWN:
            if not game_over and not game_started and event.key == pygame.K_SPACE:
                game_started = True
                game_start_msg.kill()
                pygame.time.set_timer(column_create_event, 3000)
            if game_over and (event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE):
                game_over = False
                game_Started = False
                sprites.empty()
                bird, game_start_msg, score = create_sprites()
        if not game_over:
            bird.handle_event(event)

    screen.fill(0)
    sprites.draw(screen)

    if game_started and not game_over:
        sprites.update()

    if not game_over and bird.check_collision(sprites):
        assets.play_audio("hit")
        game_over = True
        game_started = False

        GameOverMessage(sprites)
        pygame.time.set_timer(column_create_event, 0)

    for sprite in sprites:
        if type(sprite) is Column and sprite.is_passed():
            score.value += 1
            assets.play_audio("point")

    pygame.display.flip()
    clock.tick(configs.FPS)

pygame.quit()

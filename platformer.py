# !/usr/bin/env python3
# File Encoding : UTF-8
# Alexandre Buisset

import pygame, sys
from pygame.locals import *
import json

pygame.mixer.init()
pygame.font.init()
pygame.init()  # VroomVroom pygame lance toi

WINDOW_SIZE = (1280, 720)  # taille du jeu
screen = pygame.display.set_mode(WINDOW_SIZE, FULLSCREEN, 32)  # initiate screen
# NOFRAME pour enlever la bordure

# Important taille des élements de la fenêtre donc mettre même taille que la fenêtre
display = pygame.Surface((1280, 720), pygame.HWSURFACE)
pygame.mouse.set_cursor(*pygame.cursors.arrow)
pygame.mouse.set_visible(0)


cheating = False
score_write = False
boss_fighting = False
invisible = False
invincible = False
FPS = 60
nv = 0
volume = 1

walkCount = 0
walkCount_vulcan = 0
walkCount_Boss = 0
time_vulcan = 0
position_scrolling = [0, 0]
position_Bx = 0
position_B2x = 3840
attaqued_temps = 0
vie_boss = 3
time_boss_invincible = 0
INVINCIBLE_BOSS = False
time_boss_death = 0

boss_x = 6500
boss_y = 285
boss_rect = pygame.Rect(boss_x, boss_y, 607, 394)
boss_rect_top = pygame.Rect(boss_x, boss_y, 607, 100)
boss_barre_vie = 1000

monstre1_posx, monstre1_posy = 1800, 550
monstre2_posx, monstre2_posy = 3100, 250

number_tries = 1
time_particles = 0
time_music_fighting = 0
alpha = 128
scroll = [0, 0]
timer = 0
START_GAME = 0
ACTIVATION = False
VICTOIRE = False
PAUSE = False

menu_title = pygame.image.load("data/menu/GameOfSteel_+petit.png").convert_alpha()
menu_jouer = pygame.image.load("data/menu/JOUER_petit.png").convert_alpha()

particles_electro = [pygame.image.load(f"data/menu/frame-{i}.gif").convert_alpha()
                     for i in range(1, 10)]

background_vulcan = [pygame.image.load(f"data/menu/vulcan{i}.gif").convert_alpha()
                     for i in range(1, 17)]

background_vulcan_inverse = [pygame.transform.flip(background_vulcan[i], True, False).convert_alpha()
                             for i in range(16)]

boss_walking = [pygame.image.load(f"data/boss/walking/skeleton-walking_{i}.png").convert_alpha()
                for i in range(21)]

boss_walking_right = [pygame.transform.flip(boss_walking[i], True, False).convert_alpha()
                      for i in range(21)]

boss_defeated = [pygame.image.load(f"data/boss/defeated/skeleton-defeated_{i}.png").convert_alpha()
                 for i in range(26)]

fire_door = [pygame.image.load(f"data/boss/fire/frame-{i}.gif").convert_alpha()
             for i in range(1, 17)]

boss_opacity = [pygame.image.load(f"data/boss/opacity/opacity{i}.png").convert_alpha()
                for i in range(0, 10)]

boss_opacity_right = [pygame.transform.flip(boss_opacity[i], True, False).convert_alpha()
                      for i in range(0, 10)]
# -----------------------------------------------------------------------------------------

idle1 = pygame.image.load("data/perso/right/standing/standing_0.png")

# Frames du personnages quand il est immobile
player_standing_right = [idle1,
                         pygame.image.load("data/perso/right/standing/standing_1.png").convert_alpha()]

idle_opacity = [pygame.image.load("data/perso/right/standing/idle0T1.png").convert_alpha(),
                pygame.image.load("data/perso/right/standing/idle0T2.png").convert_alpha(),
                pygame.image.load("data/perso/right/standing/idle0T3.png").convert_alpha(),
                pygame.image.load("data/perso/right/standing/idle1T1.png").convert_alpha(),
                pygame.image.load("data/perso/right/standing/idle1T2.png").convert_alpha(),
                pygame.image.load("data/perso/right/standing/idle1T3.png").convert_alpha()]

run_right_opacity = [pygame.image.load(f"data/perso/right/running/running_T{i}.png").convert_alpha()
                     for i in range(18)]

run_left_opacity = [pygame.transform.flip(run_right_opacity[i], True, False).convert_alpha()
                    for i in range(18)]

mask_player_afk = [pygame.mask.from_surface(player_standing_right[0])]

# Frames du personnage quand il court

player_running_right = [pygame.image.load(f"data/perso/right/running/running_{i}.png").convert_alpha()
                        for i in range(6)]

player_running_left = [pygame.image.load(f"data/perso/left/running/running_{i}.png").convert_alpha()
                       for i in range(6)]

# -----------------------------------------------------------------------------

monster1_running_left = [pygame.image.load(f'data/mob/left/walking/frame-{i}.png').convert_alpha()
                         for i in range(1, 9)]

# Permet de rotate l'image à l'horizontal donc right > left
monster1_running_right = [pygame.transform.flip(monster1_running_left[i], True, False).convert_alpha()
                          for i in range(8)]

monster_2_walking_left = [pygame.image.load(f'data/mob/skeletonwalk{i}.png').convert_alpha()
                         for i in range(1, 14)]

monster_2_walking_right = [pygame.transform.flip(monster_2_walking_left[i], True, False).convert_alpha()
                          for i in range(13)]

monster_3_walking_left = [pygame.image.load(f'data/mob/frame-{i}.png').convert_alpha()
                         for i in range(1, 9)]

monster_3_walking_right = [pygame.transform.flip(monster_3_walking_left[i], True, False).convert_alpha()
                          for i in range(8)]
# ------------------------------------------------------------------------------------

background_image = pygame.image.load('data/images/background.png').convert_alpha()
background_inverse_image = pygame.transform.flip(background_image, True, False).convert_alpha()

background_mountain = pygame.image.load('data/images/mountain.gif').convert_alpha()
background_mountain_inversed = pygame.transform.flip(background_mountain, True, False).convert_alpha()


# Ou autre background si choisi
background_night_image = pygame.image.load('data/menu/fond_menu.png').convert_alpha()
background_inverse_night_image = pygame.transform.flip(background_night_image, True, False).convert_alpha()

background2_image = pygame.image.load('data/images/back.jpg').convert_alpha()
background2_inverse_image = pygame.transform.flip(background2_image, True, False).convert_alpha()
# Image de base du perso


MORT_image = pygame.image.load('data/images/MORT.png').convert_alpha()
# --------------------------------------------------------------------

barrevie_image = pygame.image.load("data/images/barrevie.png").convert_alpha()
barre1vie_image = pygame.image.load('data/images/barre_1vie.png').convert_alpha()
barre2vie_image = pygame.image.load("data/images/barre_2vie.png").convert_alpha()
barre_fullvie_image = pygame.image.load("data/images/barre_fullvie.png").convert_alpha()

# --------------------------------------------------------------------

spikes = pygame.image.load("data/images/spikes.png").convert_alpha()

case_mystere_image = pygame.image.load('data/images/case_mystere.png').convert_alpha()
grass_image = pygame.image.load('data/images/grass.png').convert_alpha()
panneau_droite_image = pygame.image.load('data/images/panneau_droite.png').convert_alpha()
grasscarre_image = pygame.image.load('data/images/grass2.png').convert_alpha()
grass_droit_image = pygame.image.load('data/images/grass_droit.png').convert_alpha()
grass_gauche_image = pygame.image.load('data/images/grass_gauche.png').convert_alpha()
grass_dalle_image = pygame.image.load("data/images/grass_dalle.png").convert_alpha()
pont_image = pygame.image.load("data/images/pont.png").convert_alpha()
lave_image = pygame.image.load("data/images/lava.png").convert_alpha()
laveblock_image = pygame.image.load("data/images/lavablock.png").convert_alpha()
grass_oblique_D1 = pygame.image.load("data/images/grassHillLeft.png").convert_alpha()

dirt_image = pygame.image.load('data/images/terre.png').convert_alpha()
water1_image = pygame.image.load("data/images/water.png").convert_alpha()
water_block_image = pygame.image.load("data/images/waterblock.png").convert_alpha()

door_openmid_image = pygame.image.load("data/images/door_openMid.png").convert_alpha()
door_opentop_image = pygame.image.load("data/images/door_openTop.png").convert_alpha()

plant_green_image = pygame.image.load('data/images/plant_green.png').convert_alpha()
exit_image = pygame.image.load('data/images/signExit.png').convert_alpha()

brown_tile1 = pygame.image.load("data/images/tileBrown_01.png").convert_alpha()
brown_tile2 = pygame.image.load("data/images/tileBrown_02.jpg").convert_alpha()
brown_tile3 = pygame.image.load("data/images/tileBrown_03.png").convert_alpha()
brown_tile5 = pygame.image.load("data/images/tileBrown_27.png").convert_alpha()
brown_tile6 = pygame.image.load("data/images/tileBrown_25.png").convert_alpha()
brown_tile7 = pygame.transform.flip(brown_tile6, True, False).convert_alpha()
brown_tile8 = pygame.image.load("data/images/tileBrown_23.png").convert_alpha()
brown_tile9 = pygame.image.load("data/images/tileBrown_24.png").convert_alpha()
brown_tile10 = pygame.image.load("data/images/tileBrown_08.png").convert_alpha()

tundra_mid = pygame.image.load("data/images/tundraMid.png").convert_alpha()
tundra_center = pygame.image.load("data/images/tundraCenter.png").convert_alpha()
tundraLeft = pygame.image.load("data/images/tundraLeft.png").convert_alpha()
tundraRight = pygame.image.load("data/images/tundraRight.png").convert_alpha()
deadTree = pygame.image.load("data/images/deadTree.png").convert_alpha()
iceBlock = pygame.image.load("data/images/iceBlock.png").convert_alpha()
iceBlockAlt = pygame.image.load("data/images/iceBlockAlt.png").convert_alpha()
rock = pygame.image.load("data/images/rock.png").convert_alpha()
spikesBottom = pygame.image.load("data/images/spikesBottom.png").convert_alpha()
tundraCliffLeftAlt = pygame.image.load("data/images/tundraCliffLeftAlt.png").convert_alpha()
tundraCliffRightAlt = pygame.image.load("data/images/tundraCliffRightAlt.png").convert_alpha()


TILE_SIZE = grass_image.get_width()  # 70x70

# ---------------------------------------------------------------


sound_damaged = pygame.mixer.Sound("data/audio/damaged.ogg")
sound_jump = pygame.mixer.Sound("data/audio/sound_jump.ogg")

score = 0
attaqued = False

jouerx = 520
jouery = 320
jouer_position = pygame.Rect(jouerx, jouery, 225, 83)
main_music = pygame.mixer.music.load("data/audio/CODEX.mp3")


class Monster(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("data/mob/left/idle/frame-1.png")
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 500
        self.velocity = 0
        self.gravity = 0
        self.air_timer = 0
        self.vie = 1
        self.attack = 1


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("data/perso/right/standing/standing_0.png")
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 460
        self.velocity = 0
        self.gravity = 0
        self.air_timer = 0
        self.vie = 3

    def restart_position(self):
        self.rect.x = 200
        self.rect.y = 460


def loop():
    global walkCount, player, monster, cheating, START_GAME, timer, ACTIVATION, VICTOIRE, FPS, scroll, score, \
        time_particles, score_write, number_tries, walkCount_vulcan, time_vulcan, nv, time_music_fighting, boss_fighting, \
        monstre1_posx, monstre1_posy, monstre2_posx, monstre2_posy, time_boss_death, invisible, invincible, boss_y, boss_x, \
        boss_barre_vie, alpha, volume

    clock = pygame.time.Clock()  # set up the clock
    pygame.display.set_caption('GameOfSteel')  # Nom du jeu

    icon = pygame.image.load("data/menu/s.png")
    pygame.display.set_icon(icon)
    font = pygame.font.Font('data/fonts/RifficFree-Bold.ttf', 180)
    font_end = pygame.font.Font('data/fonts/RifficFree-Bold.ttf', 120)
    font_HR = pygame.font.Font('data/fonts/RifficFree-Bold.ttf', 50)
    font_name = pygame.font.Font('data/fonts/RifficFree-Bold.ttf', 40)

    temps_invisible = 0
    walkCount = 0

    position_Bx = -200
    # ----------------------------------------------------

    temps_jump = 0

    temps_invincible = 0
    sound = True

    scroll[0] += 1


    def musicSteel():
        global volume

        if START_GAME == 0:
            pygame.mixer.music.load("data/audio/CODEX.mp3")
        '''elif START_GAME == 1:
            musique_fond = pygame.mixer.music.load("data/audio/coromusique.mp3")'''
        # Activer pour permettre le changement de musique/ou remettre après mort ou suppr

        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(volume)  # Valeur entre 0 et 1 / Règle le volume
        sound_damaged.set_volume(0.7)
        sound_jump.set_volume(0.4)


    musicSteel()

    def load_map(path):
        fichier = open("data/"+path + ".txt", "r")
        data = fichier.read()
        fichier.close()
        data = data.split('\n')
        game_map = []
        for row in data:
            game_map.append(list(row))
        return game_map

    niveau = ['map', 'map2']

    def animation_player():
        global walkCount, attaqued, attaqued_temps

        # Si pas bougé animation standing
        if not moving_right == True and not moving_left == True and not invincible:
            # Technique que je faisais sur Processing de rien pour les services
            # Plus reste est grand et division grand plus l'animation est longue
            display.blit(player_standing_right[(walkCount % 64) // 32],
                         (player.rect.x - scroll[0], player.rect.y - scroll[1]))

        elif not moving_right == True and not moving_left == True and invincible:

            display.blit(idle_opacity[(walkCount % 24) // 4],
                         (player.rect.x - scroll[0], player.rect.y - scroll[1]))

        elif moving_right and not invincible:
            # 48 divisé par 8 = 6 images
            display.blit(player_running_right[(walkCount % 48) // 8],
                         (player.rect.x - scroll[0], player.rect.y - scroll[1]))
        elif moving_right and invincible:
            display.blit(run_right_opacity[(walkCount % 72) // 4],
                         (player.rect.x - scroll[0], player.rect.y - scroll[1]))

        elif moving_left and not invincible:
            display.blit(player_running_left[(walkCount % 48) // 8],
                         (player.rect.x - scroll[0], player.rect.y - scroll[1]))

        elif moving_left and invincible:
            display.blit(run_left_opacity[(walkCount % 72) // 4],
                         (player.rect.x - scroll[0], player.rect.y - scroll[1]))

        walkCount += 1

    def boss():
        global walkCount, time_music_fighting, boss_fighting, boss_x, boss_y, boss_rect, boss_rect_top, vie_boss, \
            time_boss_invincible, INVINCIBLE_BOSS, time_boss_death, invincible, fire_door, walkCount_Boss, \
            boss_barre_vie, volume

        if nv == 1 and vie_boss > 0:

            if not INVINCIBLE_BOSS:
                display.blit(boss_walking[(walkCount % 105) // 5], (boss_x - scroll[0], boss_y - scroll[1]))

            display.blit(fire_door[(walkCount % 80) // 5], (7530 - scroll[0], 232 - scroll[1]))

            if player.rect.x >= 7480:
                player.rect.x = 7480

            if 4800 <= player.rect.x <= 5130:
                volume -= 0.01
                pygame.mixer.music.set_volume(volume)
                print(volume)
                if volume <= 0:
                    volume = 0


            # Musique boss si player >= 5000
            if player.rect.x >= 5200:
                time_music_fighting += 0.016666
                boss_fighting = True
                volume = 0.9
                pygame.mixer.music.set_volume(volume)


                # Barre de vie du boss
                pygame.draw.rect(display, (0, 0, 0), pygame.Rect(185, 645, 910, 50))
                pygame.draw.rect(display, (245, 245, 245), pygame.Rect(190, 650, 900, 40))
                pygame.draw.rect(display, (255, 0, 0), pygame.Rect(190, 650, boss_barre_vie -100, 40))

                nom_du_boss = font_name.render("CARAPATTE DE POMPÉI", True, (0, 0, 0))
                display.blit(nom_du_boss, (400, 606.5))


                if vie_boss == 3:
                    boss_barre_vie = 1000
                if vie_boss == 2:
                    boss_barre_vie = 666
                if vie_boss == 1:
                    boss_barre_vie = 333

            if boss_fighting and time_music_fighting < 0.03:
                music_fighting_sound = pygame.mixer.music.load('data/audio/monster-house-pokemon1.mp3')
                pygame.mixer.music.play(-1)

            '''AGGRO ET MOUVEMENT DU BOSS'''
            if boss_x >= 5000 and player.rect.x <= boss_x and not INVINCIBLE_BOSS:
                display.blit(boss_walking[(walkCount % 105) // 5], (boss_x - scroll[0], boss_y - scroll[1]))
                if player.rect.x >= boss_x - 700 and not INVINCIBLE_BOSS:  # Range aggro
                    boss_rect.x -= 4
                    boss_x -= 4

            elif boss_x <= 6950 and player.rect.x > boss_x + 300 and not INVINCIBLE_BOSS:
                display.blit(boss_walking_right[(walkCount % 105) // 5], (boss_x - scroll[0], boss_y - scroll[1]))
                if player.rect.x >= boss_x - 700 and not INVINCIBLE_BOSS:
                    boss_x += 3.5
                    boss_rect.x += 3.5

            # Temps que le boss ne peux pas prendre de dégâts
            if boss_x <= player.rect.x <= boss_x + 607:
                if player.rect.y <= boss_y and player.rect.y <= boss_y + 70:

                    if not INVINCIBLE_BOSS:
                        INVINCIBLE_BOSS = True
                        vie_boss -= 1

            if INVINCIBLE_BOSS:  # Animation si le boss a été attaqué
                time_boss_invincible += 1

                # Boss si attaqué et gauche position
                if boss_x >= 5000 and player.rect.x <= boss_x:
                    display.blit(boss_opacity[(walkCount % 50) // 5], (boss_x - scroll[0], boss_y - scroll[1]))
                    boss_x -= 2
                    boss_rect.x -= 2

                # Droite position
                elif boss_x <= 6950 and player.rect.x > boss_x + 300:
                    display.blit(boss_opacity_right[(walkCount % 50) // 5], (boss_x - scroll[0], boss_y - scroll[1]))
                    boss_x += 2
                    boss_rect.x += 2
                else:
                    display.blit(boss_opacity[(walkCount % 50) // 5], (boss_x - scroll[0], boss_y - scroll[1]))

            if time_boss_invincible > 140:
                INVINCIBLE_BOSS = False
                time_boss_invincible = 0

            if boss_x <= player.rect.x <= boss_x + 607 and \
                    player.rect.y >= boss_y - 200 and player.rect.y >= boss_y and INVINCIBLE_BOSS == False:

                if not invincible:
                    player.vie -= 1
                    invincible = True

        # Mort du BOSS
        elif nv == 1 and vie_boss <= 0:
            # Animation mort du Boss
            time_boss_death += 0.016666
            if time_boss_death < 3.2:
                display.blit(boss_defeated[(walkCount_Boss % 260) // 10], (boss_x - scroll[0], boss_y - scroll[1]))
            if time_boss_death > 3.2:
                display.blit(boss_defeated[25], (boss_x - scroll[0], boss_y - scroll[1]))

            walkCount_Boss += 1

    def animation_monster():
        global walkCount
        # Animation du monster 1

        if player.rect.x > monster1_rect.x:
            if nv == 0:
                display.blit(monster1_running_right[(walkCount % 64) // 8],
                            (monster1_rect.x - scroll[0], monster1_rect.y - scroll[1]))
            if nv == 1:
                display.blit(monster_3_walking_right[(walkCount % 64) // 8],
                             (monster1_rect.x - scroll[0], monster1_rect.y - scroll[1]))

            # range aggro
            if player.rect.x >= monster1_rect.x + 900:
                # Permet un déclenchement à partir d'une distance (comme les zombies de Minecraft)
                ennemie_movement[0] = 0
            else:
                ennemie_movement[0] = 4

        elif player.rect.x < monster1_rect.x:
            if nv == 0:

                display.blit(monster1_running_left[(walkCount % 64) // 8],
                             (monster1_rect.x - scroll[0], monster1_rect.y - scroll[1]))
            if nv == 1:
                display.blit(monster_3_walking_left[(walkCount % 64) // 8],
                             (monster1_rect.x - scroll[0], monster1_rect.y - scroll[1]))

            if player.rect.x < monster1_rect.x - 900:
                ennemie_movement[0] = 0
            else:
                ennemie_movement[0] = -4

        elif player.rect.x == monster1_rect.x:

            if nv == 0:
                display.blit(monster1_running_left[(walkCount % 64) // 8],
                             (monster1_rect.x - scroll[0], monster1_rect.y - scroll[1]))
                ennemie1_2_movement[0] = 0

            if nv == 1:
                display.blit(monster_3_walking_right[(walkCount % 64) // 8],
                             (monster1_rect.x - scroll[0], monster1_rect.y - scroll[1]))
                ennemie_movement[0] = 0

        # ----------------- Il faut trouver une solution plus opti applicable à tout les monstres

        if player.rect.x > monster1_2rect.x:
            if nv == 0:
                display.blit(monster1_running_right[(walkCount % 64) // 8],
                             (monster1_2rect.x - scroll[0], monster1_2rect.y - scroll[1]))
            if nv == 1:
                display.blit(monster_3_walking_right[(walkCount % 64) // 8],
                             (monster1_2rect.x - scroll[0], monster1_2rect.y - scroll[1]))

            if player.rect.x >= monster1_2rect.x + 900:
                ennemie1_2_movement[0] = 0
            else:
                ennemie1_2_movement[0] = 4

        elif player.rect.x < monster1_2rect.x:
            if nv == 0:
                display.blit(monster1_running_left[(walkCount % 64) // 8],
                             (monster1_2rect.x - scroll[0], monster1_2rect.y - scroll[1]))
            if nv == 1:
                display.blit(monster_3_walking_left[(walkCount % 64) // 8],
                             (monster1_2rect.x - scroll[0], monster1_2rect.y - scroll[1]))

            if player.rect.x < monster1_2rect.x - 900:
                ennemie1_2_movement[0] = 0
            else:
                ennemie1_2_movement[0] = -4

        elif player.rect.x == monster1_2rect.x:
            if nv == 0:
                display.blit(monster1_running_left[(walkCount % 64) // 8],
                             (monster1_2rect.x - scroll[0], monster1_2rect.y - scroll[1]))
                ennemie1_2_movement[0] = 0
            if nv == 1:
                display.blit(monster_3_walking_left[(walkCount % 64) // 8],
                             (monster1_2rect.x - scroll[0], monster1_2rect.y - scroll[1]))

    # ------------------------------------------------------------------

    def reset_level():
        global number_tries, monster, ACTIVATION, timer, boss_x, monstre1_posx, monstre1_posy, monstre2_posx, \
            monstre2_posy, vie_boss, time_boss_death, INVINCIBLE_BOSS, boss_fighting, time_music_fighting, \
            walkCount_Boss, VICTOIRE

        player.restart_position()
        monster = Monster()
        vie_boss = 3
        boss_x = 6500
        boss_rect.x = 6500
        ACTIVATION = False
        VICTOIRE = False
        time_boss_death = 0
        walkCount_Boss = 0
        pygame.mixer.stop()
        pygame.mixer.music.load("data/audio/CODEX.mp3")
        INVINCIBLE_BOSS = False
        boss_fighting = False
        time_music_fighting = 0
        player.air_timer = 0
        player.gravity = 0
        timer = 0
        player.vie = 3
        number_tries += 1
        loop()


        monster1_rect.x, monster1_rect.y = 1800, 550
        monster1_2rect.x, monster1_2rect.y = 3100, 250

    def level_up():
        global VICTOIRE, number_tries, timer, nv, monstre2_posy, monstre2_posx, monstre1_posx, monstre1_posy, boss_x, \
            monster, vie_boss, player

        monster1_rect.x, monster1_rect.y = 1800, 550
        monster1_2rect.x, monster1_2rect.y = 3100, 250
        vie_boss = 3
        VICTOIRE = False
        nv += 1
        number_tries = 1
        player.restart_position()
        monster = Monster()
        timer = 0
        player.air_timer = 0
        player.vie = 3

    def menu():
        global START_GAME, position_Bx, position_B2x, walkCount, time_particles, walkCount_vulcan, time_vulcan

        display.blit(background_night_image, (0 - (scroll[0] / 5), 0))  # Background 2
        display.blit(background_inverse_night_image, (1920 - (scroll[0] / 5), 0))
        display.blit(background_night_image, (3840 - (scroll[0] / 5), 0))
        display.blit(background_inverse_night_image, (5760 - (scroll[0] / 5), 0))

        time_particles += 0.01666

        if time_particles >= 3:
            display.blit(particles_electro[(walkCount % 45) // 5], (600, 270))
            walkCount += 1

        # Temps entre chaque séquences de particules (1 dure 0.666s)
        if time_particles >= 4.3334:
            time_particles = 0
            if walkCount >= 45:
                walkCount = 0

        # Déplacement du menu
        scroll[0] += 5

        display.blit(menu_title, (320, 40))
        display.blit(menu_jouer, (jouerx, jouery))

    def lava_touch():
        global number_tries, monster, ACTIVATION, timer, time_music_fighting

        # Position du lac de lave
        if nv == 1 and 4210 <= player.rect.x < 5410:
            if 560 <= player.rect.y < 660 and not VICTOIRE:
                player.restart_position()
                monster = Monster()

                ACTIVATION = False
                timer = 0
                player.vie = 3
                number_tries += 1
                time_music_fighting = 0
                loop()

    def save_score():
        global score_write

        if nv == 0 and score_write:
            score_save = open("data/World_Record.txt", 'a')
            score_save.write(f'TEMPS SUR LE NIVEAU 1 : {round(timer, 3)}s / VIE RESTANTES : {player.vie}'
                             f" / NOMBRE DE TENTATIVES : {number_tries}\n")
            score_write = False

        if nv == 1 and score_write:
            score_save = open("data/World_Record.txt", 'a')
            score_save.write(f'TEMPS SUR LE NIVEAU 2 : {round(timer, 3)}s / VIE RESTANTES : {player.vie}'
                             f" / NOMBRE DE TENTATIVES : {number_tries}\n")
            score_write = False

    def collision_test(rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(rect, movement, tiles):
        # Axe x collsion droite gauche
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        rect.x += movement[0]
        hit_list = collision_test(rect, tiles)
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True
        # Axe y collision haut et bas
        rect.y += movement[1]
        hit_list = collision_test(rect, tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        return rect, collision_types

    # Pas de mouvement de base
    moving_right = False
    moving_left = False

    enemies_gravity = 0

    # position de départ + hitbox

    monster1_rect = pygame.Rect(monstre1_posx, monstre1_posy, player.image.get_width(), player.image.get_height() - 18)
    monster1_2rect = pygame.Rect(monstre2_posx, monstre2_posy, player.image.get_width(), player.image.get_height() - 18)

    # -18 pour mieux régler la hitbox

    # --------------------------------------------------------------------------------

    while True:  # game loop

        game_map = load_map(niveau[nv])

        if START_GAME == 0:
            pygame.mouse.set_visible(255)
            menu()

        if START_GAME == 1:
            pygame.mouse.set_visible(0)

            if nv == 0:
                display.blit(background_mountain, (-200 - (scroll[0] / 5), -110))  # Background
                display.blit(background_mountain_inversed, (2200 - (scroll[0] / 5), -110))

            elif nv == 1:
                display.blit(background_vulcan[0], (0 - (scroll[0] / 5), -310))
                display.blit(background_vulcan_inverse[0], (2400 - (scroll[0] / 5), -310))

                time_vulcan += 0.016666

                if time_vulcan >= 4:
                    display.blit(background_vulcan[(walkCount_vulcan % 192) // 12], (0 - (scroll[0] / 5), -310))
                    display.blit(background_vulcan_inverse[(walkCount_vulcan % 160) // 10],
                                 (2400 - (scroll[0] / 5), -310))
                    display.blit(background_vulcan[(walkCount_vulcan % 192) // 12], (4800 - (scroll[0] / 5), -310))

                    walkCount_vulcan += 1
                if time_vulcan >= 7.2:
                    time_vulcan = 0
                    if walkCount_vulcan >= 200:
                        walkCount_vulcan = 0

            boss_rect = pygame.Rect(boss_x, boss_y, 607, 394)

            # Permet de changer alpha, couleurs
            # player_image.fill((255, 255, 255, 255), special_flags=BLEND_RGBA_MULT)

            if player.vie == 3:
                display.blit(barre_fullvie_image, (45, 25))
            if player.vie == 2:
                display.blit(barre2vie_image, (45, 25))
            if player.vie == 1:
                display.blit(barre1vie_image, (45, 25))
            if player.vie == 0:
                display.blit(barrevie_image, (45, 25))

            # Le joueur est suivi par la caméra
            scroll[0] += (player.rect.x - scroll[0] - 510) / 6  # -540 moitié de 1080 pour caméra au centre
            if scroll[0] <= 75:
                scroll[0] = 75

            scroll[1] += (player.rect.y - scroll[1] - 480) / 10
            if scroll[1] <= 100:
                scroll[1] = 100

            if nv == 0 and scroll[0] >= 4700:
                scroll[0] = 4700
            elif nv == 1 and scroll[0] >= 6800:
                scroll[0] = 6800

            # --------------------------------------------------------------------
            # Permettant un temps d'attente entre chaque jump
            temps_jump += 1

            if temps_jump >= 65:
                sound = False
                temps_jump = 0
            # ----------------------------------------------------------------------
            tile_mort = []
            tile_rects = []
            y = 0

            for row in game_map:
                # Analyse les lignes pour types de tuiles
                x = 0
                for tile in row:
                    if tile == '1':
                        # Tailles de tuiles en fonction de x et y pour bien coller
                        display.blit(dirt_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == '2':
                        display.blit(grass_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                        # Rajouter ici pour plus de tuiles différentes
                    if tile == "3":  # Grass arrondi
                        display.blit(grasscarre_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == "&":
                        display.blit(grass_oblique_D1, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == "4":  # Grass arrondi
                        display.blit(panneau_droite_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == "5":  # case mystere
                        display.blit(case_mystere_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == "6":  # water1
                        display.blit(water1_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == "7":  # waterblock
                        display.blit(water_block_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == '8':  # grass droit
                        display.blit(grass_droit_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == "9":  # grass gauche
                        display.blit(grass_gauche_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == "D":
                        display.blit(grass_dalle_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == "P":
                        display.blit(pont_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == "L":
                        display.blit(lave_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == "l":
                        display.blit(laveblock_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == "w":  # porte mid open
                        display.blit(door_openmid_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == "W":  # porte haut open
                        display.blit(door_opentop_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == 'f':
                        display.blit(plant_green_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == 'E':
                        display.blit(exit_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                    if tile == 'B':
                        display.blit(brown_tile1, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == 'b':
                        display.blit(brown_tile2, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == 'C':
                        display.blit(brown_tile3, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == 'c':
                        display.blit(brown_tile5, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == ':':
                        display.blit(brown_tile6, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == '/':
                        display.blit(brown_tile7, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == '!':
                        display.blit(brown_tile8, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                    if tile == 'y':
                        display.blit(brown_tile10, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                        # Si ce c'est pas 0 alors hitbox
                    if tile == "R":  # Block invisible
                        tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    if tile != '0' and tile != "6" and tile != '4' and tile != "w" and tile != 'W' \
                            and tile != 'f' and tile != 'E' and tile != "L":  # Ceux là n'ont pas de hitbox
                        tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                        # Block de la mort
                    if tile == 'M':
                        tile_mort.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

                    x += 1
                y += 1

            # Pics
            spikes_rect1 = pygame.Rect(2990, 370, 131, 52)
            display.blit(spikes, (2990 - scroll[0], 370 - scroll[1]))

            spikes_collision = [spikes_rect1]

            if nv == 1:
                spikes_rect2 = pygame.Rect(3508, 720, 131, 52)
                display.blit(spikes, (3508 - scroll[0], 720 - scroll[1]))
                spikes_collision.append(spikes_rect2)

            # -------------------------------------------------------------

            # Vitesse du joueur ou vélocité pour plus de steel
            player_movement = [0, 0]
            ennemie_movement = [0, 0]
            ennemie1_2_movement = [0, 0]

            animation_monster()
            if moving_right:
                player_movement[0] += 6.2  # vitesse x
            if moving_left:
                player_movement[0] -= 6.2  # vitesse -x
                # Momentum et gravite pareil

            player_movement[1] += player.gravity
            ennemie1_2_movement[1] += enemies_gravity
            ennemie_movement[1] += enemies_gravity

            player.gravity += 0.60  # chute / gravité, plus la valeur est basse moins il y a de gravité
            enemies_gravity += 0.80

            # Vitesse du retomber
            if player.gravity > 40:
                player.gravity = 5

            if enemies_gravity > 1:
                enemies_gravity = 6

            monster1_rect, collisions = move(monster1_rect, ennemie_movement, tile_rects)
            monster1_2rect, collisions = move(monster1_2rect, ennemie1_2_movement, tile_rects)

            # Toujours mettre le personnage en dernier
            player.rect, collisions = move(player.rect, player_movement, tile_rects)

            # ------------------------------------------------------
            if player.rect.colliderect(monster1_rect) or player.rect.colliderect(monster1_2rect) \
                    or player.rect.collidelistall(spikes_collision):

                if not invincible:
                    player.vie -= 1
                    invincible = True

            if invincible:
                temps_invincible += 1

            if temps_invisible > 0:
                temps_invisible -= -1

            if temps_invincible > 60:
                invincible = False
                temps_invincible = 0

            if cheating:  # Code cheat
                player.vie = 3

            # Quand le joueur n'a plus de vie
            if player.vie <= 0:
                temps_invincible = 0
                invincible = False

                reset_level()
                musique_menu = pygame.mixer.music.load("data/audio/CODEX.mp3")

            if ACTIVATION:
                timer += 0.01666
            text_timer = font_HR.render(f'{round(timer, 1)}s', True, (0, 0, 0))
            display.blit(text_timer, (1120, 10))

            # ----------------------------------------------------------------

            # Collision avec le bas chute
            if collisions['bottom']:
                player.gravity = 0

                player.air_timer = 0
            else:
                player.air_timer += 0.4
            # Affiche le personnage

            boss()

            animation_player()

            # Position porte de la victoire
            if 5700 <= player.rect.x < 5800 and nv == 0:
                if 300 <= player.rect.y < 600 and VICTOIRE == False:
                    score_write = True
                    VICTOIRE = True
            elif 7880 <= player.rect.x < 7960 and nv == 1:
                if 300 <= player.rect.y < 600 and VICTOIRE == False:
                    score_write = True
                    VICTOIRE = True

            lava_touch()
            save_score()

            if VICTOIRE and nv != 1:
                text_win = font.render("Victoire", True, (255, 0, 0))
                text_instruction_win = font_HR.render("UP pour continuer", True, (0, 0, 0))
                display.blit(text_win, (320, 150))
                display.blit(text_instruction_win, (480, 360))
                ACTIVATION = False
                moving_right = False
                moving_left = False

            if VICTOIRE and nv == 1:
                text_win_game = font_end.render("BRAVO FIN DU JEU", True, (255, 0, 0))
                text_win_game_up = font_HR.render("UP pour recommencer", True, (0, 0, 0))
                display.blit(text_win_game, (120, 200))
                display.blit(text_win_game_up, (460, 340))
                ACTIVATION = False
                moving_right = False
                moving_left = False

        # ------------------------------------------------------------------------------
        for event in pygame.event.get():  # event loop
            if event.type == QUIT:
                pygame.quit()  # stop pygame
                sys.exit()  # stop le script

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Restart de la partie mais pas du jeu
                if event.key == K_DELETE:
                    reset_level()

            # Appuyez sur UP
            if VICTOIRE and not nv == 1:
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        level_up()
                        break

            if VICTOIRE and nv == 1:
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        nv = 0
                        reset_level()

            if not VICTOIRE:
                if event.type == KEYDOWN:  # Si touche pressé
                    if START_GAME == 1:
                        ACTIVATION = True

                    if event.key == K_RIGHT:  # Si touche droite pressé
                        moving_right = True  # Activation du mouvement

                    if event.key == K_LEFT:
                        moving_left = True

                    if event.key == K_SPACE:
                        if not sound:
                            sound_jump.play()
                            sound = True

                        if player.air_timer < 1:
                            player.gravity = -15
                    if nv == 0:
                        if event.key == K_END:
                            player.rect.x = 5500
                        if event.key == K_p:
                            cheating = True
                    elif nv == 1:
                        if event.key == K_END:
                            player.rect.x = 7400
                        if event.key == K_p:
                            cheating = True

                if event.type == KEYUP:
                    if event.key == K_RIGHT:
                        moving_right = False  # désactivation du mouvement
                    if event.key == K_LEFT:
                        moving_left = False

            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # Now it will have the coordinates of click point.
                if jouer_position.collidepoint(mouse_pos):
                    START_GAME = 1

                    # Activer pour chnager de musique menu/game
                    '''musique_fond = pygame.mixer.music.load("data/audio/coromusique.mp3")
                    pygame.mixer.music.play(-1)'''

        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()  # update
        clock.tick(FPS)  # 60 fps


if __name__ == "__main__":
    player = Player()
    monster = Monster()
    loop()

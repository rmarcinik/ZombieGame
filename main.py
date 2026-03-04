import pygame, random, sys, os

CELL = 30
COLS = ROWS = 20
W = H = COLS * CELL
ZOMBIE_DELAY = 140
INTRO, PLAYING, WON, LOST = range(4) # TODO Enum?
sign = lambda x: (1 if x > 0 else -1 if x < 0 else 0)


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Dead Escape")
    clock = pygame.time.Clock()

    ROOT = os.path.dirname(os.path.abspath(__file__))
    img  = lambda n: pygame.image.load(os.path.join(ROOT, "images", n)).convert_alpha()
    snd  = lambda n: pygame.mixer.Sound(os.path.join(ROOT, "sounds", n))

    bg = pygame.Surface((W, H))
    tile = img("Cell.gif")
    for r in range(ROWS):
        for c in range(COLS):
            bg.blit(tile, (c * CELL, r * CELL))

    hero_imgs   = [img("Hero.gif"),       img("Hero2.gif")]
    dead_imgs   = [img("ZombieHero.gif"), img("ZombieHero2.gif")]
    zombie_imgs = [img("Zombie.gif"),     img("Zombie2.gif")]
    pile_img    = img("ZombiePile2.gif")
    intro_img   = img("introscreen.gif")
    win_img     = img("winscreen.gif")
    over_img    = img("gameover.png")

    snd_die  = snd("die.wav")
    snd_lose = snd("lose.wav")
    snd_win  = snd("win.wav")

    font = pygame.font.SysFont(None, 16)

    state      = INTRO
    hero       = [9, 9]
    hero_alive = True
    zombies    = []
    piles      = set()
    steps      = 0
    zombie_q   = []
    z_timer    = 0
    anim, anim_t = 0, 0
    prev_dir   = None   # direction saved after last zombie turn; None = zombies skip
    pending_dir = None  # direction pressed this turn, becomes prev_dir after zombies move
    z_target   = (0, 0) # tile zombies chase this turn

    def new_game():
        nonlocal state, hero_alive, steps, z_timer, prev_dir, pending_dir
        state = PLAYING
        hero[:] = [9, 9]
        hero_alive = True
        zombies[:] = [[random.randrange(COLS), random.randrange(ROWS)] for _ in range(12)]
        piles.clear()
        zombie_q.clear()
        steps = z_timer = 0
        prev_dir = pending_dir = None

    def move_zombie(z, target):
        tx, ty = target
        z[0] = max(0, min(COLS - 1, z[0] + sign(tx - z[0])))
        z[1] = max(0, min(ROWS - 1, z[1] + sign(ty - z[1])))
        pos = (z[0], z[1])

        if pos == (hero[0], hero[1]):
            return True

        other = next((o for o in zombies if o is not z and o[0] == z[0] and o[1] == z[1]), None)
        if other:                           # Z + Z → pile
            zombies[:] = [o for o in zombies if o is not z and o is not other]
            piles.add(pos)
            snd_die.play()
        elif pos in piles:                  # Z + pile → both gone
            zombies[:] = [o for o in zombies if o is not z]
            piles.discard(pos)
            snd_die.play()
        return False

    while True:
        dt = clock.tick(60)
        anim_t += dt
        if anim_t > 400:
            anim ^= 1
            anim_t = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if state in (INTRO, WON, LOST):
                    new_game()
                elif state == PLAYING and not zombie_q and hero_alive:
                    dx = dy = 0
                    moved = True
                    if   event.key == pygame.K_LEFT:  dx = -1
                    elif event.key == pygame.K_RIGHT: dx =  1
                    elif event.key == pygame.K_UP:    dy = -1
                    elif event.key == pygame.K_DOWN:  dy =  1
                    elif event.key == pygame.K_SPACE:
                        hero[:] = [random.randrange(COLS), random.randrange(ROWS)]
                    else:
                        moved = False

                    if moved:
                        old_pos = (hero[0], hero[1])
                        if dx or dy:
                            hero[0] = max(0, min(COLS - 1, hero[0] + dx))
                            hero[1] = max(0, min(ROWS - 1, hero[1] + dy))
                            steps += 1
                        hpos = (hero[0], hero[1])
                        if any(o[0] == hpos[0] and o[1] == hpos[1] for o in zombies) or hpos in piles:
                            hero_alive = False
                            snd_lose.play()
                            state = LOST
                        else:
                            cur_dir = (dx, dy) if (dx or dy) else prev_dir
                            if prev_dir:
                                z_target = (
                                    max(0, min(COLS - 1, old_pos[0] + prev_dir[0])),
                                    max(0, min(ROWS - 1, old_pos[1] + prev_dir[1])),
                                )
                                zombie_q[:] = list(zombies)
                                pending_dir = cur_dir   # saved after zombies finish
                            else:
                                prev_dir = cur_dir      # first move: no zombies, save now

        if state == PLAYING and zombie_q:
            z_timer += dt
            if z_timer >= ZOMBIE_DELAY:
                z_timer = 0
                z = zombie_q.pop(0)
                if any(o is z for o in zombies):
                    if move_zombie(z, z_target):
                        hero_alive = False
                        snd_lose.play()
                        state = LOST
                        zombie_q.clear()
            if not zombie_q and state == PLAYING:
                prev_dir = pending_dir          # save direction after zombies finish
                if not zombies:
                    snd_win.play()
                    state = WON

        screen.blit(bg, (0, 0))

        if state != INTRO:
            for pos in piles:
                screen.blit(pile_img, (pos[0] * CELL, pos[1] * CELL))
            for z in zombies:
                screen.blit(zombie_imgs[anim], (z[0] * CELL, z[1] * CELL))
            hi = hero_imgs if hero_alive else dead_imgs
            screen.blit(hi[anim], (hero[0] * CELL, hero[1] * CELL))
            screen.blit(font.render(str(steps), True, (220, 220, 220)),
                        (hero[0] * CELL + 18, hero[1] * CELL + 18))

        if state == INTRO:
            screen.blit(intro_img, intro_img.get_rect(center=(W // 2, H // 2)))
        elif state == WON:
            screen.blit(win_img,   win_img.get_rect(center=(W // 2, H // 2)))
        elif state == LOST:
            screen.blit(over_img,  over_img.get_rect(center=(W // 2, H // 2)))

        pygame.display.flip()


if __name__ == "__main__":
    main()

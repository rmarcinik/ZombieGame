import pygame, random, sys, os
from dataclasses import dataclass, field
from enum import Enum, auto

CELL = 30
COLS = ROWS = 20
W = H = COLS * CELL
ZOMBIE_DELAY = 140

class Mode(Enum):
    INTRO = auto(); PLAYING = auto(); WON = auto(); LOST = auto()

sign  = lambda x: (x > 0) - (x < 0)
clamp = lambda v, lo, hi: max(lo, min(hi, v))
px    = lambda pos: (pos[0] * CELL, pos[1] * CELL)

KEYS = {pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0),
        pygame.K_UP:   (0, -1), pygame.K_DOWN:  (0, 1)}


@dataclass
class State:
    mode:        Mode  = Mode.INTRO
    hero:        list  = field(default_factory=lambda: [9, 9])
    alive:       bool  = True
    zombies:     list  = field(default_factory=list)
    piles:       set   = field(default_factory=set)
    steps:       int   = 0
    z_q:         list  = field(default_factory=list)
    z_timer:     int   = 0
    prev_dir:    tuple = None
    pending_dir: tuple = None
    z_target:    tuple = (0, 0)
    anim:        int   = 0
    anim_t:      int   = 0


def load_assets(root):
    img = lambda n: pygame.image.load(os.path.join(root, "images", n)).convert_alpha()
    snd = lambda n: pygame.mixer.Sound(os.path.join(root, "sounds", n))
    tile = img("Cell.gif")
    bg   = pygame.Surface((W, H))
    for r in range(ROWS):
        for c in range(COLS):
            bg.blit(tile, (c * CELL, r * CELL))
    return (
        dict(bg=bg, pile=img("ZombiePile2.gif"),
             intro=img("introscreen.gif"), win=img("winscreen.gif"), over=img("gameover.png"),
             hero  =[img("Hero.gif"),        img("Hero2.gif")],
             dead  =[img("ZombieHero.gif"),  img("ZombieHero2.gif")],
             zombie=[img("Zombie.gif"),       img("Zombie2.gif")],
             font  =pygame.font.SysFont(None, 16)),
        dict(die=snd("die.wav"), lose=snd("lose.wav"), win=snd("win.wav")),
    )


def new_game(s):
    s.mode, s.alive, s.steps, s.z_timer = Mode.PLAYING, True, 0, 0
    s.hero[:] = [9, 9]
    s.zombies[:] = [[random.randrange(COLS), random.randrange(ROWS)] for _ in range(12)]
    s.piles.clear(); s.z_q.clear()
    s.prev_dir = s.pending_dir = None


def move_zombie(s, z, snd_die):
    z[0] = clamp(z[0] + sign(s.z_target[0] - z[0]), 0, COLS - 1)
    z[1] = clamp(z[1] + sign(s.z_target[1] - z[1]), 0, ROWS - 1)
    pos  = (z[0], z[1])
    if pos == (s.hero[0], s.hero[1]):
        return True
    other = next((o for o in s.zombies if o is not z and (o[0], o[1]) == pos), None)
    if other:
        s.zombies[:] = [o for o in s.zombies if o is not z and o is not other]
        s.piles.add(pos);   snd_die.play()
    elif pos in s.piles:
        s.zombies[:] = [o for o in s.zombies if o is not z]
        s.piles.discard(pos); snd_die.play()
    return False


def handle_input(s, event, snd):
    if event.type == pygame.QUIT:
        sys.exit()
    if event.type != pygame.KEYDOWN:
        return
    if s.mode in (Mode.INTRO, Mode.WON, Mode.LOST):
        new_game(s); return
    if s.mode != Mode.PLAYING or s.z_q or not s.alive:
        return

    dx, dy = KEYS.get(event.key, (0, 0))
    if event.key == pygame.K_SPACE:
        s.hero[:] = [random.randrange(COLS), random.randrange(ROWS)]
    elif not (dx or dy):
        return

    old = (s.hero[0], s.hero[1])   # capture after possible teleport
    if dx or dy:
        s.hero[0] = clamp(s.hero[0] + dx, 0, COLS - 1)
        s.hero[1] = clamp(s.hero[1] + dy, 0, ROWS - 1)
        s.steps += 1

    hpos = (s.hero[0], s.hero[1])
    if any((z[0], z[1]) == hpos for z in s.zombies) or hpos in s.piles:
        s.alive, s.mode = False, Mode.LOST
        snd['lose'].play(); return

    cur_dir = (dx, dy) if (dx or dy) else s.prev_dir
    if s.prev_dir:
        s.z_target    = (clamp(old[0] + s.prev_dir[0], 0, COLS-1),
                         clamp(old[1] + s.prev_dir[1], 0, ROWS-1))
        s.z_q[:]      = list(s.zombies)
        s.pending_dir = cur_dir
    else:
        s.prev_dir = cur_dir


def update(s, dt, snd):
    s.anim_t += dt
    if s.anim_t > 400:
        s.anim ^= 1; s.anim_t = 0

    if s.mode == Mode.PLAYING and s.z_q:
        s.z_timer += dt
        if s.z_timer >= ZOMBIE_DELAY:
            s.z_timer = 0
            z = s.z_q.pop(0)
            if any(o is z for o in s.zombies) and move_zombie(s, z, snd['die']):
                s.alive, s.mode = False, Mode.LOST
                snd['lose'].play(); s.z_q.clear()
        if not s.z_q and s.mode == Mode.PLAYING:
            s.prev_dir = s.pending_dir
            if not s.zombies:
                snd['win'].play(); s.mode = Mode.WON


def draw(screen, s, a):
    screen.blit(a['bg'], (0, 0))
    if s.mode != Mode.INTRO:
        for pos in s.piles:
            screen.blit(a['pile'], px(pos))
        for z in s.zombies:
            screen.blit(a['zombie'][s.anim], px(z))
        screen.blit((a['hero'] if s.alive else a['dead'])[s.anim], px(s.hero))
        screen.blit(a['font'].render(str(s.steps), True, (220, 220, 220)),
                    (s.hero[0] * CELL + 18, s.hero[1] * CELL + 18))
    overlay = {Mode.INTRO: 'intro', Mode.WON: 'win', Mode.LOST: 'over'}.get(s.mode)
    if overlay:
        img = a[overlay]
        screen.blit(img, img.get_rect(center=(W//2, H//2)))
    pygame.display.flip()


def main():
    pygame.init(); pygame.mixer.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Dead Escape")
    clock  = pygame.time.Clock()
    assets, snd = load_assets(os.path.dirname(os.path.abspath(__file__)))
    s = State()
    while True:
        dt = clock.tick(60)
        for event in pygame.event.get():
            handle_input(s, event, snd)
        update(s, dt, snd)
        draw(screen, s, assets)


if __name__ == "__main__":
    main()

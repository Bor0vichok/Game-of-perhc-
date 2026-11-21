import json
import math
import random
import socket
import sys
import threading
import pygame

pygame.init()
pygame.font.init()

W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Underwater World")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 16)

WATER = 500
WORLD_WIDTH = 3600
WORLD_HEIGHT = 2400
WOOD_START_X, WOOD_END_X = 1800, 2200
LAIR_X = 200

GAME_PORT = 5555
DISCOVERY_PORT = 5556


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip, _ = s.getsockname()
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def get_bottom_y(world_x):
    if world_x < 900:
        t = world_x / 900.0
        return int(950 + (1350 - 950) * (math.sin(t * math.pi / 2)))
    elif 900 <= world_x <= 1700:
        t = (world_x - 900) / 800.0
        return int(1350 + 90 * (math.sin(t * math.pi)))
    elif 1700 < world_x < 2200:
        return 1350
    elif 2200 <= world_x <= 2930:
        t = (world_x - 2200) / 730.0
        return int(1350 + 100 * (math.sin(t * math.pi)))
    elif 2930 < world_x <= 3100:
        t = (world_x - 2930) / 170.0
        return int(1420 - 420 * (math.sin(t * math.pi / 2)))
    else:
        return 1000


class Particle:
    def __init__(self, x, y, vx, vy, color, is_silt=False, is_bubble=False):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.color, self.is_silt, self.is_bubble = color, is_silt, is_bubble
        self.lifetime = random.randint(40, 80) if is_silt else random.randint(20, 60)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.is_silt:
            self.vx *= 0.95
            self.vy *= 0.95
            self.vy += 0.02
        elif self.is_bubble:
            self.vy -= 0.05
            self.vx += random.uniform(-0.1, 0.1)
        else:
            self.vy += 0.2
        self.lifetime -= 1

    def draw(self, cam_x, cam_y):
        sx, sy = int(self.x - cam_x), int(self.y - cam_y)
        if 0 <= sx <= W and 0 <= sy <= H and self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (sx, sy), random.randint(2, 4), 1 if self.is_bubble else 0)
def draw_world_scenery(cam_x, cam_y, algae_timer):
    for bx, w_w in ((WOOD_START_X, 30), (WOOD_START_X + 140, 25), (WOOD_END_X - 100, 35)):
        b_y = get_bottom_y(bx)
        h = b_y - 200
        s_bx, s_h, s_by = int(bx - cam_x), int(h - cam_y), int(b_y - cam_y)
        pygame.draw.rect(screen, (55, 38, 22), (s_bx, s_h, w_w, s_by - s_h))
        pygame.draw.line(screen, (55, 38, 22), (s_bx + w_w // 2, s_h + 20), (s_bx - 60, s_h - 40), 8)
        pygame.draw.line(screen, (55, 38, 22), (s_bx + w_w // 2, s_h + 50), (s_bx + 70, s_h - 30), 6)

    for cx in range(10, 950, 35):
        b_y = get_bottom_y(cx)
        s_cx, s_by = int(cx - cam_x), int(b_y - cam_y)
        if -50 <= s_cx <= W + 50:
            points = ((s_cx, s_by), (s_cx - 10, s_by - 80), (s_cx + 5, s_by - 170), (s_cx - 2, s_by - 230))
            pygame.draw.lines(screen, (50, 110, 50), False, points, 4)
            pygame.draw.ellipse(screen, (90, 55, 30), (s_cx - 7, s_by - 210, 10, 35))

    for sedge_x in range(3100, 3600, 20):
        b_y = get_bottom_y(sedge_x)
        s_sx, s_sy = int(sedge_x - cam_x), int(b_y - cam_y)
        if -30 <= s_sx <= W + 30:
            w = math.sin(algae_timer * 0.05 + sedge_x) * 12
            pts = ((s_sx, s_sy), (s_sx + int(w * 0.5), s_sy - 90), (s_sx + int(w), s_sy - 180))
            pygame.draw.lines(screen, (70, 140, 45), False, pts, 3)


def draw_perch_sprite(x, y, size_x, size_y, right, cam_x, cam_y, is_p2=False, label=None):
    sx, sy = int(x - cam_x), int(y - cam_y)
    if not (-150 <= sx <= W + 150 and -150 <= sy <= H + 150):
        return
    d = 1 if right else -1
    tail_col = (60, 160, 220) if is_p2 else (220, 80, 40)
    body_col = (75, 110, 130) if is_p2 else (85, 120, 75)
    stripe_col = (30, 45, 65) if is_p2 else (40, 55, 35)

    pygame.draw.polygon(
        screen, tail_col,
        ((sx - size_x * d, sy),
         (sx - (size_x + int(size_x * 0.75)) * d, sy - int(size_y * 0.9)),
         (sx - (size_x + int(size_x * 0.5)) * d, sy),
         (sx - (size_x + int(size_x * 0.75)) * d, sy + int(size_y * 0.9)))
    )
    pygame.draw.ellipse(screen, body_col, (sx - size_x, sy - size_y, size_x * 2, size_y * 2))
    for dx in (-int(size_x * 0.4), -int(size_x * 0.1), int(size_x * 0.25)):
        pygame.draw.line(screen, stripe_col, (sx + dx * d, sy - size_y + 2), (sx + dx * d, sy + int(size_y * 0.25)), 3)
    pygame.draw.circle(screen, (0, 0, 0), (int(sx + (size_x - int(size_x * 0.33)) * d), int(sy - int(size_y * 0.25))), 3)

    if label:
        txt = small_font.render(label, True, (255, 255, 180))
        screen.blit(txt, (sx - txt.get_width() // 2, sy - size_y - 22))


class Crustacean:
    def __init__(self):
        self.x = random.randint(300, WORLD_WIDTH - 100)
        self.y = get_bottom_y(self.x)
        self.vx = random.choice((-0.4, 0.4))

    def update(self):
        self.x += self.vx
        self.y = get_bottom_y(self.x)
        if self.x < 100 or self.x > WORLD_WIDTH - 50:
            self.vx *= -1
        if random.random() < 0.01:
            self.vx *= -1

    def draw(self, cam_x, cam_y):
        sx, sy = int(self.x - cam_x), int(self.y - cam_y)
        if 0 <= sx <= W and 0 <= sy <= H:
            pygame.draw.ellipse(screen, (115, 75, 45), (sx - 7, sy - 5, 14, 8))
            pygame.draw.line(screen, (90, 55, 30), (sx, sy), (sx + (8 if self.vx > 0 else -8), sy + 3), 2)


class Plankton:
    def __init__(self):
        self.x = random.randint(50, WORLD_WIDTH - 50)
        self.y = random.randint(WATER + 30, get_bottom_y(self.x) - 30)

    def draw(self, cam_x, cam_y):
        sx, sy = int(self.x - cam_x), int(self.y - cam_y)
        if 0 <= sx <= W and 0 <= sy <= H:
            pygame.draw.circle(screen, (100, 200, 80), (sx, sy), 3)
class Fry:
    def __init__(self, group_id):
        self.group_id = group_id
        self.x = random.randint(100, WORLD_WIDTH - 200)
        self.y = random.randint(WATER + 50, get_bottom_y(self.x) - 50)
        self.vx, self.vy = random.uniform(-0.8, 0.8), random.uniform(-0.4, 0.4)

    def update(self, center_x, center_y, players, neighbors):
        nearest_p = min(players, key=lambda p: math.hypot(p.x - self.x, p.y - self.y))
        dist_p = math.hypot(nearest_p.x - self.x, nearest_p.y - self.y)
        if dist_p < 85:
            dx, dy = self.x - nearest_p.x, self.y - nearest_p.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                self.vx += (dx / dist) * 0.25
                self.vy += (dy / dist) * 0.25
        else:
            if center_x is not None and center_y is not None:
                dx, dy = center_x - self.x, center_y - self.y
                dist = math.hypot(dx, dy)
                if dist > 5:
                    self.vx += (dx / dist) * 0.2
                    self.vy += (dy / dist) * 0.2
            for n in neighbors:
                if n != self:
                    nd = math.hypot(n.x - self.x, n.y - self.y)
                    if 0 < nd < 18:
                        self.vx -= ((n.x - self.x) / nd) * 0.25
                        self.vy -= ((n.y - self.y) / nd) * 0.25

        self.vx += random.uniform(-0.15, 0.15)
        self.vy += random.uniform(-0.08, 0.08)
        max_s = 2.6 if dist_p < 85 else 1.8
        speed = math.hypot(self.vx, self.vy)
        if speed > max_s:
            self.vx, self.vy = (self.vx / speed) * max_s, (self.vy / speed) * max_s
        self.x += self.vx
        self.y += self.vy
        cb = get_bottom_y(self.x)
        if self.x < 20 or self.x > WORLD_WIDTH - 20:
            self.vx *= -1
        if self.y < WATER + 20 or self.y > cb - 20:
            self.vy *= -1

    def draw(self, cam_x, cam_y):
        sx, sy = int(self.x - cam_x), int(self.y - cam_y)
        if 0 <= sx <= W and 0 <= sy <= H:
            pygame.draw.ellipse(screen, (170, 180, 180), (sx - 6, sy - 3, 12, 6))
            td = 1 if self.vx >= 0 else -1
            pygame.draw.polygon(screen, (140, 150, 150), ((sx - 6 * td, sy), (sx - 10 * td, sy - 2), (sx - 10 * td, sy + 2)))


class Crucidian(Fry):
    def __init__(self, group_id):
        super().__init__(group_id)
        self.size_x, self.size_y = 30, 20

    def draw(self, cam_x, cam_y):
        sx, sy = int(self.x - cam_x), int(self.y - cam_y)
        if 0 <= sx <= W and 0 <= sy <= H:
            d = 1 if self.vx >= 0 else -1
            pygame.draw.polygon(
                screen, (230, 120, 40),
                ((sx - int(self.size_x * 0.8) * d, sy),
                 (sx - int(self.size_x * 1.3) * d, sy - int(self.size_y * 0.7)),
                 (sx - int(self.size_x * 1.1) * d, sy),
                 (sx - int(self.size_x * 1.3) * d, sy + int(self.size_y * 0.7)))
            )
            pygame.draw.ellipse(screen, (185, 195, 195), (sx - self.size_x, sy - self.size_y, self.size_x * 2, self.size_y * 2))
            pygame.draw.circle(screen, (0, 0, 0), (int(sx + (self.size_x * 0.6) * d), int(sy - int(self.size_y * 0.25))), 3)


class Pike:
    def __init__(self, lair_x):
        self.lair_x, self.x, self.y, self.vx, self.vy = lair_x, lair_x, get_bottom_y(lair_x) - 80, 0, 0
        self.state, self.pike_len = "inactive", 200
        self.timer = random.randint(450, 850)

    def update(self, players, crucians, brothers_list, global_mode):
        lair_y = get_bottom_y(self.lair_x) - 80
        if self.state == "inactive":
            self.x, self.y, self.vx, self.vy = self.lair_x, lair_y, 0, 0
            if global_mode == "frenzy":
                self.timer -= 1
                if self.timer <= 0:
                    self.state = "hunting"
            return

        if self.state == "hunting":
            if global_mode == "calm":
                self.state = "returning"
                return
            valid_players = [p for p in players if not p.hidden and (p.size_x * 2) <= (self.pike_len + 1)]
            targets = valid_players + [b for b in brothers_list if b.ai_state != "resting"] + crucians
            best_v, min_d = None, 9999
            for t in targets:
                d = math.hypot(t.x - self.x, t.y - self.y)
                if d < min_d:
                    min_d, best_v = d, t
            if best_v and min_d > 0:
                self.vx, self.vy = ((best_v.x - self.x) / min_d) * 5.2, ((best_v.y - self.y) / min_d) * 5.2
            else:
                self.state = "returning"

            for p in valid_players:
                if math.hypot(p.x - self.x, p.y - self.y) < (p.size_x + 12):
                    p.respawn()
                    self.state = "returning"

            for b in brothers_list[:]:
                if math.hypot(b.x - self.x, b.y - self.y) < (b.size_x + 12):
                    brothers_list.remove(b)
                    brothers_list.append(Brother(WORLD_WIDTH // 3))
                    self.state = "returning"

        elif self.state == "returning":
            dx, dy = self.lair_x - self.x, lair_y - self.y
            dist = math.hypot(dx, dy)
            if dist > 10:
                self.vx, self.vy = (dx / dist) * 5.5, (dy / dist) * 5.5
            else:
                self.state, self.timer = "inactive", random.randint(500, 1000)
        self.x += self.vx
        self.y += self.vy

    def draw(self, cam_x, cam_y):
        if self.state != "inactive":
            sx, sy = int(self.x - cam_x), int(self.y - cam_y)
            pygame.draw.ellipse(screen, (60, 90, 60), (sx - 100, sy - 25, self.pike_len, 50))
            d = 1 if self.vx >= 0 else -1
            pygame.draw.polygon(screen, (180, 100, 50), ((sx - 100 * d, sy), (sx - 135 * d, sy - 60), (sx - 115 * d, sy), (sx - 135 * d, sy + 60)))
            pygame.draw.circle(screen, (235, 190, 30), (int(sx + 75 * d), int(sy - 8)), 6)
            pygame.draw.circle(screen, (0, 0, 0), (int(sx + 75 * d), int(sy - 8)), 3)
class Catfish:
    def __init__(self):
        self.x, self.y, self.vx, self.vy, self.active, self.angle = 2500, 1350, 0, 0, False, 0
        self.size_x, self.size_y = 200, 45

    def update(self, global_mode, crucians, players, brothers_list):
        if global_mode == "calm" and self.size_x > 0:
            self.active = True
            targets = crucians[:]
            for b in brothers_list:
                if b.y > get_bottom_y(b.x) - 130:
                    targets.append(b)
            for p in players:
                if p.y > get_bottom_y(p.x) - 130 and (p.size_x * 2) <= (self.size_x * 2 + 20):
                    targets.append(p)
            best_t, min_d = None, 700
            for t in targets:
                d = math.hypot(t.x - self.x, t.y - self.y)
                if d < min_d:
                    min_d, best_t = d, t
            if best_t and min_d > 0:
                self.vx, self.vy = ((best_t.x - self.x) / min_d) * 3.4, ((best_t.y - self.y) / min_d) * 3.4
            else:
                self.angle += 0.02
                self.vx, self.vy = math.cos(self.angle) * 2.5, math.sin(self.angle * 2) * 0.8
        else:
            self.active = False
            dx, dy = 2500 - self.x, 1350 - self.y
            dist = math.hypot(dx, dy)
            if dist > 5:
                self.vx, self.vy = (dx / dist) * 4.0, (dy / dist) * 4.0
            else:
                self.vx = self.vy = 0
        self.x += self.vx
        self.y += self.vy
        cb = get_bottom_y(self.x)
        if self.y > cb - self.size_y:
            self.y = cb - self.size_y
        self.x = max(self.size_x, min(WORLD_WIDTH - self.size_x, self.x))

    def draw(self, cam_x, cam_y):
        if self.size_x <= 0:
            return
        sx, sy = int(self.x - cam_x), int(self.y - cam_y)
        pygame.draw.ellipse(screen, (45, 55, 65), (sx - self.size_x, sy - self.size_y, self.size_x * 2, self.size_y * 2))
        d = 1 if self.vx >= 0 else -1
        pygame.draw.polygon(screen, (30, 38, 45), ((sx - self.size_x * d, sy), (sx - (self.size_x + 60) * d, sy - 45), (sx - (self.size_x + 60) * d, sy + 45)))
        pygame.draw.line(screen, (20, 25, 30), (sx + (self.size_x - 30) * d, sy + 10), (sx + (self.size_x + 20) * d, sy + 35), 4)
        pygame.draw.circle(screen, (235, 190, 30), (int(sx + (self.size_x - 40) * d), int(sy - 10)), 6)
        pygame.draw.circle(screen, (0, 0, 0), (int(sx + (self.size_x - 40) * d), int(sy - 10)), 3)


class Zander:
    def __init__(self):
        self.x = random.randint(3100, 3500)
        self.y = random.randint(WATER + 30, WATER + 120)
        self.target_x = random.randint(100, WORLD_WIDTH - 100)
        self.target_y = random.randint(WATER + 30, WATER + 150)
        self.size_x, self.size_y = 50, 22
        self.vx = self.vy = 0
        self.hidden = False

    def update(self, global_mode, frys, players, pikes):
        if global_mode != "frenzy":
            if self.x < 3480:
                self.vx = 4.5
                self.x += self.vx
                if self.y < WATER + 80:
                    self.y += 1
            else:
                self.vx = 0
                self.hidden = True
            return

        self.hidden = False
        near_pike = any(p.state == "hunting" and math.hypot(p.x - self.x, p.y - self.y) < 250 for p in pikes)
        if near_pike:
            if self.x < 3420:
                self.x += 4.0
                self.vx = 4.0
            return

        targets = frys[:] + [p for p in players if int(p.size_x * 2) < 50]
        best_t, min_d = None, 500
        for t in targets:
            d = math.hypot(t.x - self.x, t.y - self.y)
            if d < min_d:
                min_d, best_t = d, t

        if best_t and min_d > 0:
            dx, dy = best_t.x - self.x, best_t.y - self.y
            self.vx = (dx / min_d) * 3.8
            self.vy = (dy / min_d) * 1.2
        else:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = math.hypot(dx, dy)
            if dist < 30:
                self.target_x = random.randint(100, WORLD_WIDTH - 100)
                self.target_y = random.randint(WATER + 25, WATER + 160)
            else:
                self.vx = (dx / dist) * 3.0
                self.vy = (dy / dist) * 0.8

        self.x += self.vx
        self.y += self.vy
        if self.y < WATER + 15:
            self.y = WATER + 15
        if self.y > WATER + 175:
            self.y = WATER + 175

    def draw(self, cam_x, cam_y):
        if self.hidden:
            return
        sx, sy = int(self.x - cam_x), int(self.y - cam_y)
        if 0 <= sx <= W and 0 <= sy <= H:
            d = 1 if self.vx >= 0 else -1
            pygame.draw.polygon(screen, (90, 100, 80), ((sx - 10 * d, sy - self.size_y), (sx + 15 * d, sy - self.size_y - 15), (sx + 25 * d, sy - self.size_y + 2)))
            pygame.draw.ellipse(screen, (120, 130, 110), (sx - self.size_x, sy - self.size_y, self.size_x * 2, self.size_y * 2))
            pygame.draw.polygon(screen, (90, 100, 80), ((sx - self.size_x * d, sy), (sx - (self.size_x + 20) * d, sy - 15), (sx - (self.size_x + 20) * d, sy + 15)))
            pygame.draw.circle(screen, (200, 205, 210), (int(sx + (self.size_x - 12) * d), int(sy - 4)), 5)
            pygame.draw.circle(screen, (0, 0, 0), (int(sx + (self.size_x - 12) * d), int(sy - 4)), 2)


class Fish:
    def __init__(self, start_x=WORLD_WIDTH // 3, is_p2=False):
        self.start_x = start_x
        self.is_p2 = is_p2
        self.respawn()

    def respawn(self):
        self.x, self.y, self.vx, self.vy, self.right, self.hidden = self.start_x, 1100, 0, 0, True, False
        self.size_x, self.size_y = 24, 15

    def update(self, target_world_pos, parts_list):
        if self.y > WATER:
            if target_world_pos is not None:
                tx, ty = target_world_pos
                dx = tx - self.x
                dy = ty - self.y
                dist = math.hypot(dx, dy)
                if dist > 5:
                    self.vx, self.vy = (dx / dist) * 4.8, (dy / dist) * 4.8
                else:
                    self.vx = self.vy = 0
            else:
                self.vx, self.vy = self.vx * 0.8, self.vy * 0.8
            if (self.vx != 0 or self.vy != 0) and random.random() < 0.15:
                parts_list.append(Particle(self.x, self.y, -self.vx * 0.2, -1, (180, 220, 240), is_bubble=True))
        else:
            self.vy, self.vx = self.vy + 0.4, self.vx * 0.98

        fy = self.y + self.vy
        if (self.y > WATER and fy <= WATER) or (self.y <= WATER and fy > WATER):
            if abs(self.vy) > 1.5:
                for _ in range(12):
                    parts_list.append(Particle(self.x, WATER, random.uniform(-2, 2), -abs(self.vy) * 0.3, (220, 240, 240)))

        self.x += self.vx
        self.y += self.vy
        if self.vx > 0.2 or self.vx < -0.2:
            self.right = self.vx > 0.2
        cb = get_bottom_y(self.x)
        self.hidden = WOOD_START_X <= self.x <= WOOD_END_X and (cb - 200) <= self.y <= cb
        if self.y > cb - self.size_y:
            if self.vy > 1.5:
                for _ in range(int(min(12, self.vy * 2))):
                    parts_list.append(Particle(self.x, cb, random.uniform(-1, 1), random.uniform(-0.5, -2), (110, 85, 60), is_silt=True))
            self.y, self.vy = cb - self.size_y, 0
        self.x = max(self.size_x, min(WORLD_WIDTH - self.size_x, self.x))

    def draw(self, cam_x, cam_y, show_label=True):
        lbl = ("Игрок 2" if self.is_p2 else "Игрок 1") if show_label else None
        draw_perch_sprite(self.x, self.y, self.size_x, self.size_y, self.right, cam_x, cam_y, self.is_p2, lbl)
class Brother(Fish):
    def __init__(self, start_x):
        super().__init__(start_x, is_p2=False)
        self.y = random.randint(WATER + 100, 1100)
        self.fry_eaten, self.rest_timer, self.ai_state = 0, 0, "hunting"

    def update_ai(self, target_list, crucians, plankton_list, pikes, crusts):
        cb = get_bottom_y(self.x)
        any_p = any(p.state == "hunting" for p in pikes)
        if any_p:
            self.ai_state = "panicked"
            dx, dy = (WOOD_START_X + WOOD_END_X) // 2 - self.x, cb - 50 - self.y
            dist = math.hypot(dx, dy)
            if dist > 20:
                self.vx, self.vy = (dx / dist) * 6.5, (dy / dist) * 6.5
            else:
                self.vx = self.vy = 0
        elif self.ai_state == "resting" or self.fry_eaten >= 6:
            if self.ai_state != "resting":
                self.ai_state = "resting"
                self.rest_timer = 300
            self.rest_timer -= 1
            dx, dy = (WOOD_START_X + WOOD_END_X) // 2 - self.x, cb - 40 - self.y
            dist = math.hypot(dx, dy)
            if dist > 20:
                self.vx, self.vy = (dx / dist) * 4.0, (dy / dist) * 4.0
            else:
                self.vx = self.vy = 0
            if self.rest_timer <= 0:
                self.fry_eaten, self.ai_state = 0, "hunting"
        elif self.ai_state in ("hunting", "panicked"):
            if self.ai_state == "panicked" and not any_p:
                self.ai_state = "hunting"
            best_t, min_d = None, 400
            all_food = target_list + plankton_list + crusts + [c for c in crucians if (self.size_x * 2) > (c.size_x * 2 + 1)]
            for food in all_food:
                d = math.hypot(food.x - self.x, food.y - self.y)
                if d < min_d:
                    min_d, best_t = d, food
            if best_t and min_d > (self.size_x + 5):
                dx, dy = best_t.x - self.x, best_t.y - self.y
                self.vx, self.vy = (dx / min_d) * 3.5, (dy / min_d) * 3.5
            else:
                if random.random() < 0.02:
                    self.vx, self.vy = random.uniform(-2, 2), random.uniform(-1, 1)
        self.x += self.vx
        self.y += self.vy
        if self.vx > 0.2 or self.vx < -0.2:
            self.right = self.vx > 0.2
        if self.y > cb - self.size_y:
            self.y, self.vy = cb - self.size_y, 0
        if self.y < WATER + 30:
            self.y, self.vy = WATER + 30, 0
        self.x = max(self.size_x, min(WORLD_WIDTH - self.size_x, self.x))

    def draw(self, cam_x, cam_y, show_label=False):
        draw_perch_sprite(self.x, self.y, self.size_x, self.size_y, self.right, cam_x, cam_y, False, None)


def draw_bg_crucian(sx, sy, d, wobble):
    sy = int(sy + wobble)
    pygame.draw.polygon(screen, (230, 120, 40), ((sx - 24 * d, sy), (sx - 39 * d, sy - 14), (sx - 33 * d, sy), (sx - 39 * d, sy + 14)))
    pygame.draw.ellipse(screen, (185, 195, 195), (sx - 30, sy - 20, 60, 40))
    pygame.draw.circle(screen, (0, 0, 0), (int(sx + 18 * d), sy - 5), 3)


def draw_bg_pike(sx, sy, d, wobble):
    sy = int(sy + wobble)
    pygame.draw.ellipse(screen, (60, 90, 60), (sx - 90, sy - 22, 180, 44))
    pygame.draw.polygon(screen, (180, 100, 50), ((sx - 90 * d, sy), (sx - 120 * d, sy - 48), (sx - 102 * d, sy), (sx - 120 * d, sy + 48)))
    pygame.draw.circle(screen, (235, 190, 30), (int(sx + 65 * d), sy - 7), 5)
    pygame.draw.circle(screen, (0, 0, 0), (int(sx + 65 * d), sy - 7), 2)


def draw_bg_catfish(sx, sy, d, wobble):
    sy = int(sy + wobble)
    pygame.draw.ellipse(screen, (45, 55, 65), (sx - 190, sy - 48, 380, 96))
    pygame.draw.polygon(screen, (30, 38, 45), ((sx - 190 * d, sy), (sx - 250 * d, sy - 48), (sx - 250 * d, sy + 48)))
    pygame.draw.line(screen, (20, 25, 30), (sx + 150 * d, sy + 12), (sx + 215 * d, sy + 42), 5)
    pygame.draw.line(screen, (20, 25, 30), (sx + 135 * d, sy + 18), (sx + 190 * d, sy + 52), 3)
    pygame.draw.circle(screen, (235, 190, 30), (int(sx + 145 * d), sy - 12), 7)
    pygame.draw.circle(screen, (0, 0, 0), (int(sx + 145 * d), sy - 12), 3)
def lobby_menu():
    ip_input = ""
    found_host_ip = None
    status_msg = "Поиск комнат в Wi-Fi сети..."
    anim_t = 0
    menu_bubbles = [[random.randint(0, W), random.randint(0, H), random.uniform(0.5, 1.5)] for _ in range(25)]

    def listen_broadcast():
        nonlocal found_host_ip, status_msg
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("", DISCOVERY_PORT))
            sock.settimeout(1.0)
        except Exception:
            return
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                if data.decode("utf-8") == "PERCH_GAME_HOST":
                    sender_ip, _ = addr
                    found_host_ip = sender_ip
                    status_msg = f"Найдена игра в сети: {found_host_ip}"
            except socket.timeout:
                continue
            except Exception:
                break

    threading.Thread(target=listen_broadcast, daemon=True).start()

    while True:
        anim_t += 1
        for y_line in range(0, H, 4):
            r = y_line / float(H)
            pygame.draw.rect(screen, (int(25 + 15 * r), int(110 - 65 * r), int(145 - 85 * r)), (0, y_line, W, 4))

        for b in menu_bubbles:
            bx, by, bspd = b
            by -= bspd
            if by < -10:
                by = H + 10
                bx = random.randint(0, W)
            b[0], b[1] = bx, by
            pygame.draw.circle(screen, (180, 225, 245), (int(bx), int(by)), 3, 1)

        cycle = anim_t % 480
        if cycle < 220:
            p = cycle / 220.0
            lead_x = -80 + p * (W + 420)
            for idx, (ox, oy) in enumerate(((0, 220), (-45, 275), (-20, 330), (-70, 250))):
                draw_bg_crucian(int(lead_x + ox), oy, 1, math.sin(anim_t * 0.25 + idx) * 6)
            for idx, (ox, oy) in enumerate(((-200, 240), (-260, 310))):
                draw_bg_pike(int(lead_x + ox), oy, 1, math.sin(anim_t * 0.2 + idx) * 5)
        else:
            p = (cycle - 220) / 260.0
            pack_x = W + 120 - p * (W + 780)
            draw_bg_crucian(int(pack_x), 210, -1, math.sin(anim_t * 0.35) * 7)
            draw_bg_pike(int(pack_x + 35), 255, -1, math.sin(anim_t * 0.35 + 1) * 7)
            draw_bg_crucian(int(pack_x + 15), 300, -1, math.sin(anim_t * 0.35 + 2) * 7)
            draw_bg_pike(int(pack_x + 55), 345, -1, math.sin(anim_t * 0.35 + 3) * 7)
            draw_bg_crucian(int(pack_x + 80), 225, -1, math.sin(anim_t * 0.35 + 4) * 7)
            draw_bg_catfish(int(pack_x + 420), 280, -1, math.sin(anim_t * 0.15) * 4)

        mouse_pos = pygame.mouse.get_pos()

        panel = pygame.Surface((420, 440), pygame.SRCALPHA)
        panel.fill((10, 25, 40, 155))
        screen.blit(panel, (W // 2 - 210, 55))

        title = font.render("UNDERWATER WORLD", True, (255, 255, 255))
        screen.blit(title, (W // 2 - title.get_width() // 2, 70))

        my_ip_txt = small_font.render(f"Ваш Wi-Fi IP: {get_local_ip()}", True, (170, 220, 240))
        screen.blit(my_ip_txt, (W // 2 - my_ip_txt.get_width() // 2, 105))

        btn_solo = pygame.Rect(W // 2 - 180, 140, 360, 50)
        btn_host = pygame.Rect(W // 2 - 180, 205, 360, 50)
        btn_join_auto = pygame.Rect(W // 2 - 180, 270, 360, 50)
        input_box = pygame.Rect(W // 2 - 180, 365, 240, 45)
        btn_join_manual = pygame.Rect(W // 2 + 70, 365, 110, 45)

        pygame.draw.rect(screen, (210, 125, 40), btn_solo, border_radius=12)
        t_solo = font.render("Играть в одиночку", True, (255, 255, 255))
        screen.blit(t_solo, (btn_solo.centerx - t_solo.get_width() // 2, btn_solo.centery - t_solo.get_height() // 2))

        pygame.draw.rect(screen, (45, 130, 85), btn_host, border_radius=12)
        t_host = font.render("Создать игру (Wi-Fi Хост)", True, (255, 255, 255))
        screen.blit(t_host, (btn_host.centerx - t_host.get_width() // 2, btn_host.centery - t_host.get_height() // 2))

        auto_col = (50, 120, 170) if found_host_ip else (70, 85, 95)
        pygame.draw.rect(screen, auto_col, btn_join_auto, border_radius=12)
        t_auto = font.render("Подключиться (Авто)", True, (255, 255, 255))
        screen.blit(t_auto, (btn_join_auto.centerx - t_auto.get_width() // 2, btn_join_auto.centery - t_auto.get_height() // 2))

        st_surf = small_font.render(status_msg, True, (200, 245, 180) if found_host_ip else (220, 220, 220))
        screen.blit(st_surf, (W // 2 - st_surf.get_width() // 2, 330))

        pygame.draw.rect(screen, (255, 255, 255), input_box, border_radius=8)
        ip_surf = font.render(ip_input or "Ввести IP вручную...", True, (0, 0, 0) if ip_input else (140, 140, 140))
        screen.blit(ip_surf, (input_box.x + 10, input_box.y + 8))

        pygame.draw.rect(screen, (65, 110, 150), btn_join_manual, border_radius=8)
        t_man = font.render("Войти", True, (255, 255, 255))
        screen.blit(t_man, (btn_join_manual.centerx - t_man.get_width() // 2, btn_join_manual.centery - t_man.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    ip_input = ip_input[:-1]
                elif event.unicode in "0123456789.":
                    ip_input += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_solo.collidepoint(mouse_pos):
                    return "solo", None
                if btn_host.collidepoint(mouse_pos):
                    return "host", None
                if btn_join_auto.collidepoint(mouse_pos) and found_host_ip:
                    return "client", found_host_ip
                if btn_join_manual.collidepoint(mouse_pos) and ip_input:
                    return "client", ip_input

        pygame.display.flip()
        clock.tick(30)
def draw_water_gradient(camera_y):
    screen.fill((160, 210, 230))
    s_water_y = max(0, int(WATER - camera_y))
    if s_water_y < H:
        step = 4
        for y_line in range(max(0, s_water_y), H, step):
            r = min(1.0, max(0.0, (camera_y + y_line - WATER) / (WORLD_HEIGHT - WATER)))
            col = (int(35 + 25 * r), int(130 - 90 * r), int(140 - 115 * r))
            pygame.draw.rect(screen, col, (0, y_line, W, step))


def run_host(is_solo=False):
    server = None
    if not is_solo:
        def broadcast_loop():
            b_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            b_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            while True:
                try:
                    b_sock.sendto(b"PERCH_GAME_HOST", ("<broadcast>", DISCOVERY_PORT))
                except Exception:
                    pass
                pygame.time.wait(1000)

        threading.Thread(target=broadcast_loop, daemon=True).start()

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", GAME_PORT))
        server.listen(1)
        server.setblocking(False)

    client_conn = None
    p2_target = None
    recv_buf = ""

    fish1 = Fish(WORLD_WIDTH // 3, is_p2=False)
    fish2 = Fish(WORLD_WIDTH // 3 + 120, is_p2=True)
    pikes = [Pike(100), Pike(280), Pike(450)]
    som = Catfish()
    zanders = [Zander() for _ in range(5)]
    parts, plankton_list = [], [Plankton() for _ in range(30)]
    frys_list = [Fry(g) for g in range(4) for _ in range(10)]
    crucians_list = [Crucidian(10 + g) for g in range(4) for _ in range(5)]
    crustaceans = [Crustacean() for _ in range(6)]
    brothers = [Brother(WORLD_WIDTH // 3 + i * 80) for i in range(3)]

    camera_x = camera_y = algae_timer = 0
    pike_mode_timer, global_pike_mode = 2000, "frenzy"
    is_paused = False

    while True:
        if not is_solo and server and client_conn is None:
            try:
                conn, _ = server.accept()
                conn.setblocking(False)
                client_conn = conn
            except BlockingIOError:
                pass

        if client_conn:
            try:
                data = client_conn.recv(4096).decode("utf-8")
                if not data:
                    client_conn = None
                    p2_target = None
                else:
                    recv_buf += data
                    while "\n" in recv_buf:
                        line, recv_buf = recv_buf.split("\n", 1)
                        if line:
                            msg = json.loads(line)
                            p2_target = msg.get("target")
            except BlockingIOError:
                pass
            except Exception:
                client_conn = None
                p2_target = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        mouse_pos = pygame.mouse.get_pos()
        mx, my = mouse_pos
        lmb, _, _ = pygame.mouse.get_pressed()

        if not is_paused and lmb and pygame.Rect(W - 70, 20, 50, 50).collidepoint(mouse_pos):
            is_paused = True

        if not is_paused:
            touch = (camera_x + mx, camera_y + my) if lmb else None
            algae_timer += 1
            pike_mode_timer -= 1
            if pike_mode_timer <= 0:
                global_pike_mode = "calm" if global_pike_mode == "frenzy" else "frenzy"
                pike_mode_timer = 2000 if global_pike_mode == "frenzy" else 1500

            players = [fish1, fish2] if client_conn else [fish1]

            fish1.update(touch, parts)
            if client_conn:
                fish2.update(p2_target, parts)

            for pike in pikes:
                pike.update(players, crucians_list, brothers, global_pike_mode)
            som.update(global_pike_mode, crucians_list, players, brothers)
            for z in zanders:
                z.update(global_pike_mode, frys_list, players, pikes)
            for b in brothers:
                b.update_ai(frys_list, crucians_list, plankton_list, pikes, crustaceans)
            for cr in crustaceans:
                cr.update()

            for p in players:
                for p_cell in plankton_list[:]:
                    if math.hypot(p.x - p_cell.x, p.y - p_cell.y) < (p.size_x + 2):
                        plankton_list.remove(p_cell)
                        plankton_list.append(Plankton())
                        p.size_x += 0.05
                        p.size_y += 0.03
                for cr in crustaceans[:]:
                    if math.hypot(p.x - cr.x, p.y - cr.y) < (p.size_x + 5):
                        crustaceans.remove(cr)
                        crustaceans.append(Crustacean())
                        p.size_x += 0.6
                        p.size_y += 0.4
                for fry in frys_list[:]:
                    if math.hypot(p.x - fry.x, p.y - fry.y) < (p.size_x + 2):
                        f_id = fry.group_id
                        frys_list.remove(fry)
                        frys_list.append(Fry(f_id))
                        p.size_x += 0.4
                        p.size_y += 0.25
                for c in crucians_list[:]:
                    if math.hypot(p.x - c.x, p.y - c.y) < (p.size_x + 5) and (p.size_x * 2) > (c.size_x * 2 + 1):
                        crucians_list.remove(c)
                        crucians_list.append(Crucidian(c.group_id))
                        p.size_x += 2.5
                        p.size_y += 1.6
                for pike in pikes:
                    if pike.state != "inactive" and math.hypot(p.x - pike.x, p.y - pike.y) < (p.size_x + 20) and (p.size_x * 2) > (pike.pike_len + 1):
                        pike.state, pike.timer = "inactive", 1200
                        p.size_x += 5.0
                        p.size_y += 3.0
                if som.active and som.size_x > 0 and math.hypot(som.x - p.x, som.y - p.y) < (p.size_x + 35):
                    if (p.size_x * 2) > (som.size_x * 2 + 20):
                        som.size_x = 0
                        p.size_x += 15.0
                        p.size_y += 9.0
                    else:
                        p.respawn()

            if client_conn and math.hypot(fish1.x - fish2.x, fish1.y - fish2.y) < max(fish1.size_x, fish2.size_x):
                if fish1.size_x * 2 > fish2.size_x * 2 + 10:
                    fish1.size_x += fish2.size_x * 0.3
                    fish1.size_y += fish2.size_y * 0.3
                    fish2.respawn()
                elif fish2.size_x * 2 > fish1.size_x * 2 + 10:
                    fish2.size_x += fish1.size_x * 0.3
                    fish2.size_y += fish1.size_y * 0.3
                    fish1.respawn()
            if global_pike_mode == "frenzy":
                for z in zanders:
                    if not z.hidden and z.vx != 0:
                        for fry in frys_list[:]:
                            if math.hypot(z.x - fry.x, z.y - fry.y) < (z.size_x + 20):
                                frys_list.remove(fry)
                                frys_list.append(Fry(fry.group_id))
                                z.size_x += 0.5
                                z.size_y += 0.2
                        for p in players:
                            if math.hypot(z.x - p.x, z.y - p.y) < (z.size_x + 12) and int(p.size_x * 2) < 50:
                                p.respawn()
                                z.size_x, z.size_y = 50, 22
                            elif math.hypot(p.x - z.x, p.y - z.y) < (p.size_x + 25) and int(p.size_x * 2) > int(z.size_x * 2):
                                z.x, z.y = random.randint(3200, 3500), random.randint(WATER + 30, WATER + 120)
                                z.size_x, z.size_y = 50, 22
                                p.size_x += 7.5
                                p.size_y += 4.5

            if som.active and som.size_x > 0:
                for c in crucians_list[:]:
                    if math.hypot(som.x - c.x, som.y - c.y) < 70:
                        crucians_list.remove(c)
                        crucians_list.append(Crucidian(c.group_id))
                        som.size_x += 2.0
                for b in brothers[:]:
                    if math.hypot(som.x - b.x, som.y - b.y) < 70:
                        brothers.remove(b)
                        brothers.append(Brother(WORLD_WIDTH // 3))
                        som.size_x += 2.0

            for b in brothers:
                for p_cell in plankton_list[:]:
                    if math.hypot(b.x - p_cell.x, b.y - p_cell.y) < (b.size_x + 5):
                        plankton_list.remove(p_cell)
                        plankton_list.append(Plankton())
                        b.size_x += 0.05
                        b.size_y += 0.03
                for fry in frys_list[:]:
                    if math.hypot(b.x - fry.x, b.y - fry.y) < (b.size_x + 5):
                        frys_list.remove(fry)
                        frys_list.append(Fry(fry.group_id))
                        b.size_x += 0.15
                        b.size_y += 0.1
                        b.fry_eaten += 1
                for cr in crustaceans[:]:
                    if math.hypot(b.x - cr.x, b.y - cr.y) < (b.size_x + 5):
                        crustaceans.remove(cr)
                        crustaceans.append(Crustacean())
                        b.size_x += 0.3
                        b.size_y += 0.2

            fry_centers = {}
            for g_id in set(f.group_id for f in frys_list):
                mbs = [f for f in frys_list if f.group_id == g_id]
                if mbs:
                    fry_centers[g_id] = (sum(f.x for f in mbs) / len(mbs), sum(f.y for f in mbs) / len(mbs))
            for fry in frys_list:
                gc = fry_centers.get(fry.group_id)
                if gc:
                    gx, gy = gc
                    fry.update(gx, gy, players, [f for f in frys_list if f.group_id == fry.group_id])

            c_centers = {}
            for g_id in set(c.group_id for c in crucians_list):
                mbs = [c for c in crucians_list if c.group_id == g_id]
                if mbs:
                    c_centers[g_id] = (sum(c.x for c in mbs) / len(mbs), sum(c.y for c in mbs) / len(mbs))
            for c in crucians_list:
                gc = c_centers.get(c.group_id)
                if gc:
                    gx, gy = gc
                    c.update(gx, gy, players, [f for f in crucians_list if f.group_id == c.group_id])

            for p in parts[:]:
                p.update()
                if p.lifetime <= 0 or p.y > get_bottom_y(p.x):
                    parts.remove(p)
            if random.random() < 0.03:
                p_x = random.randint(0, WORLD_WIDTH)
                parts.append(Particle(p_x, get_bottom_y(p_x), 0, random.uniform(-0.3, -0.8), (180, 220, 240), is_bubble=True))

        if client_conn:
            state = {
                "algae": algae_timer,
                "f1": (round(fish1.x, 1), round(fish1.y, 1), round(fish1.size_x, 1), round(fish1.size_y, 1), fish1.right),
                "f2": (round(fish2.x, 1), round(fish2.y, 1), round(fish2.size_x, 1), round(fish2.size_y, 1), fish2.right),
                "plankton": tuple((int(p.x), int(p.y)) for p in plankton_list),
                "crusts": tuple((int(c.x), int(c.y), 1 if c.vx > 0 else -1) for c in crustaceans),
                "frys": tuple((int(f.x), int(f.y), 1 if f.vx >= 0 else -1) for f in frys_list),
                "crucians": tuple((int(c.x), int(c.y), round(c.size_x, 1), round(c.size_y, 1), 1 if c.vx >= 0 else -1) for c in crucians_list),
                "brothers": tuple((int(b.x), int(b.y), round(b.size_x, 1), round(b.size_y, 1), b.right) for b in brothers),
                "pikes": tuple((int(p.x), int(p.y), p.pike_len, 1 if p.vx >= 0 else -1) for p in pikes if p.state != "inactive"),
                "som": (int(som.x), int(som.y), round(som.size_x, 1), round(som.size_y, 1), 1 if som.vx >= 0 else -1) if som.size_x > 0 else None,
                "zanders": tuple((int(z.x), int(z.y), round(z.size_x, 1), round(z.size_y, 1), 1 if z.vx >= 0 else -1) for z in zanders if not z.hidden)
            }
            try:
                client_conn.sendall((json.dumps(state) + "\n").encode("utf-8"))
            except Exception:
                client_conn = None

        camera_x += (fish1.x - W // 2 - camera_x) * 0.1
        camera_y += (fish1.y - H // 2 - camera_y) * 0.1
        camera_x = max(0, min(WORLD_WIDTH - W, camera_x))
        camera_y = max(0, min(WORLD_HEIGHT - H, camera_y))

        draw_water_gradient(camera_y)
        draw_world_scenery(camera_x, camera_y, algae_timer)
        for p_cell in plankton_list:
            p_cell.draw(camera_x, camera_y)
        for fry in frys_list:
            fry.draw(camera_x, camera_y)
        for c in crucians_list:
            c.draw(camera_x, camera_y)
        for cr in crustaceans:
            cr.draw(camera_x, camera_y)
        for p in parts:
            p.draw(camera_x, camera_y)
        for b in brothers:
            b.draw(camera_x, camera_y, False)
        fish1.draw(camera_x, camera_y, show_label=(not is_solo))
        if client_conn:
            fish2.draw(camera_x, camera_y, show_label=True)
        for pike in pikes:
            pike.draw(camera_x, camera_y)
        som.draw(camera_x, camera_y)
        for z in zanders:
            z.draw(camera_x, camera_y)

        for x_line in range(0, W):
            world_x = int(camera_x + x_line)
            s_by = int(get_bottom_y(world_x) - camera_y)
            if s_by < H:
                pygame.draw.line(screen, (80, 50, 30), (x_line, max(0, s_by)), (x_line, H))

        lbl_prefix = "Размер окуня" if is_solo else "Игрок 1"
        size_text = font.render(f"{lbl_prefix}: {int(fish1.size_x * 2)} см", True, (255, 255, 255))
        screen.blit(size_text, (20, 20))

        if not is_solo:
            net_lbl = "Игрок 2 подключен!" if client_conn else f"Ожидание игрока (IP: {get_local_ip()})"
            net_surf = small_font.render(net_lbl, True, (150, 255, 150) if client_conn else (255, 220, 140))
            screen.blit(net_surf, (20, 50))

        if not is_paused:
            pygame.draw.circle(screen, (40, 60, 80), (W - 45, 45), 25)
            pygame.draw.rect(screen, (255, 255, 255), (W - 52, 33, 5, 24))
            pygame.draw.rect(screen, (255, 255, 255), (W - 43, 33, 5, 24))
        else:
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            btn_res = pygame.draw.rect(screen, (45, 110, 75), (W // 2 - 120, H // 2 - 60, 240, 50), border_radius=12)
            btn_ex = pygame.draw.rect(screen, (140, 45, 45), (W // 2 - 120, H // 2 + 10, 240, 50), border_radius=12)
            t_title = font.render("ПАУЗА", True, (255, 255, 255))
            t_res = font.render("Продолжить", True, (255, 255, 255))
            t_ex = font.render("Выйти", True, (255, 255, 255))
            screen.blit(t_title, (W // 2 - t_title.get_width() // 2, H // 2 - 120))
            screen.blit(t_res, (btn_res.centerx - t_res.get_width() // 2, btn_res.centery - t_res.get_height() // 2))
            screen.blit(t_ex, (btn_ex.centerx - t_ex.get_width() // 2, btn_ex.centery - t_ex.get_height() // 2))
            if lmb:
                if btn_res.collidepoint(mouse_pos):
                    is_paused = False
                    pygame.time.wait(200)
                elif btn_ex.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)
def run_client(host_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    try:
        sock.connect((host_ip, GAME_PORT))
    except Exception as e:
        screen.fill((40, 20, 20))
        err = font.render(f"Не удалось подключиться к {host_ip}: {e}", True, (255, 150, 150))
        screen.blit(err, (W // 2 - err.get_width() // 2, H // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        return

    sock.setblocking(False)
    recv_buf = ""
    state = None
    camera_x = camera_y = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        try:
            data = sock.recv(65536).decode("utf-8")
            if not data:
                break
            recv_buf += data
            while "\n" in recv_buf:
                line, recv_buf = recv_buf.split("\n", 1)
                if line:
                    state = json.loads(line)
        except BlockingIOError:
            pass
        except Exception:
            break

        mx, my = pygame.mouse.get_pos()
        lmb, _, _ = pygame.mouse.get_pressed()
        target = (camera_x + mx, camera_y + my) if lmb else None
        try:
            sock.sendall((json.dumps({"target": target}) + "\n").encode("utf-8"))
        except Exception:
            break

        if state:
            f1x, f1y, f1sx, f1sy, f1r = state["f1"]
            f2x, f2y, f2sx, f2sy, f2r = state["f2"]
            camera_x += (f2x - W // 2 - camera_x) * 0.1
            camera_y += (f2y - H // 2 - camera_y) * 0.1
            camera_x = max(0, min(WORLD_WIDTH - W, camera_x))
            camera_y = max(0, min(WORLD_HEIGHT - H, camera_y))

            draw_water_gradient(camera_y)
            draw_world_scenery(camera_x, camera_y, state["algae"])

            for px, py in state["plankton"]:
                sx, sy = int(px - camera_x), int(py - camera_y)
                if 0 <= sx <= W and 0 <= sy <= H:
                    pygame.draw.circle(screen, (100, 200, 80), (sx, sy), 3)

            for fx, fy, td in state["frys"]:
                sx, sy = int(fx - camera_x), int(fy - camera_y)
                if 0 <= sx <= W and 0 <= sy <= H:
                    pygame.draw.ellipse(screen, (170, 180, 180), (sx - 6, sy - 3, 12, 6))
                    pygame.draw.polygon(screen, (140, 150, 150), ((sx - 6 * td, sy), (sx - 10 * td, sy - 2), (sx - 10 * td, sy + 2)))

            for cx, cy, csx, csy, d in state["crucians"]:
                sx, sy = int(cx - camera_x), int(cy - camera_y)
                if -100 <= sx <= W + 100 and -100 <= sy <= H + 100:
                    pygame.draw.polygon(screen, (230, 120, 40), ((sx - int(csx * 0.8) * d, sy), (sx - int(csx * 1.3) * d, sy - int(csy * 0.7)), (sx - int(csx * 1.1) * d, sy), (sx - int(csx * 1.3) * d, sy + int(csy * 0.7))))
                    pygame.draw.ellipse(screen, (185, 195, 195), (sx - csx, sy - csy, csx * 2, csy * 2))
                    pygame.draw.circle(screen, (0, 0, 0), (int(sx + (csx * 0.6) * d), int(sy - int(csy * 0.25))), 3)

            for crx, cry, d in state["crusts"]:
                sx, sy = int(crx - camera_x), int(cry - camera_y)
                if 0 <= sx <= W and 0 <= sy <= H:
                    pygame.draw.ellipse(screen, (115, 75, 45), (sx - 7, sy - 5, 14, 8))
                    pygame.draw.line(screen, (90, 55, 30), (sx, sy), (sx + 8 * d, sy + 3), 2)

            for bx, by, bsx, bsy, bright in state["brothers"]:
                draw_perch_sprite(bx, by, bsx, bsy, bright, camera_x, camera_y, False, None)

            draw_perch_sprite(f1x, f1y, f1sx, f1sy, f1r, camera_x, camera_y, False, "Игрок 1")
            draw_perch_sprite(f2x, f2y, f2sx, f2sy, f2r, camera_x, camera_y, True, "Игрок 2")

            for px, py, plen, d in state["pikes"]:
                sx, sy = int(px - camera_x), int(py - camera_y)
                pygame.draw.ellipse(screen, (60, 90, 60), (sx - 100, sy - 25, plen, 50))
                pygame.draw.polygon(screen, (180, 100, 50), ((sx - 100 * d, sy), (sx - 135 * d, sy - 60), (sx - 115 * d, sy), (sx - 135 * d, sy + 60)))
                pygame.draw.circle(screen, (235, 190, 30), (int(sx + 75 * d), int(sy - 8)), 6)
                pygame.draw.circle(screen, (0, 0, 0), (int(sx + 75 * d), int(sy - 8)), 3)

            if state["som"]:
                smx, smy, smsx, smsy, d = state["som"]
                sx, sy = int(smx - camera_x), int(smy - camera_y)
                pygame.draw.ellipse(screen, (45, 55, 65), (sx - smsx, sy - smsy, smsx * 2, smsy * 2))
                pygame.draw.polygon(screen, (30, 38, 45), ((sx - smsx * d, sy), (sx - (smsx + 60) * d, sy - 45), (sx - (smsx + 60) * d, sy + 45)))
                pygame.draw.line(screen, (20, 25, 30), (sx + (smsx - 30) * d, sy + 10), (sx + (smsx + 20) * d, sy + 35), 4)
                pygame.draw.circle(screen, (235, 190, 30), (int(sx + (smsx - 40) * d), int(sy - 10)), 6)
                pygame.draw.circle(screen, (0, 0, 0), (int(sx + (smsx - 40) * d), int(sy - 10)), 3)

            for zx, zy, zsx, zsy, d in state["zanders"]:
                sx, sy = int(zx - camera_x), int(zy - camera_y)
                pygame.draw.polygon(screen, (90, 100, 80), ((sx - 10 * d, sy - zsy), (sx + 15 * d, sy - zsy - 15), (sx + 25 * d, sy - zsy + 2)))
                pygame.draw.ellipse(screen, (120, 130, 110), (sx - zsx, sy - zsy, zsx * 2, zsy * 2))
                pygame.draw.polygon(screen, (90, 100, 80), ((sx - zsx * d, sy), (sx - (zsx + 20) * d, sy - 15), (sx - (zsx + 20) * d, sy + 15)))
                pygame.draw.circle(screen, (200, 205, 210), (int(sx + (zsx - 12) * d), int(sy - 4)), 5)
                pygame.draw.circle(screen, (0, 0, 0), (int(sx + (zsx - 12) * d), int(sy - 4)), 2)

            for x_line in range(0, W):
                world_x = int(camera_x + x_line)
                s_by = int(get_bottom_y(world_x) - camera_y)
                if s_by < H:
                    pygame.draw.line(screen, (80, 50, 30), (x_line, max(0, s_by)), (x_line, H))

            size_text = font.render(f"Игрок 2: {int(f2sx * 2)} см", True, (255, 255, 255))
            screen.blit(size_text, (20, 20))
        else:
            screen.fill((25, 65, 90))
            wait_t = font.render("Подключение к миру хоста...", True, (255, 255, 255))
            screen.blit(wait_t, (W // 2 - wait_t.get_width() // 2, H // 2))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    mode, host_ip = lobby_menu()
    if mode == "solo":
        run_host(is_solo=True)
    elif mode == "host":
        run_host(is_solo=False)
    else:
        run_client(host_ip)

from random import randint

from pygame import *

width = 1900
height = 1000
size_window = (width,height)
window = display.set_mode(size_window)
display.set_caption("platformer")
platform1 = Surface((400,20))
platform1.fill((204, 117, 7))
playing = True
square = Surface((50,50))
square.fill((204, 34, 7 ))

class GameSprite(sprite.Sprite):
    def __init__(self, path, speed, size, walking_right_anim,walking_left_anim, jump_size, x, y):
        super().__init__()
        self.path = path
        self.size = size
        self.num_of_animation = 0
        self.walking_right_anim = walking_right_anim
        self.walking_left_anim = walking_left_anim
        self.image = transform.scale(image.load(self.path), self.size)
        self.rect = self.image.get_rect()
        self.isJump = False
        self.speed = speed
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 15
        self.jump_size = jump_size
    def show_on_screen(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def jump(self):
        if self.jump_size >= -13:
                if self.jump_size < 0:
                    self.speed_y = (self.jump_size ** 2 ) // 2
                else:
                    self.speed_y = -((self.jump_size ** 2 ) // 2)
                self.jump_size -= 2

        else:
            self.isJump = False
            self.speed_y = 0
            self.jump_size = 13


    def update(self, platforms):
        global width
        global height
        global ground_height
        #этот код не трогать(он на крайний случай):
        #for platform in platforms:
#
        #    if self.rect.x >= platform.rect.x and self.rect.x <= platform.rect.x + platform.image.get_width():
        #        self.gravity = 0
        #    else:
        #        self.rect.x += self.speed_x
        #        self.rect.y += self.gravity
        #        self.rect.y += self.speed_y
        #    if self.rect.x >= 390 and self.rect.x <= 450:
        #        self.gravity = 12
        #    elif self.rect.x >= -90 and self.rect.x <= -10:
        #        self.gravity = 12
        #    elif self.rect.x >= 890 and self.rect.x <= 1050:
        #        self.gravity = 12
        #    elif self.rect.x >= platform.rect.x - 110 and self.rect.x <= platform.rect.x - 150 + platform.image.get_width() and self.rect.bottom != platform.rect.top:
        #        self.rect.x += self.speed_x
        #        self.rect.y += self.gravity
        #        self.rect.y += self.speed_y
        keys = key.get_pressed()
        self.rect.x += self.speed_x
        self.rect.y += self.gravity
        self.rect.y += self.speed_y
        for platform in platforms:
            if platform.rect.colliderect(self.rect.x, self.rect.y + self.speed_y, self.image.get_width(), self.image.get_height()):
                if self.rect.bottom < platform.rect.centery:
                    if self.speed_y >= 0:
                        if self.rect.x >= platform.rect.x - 110 and self.rect.x <= platform.rect.x - 150 + platform.image.get_width():
                            self.rect.bottom = platform.rect.top
                            self.isJump = False
                            if keys[K_SPACE]:
                                self.rect.bottom -= 150

        if self.rect.bottom - 25 > height - ground_height:
            self.speed_y = 0
            self.rect.bottom = height - ground_height + 25


class Bullet(GameSprite):
    def update(self, direction=0):
        global nuggets
        if self.rect.x <= 1800 and direction == 0:
            self.rect.x += self.speed
        elif self.rect.x > -90 and direction == 1:
            self.rect.x += self.speed
        else:
            self.kill()
        for nugget in nuggets:
            if self.rect.colliderect(nugget.rect):
                nugget.HP -= 8
                self.kill()


class Player(GameSprite):
    def __init__(self, path, speed, size, walking_right_anim,walking_left_anim, jump_size, x, y, hit_animation, hit_animation_left,HP, damage):
        super().__init__(path, speed, size, walking_right_anim,walking_left_anim, jump_size, x, y)
        self.hit_animation = hit_animation
        self.hit_animation_left = hit_animation_left
        self.HP = HP
        self.num_of_clips = 1
        self.num_of_bullets_in_clip = 25 * self.num_of_clips
        self.damage = damage
    def move_right(self):
        keys = key.get_pressed()
        global direction
        if keys[K_d] and self.rect.x < 1750:
            self.rect.x += self.speed
            self.image = transform.scale(self.walking_right_anim[self.num_of_animation], self.size)
            direction = 0
    def move_left(self):
        global direction
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > -90:
            self.rect.x -= self.speed
            self.image = transform.scale(self.walking_left_anim[self.num_of_animation], self.size)
            direction = 1

    def fire_in_the_hole(self,sound):
        keys = key.get_pressed()
        global bullets
        global direction
        if self.num_of_bullets_in_clip > 0:
            if (keys[K_q] and keys[K_d] and direction == 0) or (keys[K_q] and direction == 0):
                self.image = transform.scale(image.load("sprites/shooting/shooting_jugg.png"), self.size)
                bullets.add(Bullet("sprites/bullets/bullet1.png", 20, (30, 15), ..., ..., ..., self.rect.x + 195, randint(self.rect.centery + 27, self.rect.centery + 37)))
                sound.play()
                direction = 0
                self.num_of_bullets_in_clip -= 1
            if (keys[K_q] and keys[K_a] and direction == 1) or (keys[K_q] and direction == 1):
                self.image = transform.scale(image.load("sprites/shooting/shooting_jugg2.png"), self.size)
                bullets.add(Bullet("sprites/bullets/bullet2.png", -20, (30, 15), ..., ..., ..., self.rect.x + 20,randint(self.rect.centery + 27, self.rect.centery + 37)))
                sound.play()
                direction = 1
                self.num_of_bullets_in_clip -= 1
    def hitting(self, sound):
        global num_anim
        keys = key.get_pressed()
        if keys[K_e] and direction == 0:
            if num_anim == 15:
                sound.play()
            self.image = transform.scale(self.hit_animation[num_anim // 2], self.size)
        elif keys[K_e] and direction == 1:
            if num_anim == 15:
                sound.play()
            self.image = transform.scale(self.hit_animation_left[num_anim // 2], self.size)
        num_anim += 1
    def collision_when_hit(self):
        global nuggets
        keys = key.get_pressed()
        for nugget in nuggets:
            if keys[K_e]:
                if self.rect.colliderect(nugget.rect):
                    nugget.HP -= self.damage

class Monster(GameSprite):
    def __init__(self, path, speed, size, walking_right_anim,walking_left_anim, jump_size, x, y, HP):
        super().__init__( path, speed, size, walking_right_anim,walking_left_anim, jump_size, x, y)
        self.HP = HP
    def update(self, sound):
        global chests_of_bullets
        if self.HP <= 0:
            sound.play()
            chest = Chest_of_Bullets("sprites/bullets/chest_with_bullets.png", 0, (150, 50), ..., ..., 0, self.rect.x, self.rect.y+65, 25)
            chests_of_bullets.add(chest)
            self.kill()
class Chest_of_Bullets(GameSprite):
    def __init__(self, path, speed, size, walking_right_anim,walking_left_anim, jump_size, x, y, num_bullets):
        super().__init__(path, speed, size, walking_right_anim,walking_left_anim, jump_size, x, y)
        self.num_bullets = num_bullets
    def update(self, player):
        if self.rect.colliderect(player.rect):
            self.kill()
            player.num_of_bullets_in_clip += self.num_bullets
bg = transform.scale(image.load("sprites/main_desert.jpg"),size_window)

walking_right = [
    image.load("sprites/jugg/jugg_without_bg.png"),
    image.load("sprites/walking_right/walking_jugg_r1.png"),
    image.load("sprites/walking_right/walking_jugg_r2.png"),
    image.load("sprites/walking_right/walking_jugg_r3.png"),
    image.load("sprites/walking_right/walking_jugg_r4.png"),
]
walking_left = [
    image.load("sprites/jugg/jugg_without_bg2.png"),
    image.load("sprites/walking_left/walking_jugg_l1.png"),
    image.load("sprites/walking_left/walking_jugg_l2.png"),
    image.load("sprites/walking_left/walking_jugg_l3.png"),
    image.load("sprites/walking_left/walking_jugg_l4.png"),
]
hit_animation = [
    image.load("sprites/hit/hitting_jugg1.png"),
    image.load("sprites/hit/hitting_jugg2.png"),
    image.load("sprites/hit/hitting_jugg3.png"),
    image.load("sprites/hit/hitting_jugg4.png"),
    image.load("sprites/hit/hitting_jugg5.png"),
    image.load("sprites/hit/hitting_jugg6.png"),
    image.load("sprites/hit/hitting_jugg7.png"),
    image.load("sprites/hit/hitting_jugg8.png")
]
hit_animation_left = [
    image.load("sprites/hit_left/hitting_jugg1.png"),
    image.load("sprites/hit_left/hitting_jugg2.png"),
    image.load("sprites/hit_left/hitting_jugg3.png"),
    image.load("sprites/hit_left/hitting_jugg4.png"),
    image.load("sprites/hit_left/hitting_jugg5.png"),
    image.load("sprites/hit_left/hitting_jugg6.png"),
    image.load("sprites/hit_left/hitting_jugg7.png"),
    image.load("sprites/hit_left/hitting_jugg8.png")
]


clock = time.Clock()
floor = GameSprite("sprites/dirt_floor.png", 1, (width+100, 100), ...,...,1, -50, 900)
ground_height = floor.image.get_height()

font.init()
jugg = Player("sprites/jugg/jugg_without_bg.png", 20,(250,200),walking_right, walking_left,13,50,720,hit_animation, hit_animation_left, 200, 2)
font1 = font.SysFont("Arial",50)

chests_of_bullets = sprite.Group()


nuggets = sprite.Group()
nugget = Monster("sprites/monsters/nugget.png", 10, (150, 125),..., ..., 0, 700, 820, 100)
nugget2 = Monster("sprites/monsters/nugget.png", 10, (150, 125),..., ..., 0, 1000, 820, 100)
nuggets.add(nugget)
nuggets.add(nugget2)

bullets = sprite.Group()
direction = 0
num_anim = 0
platforms = sprite.Group()
platform1 = GameSprite("sprites/sand_platform.png", 1, (400,60), ..., ..., 1, 700,750)
platform2 = GameSprite("sprites/sand_platform.png", 1, (500,60), ..., ..., 1, 100, 800)
platform3 = GameSprite("sprites/sand_platform.png", 1, (400,60), ..., ..., 1, 100, 700)
platforms.add(platform1)
platforms.add(platform2)
platforms.add(platform3)

mixer.init()
mixer.music.load("sounds/desert_sound.mp3")
mixer.music.play()
shooting_sound = mixer.Sound("sounds/shooting_sound.mp3")
hitting_sound = mixer.Sound("sounds/hitting_sound.mp3")
dying_sound = mixer.Sound("sounds/nugget_dying.mp3")
#icon_num_bullets = transform.scale(image.load("icons/num_bullets.png"), (70,70))
while playing:
    for ev in event.get():
        if ev.type == QUIT:
            playing = False
        if ev.type == KEYDOWN:
            if ev.key == K_SPACE and jugg.rect.bottom > platform2.rect.bottom:
                jugg.isJump = True
            elif ev.key == K_SPACE and jugg.rect.bottom == platform2.rect.top:
                jugg.speed_y = 0
                jugg.rect.bottom -= 150
                jugg.isJump = False

    window.blit(bg, (0, 0))
    floor.show_on_screen()
    if jugg.num_of_bullets_in_clip > 0:
        num_of_bullets_text = font1.render(f"{jugg.num_of_bullets_in_clip}", True, (40, 40, 40))
    else:
         num_of_bullets_text = font1.render("0", True, (40, 40, 40))
    window.blit(num_of_bullets_text, (1750,25))
    if jugg.isJump:
        jugg.jump()
    jugg.move_right()
    jugg.move_left()
    jugg.fire_in_the_hole(shooting_sound)
    jugg.collision_when_hit()
    jugg.update(platforms)

    platforms.draw(window)

    nuggets.draw(window)
    nuggets.update(dying_sound)

    jugg.show_on_screen()

    chests_of_bullets.draw(window)
    chests_of_bullets.update(jugg)

    bullets.draw(window)
    bullets.update()
    if jugg.num_of_animation == len(walking_left) - 1:
        jugg.num_of_animation = 0
    else:
        jugg.num_of_animation += 1
    keys = key.get_pressed()
    if not keys[K_d] and direction == 0:
        jugg.image = transform.scale(jugg.walking_right_anim[0], jugg.size)
    elif not keys[K_a] and direction == 1:
        jugg.image = transform.scale(jugg.walking_left_anim[0], jugg.size)

    if num_anim >= 16:
        num_anim = 0
    else:
        jugg.hitting(hitting_sound)

    display.update()
    num_anim += 1
    clock.tick(10)



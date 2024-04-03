from random import randint

from pygame import *

width = 1200
height = 800
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
    def jump(self, platforms):
        #if not self.isJump:
        #        self.can_jump = True

        #    if keys[K_SPACE]:
        #        self.isJump = True
          #else:
            #if not platform.rect.colliderect(self.rect.x, self.rect.y - (self.jump_size ** 2 ) / 2, self.image.get_width(), self.image.get_height()):
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

        self.rect.x += self.speed_x
        self.rect.y += self.gravity
        self.rect.y += self.speed_y
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
        number_platform = 0
        for platform in platforms:
            if platform.rect.colliderect(self.rect.x, self.rect.y + self.speed_y, self.image.get_width(), self.image.get_height()):
                if self.rect.bottom < platform.rect.centery:
                    if self.speed_y >= 0:
                        if self.rect.x >= platform.rect.x - 110 and self.rect.x <= platform.rect.x - 150 + platform.image.get_width():
                            self.rect.bottom = platform.rect.top
                            self.isJump = False
                            if keys[K_SPACE]:
                                self.jump_size = 13
                                self.speed_y = -13


        for platform in platforms:
            if self.rect.bottom > platform.rect.top and self.speed_y == -13:
                self.speed_y = 0
                self.rect.bottom -= 150
                self.isJump = False
        if self.rect.bottom-25 > height - ground_height:
            self.speed_y = 0
            self.rect.bottom = height - ground_height + 25


class Bullet(GameSprite):
    def update(self, direction=0):
        if self.rect.x <= 1100 and direction == 0:
            self.rect.x += self.speed
        elif self.rect.x > -90 and direction == 1:
            self.rect.x += self.speed
        else:
            self.kill()
class Player(GameSprite):
    def __init__(self, path, speed, size, walking_right_anim,walking_left_anim, jump_size, x, y, hit_animation, hit_animation_left):
        super().__init__(path, speed, size, walking_right_anim,walking_left_anim, jump_size, x, y)
        self.hit_animation = hit_animation
        self.hit_animation_left = hit_animation_left
    def move_right(self):
        global direction
        keys = key.get_pressed()
        self.speed_x = 0
        if keys[K_d] and self.rect.x < 1050:
            self.rect.x += self.speed
            self.image = transform.scale(self.walking_right_anim[self.num_of_animation], self.size)
            direction = 0
    def move_left(self):
        global direction
        self.speed_x = 0
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > -90:
            self.rect.x -= self.speed
            self.image = transform.scale(self.walking_left_anim[self.num_of_animation], self.size)
            direction = 1

    #def jump(self, platform):
    #    keys = key.get_pressed()
    #    if not self.isJump:
    #        if keys[K_SPACE]:
    #            self.isJump = True
    #            self.can_jump = True
    #    else:
    #        #if not platform.rect.colliderect(self.rect.x, self.rect.y - (self.jump_size ** 2 ) / 2, self.image.get_width(), self.image.get_height()):
    #            if self.jump_size >= -12:
#
    #                if self.jump_size < 0:
    #                    self.speed_y = (self.jump_size ** 2 ) / 2
    #                    if self.rect.bottom <= platform.rect.top:
    #                        if self.rect.x >= platform.rect.x - 110 and self.rect.x <= platform.rect.x - 150 + platform.image.get_width():
    #                            print(self.rect.x, platform.rect.centerx)
    #                        #print(f"platforms x: {platform.rect.x}, platforms x + his width: {platform.rect.x + platform.image.get_width()}")
    #                            self.gravity = 0
    #                            self.isJump = False
    #                            if self.isJump == False:
    #                                self.rect.bottom = platform.rect.top + 10
#
    #                elif self.jump_size > 0:
    #                    self.speed_y = -((self.jump_size ** 2 ) / 2)
#
    #                self.jump_size -= 2
    #                    #else:
    #                #       self.isJump = False
#
    #            else:
    #                self.isJump = False
    #                self.can_jump = False
    #                self.jump_size = 13

            #else:
            #    self.jump_size = self.rect.top - platform.rect.bottom

            #    if self.jump_size >= self.jump_size:
            #        if self.jump_size < 0:
            #            self.speed_y = (self.jump_size ** 2 ) / 2
            #        elif self.jump_size > 0:
            #            self.speed_y = -((self.jump_size ** 2 ) / 2)
            #        self.jump_size -= 1

            #    else:
            #        self.isJump = False
            #        self.jump_size = 12

    def fire_in_the_hole(self):
        keys = key.get_pressed()
        global bullets
        global direction
        if (keys[K_q] and keys[K_d] and direction == 0) or (keys[K_q] and direction == 0):
            self.image = transform.scale(image.load("sprites/shooting/shooting_jugg.png"), self.size)
            bullets.add(Bullet("sprites/bullets/bullet1.png", 20, (30, 15), ..., ..., ..., self.rect.x + 195, randint(self.rect.centery + 27, self.rect.centery + 37)))
            direction = 0
        if (keys[K_q] and keys[K_a] and direction == 1) or (keys[K_q] and direction == 1):
            self.image = transform.scale(image.load("sprites/shooting/shooting_jugg2.png"), self.size)
            bullets.add(Bullet("sprites/bullets/bullet2.png", -20, (30, 15), ..., ..., ..., self.rect.x + 20,randint(self.rect.centery + 27, self.rect.centery + 37)))
            direction = 1
    def hitting(self):
        global num_anim
        keys = key.get_pressed()
        if keys[K_e] and direction == 0:
            jugg.image = transform.scale(jugg.hit_animation[num_anim // 2], jugg.size)
        elif keys[K_e] and direction == 1:
            jugg.image = transform.scale(jugg.hit_animation_left[num_anim // 2], jugg.size)
        num_anim += 1
bg = transform.scale(image.load("sprites/desert.jpg"),size_window)

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
floor = GameSprite("sprites/dirt_floor.png", 1, (width+100, 100), ...,...,1, -50, 700)
ground_height = floor.image.get_height()

jugg = Player("sprites/jugg/jugg_without_bg.png", 20,(250,200),walking_right, walking_left,13,50,520,hit_animation, hit_animation_left)

bullets = sprite.Group()
direction = -1
num_anim = 0
platforms = sprite.Group()
platform1 = GameSprite("sprites/sand_platform.png", 1, (400,60), ..., ..., 1, 700,550)
platform2 = GameSprite("sprites/sand_platform.png", 1, (500,60), ..., ..., 1, 100, 600)
platform3 = GameSprite("sprites/sand_platform.png", 1, (400,60), ..., ..., 1, 100, 500)
platforms.add(platform1)
platforms.add(platform2)
platforms.add(platform3)
while playing:
    for ev in event.get():
        if ev.type == QUIT:
            playing = False
        if ev.type == KEYDOWN:
            if ev.key == K_SPACE and jugg.rect.bottom > platform2.rect.bottom:
                jugg.isJump = True
            elif ev.key == K_SPACE and jugg.rect.bottom <= platform2.rect.top:
                jugg.speed_y = 0
                jugg.rect.bottom -= 150

        #if ev.key == K_q and ev.type == KEYDOWN:
        #    jugg.image = transform.scale(image.load("sprites/shooting_jugg.png"), jugg.size)
        #    jugg.fire_in_the_hole()


    # window.fill((49, 204, 7)) // заливала задний фон зелёным цветом по rgb коду
    #window.blit(floor, (0, 500))
    #window.blit(platform1,(450, 400))
    #window.blit(square, (100,500))
    #window.blit(walking_right[number_animation],(50,350))
    window.blit(bg, (0, 0))
    floor.show_on_screen()
    jugg.move_right()
    jugg.move_left()
    jugg.fire_in_the_hole()
    jugg.update(platforms)
    if jugg.isJump:
        jugg.jump(platforms)
    bullets.draw(window)
    bullets.update()
    platforms.draw(window)
    jugg.show_on_screen()
    keys = key.get_pressed()
    #if sprite.collide_rect(jugg, platform1):
    #    jugg.jump_size = 12
    #    jugg.isJump = False
    #    jugg.rect.y = platform1.rect.y - jugg.rect.height
    #    if sprite.collide_rect(jugg,platform1):
    #        jugg.rect.y = platform1.rect.y + jugg.rect.height
    if jugg.num_of_animation == 4:
        jugg.num_of_animation = 0
    else:
        jugg.num_of_animation += 1
    if not keys[K_d] and direction == 0:
        jugg.image = transform.scale(jugg.walking_right_anim[0], jugg.size)
    elif not keys[K_a] and direction == 1:
        jugg.image = transform.scale(jugg.walking_left_anim[0], jugg.size)

    #print(direction)
    if num_anim > 16:
        num_anim = 0
    else:
        jugg.hitting()
        
    display.update()
    num_anim += 1
    clock.tick(10)



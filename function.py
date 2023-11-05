from data import *

boss_shoot = pygame.USEREVENT
pygame.time.set_timer(boss_shoot, 2000)

class Background():
    def __init__(self):
        self.y = 0
        self.y1 = setting_win['HEIGHT']
        self.SPEED = 2
        self.IMAGE = bg_image

    def move(self, window):
        self.y += self.SPEED
        self.y1 += self.SPEED
        window.blit(self.IMAGE, (0, self.y))
        window.blit(self.IMAGE, (0, self.y1))
        if self.y > setting_win['HEIGHT']:
            self.y = - setting_win['HEIGHT']
        if self.y1 > setting_win['HEIGHT']:
            self.y1 = - setting_win['HEIGHT']


class Sprite(pygame.Rect):
    def __init__(self, x, y, width, height, hp = None, image = None, speed = None):
        super().__init__(x, y, width, height)
        self.IMAGE_LIST = image
        self.HP = hp
        self.IMAGE = self.IMAGE_LIST[0]
        self.IMAGE_COUNT = 0
        self.SPEED = speed

    def move_image(self):
        self.IMAGE_COUNT += 1
        if self.IMAGE_COUNT > len(self.IMAGE_LIST) * 10 - 1:
            self.IMAGE_COUNT = 0
        if self.IMAGE_COUNT % 10 == 0:
            self.IMAGE = self.IMAGE_LIST[self.IMAGE_COUNT // 10]

class Hero(Sprite):
    def __init__(self, x, y, width, height, hp = 3, image = None, speed = 5):
        super().__init__(x, y, width, height, hp, image, speed)
        self.MOVE = {'LEFT' : False, "RIGHT": False}
        self.BULLET =list()
        self.SCORE = 0
        self.LVL = 1

    def move(self, window):
        if self.MOVE['LEFT'] == True and self.x > 0:
            self.x -= self.SPEED
        if self.MOVE['RIGHT'] == True and self.x + self.width< setting_win['WIDTH']:
            self.x += self.SPEED
        window.blit(self.IMAGE, (self.x, self.y))
        self.move_image()


class Bot(Sprite):
    def __init__(self, x, y, width, height, speed = 1, image = None, hp = 1, body_damage = 1):
        super().__init__(x, y, width, height, hp, image, speed)
        self.SHOT = 0
        self.BODY_DAMAGE = body_damage

    def move(self, window, hero):
        self.y += self.SPEED
        window.blit(self.IMAGE, (self.x, self.y))
        self.move_image()

        self.SHOT += 1
        if self.SHOT % (setting_win['FPS'] * 2) == 0:
            bullet_list.append(Bullet(self.centerx, self.bottom, 10, 20))

        if self.y > setting_win['HEIGHT']:
            bot_list.remove(self)
            return 0
        
        if self.colliderect(hero):
            hero.HP -= self.BODY_DAMAGE
            hero.SCORE += 1
            bot_list.remove(self)
            return 0


class Boss(Sprite):
    def __init__(self, x, y, width, height, speed= 1, image= None, hp= 10):
        super().__init__(x, y, width, height, hp, image, speed)
        self.ANIMATION = False
        self.LIVE = False

    def move(self, window, hero):

        if self.y < 10 and not self.ANIMATION:
            self.y += abs(self.SPEED)
        self.x += self.SPEED
        #print(self.x, self.right, self.width, self.height)
        if self.x < 0 or self.right > setting_win["WIDTH"]:
            self.SPEED *= -1
        window.blit(self.IMAGE, (self.x, self.y))
        self.move_image()
        if self.ANIMATION:
            self.leave(hero)
            self.LIVE = False

    def leave(self, hero):
        self.y -= abs(self.SPEED)
        if self.bottom < 0:
            self.ANIMATION = False
            hero.LVL += 1
            self.HP = 10 + hero.LVL * 2
            self.x = setting_win["WIDTH"] // 2 - self.width // 2
            self.y = - self.height
            


class Bullet(pygame.Rect):
    def __init__(self, x, y, width, height, image = None, speed = 3):
        super().__init__(x, y, width, height)
        self.SPEED = speed
    
    def move_from_hero(self, window, hero, boss):
        self.y -= self.SPEED
        pygame.draw.rect(window, (255, 20, 30), self)
        index = self.collidelist(bot_list)
        if index != -1:
            bot_list[index].HP -= 1
            if bot_list[index].HP == 0:
                hero.SCORE += 1
                bot_list.pop(index)
            hero.BULLET.remove(self)
            return 0
        if self.y < 0:
            hero.BULLET.remove(self)
            return 0
        if self.colliderect(boss):
            boss.HP -= 1
            hero.BULLET.remove(self)
            if boss.HP == 0:
                boss.ANIMATION = True
            return 0

    def move_from_bot_boss(self,window, hero):
        self.y += self.SPEED
        pygame.draw.rect(window, (20, 200, 20), self)

        if self.colliderect(hero):
            hero.HP -= 1
            bullet_list.remove(self)
            return 0
        if self.y > setting_win['HEIGHT']:
            bullet_list.remove(self)
            return 0
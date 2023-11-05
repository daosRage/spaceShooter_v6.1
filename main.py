from function import*
from random import randint

window = pygame.display.set_mode((setting_win['WIDTH'], setting_win['HEIGHT']))
pygame.display.set_caption('КОСМІЧНИЙ ШУТЕР')

def run():
    game = True
    menu = False
    start_time, end_time = 0, 0
    hero = Hero(setting_win['WIDTH'] // 2 - setting_hero['WIDTH'] // 2,
                setting_win['HEIGHT'] - setting_hero['HEIGHT'] - 10,
                setting_hero['WIDTH'],
                setting_hero['HEIGHT'],
                image= hero_image_list)
    boss = Boss(setting_win["WIDTH"] // 2 - setting_boss["WIDTH"] // 2,
                - setting_boss["HEIGHT"],
                setting_boss["WIDTH"],
                setting_boss["HEIGHT"],
                image= boss_image_list)
    clock = pygame.time.Clock()
    bg = Background()
    hp_bar_ = pygame.Rect((5,5), (150, 10))
    hp_width = 150 / hero.HP
    fon_startend = pygame.font.Font(None, 50)
    rect_start = pygame.Rect((setting_win['WIDTH'] // 2 - 100, setting_win['HEIGHT'] // 2- 85), (200, 60))
    rect_end = pygame.Rect((setting_win['WIDTH'] // 2 - 100, setting_win['HEIGHT'] // 2 + 25), (200, 60))


    while game:
        #window.fill((0, 20, 200))
        events = pygame.event.get()
        bg.move(window)
        pygame.draw.rect(window, (255, 255, 255), hp_bar_)
        hp_bar = pygame.Rect((5,5), (hp_width*hero.HP, 10))
        pygame.draw.rect(window, (255, 0, 0), hp_bar)
        window.blit(fon_startend.render(f'{hero.SCORE}', True, (255, 255, 255)), (setting_win['WIDTH'] - 50, 5))

        #HERO
        hero.move(window)
        if hero.HP >= 0:
            for bullet in hero.BULLET:
                bullet.move_from_hero(window, hero, boss)
        if hero.HP <= 0:
            menu = True
            hero.SPEED = 0
            start_time = end_time

        #BOT
        end_time = pygame.time.get_ticks()
        if end_time - start_time > 2000 and hero.SCORE <= 5 * hero.LVL:
            bot_list.append(Bot(randint(0, setting_win['WIDTH'] - setting_bot['WIDTH']),
                                - setting_bot['HEIGHT'],
                                setting_bot['WIDTH'],
                                setting_bot['HEIGHT'],
                                image= bot_image_list))
            start_time = end_time
        for bot in bot_list:
            bot.move(window, hero)

        for bullet in bullet_list:
            bullet.move_from_bot_boss(window, hero)

        #BOSS
        if hero.SCORE >= 5 * hero.LVL:
            boss.LIVE = True
            boss.move(window, hero)
            while len(bot_list) > 0:
                bot_list.pop(0)

        #MENU
        if menu == True:
            pygame.draw.rect(window, (255, 65, 87), rect_start)
            pygame.draw.rect(window, (255, 65, 87), rect_end)
            render_start = fon_startend.render('START', True, (0, 0, 0))
            render_end = fon_startend.render('END', True, (0, 0, 0))
            window.blit(render_start, (rect_start.x + 50, rect_start.y + 13))
            window.blit(render_end, (rect_end.x + 65, rect_end.y + 13))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if rect_start.collidepoint(x, y):
                        hero.HP = 3
                        while len(bot_list) > 0:
                            bot_list.pop(0)
                        while len(bullet_list) > 0:
                            bullet_list.pop(0)
                        hero.SCORE = 0
                        hero.x = setting_win['WIDTH'] // 2 - setting_hero['WIDTH'] // 2
                        menu = False
                    if rect_end.collidepoint(x, y):
                        game = False

        

        for event in events:
            if event.type == boss_shoot and boss.LIVE:
                bullet_list.append(Bullet(boss.centerx + 40, boss.bottom, 10, 20))
                bullet_list.append(Bullet(boss.centerx - 50, boss.bottom, 10, 20))
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    hero.MOVE['LEFT'] = True
                if event.key == pygame.K_d:
                    hero.MOVE['RIGHT'] = True
                if event.key == pygame.K_SPACE:
                    hero.BULLET.append(Bullet(hero.centerx + 15, hero.y+ 40, 10,20))
                    hero.BULLET.append(Bullet(hero.centerx - 25, hero.y+ 40, 10, 20))
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    hero.MOVE['LEFT'] = False
                if event.key == pygame.K_d:
                    hero.MOVE['RIGHT'] = False

        clock.tick(setting_win['FPS'])
        pygame.display.flip()

run() 
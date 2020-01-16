import arcade
import math
import random
import settings

# default window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "WeFly X Charlie"
BULLET_SPEED = 2
Score = 0
INSTRUCTIONS_PAGE_0 = 0
INSTRUCTIONS_PAGE_1 = 1
GAME_RUNNING = 2
GAME_OVER = 3
WIN = 4
position_y_1 = 600
position_y_2 = 0

# default boss' properties
explode = 0
explode_x = 0
explode_y = 0
fps = 0
boss_create_fps = 0

level = 0
# boss level prompt
prompt = False
prompt_time = 0

boss_sound_on = 0
game_sound_on = 0

boss_hp = 0
boss_hp_current = 0

# default boss laser
laser_bomb = False
laser_effect = 0
laser_fps = 0

# Calculate the remaining missile
laser_counter = 0
laser_counter_update = 0

try:
    background_sound = arcade.sound.load_sound("music/bgm_zhuxuanlv.mp3")
    missile_sound_1 = arcade.load_sound("music/rocketswitch.wav")
    hp_bonus_sound = arcade.load_sound("music/supply.wav")
    button_sound = arcade.load_sound("music/button.wav")
    bomb_sound = arcade.load_sound("music/all_bomb.wav")

    game_sound = arcade.sound.load_sound("music/bgm_zhandou2.mp3.wav")
    game_sound_1 = arcade.sound.load_sound("music/bgm_zhandou2.mp3.wav")
    game_sound_2 = arcade.sound.load_sound("music/bgm_zhandou2.mp3.wav")
    game_sound_3 = arcade.sound.load_sound("music/bgm_zhandou2.mp3.wav")

    boss_sound_1 = arcade.sound.load_sound("music/boss_sound.wav")
    boss_sound_2 = arcade.sound.load_sound("music/boss_sound.wav")
    boss_sound_3 = arcade.sound.load_sound("music/boss_sound.wav")
    boss_sound_4 = arcade.sound.load_sound("music/boss_sound.wav")

except Exception as e:
    print("Error loading sound.", e)


class Enemy(arcade.Sprite):
    # pass attribute to enemy
    def __init__(self, image, scale, ehp, score, speed, boss):
        """
        Initialize an enemy with information passed in.

        :param image: enemy image
        :param scale: enemy scale
        :param ehp: enemy hit points
        :param score: kill enemy score
        :param speed: enemy speed
        :param boss: enemy type, True when he is boss
        """
        arcade.Sprite.__init__(self, image, scale)
        self.ehp = ehp
        self.score = score
        self.speed = speed
        self.boss = boss
        self.left_boss = True

    # self armo damage, hhp
    def hitted(self, hhp):
        """
        Enemy hit by self bullet. Return boss kill information and killed coordinates.

        :param hhp: self bullet damage to the enemy
        :return: Tuple, represents boss killed(1), otherwise(0); killed xy coordinates in order.
        """
        global Score
        self.ehp = max(0, self.ehp - hhp)
        if self.ehp == 0:
            self.kill()
            Score += self.score
            if self.boss:
                return (1, self.center_x, self.center_y)
        return (0, 0, 0)

    def drop(self):
        """
        Update enemy location
        :return: None
        """
        if self.boss and self.center_y <= 450:

            if self.center_x <= 100:
                self.left_boss = False

            if self.center_x >= 700:
                self.left_boss = True

            if self.left_boss:
                self.center_x -= 2
            else:
                self.center_x += 2

            if self.center_x == 100:
                self.left_boss = False
            if self.center_x == 700:
                self.left_boss = True

        else:
            self.center_y -= self.speed

        if self.center_y < 0:
            self.kill()


class Chapter1View(arcade.View):
    def __init__(self):
        super().__init__()
        self.frame_count = 0
        self.hp = 100
        self.boss = False
        self.laser_player = 0

        self.enemy_list = None
        self.bullet_list = None
        self.bullet_self_list = None
        self.player_list = None
        self.player = None
        self.assist = None
        self.bonus = None

        self.instructions = []
        texture = arcade.load_texture("images/fm.jpeg")
        self.instructions.append(texture)
        texture = arcade.load_texture("images/intro.jpeg")
        self.instructions.append(texture)

        self.current_state = INSTRUCTIONS_PAGE_0

    def setup(self):
        """
        Initialize game interface. Default schedule is 60 fps.
        :return: None
        """
        self.frame_count = 0
        self.hp = 100
        self.boss = False
        self.laser_player = 0

        self.enemy_list = None
        self.bullet_list = None
        self.bullet_self_list = None
        self.player_list = None
        self.player = None
        self.assist = None
        self.bonus = None

        arcade.schedule(self.on_update, 1 / 60)
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.bullet_self_list = arcade.SpriteList()
        self.assist = arcade.SpriteList()
        self.bonus = arcade.SpriteList()

        # Add player ship
        self.player = arcade.Sprite("images/SeHero.png", 0.6)

        self.player_list.append(self.player)

        # draw instruction page

    def draw_instructions_page(self, page_number):
        """
        Draw an instruction page. Load the page as an image.

        """
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, page_texture.width,
                                      page_texture.height,
                                      page_texture, 0)
        if self.current_state == INSTRUCTIONS_PAGE_0:
            page_texture = arcade.load_texture("images/play.png")
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, 200, page_texture.width, page_texture.height,
                                          page_texture,
                                          0)

    # draw game over page
    def draw_game_over(self):
        """
        Draw "Game over" across the screen.
        """
        output = "Game Over"
        arcade.draw_text(output, 220, 350, arcade.color.WHITE, 54)

        output = "Click anywhere to quit"
        arcade.draw_text(output, 245, 260, arcade.color.WHITE, 24)

    def draw_game_win(self):
        texture = arcade.load_texture("images/win_page.jpeg")
        arcade.draw_texture_rectangle(400, 300, 800, 600, texture)

    def draw_game(self):

        # Draw background and boss for each level
        if level == 0:
            texture_1 = arcade.load_texture("images/bg_0.jpg")
            arcade.draw_texture_rectangle(400, position_y_1, 800, 600, texture_1)
            texture_2 = arcade.load_texture("images/bg_0.jpg")
            arcade.draw_texture_rectangle(400, position_y_2, 800, 600, texture_1)
            texture_0 = arcade.load_texture("images/boss_2.png")

        if level == 1:
            texture_1 = arcade.load_texture("images/bg_new.jpg")
            arcade.draw_texture_rectangle(400, position_y_1, 800, 600, texture_1)
            texture_2 = arcade.load_texture("images/bg_new.jpg")
            arcade.draw_texture_rectangle(400, position_y_2, 800, 600, texture_1)
            texture_0 = arcade.load_texture("images/boss_4.png")

        if level == 2:
            texture_1 = arcade.load_texture("images/bg_1.jpg")
            arcade.draw_texture_rectangle(400, position_y_1, 800, 600, texture_1)
            texture_2 = arcade.load_texture("images/bg_1.jpg")
            arcade.draw_texture_rectangle(400, position_y_2, 800, 600, texture_1)
            texture_0 = arcade.load_texture("images/boss_1.png")

        if level == 3:
            texture_1 = arcade.load_texture("images/bg_new_1.jpg")
            arcade.draw_texture_rectangle(400, position_y_1, 800, 600, texture_1)
            texture_2 = arcade.load_texture("images/bg_new_1.jpg")
            arcade.draw_texture_rectangle(400, position_y_2, 800, 600, texture_1)
            texture_0 = arcade.load_texture("images/boss_5.png")

        # draw images
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        self.bullet_self_list.draw()
        self.assist.draw()
        self.bonus.draw()

        # boss killed explode animation
        if explode == 1:
            arcade.draw_texture_rectangle(explode_x, explode_y, 240, 180, texture_0)
            texture_1 = arcade.load_texture("images/bigairplane3.png")
            arcade.draw_texture_rectangle(explode_x, explode_y, 90, 90, texture_1)
        elif explode == 2:
            arcade.draw_texture_rectangle(explode_x, explode_y, 240, 180, texture_0)
            texture_1 = arcade.load_texture("images/bigairplane4.png")
            arcade.draw_texture_rectangle(explode_x, explode_y, 90, 90, texture_1)
        elif explode == 3:
            arcade.draw_texture_rectangle(explode_x, explode_y, 240, 180, texture_0)
            texture_1 = arcade.load_texture("images/bigairplane5.png")
            arcade.draw_texture_rectangle(explode_x, explode_y, 90, 90, texture_1)
        elif explode == 4:
            texture_0 = arcade.load_texture("images/bg_road.png")
            arcade.draw_texture_rectangle(400, 300, 450, 430, texture_0)

        # Draw different boss lasers
        for b in self.enemy_list:
            if level == 0:
                if laser_effect == 1:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser6.png"))
                elif laser_effect == 2:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser7.png"))
                elif laser_effect == 3:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser8.png"))
                elif laser_effect == 4:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser9.png"))
                elif laser_effect == 5:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser10.png"))
                elif laser_effect == 6:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser11.png"))

            if level == 1:
                if laser_effect == 1:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser6.png"))
                elif laser_effect == 2:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser7.png"))
                elif laser_effect == 3:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser8.png"))
                elif laser_effect == 4:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser9.png"))
                elif laser_effect == 5:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser10.png"))
                elif laser_effect == 6:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser11.png"))

            if level == 2:
                if laser_effect == 1:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser6.png"))
                    arcade.draw_texture_rectangle(b.center_x + 30, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser6.png"))
                elif laser_effect == 2:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser7.png"))
                    arcade.draw_texture_rectangle(b.center_x + 30, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser7.png"))
                elif laser_effect == 3:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser8.png"))
                    arcade.draw_texture_rectangle(b.center_x + 30, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser8.png"))
                elif laser_effect == 4:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser9.png"))
                    arcade.draw_texture_rectangle(b.center_x + 30, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser9.png"))
                elif laser_effect == 5:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser10.png"))
                    arcade.draw_texture_rectangle(b.center_x + 30, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser10.png"))
                elif laser_effect == 6:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser11.png"))
                    arcade.draw_texture_rectangle(b.center_x + 30, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser11.png"))

            if level == 3:
                if laser_effect == 1:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser6.png"))
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser6.png"))
                    arcade.draw_texture_rectangle(b.center_x + 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser6.png"))
                elif laser_effect == 2:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser7.png"))
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser7.png"))
                    arcade.draw_texture_rectangle(b.center_x + 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser7.png"))
                elif laser_effect == 3:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser8.png"))
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser8.png"))
                    arcade.draw_texture_rectangle(b.center_x + 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser8.png"))
                elif laser_effect == 4:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser9.png"))
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser9.png"))
                    arcade.draw_texture_rectangle(b.center_x + 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser9.png"))
                elif laser_effect == 5:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser10.png"))
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser10.png"))
                    arcade.draw_texture_rectangle(b.center_x + 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser10.png"))
                elif laser_effect == 6:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser11.png"))
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser11.png"))
                    arcade.draw_texture_rectangle(b.center_x + 40, b.center_y - 300, 30, 600,
                                                  arcade.load_texture("images/bomb_laser11.png"))

        if prompt:
            arcade.draw_texture_rectangle(400, 350, 300, 200, arcade.load_texture("images/boss_prompt.png"))

        if self.boss:
            arcade.draw_lrtb_rectangle_outline(300, 500, 580, 560, arcade.color.BLACK, 2)
            arcade.draw_lrtb_rectangle_filled(302, 302 + (198 * boss_hp_current) // boss_hp, 578, 562,
                                              arcade.color.RADICAL_RED)

        # show hp, current score, and remaining laser times on the screen
        arcade.draw_text("Score: {0:10.2f}".format(Score), 610, 560, arcade.color.WHITE, 12)
        arcade.draw_lrtb_rectangle_outline(60, 170, 580, 560, arcade.color.WHITE, 2)
        arcade.draw_lrtb_rectangle_filled(62, 62 + (106 * self.hp) // 100, 578, 562, arcade.color.WHITE)
        arcade.draw_text("HP: {0:10.2f}%".format(self.hp), 180, 562, arcade.color.WHITE, 12)
        if self.laser_player >= 1:
            for i in range(self.laser_player):
                arcade.draw_texture_rectangle(760 - i * 50, 520, 50, 40,
                                              arcade.load_texture("images/missile_icon.png"))

    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE_SAPPHIRE)

    def dead(self):
        """
        Clear the screen when dead
        :return: None
        """
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.bullet_self_list = arcade.SpriteList()
        self.current_state = GAME_OVER

    def on_draw(self):
        arcade.start_render()
        # arcade.draw_text("Chapter 1", settings.WIDTH/2, settings.HEIGHT/2,
        #                  arcade.color.BLACK, font_size=30, anchor_x="center")
        # page_texture = arcade.load_texture("Icon-57.png")
        # arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, 200, page_texture.width, page_texture.height, page_texture,
        #                               0)
        #
        # arcade.start_render()
        if self.current_state == GAME_RUNNING:
            self.draw_game()
        elif self.current_state == INSTRUCTIONS_PAGE_0:
            self.draw_instructions_page(0)
        elif self.current_state == INSTRUCTIONS_PAGE_1:
            self.draw_instructions_page(1)
        elif self.current_state == GAME_OVER:
            self.draw_game()
            self.draw_game_over()
        elif self.current_state == WIN:
            self.draw_game_win()

    def update(self, delta_time):
        """All the logic to move, and the game logic goes here. """
        global explode, explode_x, explode_y, fps, position_y_1, position_y_2, level, prompt, prompt_time, boss_hp, boss_hp_current
        global up_pressed, down_pressed, left_pressed, right_pressed, laser_bomb, laser_effect, laser_fps, laser_counter, laser_counter_update
        global boss_create_fps, boss_sound_on, game_sound_on, game_sound_1, game_sound_2, game_sound_3, boss_sound_1, boss_sound_2, boss_sound_3, game_sound, boss_sound_4

        if self.current_state != GAME_RUNNING and self.frame_count % 3480 == 0:
            try:
                arcade.play_sound(background_sound)
            except Exception as e:
                print("Error playing sound.", e)
            pass
        if self.current_state == GAME_RUNNING:
            try:
                arcade.stop_sound(background_sound)
            except Exception as e:
                print("Error pausing sound.", e)
            pass

        if level == 4:
            self.current_state = WIN
            return
        if self.current_state == GAME_RUNNING:

            if self.boss and boss_sound_on == 0:
                boss_sound_on = 1
                try:
                    if level == 0:
                        arcade.stop_sound(game_sound)
                        arcade.play_sound(boss_sound_1)
                    if level == 1:
                        game_sound_1.pause()
                        arcade.play_sound(boss_sound_2)
                    if level == 2:
                        game_sound_2.pause()
                        arcade.play_sound(boss_sound_3)
                    if level == 3:
                        game_sound_3.pause()
                        arcade.play_sound(boss_sound_4)
                except Exception as e:
                    print("Error pausing sound.", e)
                pass

            if not self.boss:
                try:
                    if level == 0:
                        boss_sound_1.pause()
                    if level == 1:
                        boss_sound_2.pause()
                    if level == 2:
                        boss_sound_3.pause()
                    if level == 3:
                        boss_sound_4.pause()

                except Exception as e:
                    print("Error pausing sound.", e)
                pass

                boss_sound_on = 0
                # if (self.frame_count - fps) == 180 and fps != 0:
                #     game_sound_on = 0

            if game_sound_on == 0:
                try:
                    if level == 0:
                        arcade.play_sound(game_sound)
                    if level == 1:
                        arcade.play_sound(game_sound_1)
                    if level == 2:
                        arcade.play_sound(game_sound_2)
                    if level == 3:
                        arcade.play_sound(game_sound_3)

                except Exception as e:
                    print("Error playing sound.", e)
                pass
                game_sound_on = 1

            # update remaining laser based on current score
            laser_counter = Score // 1000 + 1
            if laser_counter + laser_counter_update == 1:
                arcade.play_sound(missile_sound_1)
                self.laser_player += 1
                laser_counter_update -= 1

            if self.hp <= 0:
                game_sound_on = 10
                try:
                    arcade.stop_sound(game_sound)
                    # game_sound_1.pause()
                    # game_sound_2.pause()
                    # game_sound_3.pause()
                    # boss_sound_1.pause()
                    # boss_sound_2.pause()
                    # boss_sound_3.pause()
                    # boss_sound_4.pause()

                except Exception as e:
                    print("Error pausing sound.", e)

                self.dead()

            else:
                # drop hp bonus every 60s
                if self.frame_count % 3600 == 3599:
                    bonus_hp = arcade.Sprite("images/hp_bonus.png", 0.45)
                    bonus_hp.center_x = random.randrange(0, SCREEN_WIDTH)
                    bonus_hp.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT * 1.25)
                    self.bonus.append(bonus_hp)

                if self.frame_count % 240 == 0 and not self.boss and not 1 <= explode <= 4:
                    for _ in range(2 + level):
                        # generate randomly enemy planes of different levels
                        ranNum = random.randint(0, 1000)
                        if ranNum < 500:
                            enemy = Enemy("images/plane_small.png", 0.8, 2, 10, 4, False)
                        elif ranNum < 850:
                            enemy = Enemy("images/bigplane0.png", 0.7, 3, 50, 3, False)
                        else:
                            enemy = Enemy("images/boss0.png", 0.35, 5, 100, 2, False)

                        enemy.center_x = random.randrange(0, SCREEN_WIDTH)
                        enemy.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT * 1.25)
                        enemy.angle = 180
                        self.enemy_list.append(enemy)

                # create a boss and ensure no small enemies appear during the boss battle
                elif self.frame_count - fps == (1799 * (level + 1)) and not self.boss and not 1 <= explode <= 4:
                    # 提示
                    boss_create_fps = self.frame_count
                    prompt = True
                    prompt_time = self.frame_count

                    # update boss image based on game level
                    if level == 0:
                        enemy = Enemy("images/boss_2.png", 0.8, 25, 500, 2, True)
                    elif level == 1:
                        enemy = Enemy("images/boss_4.png", 0.8, 35, 1000, 3, True)
                    elif level == 2:
                        enemy = Enemy("images/boss_1.png", 0.8, 50, 2000, 3, True)
                    elif level == 3:
                        enemy = Enemy("images/boss_5.png", 0.8, 70, 4000, 3, True)

                    enemy.center_x = random.randrange(0, SCREEN_WIDTH)
                    enemy.center_y = SCREEN_HEIGHT * 2
                    enemy.angle = 180
                    self.enemy_list.append(enemy)
                    self.boss = True
                    boss_hp = enemy.ehp

                # set time for boss prompt to be 3s
                if self.frame_count - prompt_time == 180 and prompt:
                    prompt = False

                # update player's hp based on different damage levels from boss
                for boss in self.enemy_list:
                    if 1 <= laser_effect <= 6:
                        # realize the disappearance of self bullet when it hits boss
                        for e in self.bullet_self_list:
                            if boss.center_x - 20 <= e.center_x <= boss.center_x + 20:
                                e.kill()
                        # calculate different damage levels of laser from boss
                        if level == 0:
                            if self.player.center_x - 36 < boss.center_x < self.player.center_x + 36:
                                self.hp = max(0, self.hp - 0.8)
                        if level == 1:
                            if self.player.center_x - 36 < boss.center_x < self.player.center_x + 36:
                                self.hp = max(0, self.hp - 0.9)
                        if level == 2:
                            if self.player.center_x - 36 < boss.center_x - 45 < self.player.center_x + 36 or self.player.center_x - 36 < boss.center_x + 15 < self.player.center_x + 36:
                                self.hp = max(0, self.hp - 1)
                        if level == 3:
                            if self.player.center_x - 36 < boss.center_x - 45 < self.player.center_x + 36 or self.player.center_x - 36 < boss.center_x < self.player.center_x + 36 or self.player.center_x - 36 < boss.center_x + 15 < self.player.center_x + 36:
                                self.hp = max(0, self.hp - 1.1)

                # update the background position
                position_y_1 -= 1
                position_y_2 -= 1

                if position_y_1 == -300:
                    position_y_1 = 900
                if position_y_2 == -300:
                    position_y_2 = 900

                # collision with bullet
                bullet_collide_list = arcade.check_for_collision_with_list(self.player, self.bullet_list)
                for collide_bullet in bullet_collide_list:
                    collide_bullet.kill()
                    self.hp = max(0, self.hp - 5)

                # collision with enemy
                enemy_collide_list = arcade.check_for_collision_with_list(self.player, self.enemy_list)
                for collide_enemy in enemy_collide_list:
                    collide_enemy.kill()
                    if self.boss:
                        self.hp = 0
                    self.hp = max(0, self.hp - 30)

                # calculate different damage of player's bullet or bomb makes on enemy or boss
                for e in self.enemy_list:
                    if e.boss:
                        boss_hp_current = e.ehp
                    bullet_hit_list = arcade.check_for_collision_with_list(e, self.bullet_self_list)
                    for bullet_hit in bullet_hit_list:
                        bullet_hit.kill()

                        boss_hit = e.hitted(1)
                        if boss_hit[0] == 1:
                            self.boss = False

                            explode = 1
                            explode_x = boss_hit[1]
                            explode_y = boss_hit[2]
                            fps = self.frame_count

                for bomb in self.assist:
                    bullet_hit_list = arcade.check_for_collision_with_list(bomb, self.bullet_list)

                    for b in bullet_hit_list:
                        b.kill()

                for e in self.enemy_list:
                    if e.boss:
                        boss_hp_current = e.ehp
                    bullet_hit_list = arcade.check_for_collision_with_list(e, self.assist)
                    for bullet_hit in bullet_hit_list:

                        boss_hit = e.hitted(0.3)
                        if boss_hit[0] == 1:
                            self.boss = False

                            explode = 1
                            explode_x = boss_hit[1]
                            explode_y = boss_hit[2]
                            fps = self.frame_count

                # boss explode animation
                if explode == 1 and self.frame_count - fps == 20:
                    arcade.play_sound(bomb_sound)
                    explode += 1
                elif explode == 2 and self.frame_count - fps == 40:
                    explode += 1
                elif explode == 3 and self.frame_count - fps == 60:
                    explode += 1
                elif explode == 4 and self.frame_count - fps == 180:
                    explode += 1
                    level += 1
                    # bomb_sound.pause()
                    game_sound_on = 0

                # use loop to make all enemies facing to the player
                for enemy in self.enemy_list:

                    # First, calculate the angle to the player. We could do this
                    # only when the bullet fires, but in this case we will rotate
                    # the enemy to face the player each frame, so we'll do this
                    # each frame.

                    # Position the start at the enemy's current location
                    start_x = enemy.center_x
                    start_y = enemy.center_y

                    # list_1[i][2]Get the destination location for the bullet
                    dest_x = self.player.center_x
                    dest_y = self.player.center_y

                    # Do math to calculate how to get the bullet to the destination.
                    # Calculation the angle in radians between the start points
                    # and end points. This is the angle the bullet will travel.
                    x_diff = dest_x - start_x
                    y_diff = dest_y - start_y
                    angle = math.atan2(y_diff, x_diff)

                    # use if statement to exclude the boss angle
                    if enemy.boss:
                        enemy.angle = 0
                    else:
                        enemy.angle = math.degrees(angle) - 270

                    # determine the shooting characteristics of enemy / boss planes
                    if enemy.boss and self.frame_count % ((120 - 20 * level) // 2) == 0:
                        bullet = arcade.Sprite("images/boss_bullet.png", 0.5)
                        bullet.center_x = start_x
                        bullet.center_y = start_y
                        bullet.angle = 0
                        bullet.change_x = 0
                        bullet.change_y = - BULLET_SPEED * (level // 3 + 1)
                        self.bullet_list.append(bullet)
                    elif self.frame_count % (120 - 20 * level) == 0:
                        bullet = arcade.Sprite("images/enemy_bullet.png", 0.5)
                        bullet.center_x = start_x
                        bullet.center_y = start_y
                        bullet.angle = math.degrees(angle)
                        bullet.change_x = math.cos(angle) * BULLET_SPEED * (level // 3 + 1)
                        bullet.change_y = math.sin(angle) * BULLET_SPEED * (level // 3 + 1)
                        self.bullet_list.append(bullet)

                # determine the shooting frequency of the player airplane
                if self.frame_count % (15 - 2 * level) == 0:
                    bullet = arcade.Sprite("images/Bomb2.png", 0.7)
                    bullet.center_x = self.player.center_x
                    bullet.center_y = self.player.center_y

                    # Angle the bullet sprite
                    bullet.angle = 0

                    # Taking into account the angle, calculate our change_x
                    # and change_y. Velocity is how fast the bullet travels.
                    bullet.change_x = 0
                    bullet.change_y = BULLET_SPEED * 3

                    self.bullet_self_list.append(bullet)
                    # arcade.play_sound(bullet_sound)

                # use loops to remove the bullet when it flies off-screen
                for bullet in self.bullet_self_list:
                    if bullet.bottom > 600:
                        bullet.kill()

                for bullet in self.assist:
                    if bullet.bottom > 600:
                        bullet.kill()

                for bullet in self.bullet_list:
                    if bullet.top < 0:
                        bullet.kill()

                # use loops to control the dropping of hp_bonus
                for hp_bonus in self.bonus:
                    hp_bonus.center_y -= 5
                    # update player's hp when it catches hp_bonus
                    if arcade.check_for_collision(self.player, hp_bonus):
                        self.hp = min(100, self.hp + 30)
                        arcade.play_sound(hp_bonus_sound)
                        hp_bonus.kill()
                    # remove hp_bonus when it gets out of windows
                    if hp_bonus.top < 0:
                        hp_bonus.kill()

                # keyboard control the movement of the player
                if up_pressed:
                    self.player.center_y = min(552, self.player.center_y + 5)
                if down_pressed:
                    self.player.center_y = max(48, self.player.center_y - 5)
                if left_pressed:
                    self.player.center_x = max(36, self.player.center_x - 5)
                if right_pressed:
                    self.player.center_x = min(764, self.player.center_x + 5)

                # trigger the missile
                if laser_bomb and self.laser_player > 0 and len(self.assist) <= 1:
                    assist_bomb = arcade.Sprite("images/assisent1_1.png", 1)
                    assist_bomb.center_x = self.player.center_x - 25
                    assist_bomb.center_y = self.player.center_y
                    assist_bomb.angle = 0
                    assist_bomb.change_x = 0
                    assist_bomb.change_y = 10
                    self.assist.append(assist_bomb)

                    assist_bomb = arcade.Sprite("images/assisent1_1.png", 1)
                    assist_bomb.center_x = self.player.center_x + 25
                    assist_bomb.center_y = self.player.center_y
                    assist_bomb.angle = 0
                    assist_bomb.change_x = 0
                    assist_bomb.change_y = 10
                    self.assist.append(assist_bomb)

                    self.laser_player -= 1

                # use if statement to set the laser shooting period to be 8s
                if self.boss and (self.frame_count - boss_create_fps) % 480 == 0 and (
                        self.frame_count - boss_create_fps) != 0:
                    laser_effect = 1
                    laser_fps = self.frame_count

                # use if statement to animate laser
                if laser_effect == 1 and self.frame_count - laser_fps == 20:
                    laser_effect += 1
                elif laser_effect == 2 and self.frame_count - laser_fps == 40:
                    laser_effect += 1
                elif laser_effect == 3 and self.frame_count - laser_fps == 60:
                    laser_effect += 1
                elif laser_effect == 4 and self.frame_count - laser_fps == 80:
                    laser_effect += 1
                elif laser_effect == 5 and self.frame_count - laser_fps == 100:
                    laser_effect += 1
                elif laser_effect == 6 and self.frame_count - laser_fps == 120:
                    laser_effect += 1

                # realize the dropping of boss and enemy planes
                for e in self.enemy_list:
                    e.drop()

                if level == 4:
                    self.current_state = WIN
                    self.set_mouse_visible(True)

                self.bullet_list.update()
                self.bullet_self_list.update()
                self.assist.update()
        # update the frame_count
        self.frame_count += 1

    # def on_key_press(self, key, modifiers):
    #     self.director.next_view()
    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        :param x: player x-location
        :param y: player y-location
        :param delta_x: player delta x
        :param delta_y: player delta y
        :return: None
        """
        if self.current_state == GAME_RUNNING:
            self.player.center_x = x
            self.player.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        global level, Score, prompt, prompt_time, boss_hp, boss_hp_current, laser_bomb, laser_effect, laser_fps, laser_counter, laser_counter_update
        global game_sound_on
        """
        Called when the user presses a mouse button.
        """

        # Change states as needed.
        if self.current_state == INSTRUCTIONS_PAGE_0 and x >= 280 and x <= 520 and y >= 102 and y <= 198:
            arcade.play_sound(button_sound)
            # Next page of instructions.
            self.current_state = INSTRUCTIONS_PAGE_1
        elif self.current_state == INSTRUCTIONS_PAGE_1:
            # Start the game
            self.current_state = GAME_RUNNING
            self.setup()

        elif self.current_state == GAME_OVER:
            self.close()

            # The addition of sound effect would mess up our page transfer
            # Restart the game.
            # level = 0
            # Score = 0
            # prompt = False
            # prompt_time = 0
            #
            # boss_hp = 0
            # boss_hp_current = 0
            #
            # laser_bomb = False
            # laser_effect = 0
            # laser_fps = 0
            #
            # laser_counter = 0
            # laser_counter_update = 0
            #
            # self.setup()
            # self.current_state = GAME_RUNNING
            # game_sound_on = 0
        elif self.current_state == WIN:
            self.close()

            # Restart the game.
            # level = 0
            # Score = 0
            # prompt = False
            # prompt_time = 0
            #
            # boss_hp = 0
            # boss_hp_current = 0
            #
            # laser_bomb = False
            # laser_effect = 0
            # laser_fps = 0
            #
            # laser_counter = 0
            # laser_counter_update = 0
            # self.setup()
            # self.current_state = GAME_RUNNING

    # def on_mouse_press(self, x, y, button, modifiers):
    #     if  x >= 280 and x <= 520 and y >= 102 and y <= 198:
    #         game_main()

# Variables to record if certain keys are being pressed.
up_pressed = False
down_pressed = False
left_pressed = False
right_pressed = False


if __name__ == "__main__":
    """This section of code will allow you to run your View
    independently from the main.py file and its Director.

    You can ignore this whole section. Keep it at the bottom
    of your code.

    It is advised you do not modify it unless you really know
    what you are doing.
    """
    from utils import FakeDirector

    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    my_view = Chapter1View()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
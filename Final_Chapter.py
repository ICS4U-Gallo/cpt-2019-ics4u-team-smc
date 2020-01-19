import json
import math
import random
import threading
from typing import Tuple, List, Dict

import arcade
import cv2
import numpy as np

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
LEADERBOARD = 5
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

# calculate the remaining missile
laser_counter = 0
laser_counter_update = 0

# store tracking information
enemy_track = []
enemy_track_1 = {}

# Default autopilot mode
mode = 2
Q = (-5, 5)
W = (0, 5)
E = (5, 5)
A = (-5, 0)
S = (0, 0)
D = (5, 0)
Z = (-5, -5)
X = (0, -5)
C = (5, -5)
directions = [Z, X, C, A, D, Q, W, E, S]
moves = []
mm = 0

# sound error handling
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
    game_sound_4 = arcade.sound.load_sound("music/bgm_zhandou2.mp3.wav")

    boss_sound_1 = arcade.sound.load_sound("music/boss_sound.wav")
    boss_sound_2 = arcade.sound.load_sound("music/boss_sound.wav")
    boss_sound_3 = arcade.sound.load_sound("music/boss_sound.wav")
    boss_sound_4 = arcade.sound.load_sound("music/boss_sound.wav")
    boss_sound_5 = arcade.sound.load_sound("music/boss_sound.wav")

except Exception as e:
    print("Error loading sound.", e)

class Enemy(arcade.Sprite):
    """ Create an Enemy class (Inherit from arcade.Sprite class)

    Attributes:
        image (str): The enemy image
        scale (float): The enemy scale
        ehp (float): The health point of enemy airplane
        score (int): Kill enemy airplane score
        speed (float): The enemy speed
        number (int): The enemy number
    """
    enemies: List["Enemy"] = []

    def __init__(self, image: str, scale: float, ehp: float, score: int, speed: float):
        """ Initialize an enemy with information passed in.

        Args:
            image: enemy image
            scale: enemy scale
            ehp: enemy hit points
            score: kill enemy score
            speed: enemy speed
        """
        arcade.Sprite.__init__(self, image, scale)
        self.ehp = ehp
        self.score = score
        self.speed = speed
        self.number = Enemy.count_enemy()
        Enemy.enemies.append(self)

    # Encapsulation getter and setter method
    def get_ehp(self) -> float:
        return self.ehp

    def set_ehp(self, new_ehp) -> None:
        self.ehp = new_ehp

    def get_score(self) -> int:
        return self.score

    def set_score(self, new_score) -> None:
        self.score = new_score

    def get_speed(self) -> float:
        return self.speed

    def set_speed(self, new_speed) -> None:
        self.speed = new_speed

    def get_number(self) -> int:
        return self.number

    @classmethod
    def count_enemy(cls) -> int:
        """ a class method that counts enemies

        Args:
            None
        Returns:
            The number of enemies
        """
        return len(cls.enemies)

    @classmethod
    def refresh_enemy(cls) -> None:
        """ a class method that clears off enemies

        Args:
            None
        Returns:
            None
        """
        cls.enemies = []

#TODO
    def pascal(self, n):
        if n == 1:
            return [[1]]
        previous = self.pascal(n - 1)
        last = [0] + previous[-1] + [0]
        new_row = [last[i] + last[i - 1] for i in range(1, len(last))]
        return previous + [new_row]

    def drop(self) -> None:
        """ A helper function that updates enemy location

        Args:
            None
        Returns:
            None
        """
        # if self.path_type == 'BSpline':
        #     if self.current_point == self.max_point:
        #         self.current_point = 0
        #     self.center_x = self.path_points[0][self.current_point]
        #     self.center_y = self.path_points[1][self.current_point]
        #     self.current_point += 1
        self.center_y -= self.get_speed()

        # clear the enemy when it flies off the screen
        if self.center_y < 0:
            self.kill()

    # self armo damage, hhp
    def hitted(self, hhp: float) -> Tuple[int, float, float]:
        """ Enemy hit by self bullet. Return boss kill information and killed coordinates.

        Args:
            hhp: self bullet damage to the enemy

        Returns:
            a tuple that represents boss killed(1), otherwise(0); killed xy coordinates in order.
        """
        global Score
        self.ehp = max(0, self.get_ehp() - hhp)
        if self.get_ehp() == 0:
            self.kill()
            Score += self.get_score()
        return (0, 0, 0)


class Boss(Enemy):
    """ Create a Boss enemy class (Inherit from arcade.Sprite class)

    Attributes:
        image (str): The enemy image
        scale (float): The enemy scale
        ehp (float): The health point of enemy airplane
        score (int): Kill enemy airplane score
        speed (float): The enemy speed
        left_boss (bool): Trigger the left movement of boss
    """
    def __init__(self, image: str, scale: float, ehp: float, score: int, speed: float):
        """ Initialize a Boss with information passed in.

       Args:
           image: boss image
           scale: boss scale
           ehp: enemy hit points
           score: kill boss score
           speed: boss speed
       """
        super().__init__(image, scale, ehp, score, speed)
        self.left_boss = True

    # drop method overriding
    def drop(self):
        """ A helper function that updates boss location

       Args:
           None
       Returns:
           None
       """
        if self.center_y <= 480:
            if self.center_x <= 100:
                self.left_boss = False

            if self.center_x >= 700:
                self.left_boss = True

            if self.left_boss:
                self.center_x -= 2
            else:
                self.center_x += 2
        else:
            super().drop()

    # hitted method overriding
    def hitted(self, hhp: float) -> Tuple[int, float, float]:
        """ Enemy hit by self bullet. Return boss kill information and killed coordinates.

        Args:
            hhp: self bullet damage to the enemy

        Returns:
            a tuple that represents boss killed(1), otherwise(0); killed xy coordinates in order.
        """
        global Score
        self.ehp = max(0, self.ehp - hhp)
        if self.ehp == 0:
            self.kill()
            Score += self.score
            # trigger explosion animation
            return (1, self.center_x, self.center_y)
        return (0, 0, 0)


class Bullet(arcade.Sprite):
    """ Create a Bullet class (Inherit from arcade.Sprite class)

    Attributes:
        img (str): The bullet image
        scale (float): The bullet scale
        hp (float): The health point of the bullet
        number (int): number of bullets
    """
    bullets: List = []

    def __init__(self, img: str, scale: float):
        """ Create a bullet with arguments passed in

       Args:
           img: the bullet image
           scale: the bullet scale
       """
        super().__init__(img, scale)
        self.number = len(Bullet.bullets)
        self.hp = 15
        Bullet.bullets.append(self)

    def hit(self, h: int) -> None:
        """ Update the hp of self bullet when hits the enemy

       Args:
           h: damage to self bullet

       Returns:
           None
       """
        self.hp -= h
        if self.hp < 0:
            self.kill()


class MyGame(arcade.Window):
    """ Create a main application class (Inherit from arcade.Window class)

    Attributes:
        width (int): Window width
        height (int): Window height
        title (str): Window title
        frame_count (int): Frame recorder
        hp (float): Airplane health point
        boss (bool): Boss state
        laser_player (int): the number of laser
# TODO
    """

    def __init__(self, width: int, height: int, title: str):
        """ Initialize the game window

        Args:
            width: Window width
            height: Window height
            title: Window title
        """
        super().__init__(width, height, title)

        self.frame_count = 0
        self.hp = 100
        self.boss = False
        self.laser_player = 0

        self.enemy_list = None
        self.bullet_list = None
        self.bullet_pet_list = None
        self.bullet_self_list = None
        self.player_list = None
        self.player = None
        self.pet_list = None
        self.pet = None
        self.pet2 = None
        self.assist = None
        self.bonus = None

        self.instructions = []
        texture = arcade.load_texture("images/fm.jpeg")
        self.instructions.append(texture)
        texture = arcade.load_texture("images/intro.jpeg")
        self.instructions.append(texture)
        texture = arcade.load_texture("images/new_leaderboard.png")
        self.instructions.append(texture)

        self.current_state = INSTRUCTIONS_PAGE_0

    @staticmethod
    def get_distance(x1: float, y1: float, x2: float, y2: float) -> float:
        """ Calculate the distance between two points

        Args:
            x1: initial horizontal location
            y1: initial vertical location
            x2: destination horizontal location
            y2: destination vertical location

        Returns:
            the distance between two points
        """
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    @staticmethod
    def msort(l: List[int]) -> List[int]:
        """ A helper function that sort the data in an ascending order

        Args:
            l: The original data

        Returns:
            a sorted list in ascending order
        """
        # base case
        if len(l) < 2:
            return l
        left_side = MyGame.msort(l[:len(l) // 2])
        right_side = MyGame.msort(l[len(l) // 2:])
        sorted_list = []
        left_marker = 0
        right_marker = 0
        while left_marker < len(left_side) and right_marker < len(right_side):
            if left_side[left_marker] < right_side[right_marker]:
                sorted_list.append(left_side[left_marker])
                left_marker += 1
            else:
                sorted_list.append(right_side[right_marker])
                right_marker += 1
        if left_marker == len(left_side):
            sorted_list.extend(right_side[right_marker:])
        if right_marker == len(right_side):
            sorted_list.extend(left_side[left_marker:])
        return sorted_list

    @staticmethod
    def sorted_data(prim_data: Dict) -> Dict:
        """ Sort the dictionary so that key (score) in descending order, value (time) in ascending order

        Args:
            prim_data: The original data where key reps score, value reps time

        Returns:
            a "sorted" dictionary that has score in descending order and time in ascending order
            {30: [6, 5], 40: [8, 2]} -> {40: [2, 8], 30: [5, 6]}
        """
        final_d = {}
        for score in MyGame.msort([int(s) for s in prim_data.keys()])[::-1]:
            for time in MyGame.msort(prim_data[str(score)]):
                if score not in final_d:
                    final_d[score] = []
                final_d[score].append(time)
        return final_d

    @staticmethod
    def slice_digit(s: str) -> List[str]:
        """ Slice the data passed in, convert all ":" to "hg"

        Args:
            s: player's data
        Returns:
            a list that contains the sliced data (str)
        """
        return [d if d != ":" else "hg" for d in list(s)]

    @staticmethod
    def sort_enemy(enemy_list: List[Enemy]) -> List[Enemy]:
        """ Sort a list of enemy based on their hp (recursion)

        Args:
            enemy_list: a list of enemy objects to be sorted

        Returns:
            enemy list (sorted)
        """
        # base case
        if len(enemy_list) == 0:
            return []
        if len(enemy_list) == 1:
            return enemy_list
        # recursive step (quick sort in list comprehension)
        return MyGame.sort_enemy([ele for ele in enemy_list[1:] if ele.ehp >= enemy_list[0].ehp]) + [
            enemy_list[0]] + MyGame.sort_enemy(
            [ele for ele in enemy_list[1:] if ele.ehp < enemy_list[0].ehp])

    # draw instruction page METHOD???
    def draw_instructions_page(self, page_number: int) -> None:
        """ Draw an instruction page. Load the page as an image.

        Args:
            page_number: A number used to specify an instruction page

        Returns:
            None
        """
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, page_texture.width, page_texture.height,
                                      page_texture, 0)
        if self.current_state == INSTRUCTIONS_PAGE_0:
            page_texture = arcade.load_texture("images/background_new.png")
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2, page_texture.width, page_texture.height, page_texture,
                                          0)

    # draw game over page
    def draw_game_over(self) -> None:
        """ Draw "Game over" across the screen.

        Args:
            None
        Returns:
            None
        """
        output = "Game Over"
        arcade.draw_text(output, 220, 350, arcade.color.WHITE, 54)

        output = "Click anywhere to quit"
        arcade.draw_text(output, 245, 260, arcade.color.WHITE, 24)

        page_texture = arcade.load_texture("images/leaderboard_button.png")
        arcade.draw_texture_rectangle(689, 38, 141, 62, page_texture, 0)

    # draw game win page
    def draw_game_win(self) -> None:
        """ Draw "You Win" across the screen.

        Args:
            None
        Returns:
            None
        """
        texture = arcade.load_texture("images/win_page.jpeg")
        arcade.draw_texture_rectangle(400, 300, 800, 600, texture)

    def draw_game(self) -> None:
        """ Draw everything in the game

        Args:
            None
        Returns:
            None
        """
        # Draw background and boss for each level
        texture_1 = arcade.load_texture("images/bg_"+str(level)+".jpg")
        arcade.draw_texture_rectangle(400, position_y_1, 800, 600, texture_1)
        arcade.draw_texture_rectangle(400, position_y_2, 800, 600, texture_1)
        texture_0 = arcade.load_texture("images/boss_"+str(level)+".png")

        # draw images
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        self.pet_list.draw()
        self.bullet_pet_list.draw()
        self.bullet_self_list.draw()
        self.assist.draw()
        self.bonus.draw()

        if prompt:
            arcade.draw_texture_rectangle(400, 350, 300, 200, arcade.load_texture("images/boss_prompt.png"))

        # boss killed explode animation
        if explode == 4:
            texture_2 = arcade.load_texture("images/explode_4.png")
            arcade.draw_texture_rectangle(400, 300, 450, 430, texture_2)
        elif 0 < explode < 4:
            texture_2 = arcade.load_texture("images/explode_" + str(explode) + ".png")
            arcade.draw_texture_rectangle(explode_x, explode_y, 240, 180, texture_0)
            arcade.draw_texture_rectangle(explode_x, explode_y, 90, 90, texture_2)

        # Draw different boss lasers
        for b in self.enemy_list:
            if 0 < laser_effect < 7:
                if 0 <= level <= 1:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 380, 30, 600,
                                                  arcade.load_texture("images/bomb_laser"+str(laser_effect+5)+".png"))

                if level == 2:
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 370, 30, 600,
                                                  arcade.load_texture("images/bomb_laser"+str(laser_effect+5)+".png"))

                if 3 <= level <= 4:
                    arcade.draw_texture_rectangle(b.center_x - 40, b.center_y - 345, 30, 600,
                                                  arcade.load_texture("images/bomb_laser"+str(laser_effect+5)+".png"))
                    arcade.draw_texture_rectangle(b.center_x, b.center_y - 360, 30, 600,
                                                  arcade.load_texture("images/bomb_laser"+str(laser_effect+5)+".png"))
                    arcade.draw_texture_rectangle(b.center_x + 40, b.center_y - 345, 30, 600,
                                                  arcade.load_texture("images/bomb_laser"+str(laser_effect+5)+".png"))

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
                arcade.draw_texture_rectangle(760 - i * 50, 520, 50, 40, arcade.load_texture("images/missile_icon.png"))

# TODO
    def draw_leaderboard(self) -> None:
        """ Draw a leader board using data from a .json file

        Args:
            None
        Returns:
            None
        """
        with open("leaderboard.json", "r") as f:
            prim_data = json.load(f)

        data = MyGame.sorted_data(prim_data)

        def leaderboard(data: Dict) -> List[List[str]]:
            """ Process the player's data and record the best performance

            Args:
                data: the original sorted data

            Returns:
                a list of actual data that will display on the leaderboard
            """
            leader_list = []
            for score in data.keys():
                for time in data[score]:
                    if len(leader_list) < 4:
                        leader_list.append([str(score), "{0}:{1}".format(time // 60, time % 60)])
                    else:
                        break
            return leader_list

        m = leaderboard(data)

        def final_output() -> Tuple:
            """ Compute the final scores and times

            Args:
                None
            Returns:
                a tuple (scores, times)
            """
            scores = []
            times = []
            for i in m:
                scores.append(MyGame.slice_digit(i[0]))
                d = i[1].find(":")
                if len(i[1][d + 1:]) <= 1:
                    i[1] = i[1][:d + 1] + "0" + i[1][d + 1:]
                times.append(MyGame.slice_digit(i[1]))
            return scores, times

        scores, times = final_output()[0], final_output()[1]
        for i in range(len(scores)):
            for j in range(len(scores[i])):
                arcade.draw_texture_rectangle(200 + j * 20, 440 - i * 100, 20, 24,
                                              arcade.load_texture("number/n_" + str(scores[i][j]) + ".png"))

        for i in range(len(times)):
            for j in range(len(times[i])):
                arcade.draw_texture_rectangle(500 + j * 20, 440 - i * 100, 20, 24,
                                              arcade.load_texture("number/n_" + str(times[i][j]) + ".png"))

    def on_draw(self) -> None:
        """ Render the screen.

        Args:
            None
        Returns:
            None
        """
        arcade.start_render()
        if self.current_state == GAME_RUNNING:
            self.draw_game()
        elif self.current_state == INSTRUCTIONS_PAGE_0:
            self.draw_instructions_page(0)
        elif self.current_state == INSTRUCTIONS_PAGE_1:
            self.draw_instructions_page(1)
        elif self.current_state == LEADERBOARD:
            self.draw_instructions_page(2)
            self.draw_leaderboard()
        elif self.current_state == GAME_OVER:
            self.draw_game()
            self.draw_game_over()
        elif self.current_state == WIN:
            self.draw_game_win()

    def setup(self) -> None:
        """ Initialize game interface. Default schedule is 60 fps.

        Args:
            None
        Returns:
            None
        """
        arcade.schedule(self.on_update, 1 / 60)
        self.frame_count = 0
        self.hp = 100
        self.boss = False
        self.laser_player = 0

        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.pet_list = arcade.SpriteList()
        self.bullet_pet_list = arcade.SpriteList()
        self.bullet_self_list = arcade.SpriteList()
        self.assist = arcade.SpriteList()
        self.bonus = arcade.SpriteList()

        # Add player ship
        self.player = arcade.Sprite("images/SeHero.png", 0.8)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.pet = arcade.Sprite("images/pet.png", 0.85)
        self.pet2 = arcade.Sprite("images/pet.png", 0.85)
        self.player_list.append(self.player)
        self.pet_list.append(self.pet)
        self.pet_list.append(self.pet2)

    def dead(self) -> None:
        """ Clear the screen when dead, stores player's information into a .json file

        Args:
            None
        Returns:
            None
        """
        with open("leaderboard.json", "r") as f:
            data = json.load(f)
            if str(Score) not in data.keys():
                data[str(Score)] = []
            data[str(Score)].append(self.frame_count//60)

        with open("leaderboard.json", "w") as f:
            json.dump(data, f)
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.pet_list = arcade.SpriteList()
        self.bullet_pet_list = arcade.SpriteList()
        self.bullet_self_list = arcade.SpriteList()
        Enemy.refresh_enemy()
        self.current_state = GAME_OVER

    def create_bullet(self, picture: str, scale: float, x: int, y: int, cx: int, cy: int, angle=0) -> None:
        """ Helper function that creates bullet

        Args:
            picture: the bullet image
            scale: the bullet scale
            x: the bullet initial x location
            y: the bullet initial y location
            cx: the bullet's change in x direction
            cy: the bullet's change in y direction
            angle: the bullet angle, default as 0

        Returns:
            None
        """
        bullet = arcade.Sprite("images/" + picture + ".png", scale)
        bullet.center_x = x
        bullet.center_y = y
        bullet.angle = angle
        bullet.change_x = cx
        bullet.change_y = cy
        self.bullet_self_list.append(bullet)

    def update(self, delta_time: float) -> None:
        """ All the logic to move, and the game logic goes here

        Args:
            delta_time: time interval since the last time the function was called

        Returns:
            None
        """
        global explode, explode_x, explode_y, fps, position_y_1, position_y_2
        global level, prompt, prompt_time, boss_hp, boss_hp_current
        global up_pressed, down_pressed, left_pressed, right_pressed
        global laser_bomb, laser_effect, laser_fps, laser_counter, laser_counter_update
        global boss_create_fps, boss_sound_on, game_sound_on, game_sound_1, game_sound_2, game_sound_3, game_sound_4
        global boss_sound_1, boss_sound_2, boss_sound_3, game_sound, boss_sound_4, boss_sound_5
        global enemy_track, enemy_track_1, mode, moves, mm

        if self.current_state != GAME_RUNNING and self.frame_count % 3480 == 0:
            try:
                arcade.play_sound(background_sound)
            except Exception as e:
                print("Error playing sound.", e)

        if self.current_state == GAME_RUNNING:
            try:
                background_sound.pause()
            except Exception as e:
                print("Error pausing sound.", e)

        if level == 5:
            self.current_state = WIN
            return
        if self.current_state == GAME_RUNNING:

            if self.boss and boss_sound_on == 0:
                boss_sound_on = 1
                try:
                    if level == 0:
                        game_sound.pause()
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
                    if level == 4:
                        game_sound_4.pause()
                        arcade.play_sound(boss_sound_5)
                except Exception as e:
                    print("Error pausing sound.", e)

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
                    if level == 4:
                        boss_sound_5.pause()

                except Exception as e:
                    print("Error pausing sound.", e)

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
                    if level == 4:
                        arcade.play_sound(game_sound_4)

                except Exception as e:
                    print("Error playing sound.", e)
                game_sound_on = 1

            # update remaining laser based on current score
            laser_counter = Score // 2000 + 1
            if laser_counter + laser_counter_update == 1:
                arcade.play_sound(missile_sound_1)
                self.laser_player += 1
                laser_counter_update -= 1

            if self.hp <= 0:
                game_sound_on = 10
                try:
                    game_sound.pause()
                    game_sound_1.pause()
                    game_sound_2.pause()
                    game_sound_3.pause()
                    game_sound_4.pause()

                    boss_sound_1.pause()
                    boss_sound_2.pause()
                    boss_sound_3.pause()
                    boss_sound_4.pause()
                    boss_sound_5.pause()

                except Exception as e:
                    print("Error pausing sound.", e)

                self.dead()

            else:
                # drop hp bonus every 15s in the normal mode
                if mode == 0 and self.frame_count % 900 == 899:
                    bonus_hp = arcade.Sprite("images/hp_bonus.png", 0.45)
                    bonus_hp.center_x = random.randrange(0, SCREEN_WIDTH)
                    bonus_hp.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT * 1.25)
                    self.bonus.append(bonus_hp)
                # drop hp bonus every 5s in the face and autopilot mode
                elif mode != 0 and self.frame_count % 300 == 299 and (not self.boss):
                    bonus_hp = arcade.Sprite("images/hp_bonus.png", 0.45)
                    bonus_hp.center_x = random.randrange(0, SCREEN_WIDTH)
                    bonus_hp.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT * 1.25)
                    self.bonus.append(bonus_hp)

                if self.frame_count % 120 == 0 and not self.boss and not 1 <= explode <= 4:
#TODO
                    for _ in range(2 + level):
                        # randomly generate enemy planes of different levels
                        ranNum = random.randint(0, 1000)
                        if ranNum < 300:
                            enemy = Enemy("images/plane_small.png", 0.85, level+2, 10, 4)
                        elif ranNum < 550:
                            enemy = Enemy("images/enemy_2.png", 0.7, level+4, 15, 4)
                        elif ranNum < 750:
                            enemy = Enemy("images/enemy_1.png", 0.6, level+6, 50, 3)
                        elif ranNum < 900:
                            enemy = Enemy("images/boss0.png", 0.35, level+8, 100, 2)
                        else:
                            enemy = Enemy("images/enemy_3.png", 0.7, level+16, 200, 2)

                        enemy.center_x = random.randrange(0, SCREEN_WIDTH)
                        enemy.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT * 1.25)
                        enemy.angle = 180
                        self.enemy_list.append(enemy)

                # create a boss and ensure no small enemies appear during the boss battle
                elif self.frame_count - fps == (899 * (level + 1)) and not self.boss and not 1 <= explode <= 4:
                    # boss prompt
                    boss_create_fps = self.frame_count
                    prompt = True
                    prompt_time = self.frame_count

                    # update boss image based on game level
                    enemy = Boss("images/boss_"+str(level)+".png",
                                  0.8,
                                  (level+1)*50,
                                  (level**2+1)*500,
                                  min(level+1.5, 3))

                    enemy.center_x = random.randrange(0, SCREEN_WIDTH)
                    enemy.center_y = SCREEN_HEIGHT * 2
                    enemy.angle = 180
                    self.enemy_list.append(enemy)
                    self.boss = True
                    boss_hp = enemy.ehp

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
                                self.hp = max(0, self.hp - 0.03)
                        if level == 1:
                            if self.player.center_x - 36 < boss.center_x < self.player.center_x + 36:
                                self.hp = max(0, self.hp - 0.09)
                        if level == 2:
                            if self.player.center_x - 36 < boss.center_x < self.player.center_x + 36:
                                self.hp = max(0, self.hp - 1.0)
                        if level == 3:
                            if self.player.center_x - 36 < boss.center_x - 45 < self.player.center_x + 36 \
                                    or self.player.center_x - 36 < boss.center_x < self.player.center_x + 36 \
                                    or self.player.center_x - 36 < boss.center_x + 15 < self.player.center_x + 36:
                                self.hp = max(0, self.hp - 1.1)
                        if level == 4:
                            if self.player.center_x - 36 < boss.center_x - 45 < self.player.center_x + 36 \
                                    or self.player.center_x - 36 < boss.center_x < self.player.center_x + 36 \
                                    or self.player.center_x - 36 < boss.center_x + 15 < self.player.center_x + 36:
                                self.hp = max(0, self.hp - 1.5)

                # update the background position (speed is 1)
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
                    if level <= 1:
                        self.hp = max(0, self.hp - 2)
                    else:
                        self.hp = max(0, self.hp - 5)

                # collision with enemy
                enemy_collide_list = arcade.check_for_collision_with_list(self.player, self.enemy_list)
                for collide_enemy in enemy_collide_list:
                    if self.boss:
                        self.hp = max(0, self.hp - collide_enemy.ehp)
                    self.hp = max(0, self.hp - 20)
                    collide_enemy.kill()

# TODO
                # calculate different damage of player's bullet or bomb makes on enemy or boss
                for e in self.enemy_list:
                    if type(e).__name__ == "Boss":
                        boss_hp_current = e.ehp
                    bullet_hit_list = arcade.check_for_collision_with_list(e, self.bullet_self_list)
                    bullet_hit_list_2 = arcade.check_for_collision_with_list(e, self.bullet_pet_list)
                    bullet_hit_list_3 = arcade.check_for_collision_with_list(e, self.assist)
                    for bullet_hit in bullet_hit_list:
                        bullet_hit.kill()
                        if level == 0:
                            boss_hit = e.hitted(2)
                        elif level < 2:
                            boss_hit = e.hitted(1)
                        elif level == 2:
                            boss_hit = e.hitted(3)
                        else:
                            boss_hit = e.hitted(5)
                        if boss_hit[0] == 1:
                            self.boss = False
                            explode = 1
                            explode_x = boss_hit[1]
                            explode_y = boss_hit[2]
                            fps = self.frame_count

                    for bullet_hit in bullet_hit_list_2:
                        if level <= 1:
                            bullet_hit.kill()
                            boss_hit = e.hitted(3)
                        else:
                            bullet_hit.hit(e.ehp)
                            boss_hit = e.hitted(4)

                        if boss_hit[0] == 1:
                            self.boss = False
                            explode = 1
                            explode_x = boss_hit[1]
                            explode_y = boss_hit[2]
                            fps = self.frame_count

                    for bullet_hit in bullet_hit_list_3:
                        boss_hit = e.hitted(0.4)
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
                    bomb_sound.pause()
                    game_sound_on = 0

                # use loop to make all enemies facing to the player
                for enemy in self.enemy_list:

                    start_x = enemy.center_x
                    start_y = enemy.center_y

                    dest_x = self.player.center_x
                    dest_y = self.player.center_y

                    x_diff = dest_x - start_x
                    y_diff = dest_y - start_y
                    angle = math.atan2(y_diff, x_diff)

                    # use if statement to exclude the boss angle
                    if type(enemy).__name__ == "Boss":
                        enemy.angle = 0
                    else:
                        enemy.angle = math.degrees(angle) - 270
# TODO A.I???
                    # determine the shooting characteristics of enemy / boss planes
                    if type(enemy).__name__ == "Boss" and self.frame_count % ((120 - 20 * level) // 2) == 0:

                        def add_bullet(n: int) -> None:
                            """ Use recursion to create boss bullet's trajectory

                            Args:
                                n: number of times it creates bullet

                            Returns:
                                None
                            """

                            if n != 4:
                                bullet_1 = arcade.Sprite("images/boss_bullet.png", 0.5)
                                bullet_2 = arcade.Sprite("images/boss_bullet.png", 0.5)

                                dx = math.sin(n/2) * BULLET_SPEED * 1.5
                                dy = math.cos(n/2+math.pi) * BULLET_SPEED * 1.5

                                bullet_1.center_x = start_x
                                bullet_1.center_y = start_y
                                bullet_1.angle = 0
                                bullet_1.change_x = dx
                                bullet_1.change_y = dy
                                self.bullet_list.append(bullet_1)

                                bullet_2.center_x = start_x
                                bullet_2.center_y = start_y
                                bullet_2.angle = 0
                                bullet_2.change_x = -dx
                                bullet_2.change_y = dy
                                self.bullet_list.append(bullet_2)

                                # recursive step
                                add_bullet(n+1)

                        add_bullet(0)

                    elif self.frame_count % (120 - 20 * level) == 0:
                        bullet = arcade.Sprite("images/enemy_bullet.png", 0.5)
                        bullet.center_x = start_x
                        bullet.center_y = start_y
                        bullet.angle = math.degrees(angle)
                        bullet.change_x = math.cos(angle) * BULLET_SPEED * 1.5
                        bullet.change_y = math.sin(angle) * BULLET_SPEED * 1.5
                        self.bullet_list.append(bullet)


# TODO youhua
                # determine the shooting frequency of the player airplane
                if self.frame_count % (15 - 2 * level) == 0:

                    if level == 0:
                        self.create_bullet("Bomb2", 0.85, self.player.center_x, self.player.center_y + 10, 0,
                                      BULLET_SPEED * 3)

                    if level == 1:
                        self.create_bullet("Bomb2", 0.85, self.player.center_x - 15, self.player.center_y, 0,
                                      BULLET_SPEED * 3)
                        self.create_bullet("Bomb2", 0.85, self.player.center_x + 15, self.player.center_y, 0,
                                      BULLET_SPEED * 3)

                    if level == 2:
                        self.create_bullet("Bomb3", 0.55, self.player.center_x, self.player.center_y + 10, 0,
                                      BULLET_SPEED * 3)
                    if level > 2:
                        self.create_bullet("Bomb5", 0.55, self.player.center_x, self.player.center_y, 0,
                                      BULLET_SPEED * 4)

                # determine the shooting frequency of the pet airplane based on the level
                if self.frame_count % (60 - 2 * level) == 0:
                    self.create_bullet("pet_bullet_3", 0.25, self.pet.center_x, self.pet.center_y, 0,
                                       BULLET_SPEED * min(2 + level, 3))
                    self.create_bullet("pet_bullet_3", 0.25, self.pet2.center_x, self.pet2.center_y, 0,
                                       BULLET_SPEED * min(2 + level, 3))

                if level == 1:

                    # store the enemy number to a list
                    sorted_enemy = MyGame.sort_enemy(self.enemy_list)
                    current_enemy = []
                    for enemy in sorted_enemy:
                        current_enemy.append(enemy.number)

                    if self.frame_count % 50 == 0:
                        bullet_1 = Bullet("images/pet_bullet.png", 0.5)
                        bullet_1.center_x = self.player.center_x - 20
                        bullet_1.center_y = self.player.center_y
                        bullet_1.angle = 0

                        bullet_2 = Bullet("images/pet_bullet.png", 0.5)
                        bullet_2.center_x = self.player.center_x + 20
                        bullet_2.center_y = self.player.center_y
                        bullet_2.angle = 0

                        if sorted_enemy:
                            # select two targets that have biggest hp
                            target_1 = sorted_enemy[0]
                            target_2 = sorted_enemy[min(len(sorted_enemy) - 1, 1)]
                            # determine the enemy, ensure no missile on the A.I level

                            self.bullet_pet_list.append(bullet_1)
                            self.bullet_pet_list.append(bullet_2)
                            # make a tracking list, with key being the number, the value being the bullet
                            if target_1.number not in enemy_track_1:
                                enemy_track_1[target_1.number] = []
                            enemy_track_1[target_1.number].append(bullet_1)
                            if target_2.number not in enemy_track_1:
                                enemy_track_1[target_2.number] = []
                            enemy_track_1[target_2.number].append(bullet_2)

                    if sorted_enemy:
                        for number, bullets in enemy_track_1.items():
                            # determine if the enemy exists in the current fps
                            if number in current_enemy:
                                # make the bullet track the enemy
                                for bullet in bullets:
                                    # set the position of the bullet
                                    start_x = bullet.center_x
                                    start_y = bullet.center_y

                                    dest_x = Enemy.enemies[number].center_x
                                    dest_y = Enemy.enemies[number].center_y

                                    x_diff = dest_x - start_x
                                    y_diff = dest_y - start_y
                                    angle = math.atan2(y_diff, x_diff)
                                    bullet.change_x = math.cos(angle) * BULLET_SPEED * (level // 3 + 3)
                                    bullet.change_y = math.sin(angle) * BULLET_SPEED * (level // 3 + 3)

                                    bullet.angle = math.degrees(angle) - 90
                else:
                    # store the enemy number to a list
                    sorted_enemy = MyGame.sort_enemy(self.enemy_list)
                    current_enemy = []
                    for enemy in sorted_enemy:
                        current_enemy.append(enemy.number)

                    # store the current pet bullet to a list for future use
                    cur_pet_bullet = []
                    for pb in self.bullet_pet_list:
                        cur_pet_bullet.append(pb)

                    if len(cur_pet_bullet) == 0:
                        bullet_1 = Bullet("images/pet_bullet.png", 0.5)
                        bullet_1.center_x = self.player.center_x - 20
                        bullet_1.center_y = self.player.center_y
                        bullet_1.angle = 0

                        if sorted_enemy:
                            # recursion and backtracking
                            def track_targets(s, hp):
                                # print(s, hp)
                                if not s or hp <= 0:
                                    return []
                                ans = []
                                for i in range(len(s)):
                                    if s[i].ehp <= hp:
                                        ans.append([s[i]] + track_targets(s[:i] + s[i+1:], hp - s[i].ehp))

                                max_score = -1
                                max_index = -1
                                for a in ans:
                                    cur_score = 0
                                    for e in a:
                                        cur_score += e.score

                                    if cur_score > max_score:
                                        max_score = cur_score
                                        max_index = ans.index(a)
                                if max_score == -1:
                                    return []
                                return ans[max_index]

                            targets = track_targets(sorted_enemy, 20 + level * 5)
                            enemy_track.append((bullet_1, targets))
                            if targets:
                                self.bullet_pet_list.append(bullet_1)

                    if sorted_enemy:
                        # print(enemy_track[0][1])
                        for bullet, targets in enemy_track:
                            # determine if the enemy exists in the current fps
                            new_targets = []
                            for enemy in targets:
                                if enemy.number in current_enemy:
                                    new_targets.append(enemy)

                            for enemy in new_targets:
                                # make the bullet track the enemy
                                # set the position of the bullet
                                start_x = bullet.center_x
                                start_y = bullet.center_y

                                dest_x = enemy.center_x
                                dest_y = enemy.center_y

                                x_diff = dest_x - start_x
                                y_diff = dest_y - start_y
                                angle = math.atan2(y_diff, x_diff)
                                bullet.change_x = math.cos(angle) * BULLET_SPEED * 1.5 * (level // 3 + 3)
                                bullet.change_y = math.sin(angle) * BULLET_SPEED * 1.5 * (level // 3 + 3)

                                bullet.angle = math.degrees(angle) - 90

                # use loops to remove the bullet when it flies off-screen
                for bullet in self.bullet_self_list:
                    if bullet.bottom > 600 or bullet.top < 0 or bullet.center_x > 800 or bullet.center_x < 0:
                        bullet.kill()

                for bullet in self.bullet_pet_list:
                    if bullet.bottom > 600 or bullet.top < 0 or bullet.center_x > 800 or bullet.center_x < 0:
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
                        if mode != 0:
                            self.hp = min(100, self.hp + 80)
                        else:
                            self.hp = min(100, self.hp + 30)
                        arcade.play_sound(hp_bonus_sound)
                        hp_bonus.kill()
                    # remove hp_bonus when it gets out of windows
                    elif hp_bonus.top < 0:
                        hp_bonus.kill()

                # move pet with self plane
                self.pet.center_x = self.player.center_x + 80
                self.pet.center_y = self.player.center_y
                self.pet2.center_x = self.player.center_x - 80
                self.pet2.center_y = self.player.center_y

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

                # set time for boss prompt to be 3s
                if self.frame_count - prompt_time == 180 and prompt:
                    prompt = False

                # realize the dropping of boss and enemy planes
                for e in self.enemy_list:
                    e.drop()

                if level == 5:
                    self.current_state = WIN
                    self.set_mouse_visible(True)

                self.bullet_list.update()
                self.bullet_self_list.update()
                self.bullet_pet_list.update()
                self.assist.update()


# TODO
                # Face Mode
                if self.current_state == GAME_RUNNING and mode == 2 and self.frame_count % 4 == 0:

                    if Communication.get_x() != '' and Communication.get_y() != '':
                        try:
                            self.player.center_x = min(800 - int(Communication.get_x()), 764)
                            self.player.center_y = min(300 - int(Communication.get_y()), 552)
                            # if len(move_list) == 2:
                            #     if -5 <= (move_list[1][0] - move_list[0][0]) <= 5:
                            #         self.player.center_x = move_list[0][0]
                            #     else:
                            #         self.player.center_x = move_list[1][0]
                            #     if -5 <= (move_list[1][1] - move_list[0][1]) <= 5:
                            #         self.player.center_y = move_list[0][1]
                            #     else:
                            #         self.player.center_y = move_list[1][1]

                        except:
                            self.player.center_x = 400
                            self.player.center_y = 100
                        # print(self.player.center_x, self.player.center_y)
                    else:
                        print("face not detected")

                if level == 0:
                    mode = 1

                # AutoPilot Mode
                if mode == 1:
                    try:
                        # Decide the next move within three frame
                        if self.frame_count % 3 == 0:
                            def make_moves(x: int, y: int, n: int) -> Tuple:
                                """ Make the player's plane move

                                Args:
                                    x: horizontal position
                                    y: vertical position
                                    n: number of moves

                                Returns:
                                     a "decision"
                                """
                                # consider 4 moves
                                if n == 4:
                                    return [], 0

                                # should only consider moves within the screen
                                valid_move = []
                                for m in directions:
                                    if 36 <= x + m[0] <= 764 and 48 <= y + m[1] <= 552:
                                        valid_move.append(m)

                                # choose best "child" move, do a recursion on state tree
                                decision = []
                                new_moves = []
                                for m in valid_move:
                                    result = make_moves(x + m[0], y + m[1], n + 1)
                                    new_moves.append(result[0])
                                    decision.append(result[1])

                                new_i = decision.index(min(decision))

                                # calculate the heuristic of a particular state
                                # wants to hit enemy
                                e = None
                                for target in self.enemy_list:
                                    e = target
                                    break
                                if e:
                                    tot_dist = MyGame.get_distance(e.center_x, e.center_y - e.speed*4 - 400, x, y)
                                    # dodge the laser from the boss while attacking
                                    if self.boss:
                                        tot_dist = MyGame.get_distance(e.center_x + 100, e.center_y - e.speed * 4 - 400, x, y)
                                else:
                                    tot_dist = MyGame.get_distance(SCREEN_WIDTH//2, 200, x, y)

                                # hp bonus is more important!
                                e = None
                                for h in self.bonus:
                                    e = h
                                    break

                                if e:
                                    tot_dist = MyGame.get_distance(e.center_x, e.center_y - 20, x, y)

                                return [valid_move[new_i]] + new_moves[new_i], decision[new_i] + tot_dist

                            moves = make_moves(self.player.center_x, self.player.center_y, 0)[0]
                            mm = 0

                            # print(moves)
                            moves.pop(3)
                            # print("done")
                            # avoid shaking
                            # for i in range(1, 3):
                            #     if moves[i][0]+moves[i-1][0] == 0 and moves[i][1]+moves[i-1][1] == 0:
                            #         moves[i] = S


                        #print(self.player.center_x, self.player.center_y)

                        self.player.center_x += moves[mm][0]
                        self.player.center_y += moves[mm][1]

                        mm += 1
                        if mm == 3:
                            mm = 0
                    except:
                        mode = 0

                if level == 1:
                    mode = 2
                if level >= 2:
                    mode = 0
                # keyboard control the movement of the player
                if up_pressed:
                    self.player.center_y = min(552, self.player.center_y + 5)
                if down_pressed:
                    self.player.center_y = max(48, self.player.center_y - 5)
                if left_pressed:
                    self.player.center_x = max(36, self.player.center_x - 5)
                if right_pressed:
                    self.player.center_x = min(764, self.player.center_x + 5)

        # update the frame_count
        self.frame_count += 1

    def on_mouse_motion(self, x: int, y: int, delta_x: int, delta_y: int) -> None:
        """ Called whenever the mouse moves.

        Args:
            x: player x-location
            y: player y-location
            delta_x: player delta x
            delta_y: player delta y

        Returns:
            None
        """
        if mode == 0:
            self.player.center_x = x
            self.player.center_y = y

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        """ Called whenever the user presses a mouse button

        Args:
            x: Player x-location
            y: Player y-location
            button: Check if the button is pressed
            modifiers: default modifier

        Returns:
            None
        """
        global level, Score, prompt, prompt_time, boss_hp, boss_hp_current, \
            laser_bomb, laser_effect, laser_fps, laser_counter, laser_counter_update
        global game_sound_on

        # Change states as needed.
        if self.current_state == INSTRUCTIONS_PAGE_0:
            if 287 <= x <= 513 and 206 <= y <= 283:
                arcade.play_sound(button_sound)
                self.current_state = INSTRUCTIONS_PAGE_1
            if 287 <= x <= 513 and 94 <= y <= 170:
                arcade.play_sound(button_sound)
                self.current_state = LEADERBOARD

        elif self.current_state == LEADERBOARD and 629 <= x <= 770 and 12 <= y <= 64:
            arcade.play_sound(button_sound)
            self.current_state = INSTRUCTIONS_PAGE_0

        elif self.current_state == INSTRUCTIONS_PAGE_1:
            # Start the game
            self.current_state = GAME_RUNNING
            self.setup()

        elif self.current_state == GAME_OVER and 629 <= x <= 770 and 12 <= y <= 64:
            self.current_state = LEADERBOARD

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

        elif self.current_state == WIN and 629 <= x <= 770 and 12 <= y <= 64:
            self.current_state = LEADERBOARD

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

    def on_key_press(self, key: int, modifier: int) -> None:
        """ Detect user key input when a key is pressed

        Args:
            key: the particular key user pressed
            modifier: default modifier

        Returns:
            None
        """
        global up_pressed, down_pressed, left_pressed, right_pressed, laser_bomb
        if key == arcade.key.W:
            up_pressed = True
        if key == arcade.key.S:
            down_pressed = True
        if key == arcade.key.A:
            left_pressed = True
        if key == arcade.key.D:
            right_pressed = True
        if key == arcade.key.Z:
            laser_bomb = True

    def on_key_release(self, key: int, modifier: int) -> None:
        """ Detect user key input when a key is released

        Args:
            key: the particular key user released
            modifier: default modifier

        Returns:
            None
        """
        global up_pressed, down_pressed, left_pressed, right_pressed, laser_bomb
        if key == arcade.key.W:
            up_pressed = False
        if key == arcade.key.S:
            down_pressed = False
        if key == arcade.key.A:
            left_pressed = False
        if key == arcade.key.D:
            right_pressed = False
        if key == arcade.key.Z:
            laser_bomb = False


# Variables to record if certain keys are being pressed. Default to False
up_pressed = False
down_pressed = False
left_pressed = False
right_pressed = False


class Communication:
    """
    This is a Communication class that use for save data

    """
    def __init__(self, x: int, y: int):
        """ Initialize Communication class
        Args:
            x_value: x value that read out from Vision
            y_value: y value that read out from Vision
        Returns:
            None
        """
        self.x_value = x
        self.y_value = y

    def write_x(self)-> None:
         """
        write x data in to database
        Args:
            x_value: x value that read out from Vision
            y_value: y value that read out from Vision
        Returns:
            None
        """
        with open("x.txt", "w") as f:
            f.write(self.x_value)
        with open("xb.txt", "w") as f:
            f.write(self.x_value)

    def write_y(self)-> None:
        """
        write y data in to database
        Args:
            x_value: x value that read out from Vision
            y_value: y value that read out from Vision
        Returns:
            None
        """

        with open("y.txt", "w") as f:
            f.write(self.y_value)

        with open("yb.txt", "w") as f:
            f.write(self.y_value)

    def get_x()-> str:
         """
        read x data from database
        Args:
            x_value: x value that read out from Vision
            y_value: y value that read out from Vision
        Returns:
            contents: x value in the database
        """
        try:
            with open("x.txt", 'r') as f:
                contents = f.read()
                return contents

        except:
            with open("xb.txt", 'r') as f:
                contents = f.read()
                return contents

    def get_y()-> str:
        """
        read y data from database
        Args:
            x_value: x value that read out from Vision
            y_value: y value that read out from Vision
        Returns:
            contents: y value in the database
        """
        try:
            with open("y.txt", 'r') as f:
                y_contents = f.read()
                return y_contents

        except:
            with open("yb.txt", 'r') as f:
                y_contents = f.read()
                return y_contents


class Vision(Communication):

    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    @staticmethod
    def Face_Detect():
        cap = cv2.VideoCapture(0)  # 捕获摄像头图像

        # 判断视频是否打开

        if cap.isOpened():
            print('Open')
        else:
            print('camra is not opened')
        cap = cv2.VideoCapture(0)
        (success, frame) = cap.read()  # 读入第一帧

        classifier = \
            cv2.CascadeClassifier("opencv-master/data/haarcascades/haarcascade_frontalface_alt.xml")

        # 定义人脸识别的分类数据集，需要自己查找，在opencv的目录下，参考上面我的路径**

        while success:  # 如果读入帧正常
            size = frame.shape[:2]
            image = np.zeros(size, dtype=np.float16)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.equalizeHist(image, image)
            divisor = 8
            (h, w) = size
            minSize = (int(w / divisor), int(h / divisor))  # 像素一定是整数，或者用w//divisor

            faceRects = classifier.detectMultiScale(image, 1.2, 2, cv2.CASCADE_SCALE_IMAGE, minSize)

            # 人脸识别

            if len(faceRects) > 0:
                for faceRect in faceRects:
                    (x, y, w, h) = faceRect
                    x_data = str(x)
                    y_data = str(y)
                    now = Communication(x_data, y_data)
                    now.write_x()
                    now.write_y()
                    # print (x, y)
                    """
                    cv2.circle(frame, (x + w // 2, y + h // 2), min(w
                               // 2, h // 2), (0xFF, 0, 0), 2)  # 圆形轮廓
                    cv2.circle(frame, (x + w // 4, y + 2 * h // 5),
                               min(w // 8, h // 8), (0, 0xFF, 0), 2)  # 左眼轮廓
                    cv2.circle(frame, (x + 3 * w // 4, y + 2 * h // 5),
                               min(w // 8, h // 8), (0, 0xFF, 0), 2)  # 右眼轮廓
                    cv2.circle(frame, (x + w // 2, y + 2 * h // 3),
                               min(w // 8, h // 8), (0, 0xFF, 0), 2)  # 鼻子轮廓
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0,
                                  0xFF), 2)  # 矩形轮廓
                    """
                    # y通道B（冗余通道）

                    with open('yb.txt', 'w') as f:
                        f.write(str(y))

                    # x通道B（冗余通道）

                    with open('xb.txt', 'w') as f:
                        f.write(str(x))

            # 显示轮廓

            (success, frame) = cap.read()  # 如正常则读入下一帧

        # 循环结束则清零

        cap.release()
        cv2.destroyAllWindows()


class MyThread(threading.Thread):
    def run(self):
        print("bs")
        Vision.Face_Detect()

def main():
    vision = MyThread()
    # Start the threading
    vision.start()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    SCREEN_TITLE = "WeFly X Charlie"
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
    # Start the threading
    vision.join()
    print("End Main threading")


if __name__ == '__main__':
    main()


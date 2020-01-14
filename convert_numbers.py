# convert score and time's font
# method_1
# input e.g. [["50", "3:15"],["50", "4:15"], ["40", "3:15"], ["30", "3:15"]]
import arcade
input_final = [["50", "3:15"],["50", "4:15"], ["40", "3:15"], ["30", "3:15"]]
input = ["50", "3:15"]
Score = "6580"
Time = "3:15"
# 先做一行
def slice_digit(list):
    l = []
    for digit in list:
        if digit == ":":
            digit = "hg"
        l.append(digit)
    return l
scores = []
times = []
for i in input_final:
    scores.append(slice_digit(i[0]))
    times.append(slice_digit(i[1]))
print(scores)
print(times)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SCREEN_TITLE = "Drawing Text Example"


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Render the screen.
        """

        arcade.start_render()

        for i in range(len(scores)):
            for j in range(len(scores[i])):
                arcade.draw_texture_rectangle(100 + j * 20, 400 - i*40, 20, 24,
                                              arcade.load_texture("number/n_" + str(scores[i][j]) + ".png"))

        for i in range(len(times)):
            for j in range(len(times[i])):
                arcade.draw_texture_rectangle(300 + j * 20, 400 - i * 40, 20, 24,
                                              arcade.load_texture("number/n_" + str(times[i][j]) + ".png"))


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()


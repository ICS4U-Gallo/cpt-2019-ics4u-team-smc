import arcade
import json
from typing import List, Dict

with open("Leaderboard.json", "r") as f:
    prim_data = json.load(f)

def msort(l: List[int]) -> List[int]:
    # base case
    if len(l) < 2:
        return l
    left_side = msort(l[:len(l) // 2])
    right_side = msort(l[len(l) // 2:])
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

def output(prim_data: Dict) -> Dict:
    """ Sort the dictionary so that key (score) in descending order, value (time) in ascending order

    Args:
        prim_data: The original data where key reps score, value reps time

    Returns:
        a "sorted" dictionary that has score in descending order and time in ascending order
        {30: [6, 5], 40: [8, 2]} -> {40: [2, 8], 30: [5, 6]}
    """
    final_d = {}
    for score in msort([int(s) for s in prim_data.keys()])[::-1]:
        for v in msort(prim_data[str(score)]):
            if score not in final_d:
                final_d[score] = []
            final_d[score].append(v)
    return final_d


data = output(prim_data)

print(data)
def leaderboard(data: Dict) -> List[List[str]]:
    leader_list = []
    for score in data.keys():
        for time in data[score]:
            if len(leader_list) < 4:
                leader_list.append([str(score), "{0}:{1}".format(time // 60, time % 60)])
            else:
                break
    return leader_list


m = leaderboard(data)
print("m",m)

# input_final = [["50", "3:15"],["50", "4:15"], ["40", "3:15"], ["30", "3:15"]]
# input = ["50", "3:15"]
# Score = "6580"
# Time = "3:15"
# 先做一行
def slice_digit(s):
    return [d if d != ":" else "hg" for d in list(s)]

def final_output():
    scores = []
    times = []
    for i in m:
        scores.append(slice_digit(i[0]))
        d = i[1].find(":")
        if len(i[1][d+1:]) <= 1:
            i[1] = i[1][:d+1]+"0"+i[1][d+1:]
        times.append(slice_digit(i[1]))
    return scores, times
print(final_output()[0])
print(final_output()[1])
scores = final_output()[0]
times = final_output()[1]

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

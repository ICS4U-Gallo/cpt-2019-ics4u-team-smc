enemy_list = [2, 2, 4 ,2, 1, 2, 0, 10]
def sort_enemy(enemy_list):
    if len(enemy_list) == 0:
        return []
    if len(enemy_list) == 1:
        return enemy_list
    if len(enemy_list) == 2:
        if enemy_list[0] > enemy_list[1]:
            return [enemy_list[0], enemy_list[1]]
        return [enemy_list[1], enemy_list[0]]
    return sort_enemy([ele for ele in enemy_list[1:] if ele >= enemy_list[0]]) + [enemy_list[0]] + sort_enemy(
        [ele for ele in enemy_list[1:] if ele < enemy_list[0]])
# print(sort_enemy(enemy_list))
W = 25
points = [1, 2, 1, 2, 1, 2, 3, 2, 1]
n = len(points)
ehps = [5, 5, 5, 5, 5, 5, 5, 5, 5]
dic = {}
m = []
def opti_missile(W, n):
    if n == 0 or W == 0:
        return 0
    key = str(W) + "#" + str(n)

    if key in dic:
        return dic[key]

    if (ehps[n - 1] > W):
        dic[key] = opti_missile(W, n - 1)
        return dic[key]

    else:
        previous = opti_missile(W - ehps[n - 1], n - 1)
        previous_not = opti_missile(W, n - 1)
        dic[key] = max(points[n - 1] + previous,
                      previous_not)
        m.append(dic[key])
        return dic[key]
# 11?
print(opti_missile(W, n))
print(m[-1])


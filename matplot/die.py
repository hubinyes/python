from random import randint
import pygal

class Die():
    def __init__(self,num_sides=6):
        self.num_sides = num_sides

    def roll(self):
        """" 返回一个位于 1 和骰子面数之间的随机值 """
        return randint(1, self.num_sides)

die_1 = Die()
die_2 = Die()

results = []
for roll_num in range(1000):
    result = die_1.roll() + die_2.roll()
    results.append(result)
# 分析结果
frequencies = []
max_result = die_1.num_sides + die_2.num_sides
for value in range(2, max_result+1):
    frequency = results.count(value)
    frequencies.append(frequency)

hist = pygal.Bar()
hist.title = "Results of rolling one D6 1000 times."
hist.x_labels = [x for x in range(2,13)]
hist.x_title = "Result"
hist.y_title = "Frequency of Result"
hist.add("D6+D6",frequencies)
hist.render_to_file("die.svg")
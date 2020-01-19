# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 10:21:42 2020

@author: Simon
"""
from typing import List
import numpy as np

class UserHabitLearn:
    """
    This class is a user habit learning class.
    This class use essential machine learning to learn user habit.
    It is also an API that helps data science people to sort and clean the data.
    It even able to train the Vision class CNN network by its self.
    """
    database = {}
    def __init__(self, name: str):
        """
         Initialize userhabitlearn class
        
        arg:
            name: name of the data for this time
            x_contents:The x value read out from data base
            y_contents:The y value read out from data base
            database: This is a dictionary that storge data from the database
        """
        self.name = name
        with open("x_data(for_training).txt", "r") as f:
           #self.x_contents = f.read()      
           database = {"x":list(map(int, f.read().split(",")))}
           #print(database)
        
        with open("y_data(for_training).txt", "r") as f:
           #self.y_contents = f.read()
           database["y"] = f.read().split(",")
        self.database = database
        print(self.database)


    def bubble_sort(numbers) -> List[int]:
        """
        this is a sort function that use bubbles sort structure
        it sort a list of numbers and return a sorted list
        """
        for i in range(len(numbers)):
            for i in range(len(numbers)-1):
                if numbers[i] < numbers[i+1]:
                    target = numbers[i]
                    numbers[i] = numbers[i+1]
                    numbers[i+1] = target
        return numbers


    def sort(self):
        """
         sort data autolly
         
        arg:
            x_contents:The x value read out from data base
            y_contents:The y value read out from data base
            database: This is a dictionary that storge data from the database
        """
        print(type(self))
        x_value_list = self.database['x']
        self.database.pop("x")
        y_value_list = self.database["y"]
        self.database.pop("y")
        sorted_x = UserHabitLearn.bubble_sort(x_value_list)
        sorted_y = UserHabitLearn.bubble_sort(y_value_list)
        self.database = {"x":sorted_x}
        self.database["y"] = sorted_y
    
    
    
    def find_x_mode(self) -> int():
        """
         findy mode number for y numbers
         
        arg:
            database: This is minimum dictionary that storge data from the database
            x_value_list:The x value read out from data base
            maximum: the maximum number in x value
            minimum: the minimum number in x value
            x_mode: a int that is the mode of x
        """
        print(self.database)
        x_value_list = self.database['x']
        maximum = x_value_list.index(min(x_value_list))
        minimum = x_value_list.index(max(x_value_list))
        x_value_list.pop(maximum-1)
        x_value_list.pop(minimum-1)
        counts = np.bincount(x_value_list)
        #返回众数
        x_mode = np.argmax(counts)
        
        return x_mode

    def find_y_mode(self) -> int():
        """
         findy mode number for y numbers
         
        arg:
            database: This is minimum dictionary that storge data from the database
            y_value_list:The y value read out from data base
            maximum: the maximum number in y value
            minimum: the minimum number in y value
            x_mode: a int that is the mode of y
        """
        y_value_list = self.database["y"]
        maximum = y_value_list.index(min(y_value_list))
        minimum = y_value_list.index(max(y_value_list))
        y_value_list.pop(maximum-1)
        y_value_list.pop(minimum-1)
        counts = np.bincount(y_value_list)
        #返回众数
        y_mode = np.argmax(counts)
        
        return y_mode
class Calc:
    """
    this is a math API that ready for use for data science learning 
    This class is encapsulated
     
    set_a_b(): is the setter for to number that user want to process
    """
    # 初始化
    def __init__(self, a, b):
        """
         Initialize Calc class
        
        arg:
            a: a number use for peocess
            b: aother number use for peocess
        """
        self.a = a
        self.b = b
  
    # 重置值
    def set_a_b(self, a, b):
        """
         set a and b
        
        arg:
            a: a number use for peocess
            b: aother number use for peocess
        """
        self.a = a
        self.b = b
    
    # 加法
    def __add(self) -> int():
        """
        this is a add function that use for add a and b
        arg:
            a: a number use for peocess
            b: aother number use for peocess
        """
        return self.a + self.b

    # 减法
    def __sub(self) -> int():
        """
        this is a subtrac function that use for subtrac a and b
        arg:
            a: a number use for peocess
            b: aother number use for peocess
        """
        return self.a - self.b

    # 乘法
    def _mul(self) -> int():
        """
        this is a multiplication function that use for multipliy a and b
        arg:
            a: a number use for peocess
            b: aother number use for peocess
        """
        return self.a * self.b

    # 除法
    def _div(self) -> int():
        """
        this is a div function that use for divid a and b
        arg:
            a: a number use for peocess
            b: aother number use for peocess
        """
        # a / b 2和3版本的除法有稍许变化
        if self.b != 0:
            return self.a // self.b
        else:
            raise ('除数为0，无法计算！')

    # 加法
    def get_adds(self) -> int():
         """
        this is a getter function that get add a and b
        arg:
            a: a number use for peocess
            b: aother number use for peocess
        """
        return self.__add()

    # 减法
    def get_subs(self) -> int():
         """
        this is a getter function that get subs a and b
        arg:
            a: a number use for peocess
            b: aother number use for peocess
        """
        return self.__sub()

    def get_muls(self) -> int():
         """
        this is a getter function that get muls a and b
        arg:
            a: a number use for peocess
            b: aother number use for peocess
        """
        return self._mul()
    
    def get_divs(self) -> int():
         """
        this is a getter function that get divs a and b
        arg:
            a: a number use for peocess
            b: aother number use for peocess
        """
        return self._div()
    
    """
    math API package
    Feel free to use if you needed
    01/15/2020 Simon Li
    Here is how you use it
    eg = Calc(2, 6)
    print(eg.get_adds())
    print(eg.get_subs())
    eg.set_a_b(9, 6)
    print(eg.get_divs())
    print(eg.get_muls())
    user_habit_learn.ellipse_detect()
    """




if __name__ == "__main__":
    user_habit_learn = UserHabitLearn("你妈逼的")
    user_habit_learn.sort()
    print(user_habit_learn.find_x_mode())
    print(user_habit_learn.find_y_mode())
# WEFLY X SMC
Wefly is a simple and addicting aircraft shooting game where you play the role of a brave and daring fighter pilot. 
Dodge and weave your way around a war zone as you try to avoid enemy fire from all angles to survive. 
Destroy as many enemy aircraft as you can in this adventure to get higher scores. 
Your final goal of this game is to get through all the levels and score as many points as possible. 
Good luck brave Fighter Pilot!

## LATEST FEATURE
OpenCV + NumPy + Recursion + Auto-Tracking Missile + Levels + AutoPilot

### Group Members:
- Charlie Guo
- Simon Li
- Yingchen Ma

The compiled language for this program is python3 [这个程序的编译语言为python3(version 3.7.3)]


  (Before you run our code Please install these libraries correctly.Otherwise there is a risk of a program crash. For the safety of you and others, please install these libraries correctly.)
  [在您使用我们的程序之前，请您正确的安装这些库，否则有可能会出现程序崩溃的风险。为了您和他人的人身和财产安全，请您正确的安装这些库。]
  
  (Please download all the folders and library, the only way to start the program correctly)
  [请您下载全部的文件夹，只有这样才能正确的开始程序]
  
(You need to pay us the license fee to purchase a genuine license. The use of pirated licenses is unethical and is not permitted by law.)
  您需要向我们支付许可证费用，去购买正版许可证。使用盗版许可证是不道德的，同时也不被法律允许。]
  
  (The fiest interface is the welcome interface, welcome to our program, hello world.)
  [第一个界面为欢迎界面，欢迎来到我们的程序，你好世界。]
  
  (The secound interface is the usermanel. it teach you how to play the game with keyboard. This interface is for the user to experience freedom. (When the input value is not understandable, we will use the No. 0 camera by default))
  [第二个界面为相机选择，您需要输入您的相机端口号码来正确的调用相机，这个界面是为了让用户体验到自由。(当输入值不可理解时，我们将默认使用0号摄像头)]   
  （
  The fourth interface is the camera interface. The performance of each computer is different, so the running time will be different. You need to wait patiently for a while to wait for the camera interface to start. Please point the camera at the subject. The button 'Q' is the shutter. button. When you press the button 'Q', the frame will be recorded and sent for identification.）
  [第四个界面为拍照界面，每个电脑的性能不同所以运行时间也会不一样，您需要耐心等待一会去等待拍照界面启动，请您将摄像头对准被摄物体，按键‘q’是快门按键。当您按下按键‘Q’,这帧画面将被记录下来，并送去识别]
  
  (The fiveth interface is the result output button, you will see the result of the operation on this page. If the result is NONE, it means the recognition failed, the input picture does not contain, or contains illegal characters, you can exit the program by pressing the exit button. Thank you for using the VC vision calculator made by the SMC team, I hope you can have a perfect experience. The next time we see it in the program. "江湖路远，有缘再见")
  [第五个界面为结果输出按键，您将会在这页看到运算结果，如果结果为NONE 这表明识别失败，输入图片中不包含，或含有非法字符，您可以通过按exit按钮来退出程序。感谢您使用SM团队制作的VC视觉计算器，希望您可以拥有一个完美的使用体验。我们下一次，程序里见。江湖路远，有缘再见。]
  
  When you use 1080P or 4K camra to take the user input,the Success rate is 98%, But when you useing 720P or 480p camra to take input. The Success rate is 20%. When the light is insufficient and the ambient light is very complicated, the recognition rate will decrease.
Files in the folder: Main program test image folder(Have 5 test image inside) A few of image that program need. After you run first time have two image will be make. Do not worry about it! it's nomal and also this is a way you can check where the error come from. DO NOT DELETE THEM!!!!!! YOU ONLY NEED TO RUN THE vc_from Team SM.PY

Algorithm functions： def take_picture(camra_choose) def count_main(letter) def identification() Def test() Def main()

GUI functions： def zeropg() def firstpg() def secondpg() def campg(cram_choose)[这个为GUI和算法的端口] def fourthpg(answer)[这个为算法到GUI的输出端口]





# CPT 2019-2020
This repository will serve as a starting point for your project. Do not alter the structure without approval from Mr. Gallo.

Using [Arcade](https://arcade.academy)
- Group members will be responsible for their own arcade view.
- No Images or sound files.

## Requirements
You will be graded on how well *each* member demonstrates the following:
- Functions
- Annotation, Doc strings
- Classes
    - Inheritance
    - Encapsulation
    - Methods (instance, class, static)
- Recursion
- Searching
- Sorting
- PEP8


## Tasks
Most of these tasks can be turned into cards for your kanban boards.

### Day 1
- Get into groups (2-5) people
- Set up a kanban board

### Day 2
- The group should have an over-arching story or theme.
- Set up your group on github classroom
- Each member should attempt the following:
    - Review the project [structure](#structure)
    - [Add their personal view](#adding-views)
    - Test that their view works running from `main.py`
    - Test that their view works running the file *directly*.

### Day 3
- Sketches
- prioritized list of desired functionality
- Each person mini game idea
- Each person must explain how to include:
    - Classes
    - Searching
    - Sorting
    - recursion
- Tasks added to kanban board

## Structure
Try to limit yourselves to a `settings.py`, `main.py`, `menu.py` and one file per person in the group.

### `settings.py`
This is a place to put data that *every* view needs. You can see I have placed the screen width and height in here. Other things may include colors common to your game, image file locations, and user prefrences.

Notice how each of the files below imports from `settings`. Also notice how each file accesses values inside this file. From those other files, you can access `settings`'s `WIDTH` value by using `settings.WIDTH`, for example.

### `main.py`
I created a `Director` in the `main.py` file whose job is to switch between views. There is not much to touch in this file except [adding views to your overall game](#adding-views).

### `menu.py`
This is a file with an example view that doesn't do much of anything. This file can be imported by your `main.py` file to run as part of a larger project or run by itself. The `if __name__ == "__main__":` section of the code below will allow you to run the view directly, apart from the whole project.

### `chapter_1.py`
This is exactly the same as the `menu.py` file with some details changed. You essentially create a new view by copying this template into a new file, changing the details, then adding your game-specific code.


## Adding views
Follow the short tutorial to add a new view:
- Copy and paste the `menu.py` example code to another file. Let's call this file `chapter_2.py`.
- Change the details in that code:
    - Line 6: Change `MenuView` to `Chapter2View`
    - Line 12: Change the `"Menu"` string to `"Chapter 2"`
    - Line 31: Change `MenuView` to `Chapter2View`
    - save the file

Next, in the `main.py` file, you need to import this new file and class.

- Under Line 6, import the file and class you just modified.
    ```python
    from chapter_2 import Chapter2View
    ```
- In the `Director` class `self.views` list, add a third item.
You will need to add a comma `,` after the previous entry. It should now look like:
    ```python
    self.views = [
        MenuView,
        Chapter1View,  # it's easy to forget the comma here
        Chapter2View
    ]
    ```
- At this point, save the `main.py` file
- You can now run `main.py`, pressing a key to advance to the next window.

## Switching to the next view
To move onto the next view or scene from inside your personal scene, make a call to `self.director.next_view()`. This will tell the main director that it's time to change scenes. Chances are the user won't be pressing a key to advance, but they will advance when some certain event happens like:

```python
if player.collides_with(exit_door):
    self.director.next_view()
```

OR
```python
if len(enemy_ships) == 0:
    self.director.next_view()
```

*Note: When running your scene directly, not from `main.py`'s `Director`, I set up code to print out `"SCENE COMPLETE"` and exit
the window. You can prevent it from exiting the window by setting the key-word argument `close_on_next_view` to `False`.*

# Program Title (replace)
Program description. Replace with description of your program. Give a description of each scene.

### Group Members:
- Member1
- Member2


# CPT 2019
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

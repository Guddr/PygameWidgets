# import basic library
import os
import pygame

# import user's library


#>------------SUMMARY----------------<
# this module is used for custom decorators that provide
# additional functionality to the main library of the WPygame.py
#>------------SUMMARY----------------<

def tools(*args, **kwargs):
    def inside(func):
        def wrapper(*args, **kwargs):
            cls = args[0]
            obj = func(cls)

            if obj is not None:
                cls.screen.blit(obj, (cls.x,cls.y))
            else:
                pygame.draw.rect(cls.screen, cls.COLOR, cls.rect)

        return wrapper
    return inside

def check_size(func):
    def wrapper(*args, **kwargs):
        cls = args[0]
        wSize = cls.screen.get_window_size()
        tSize = cls.coords_list

        count = 0
        for i in tSize:
            if wSize[0] > i[0] and wSize[1] > i[1]:
                break
            else:
                count += 1
        if count == cls.amount:
            obj = func(cls)
        else:
            raise ValueError(f"Value error. Pls chech size obj №{count+1} it's size {tSize[count+1]}. Window size{wSize}")

    return wrapper

def check_key(func):
    def wrapper(*args, **kwargs):
        cls = args[0]

        try:
            if cls.input_text[-1] == "|":
                cls.input_text = cls.input_text[:-1]
        except IndexError:
            print("TEXT", cls.input_text)

        func(*args)

        cls.text.change_text(cls.input_text)

    return wrapper

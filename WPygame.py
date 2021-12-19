# import basic library
import sys
import pygame
from abstract import AbsPanel

from typing import List, Optional, Tuple

# import user's library
from decorate import tools, check_size, check_key
from logger import terminal_print_cls, termimal_print, log_print_cls, log_print
from constpack import WHITE, BLACK, GRAY


#>------------SUMMARY----------------<
# Library of widgets for the paygame library.
# The library provides extensive options for layout and customization of widgets. As well as optimized solutions for their rendering
# While available:
# -Menu( just control button and text)
# -Input Button
# -Button
# -Label
# -Text
# -Font
#
# Coming soon:
# -Buttons menu
# -Panels
# -Complete menu
# -Toolbar
# -Drop-Down Button
#>------------SUMMARY----------------<



#------------------InputButton--------------
class InputButton(AbsPanel):
    def __init__(self, screen, x, y, text, color = WHITE,
                 width=300, height=110, img_active=None, img_disactive=None, music=None,
                 function=None
                 ):
        super().__init__(screen, x, y, text, color,
                         width, height, img_active, img_disactive,
                         function)

        self.focus = False
        self.input_text = ""
        self.text.change_text("")

        # Звук кнопки, флаг звука
        self.music = music
        self.music_key = True

        self.count = 0
        self.add = 1

    def check_add(self):
        if (self.count)// 35 % 2 == self.add and self.count != 0:
            try:
                if self.input_text[-1] == "|":
                    self.input_text = self.input_text[:-1]
            except IndexError:
                pass
                
            if self.add == 1:
                self.input_text += "|"
            self.add = 1 - self.count // 30 % 2

        self.text.change_text(self.input_text)

    def update(self, *args):
        if self.focus:
            self.in_box()
            self.check_add()

            self.count += 1
        else:
            self.out_box()

        self.text.draw_in_obj(self.x, self.y)

    def click(self, mouse):
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            return True

        return False

    @check_key
    def add_key(self, key):
        self.input_text += key
        self.text.change_text(self.input_text)

    @check_key
    def delete_key(self):
        self.input_text = self.input_text[:-1]
        self.text.change_text(self.input_text)

    @check_key
    def end_key(self):
        self.focus = False
        self.text.change_text(self.input_text)

    @tools()
    def in_box(self) -> any:
        if self.music_key and self.music:
            self.music.play()
            self.music_key = False

        return self.img_active

    @tools()
    def out_box(self) -> any:
        self.music_key = True

        return self.img_disactive

    def get(self):
        return self.input_text



#-------------------MENU--------------------
class ObjsMenu:
    def __init__(self, screen, clock,
                 FPS=30, img_fon=None, sound=None
                 ):
        self.screen = screen
        self.clock = clock

        self.FPS = FPS
        self.img_fon = img_fon
        self.sound = sound

        self.list = {}

    def init_text(self, texts, coords, is_auto = False,
                  step=None, type=None, location="C",
                  font=None, font_color=GRAY, font_type=None, font_size=50, text_location="C",
                  indents=None, text_indents=None
                  ):
        obj = ObjsText(self.screen, texts, font,
                       font_color=GRAY, font_type=None, font_size=50, text_location="C",
                       indents=None, text_indents=None )
        if is_auto is True:
            try:
                obj.auto_draw(coords[0], coords[1], step, type, location)
            except:
                raise ValueError(f"Something wrong with coords. Please be confirmed that you\
                give only x and y coords. YOUR COORDS {coords}")
        else:
            obj.manual_draw(coords)

        self.list["TEXT"] = obj

    def init_button(self, amount, x, y, step, obj_texts, type=0,
                    width=300, height=110, img_active=None, img_disactive=None, music=None,
                    functions=[]
                    ):
        obj = Menu(self.screen, amount, x, y, step, obj_texts, type,
                   width, height, img_active, img_disactive,  music,
                   functions)

        self.list["BUTTON"] = obj

    def init_label(self):
        pass
    def init_panel(self):
        pass

    def update(self, mouse):
        for obj in self.list.values():
            obj.update(mouse)

    def start(self):
        try:
            clickable = [self.list.get("BUTTON")]
        except:
            pass

        cursor = pygame.mouse.set_cursor(*pygame.cursors.arrow)

        play = True
        while play:

            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    #Проверка нажатия ЛКМ
                    if event.button == 1 and clickable[0] is not None:
                        #Проверят в списке кнопок, на какую из них нажали
                        for objs in clickable:
                            for obj in objs.get_list():
                                func = obj.click()
                                #Запоминает функцию кнопки и останавливает цикл
                                if func is not False:
                                    play = False
                                    next_func = func


            if self.img_fon is None:
                self.screen.fill(BLACK)
            elif key:
                self.screen.blit(self.img_fon,(0,0))

            mouse = pygame.mouse.get_pos()
            self.update(mouse)

            pygame.display.flip()

        #Проверяет существует ли функция запомненая при нажатии на кнопку
        try:
            #Запускает следующую функцию
            next_func()
        except TypeError:
            pass


class Menu():
    def __init__(self, screen, amount, x, y, step, obj_texts, type=0,                      #Параметры меню
                 width=300, height=110, img_active=None, img_disactive=None, music=None,   #Параметры кнопки
                 functions=[],                                                             #Функции кнопки
                 ):
        # Экран отрисовки
        self.screen = screen

        self.amount = amount
        self.type = type

        self.x = x
        self.y = y
        self.step = step

        self.btn_width = width
        self.btn_height = height

        if (img_active and img_disactive) is not None:
            self.img_active = pygame.transform.scale(img_active, (width,height))
            self.img_disactive = pygame.transform.scale(img_disactive, (width,height))
        else:
            self.img_active, self.img_disactive = None, None

        self.music = music

        self.obj_texts = obj_texts
        if not functions:
            self.functions = [None for i in range(amount)]
        else:
            self.functions = functions


        self.btn_list = []
        self.coords_list = []

        self.create()

    def create(self):
        texts = self.obj_texts.get_texts()
        for i in range(self.amount):
            if self.type:
                x = self.x + (self.btn_width+self.step)*i
                y = self.y
            else:
                x = self.x
                y = self.y + (self.btn_height+self.step)*i

            print(x, y)

            btn = Button(self.screen, x, y, texts[i], WHITE,
                         self.btn_width, self.btn_height, self.img_active, self.img_disactive, self.music,
                         self.functions[i])
            self.btn_list.append(btn)

    def update(self, *args):
        for btn in self.btn_list:
            btn.update(args[0])

    def get_amount(self):
        return self.amount

    def get_list(self):
        return self.btn_list

#---------------------------------------------------------



#----------------------BUTTON------------------------------

class Button(AbsPanel):
    """
    Класс отвечающий за создание анимированных кнопок
    """
    def __init__(self, screen, x, y, text, color=WHITE,                                  #Основные параметры
                 width=300, height=110, img_active=None, img_disactive=None, music=None, #Параметры для кнопки
                 function=None                                                           #Функция кнопки
                 ):
        #Иницилизация родительского класса
        super().__init__(screen, x, y, text, color, \
                         width, height, img_active, img_disactive
                         )

        # Звук кнопки, флаг звука
        self.music = music
        self.music_key = True

        # Функцию кнопки
        self.function = function

        # Флаг нажатия кнопки
        self.key = False

    def update(self, *args) -> any:
        """Каждый кадр

        Обновляем состояние кнопки

        """
        mouse = args[0]

        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            self.in_box()
        else:
            self.out_box()

        self.text.draw_in_obj(self.x, self.y)

    def click(self) -> any:
        """На клик

        Определение нажимал ли пользователь на кнопку

        """
        if self.key:
            return self.function

        return None

    @tools()
    def in_box(self) -> any:
        if self.music_key and self.music:
           self.music.play()
           self.music_key = False

        self.key = True

        return self.img_active

    @tools()
    def out_box(self) -> any:
        self.music_key = True
        self.key = False

        return self.img_disactive

#------------------------------------------------------------------------


#---------------------LABEL-----------------------
class Label(AbsPanel):
    def __init__(self, screen, x, y, text, color = WHITE,
                 width=300, height=110, img_disactive=None
                 ):
        super().__init__(screen, x, y, text, color, \
                         width, height, img_disactive=img_disactive
                         )

    def update(self, *args) -> any:
        self.draw_img()
        self.text.draw_in_obj(self.x, self.y)

    @tools()
    def draw_img(self) -> any:
        return self.img_active

    def change_text(self, text: str) -> any:
        pass


#---------------------PANEL-----------------------

class Panel(AbsPanel):
    def __init__(self, screen, x, y,
                 width=600, height=600, image=None,
                 objs_text=None, tX = None, tY = None, step=None, type=None, location="C"
                 ):
        super().__init__(screen, x, y, None, width, height, img_disactive=image)
        self.screen = screen

        self.objs_text = objs_text
        self.objs_text.auto_draw(tX, tY, step, type, location)

    def chech_text(self):
        def check():
            coords = self.objs_text.get_size()
            indents = self.objs_text.text_indents
            x, y = self.width, self.height

            for text in range(self.objs_text.amount):
                x += indents[0]
                y += indents[1]
                if coords[text][0] > x and coords[text][1] > y:
                    raise ValueError(f"Size ERROR. Text size Text more then panel size{self.obj_texts[text].text}. \
                    Text{coords[text]} Panel{self.width, self.height}. Indents{indents}")

            pass
        pass

    #@tools
    def draw(self):
        pass

    def update(self):
        self.objs_text.draw_in_obj()

#----------------------------------------------------------

#------------------------TEXT------------------------------
class ObjsText():
    def __init__(self, screen, texts: List[str], font=None,
                 font_color=GRAY, font_type=None, font_size=50, text_location="C",
                 indents=None, text_indents=None
                 ):
        self.screen = screen
        self.amount = len(texts)
        self.texts = texts

        self.font = font
        self.fonts_setting = [font,
                              font_color, font_type, font_size, text_location,
                              indents
                              ]

        self.list = []
        self.coords_list = [self.font.get_size(texts[i]) for i in range(self.amount)]

        self.step = None
        self.text_indents = text_indents

        self.create_texts()

    def create_texts(self):
        for text in range(self.amount):
            obj = Text(self.screen, self.texts[text], *self.fonts_setting)
            self.list.append(obj)

    def get_texts(self):
        return self.list

    def get_coords(self):
        return self.coords_list

    def update(self, *args):
        self.draw(self.coords)

    #@check_size
    def draw(self, coords = None) -> None:
        if self.step is not None:
            for i in range(self.amount):
                if self.type:
                    x = self.x + (self.coords_list[i][0]+self.step)*i
                    y = self.y
                else:
                    x = self.x
                    y = self.y + (self.coords_list[i][1]+self.step)*i


                self.list[i].draw(x, y)
        else:
            for i in range(self.amount):
                self.list[i].draw(*coords)

    def draw_in_obj(self):
        pass

    def manual_draw(self, coords):
        self.coords = coords

    def auto_draw(self, x: int, y: int, step: int, type: int, location="C"):
        self.x, self.y = x, y
        self.step = step
        self.type = type
        self.location = location




class Text():
    def __init__(self, screen, text, font=None,                                             #Основные параметры
                 font_color=GRAY, font_type=None, font_size=50, text_location="C",          #Цвет, Шрифт, Размер, Выравнивание
                 indents=None                                                               #Отступы
                 ):
        # Экран отрисовки
        self.screen = screen

        # Расположение и цвет текста
        self.text_location = text_location
        self.font_color = font_color

        #Оступы
        self.activate_indent(indents)

        # Рендер текста для вывода
        self.text = text
        if font is None:
            self.font = Font(font_type, font_color, font_size)
        else:
            self.font = font

        self.text_to_render = self.font.render(text)


    def change_font(self, font: Optional[pygame.font.Font]) -> any:
        self.font = font
        self.text_to_render = self.font.render(self.text)

    def change_text(self, text:str) -> any:
        self.text = text
        self.text_to_render = self.font.render(text)


    def activate_indent(self, indents: List[int]) -> any:
        if indents is not None:
            self.indent_x, self.indent_y = indents[0], indents[1]
            self.isIndent = True
        else:
            self.indent_x, self.indent_y = 0, 0
            self.isIndent = False


    def location(self, *btn_sizes: List[int]) -> any:
        def check(x,y,curX_size):
            if x > btn_sizes[0] or y > btn_sizes[1]:
                raise ValueError(f"Font size more then button size! SIZE: Button{btn_sizes}, \
Text{x,y}. Please change button or font size.")

            if self.text_location == "C":
                indent = curX_size//2
            elif self.text_location == "R":
                indent = curX_size - 10
            elif self.text_location == "L":
                indent = 10
            else:
                raise ValueError("Font location incorrect! Please check font location!")

            return indent

        def auto_indent():
            size = self.font.get_size(self.text)
            x, y = size[0], size[1]
            curX_size = btn_sizes[0] - x

            self.indent_x += check(x,y,curX_size)
            self.indent_y += (btn_sizes[1] - y) // 2



        if self.isIndent is not True:
            auto_indent()
        else:
            pass


    def draw(self, x:int, y:int) -> None:
        """
        Отображает текст на экране
        """
        self.screen.blit(self.text_to_render, (x, y))

    def draw_in_obj(self, x:int, y:int) -> None:
        """
        Отображет текст на каком-то объекте с отступами
        """
        #print(self.indent_x, self.indent_y)
        self.screen.blit(self.text_to_render, (x+self.indent_x, y+self.indent_y))


#----------------------------------------------------------


#--------------FONTS-------------------------
class Font():
    def __init__(self, font_type, font_color, font_size,
                 *args, **kwargs
                 ):
        if font_type is not None:
            self.type = font_type
        self.color = font_color
        self.size = font_size

        self.font = self.font = pygame.font.Font(font_type, font_size, *kwargs)

    def render(self, text: str) -> any:
        return self.font.render(text, True, self.color)

    def get_color(self):
        return self.color

    def get_size(self, text:str) -> List[int]:
        return self.font.size(text)

    def set_color(self):
        self.color = color





"""
#----------------PANEL---------------------

class ObjPanel():
    def __init__(self, screen, images, coords, texts):
        self.screen = screen
        self.images = images
        self.coords = coords
        self.texts = texts

        self.list_panel = []

    def create(self):
        for i in range(len(self.images())):
            pnl = Panel(self.screen, self.images[i], self.coords[i], self.texts[i])

            self.list_panel.append(pnl)

    def update(self):
        for pnl in self.list_panel:
            pnl.update()

"""


#-------------------------------------------------------

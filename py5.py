import time
from typing import *
from tkinter import *
import enum
from typing import List
from math import *
from PIL import ImageTk, Image, ImageDraw2
import numpy as np
import sys

# angle_k = 0.0
size: Callable
circle: Callable
ellipse: Callable
triangle: Callable
square: Callable
rect: Callable
fill: Callable
stroke: Callable
noStroke: Callable
line: Callable
background: Callable
strokeWeight: Callable
clear: Callable
translate: Callable
resetTrans: Callable
push: Callable
pop: Callable
rotate: Callable
noFill: Callable
beginShape: Callable
vertex: Callable
text: Callable
endShape: Callable
grid: Callable
image: Callable
dT: Callable
setT: Callable
mX: Callable
mY: Callable
key: Callable
W: Callable
H: Callable

class PyImage:
    def __init__(self, image: any ) -> None:
        if type(image) is str:
            self.image = Image.open(image)
            
        elif type(image) is Image.Image:
            self.image = image

        if self.image is not None:
            self.width = self.image.width
            self.height = self.image.height
        
        self.conf = {
            'font': '/home/ruhailmir/.fonts/f/FiraCode-SemiBold.ttf',
            'stroke': 'red',
            'font_size': 50,
            'fill': 'white',
            'stroke_weight': 1,
            'opacity': 0,
            'filling': True,
            'stroking': False,
            'translation_stack': [],
            'translation_': (0, 0),
        }

    def get(self, x: int, y: int):
        return self.image.getpixel((x, y))
        
    '''
    pixel: Image._Color -> float
    pixel: Image._Color -> tuple(float, float ...)
    '''
    def put(self, x:int, y: int, pixel: any):
        self.image.putpixel((x, y), pixel)

    def save(self, name: str) -> None:
        self.image.save(name)

    def resize(self, width: int, height: int):
        self.image = self.image.resize((width, height))

    def noFill(self):
        self.conf['filling'] = False
    
    def fill(self, color: any):
        self.conf['filling'] = True
        self.conf['fill'] = color

    def noStroke(self):
        self.conf['stroking'] = False

    # universal state functions ...
    def translate(self, tx, ty):
        stack_:List = self.conf.get('translation_stack')
        stack_.append((tx, ty))
        tTrans_ = tuple(np.sum(stack_, 0))
        self.conf['translation_'] = tTrans_

    def background(self, color_hex: str = '#000000FF'):
        self.conf['bg'] = self.conf.get('fill')
        self.conf['fill'] = color_hex
        self.rect(-self.conf.get('translation_')[0],
            -self.conf.get('translation_')[1],
            self.width, self.height, clr=True)
        self.conf['fill'] = self.conf.get('bg')
        self.clearStates()

    def stroke(self, color: any):
        self.conf['stroking'] = True
        self.conf['stroke'] = color

    def strokeWeight(self, weight: int):
        self.conf['stroke_weight'] = weight

    def line(self, x0, y0, x1, y1):
        ctx = ImageDraw2.Draw(self.image)
        coords = Coord( x0, y0, x1, y1, transformation=TransformationType.NONE )
        coords.apply_translation(self.conf.get('translation_'))
        #
        brush_ = ImageDraw2.Brush(self.conf.get('fill'),
            self.conf.get('opacity'))
        pen_ = ImageDraw2.Pen(self.conf.get('stroke'),
            self.conf.get('stroke_weight'), self.conf.get('opacity'))

        if self.conf.get('filling') and self.conf.get('stroking'):
            ctx.line([(coords.x0, coords.y0), (coords.x1, coords.y1)],
                pen_, brush_)

        elif self.conf.get('filling'):
            ctx.line([(coords.x0, coords.y0), (coords.x1, coords.y1)],
                brush_)

        elif self.conf.get('stroking'):
            ctx.line([(coords.x0, coords.y0), (coords.x1, coords.y1)],
                pen_)
        else:
            # print('Invalid conf !', 'line')
            pass

    def get_tk(self) -> ImageTk.PhotoImage:
        self.tk_img = ImageTk.PhotoImage(self.image)
        return self.tk_img
        
    def text(self, text: str, x: int, y: int):
        ctx = ImageDraw2.Draw(self.image)
        coords = Coord( x, y, 0, 0, transformation=TransformationType.NONE )
        coords.apply_translation(self.conf.get('translation_'))
        #
        font_ = ImageDraw2.Font(self.conf.get('stroke'),
            self.conf.get('font'), self.conf.get('font_size'))
        ctx.text((coords.x0, coords.y0), text, font_)

    def circle(self, x:float, y: float, rad: float):
        self.ellipse(x, y, rad, rad)

    def clearStates(self):
        self.conf['translation_stack'] = []

    def ellipse(self, x: float, y: float, width:int, height:int):
        ctx = ImageDraw2.Draw(self.image)
        coords = Coord( x, y, 0, 0, transformation=TransformationType.NONE )
        coords.apply_translation(self.conf.get('translation_'))
        #
        brush_ = ImageDraw2.Brush(self.conf.get('fill'),
            self.conf.get('opacity'))
        pen_ = ImageDraw2.Pen(self.conf.get('stroke'),
            self.conf.get('stroke_weight'), self.conf.get('opacity'))

        if self.conf.get('filling') and self.conf.get('stroking'):
            ctx.ellipse([(coords.x0, coords.y0), (coords.x0+width, coords.y0+height)],
                pen_, brush_)

        elif self.conf.get('filling'):
            ctx.ellipse([(coords.x0, coords.y0), (coords.x0+width, coords.y0+height)],
                brush_)

        elif self.conf.get('stroking'):
            ctx.ellipse([(coords.x0, coords.y0), (coords.x0+width, coords.y0+height)],
                pen_)
        else:
            # print('Invalid conf !', 'ellipse')
            pass

    def rect(self, x: float, y: float, width: int, height: int, clr=False):
        ctx = ImageDraw2.Draw(self.image)
        coords = Coord( x, y, 0, 0, transformation=TransformationType.NONE )
        coords.apply_translation(self.conf.get('translation_'))
        #
        brush_ = ImageDraw2.Brush(self.conf.get('fill'),
            self.conf.get('opacity'))
        pen_ = ImageDraw2.Pen(self.conf.get('stroke'),
            self.conf.get('stroke_weight'), self.conf.get('opacity'))

        if self.conf.get('filling') and self.conf.get('stroking') or clr:
            ctx.rectangle([(coords.x0, coords.y0), (coords.x0+width, coords.y0+height)],
                pen_, brush_)
        elif self.conf.get('filling'):
            ctx.rectangle([(coords.x0, coords.y0), (coords.x0+width, coords.y0+height)],
                brush_)
        elif self.conf.get('stroking'):
            ctx.rectangle([(coords.x0, coords.y0), (coords.x0+width, coords.y0+height)],
                pen_)
        else:
            # print('Invalid conf !', 'rect')
            pass

    '''
        creates new image from the given conf.

        Modes: ['1', 'CMYK', 'F', 'HSV', 'I', 'L', 'LAB',
            'P', 'RGB', 'RGBA', 'RGBX', 'YCbCr']
    '''
    @staticmethod
    def create( width: int, height: int, mode: any ) -> any:
        return PyImage(Image.new(mode, (width, height)))


class Grid:
    def __init__(self, spacing: float, labels: bool = False, center: bool = True):
        self.spacing = spacing
        self.labels = labels
        self.center = center
        self.width = W()
        self.height = H()
        self.grid = []
        if not self.center:
            for x in np.arange(0, (self.width / self.spacing)+1):
                row = []
                for y in np.arange(0, (self.height / self.spacing)+1):
                    row.append((x*self.spacing, y*self.spacing))
                self.grid.append(row)
        else:
            for x in np.arange((-(self.width/2) / self.spacing), ((self.width / 2) / self.spacing)+1):
                row = []
                for y in np.arange((-(self.height/2) / self.spacing), ((self.height / 2) / self.spacing)+1):
                    row.append((x*self.spacing, y*self.spacing))
                self.grid.append(row)
                
    def show(self):
        if self.center:
            translate(W()/2, H()/2)

        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                current_ = self.grid[x][y]
                try:
                    next_x = self.grid[x+1][y]
                    next_y = self.grid[x][y+1]
                    if next_x is not None and next_y is not None:
                        stroke('#005050')
                        line(current_[0], current_[1], next_x[0], next_x[1])
                        line(current_[0], current_[1], next_y[0], next_y[1])
                    stroke('white')
                    circle(current_[0], current_[1], 2)
                except Exception:
                    pass

        # Labels !
        if not self.center:
            for x in np.arange(0, (self.width / self.spacing)+1):
                text(str(floor(x)), x * self.spacing + 7, 10, size=12)

            for y in np.arange(0, (self.height / self.spacing)+1):
                text(str(floor(y)), 7, y * self.spacing + 10, size=12)
        else:
            for x in np.arange((-(self.width/2) / self.spacing), ((self.width / 2) / self.spacing)+1):
                text(str(floor(x)), x * self.spacing + 7, 10, size=12)

            for y in np.arange((-(self.height/2) / self.spacing), ((self.height / 2) / self.spacing)+1):
                text(str(floor(y)), 7, y * self.spacing + 10, size=12)

class TransformationType(enum.Enum):
    NORMAL = 0
    TRIANGLE = 1
    POLYGON = 2
    ROTATIONAL = 3
    NONE = 4

class Coord:
    def __init__(self, x, y, W, H, poly = None, transformation: TransformationType = TransformationType.NORMAL):        
        self.x0 = 0.0
        self.y0 = 0.0
        self.x1 = 0.0
        self.y1 = 0.0
        self.x2 = 0.0
        self.y2 = 0.0
        self.x3 = 0.0
        self.y3 = 0.0
        self.poly = poly

        if transformation == TransformationType.NONE:
            self.x0 = x
            self.y0 = y
            self.x1 = W
            self.y1 = H

        elif transformation == transformation.ROTATIONAL:
            self.x0 = x - (W / 2.0)
            self.y0 = y - (H / 2.0)
            self.x1 = x + (W / 2.0)
            self.y1 = y - (H / 2.0)
            self.x2 = x + (W / 2.0)
            self.y2 = y + (H / 2.0)
            self.x3 = x - (W / 2.0)
            self.y3 = y + (H / 2.0)
            
        elif transformation == transformation.NORMAL:
                self.x0 = x - (W / 2.0)
                self.y0 = y - (H / 2.0)
                self.x1 = x + (W / 2.0)
                self.y1 = y + (W / 2.0)
                #
        elif transformation == transformation.TRIANGLE:
                self.x0 = x - (W / 2.0)
                self.y0 = y + (H / 2.0)
                self.x1 = x
                self.y1 = y - (H / 2.0)
                self.x2 = x + (W / 2.0)
                self.y2 = y + (H / 2.0)
                #

        elif transformation == transformation.POLYGON:
                if poly is not None and x is not None and y is not None:
                    self.x0 = x
                    self.y0 = y
                    self.poly = poly
        else:
                print('invalid transformation type')

    def apply_rotation(self, angle):
        a_ = np.array([
            [self.x0],
            [self.y0]])
        b_ = np.array([
            [self.x1],
            [self.y1]])
        c_ = np.array([
            [self.x2],
            [self.y2]])
        d_ = np.array([
            [self.x3],
            [self.y3]])

        rot_ = np.array([
            [cos(angle), -sin(angle)],
            [sin(angle), cos(angle)]
        ])
        
        a = rot_ @ a_
        b = rot_ @ b_
        c = rot_ @ c_
        d = rot_ @ d_
        #
        self.x0 = a[0, 0]
        self.y0 = a[1, 0]
        self.x1 = b[0, 0]
        self.y1 = b[1, 0]
        self.x2 = c[0, 0]
        self.y2 = c[1, 0]
        self.x3 = d[0, 0]
        self.y3 = d[1, 0]
        #
        #end
        
    def apply_translation(self, translation):
        self.x0 += translation[0]
        self.y0 += translation[1]
        self.x1 += translation[0]
        self.y1 += translation[1]
        self.x2 += translation[0]
        self.y2 += translation[1]
        self.x3 += translation[0]
        self.y3 += translation[1]
        if self.poly is not None:
            summed_ = list(np.array(self.poly) + np.array(translation))
            self.poly = [tuple(x) for x in summed_]
        # end

class ShapeType(enum.Enum):
    CIRCLE = 0
    ELLIPSE = 1
    RECTANGLE = 2
    SQUARE = 3
    TRIANGLE = 4
    POLYGON = 5

class GShape:
    def __init__(self, canvas: Canvas, coords: Coord, current:dict, id: int):
        self.id = id
        self.canvas = canvas
        self.coords = coords
        self.current = current
        
        self.coords.apply_rotation(self.current.get('rotation_'))
        self.coords.apply_translation(self.current.get('translation_'))

        self.bg =  self.current.get('bg')
        self.stroke = self.current.get('stroke')
        self.stroke_weight = self.current.get('stroke_weight')
        self.filling = self.current.get('filling')
        self.fill = self.current.get('fill')

    def create(self, type:ShapeType):
        if type == type.ELLIPSE:
                self.canvas.create_oval(
                    self.coords.x0, self.coords.y0,
                    self.coords.x1, self.coords.y1,
                    outline=self.stroke if self.current.get('stroke_weight') > 0 else None,
                    fill= ( self.fill if self.filling else "" ),
                    width=self.stroke_weight)
                #
        elif type == type.RECTANGLE:
                self.canvas.create_polygon (
                    self.coords.x0, self.coords.y0,
                    [(self.coords.x1, self.coords.y1),
                    (self.coords.x2, self.coords.y2),
                    (self.coords.x3, self.coords.y3)],
                    outline=self.stroke if self.current.get('stroke_weight') > 0 else None,
                    fill= ( self.fill if self.filling else "" ),
                    width=self.stroke_weight
                )
                #
        elif type == type.TRIANGLE:
                self.canvas.create_polygon (
                    self.coords.x0, self.coords.y0,
                    self.coords.x1, self.coords.y1,
                    (self.coords.x2, self.coords.y2),
                    outline=self.stroke if self.current.get('stroke_weight') > 0 else None,
                    fill= ( self.fill if self.filling else "" ),
                    width=self.stroke_weight
                )
                #
        elif type == type.POLYGON:
                self.canvas.create_polygon (
                    self.coords.x0, self.coords.y0, self.coords.poly,
                    outline=self.stroke if self.current.get('stroke_weight') > 0 else None,
                    fill= ( self.fill if self.filling else "" ),
                    width=self.stroke_weight
                )
        else:
                print('invalid shape type')

class SimpleCanvas:
    def __init__(self):
        # to objects
        self.root: Tk = None
        self.canvas: Canvas = None
        self.width:float = 300
        self.height:float = 300
        self.T_ = 10
        self.dT_ = 0.1
        self.Inf = False

        global size, circle, ellipse, triangle, square, rect, fill, stroke, \
            noStroke, line, background, strokeWeight, clear, \
                translate, push, pop, resetTrans, rotate, noFill, beginShape, vertex, \
                    endShape, text, grid, image, dT, setT, mX, mY, key, W, H
                    
        dT = self.dT
        W = self.get_width
        H = self.get_height
        mX = self.mX
        mY = self.mY
        key = self.key
        setT = self.setT
        size = self.size
        grid = self.grid
        text = self.text
        image = self.image
        circle = self.circle
        ellipse = self.ellipse
        triangle = self.triangle
        rect = self.rect
        square = self.square
        fill = self.fill
        stroke = self.stroke
        noStroke = self.noStroke
        line = self.line
        background = self.background
        strokeWeight = self.strokeWeight
        clear = self.clear
        translate = self.translate
        push = self.push
        pop = self.pop
        resetTrans = self.resetTrans
        rotate = self.rotate
        noFill = self.noFill
        beginShape = self.beginShape
        vertex = self.vertex
        endShape = self.endShape

        # Event state ...
        self.event = {
            'mouseX': 0,
            'mouseY': 0,
            'key': None
        }

        # configuration swaps ...
        self.conf_backup = {}
        self.state_exception = False

        # configuration
        self.conf = {
            'bg': 'black',
            'stroke': 'white',
            'stroke_weight': 2,
            'filling': True,
            'fill' : 'white',
            'background_rect': None,
            'shape_id_count': 0,
            'shapes_': {},
            'poly_state': [],
            'translation_stack': [],
            'translation_': (0, 0),
            'rotation_': 0.0
        }
    # ----------------------------------------------------------

    def get_conf(self, prop: str):
        return self.conf.get(prop)

    def set_conf(self, prop: str, value: any):
        self.conf[prop] = value

    #

    # universal state functions ...
    def translate(self, tx, ty):
        stack_:List = self.conf.get('translation_stack')
        stack_.append((tx, ty))
        tTrans_ = tuple(np.sum(stack_, 0))
        self.conf['translation_'] = tTrans_

    def push(self):
        self.conf_backup = self.conf.copy()
        self.state_exception = True

    def pop(self):
        self.conf = self.conf_backup
        self.state_exception = False
        self.clearStates()

    def resetTrans(self):
        self.conf['translation_'] = (0, 0)

    def rotate(self, angle):
        self.conf['rotation_'] = angle

    def clearStates(self):
        if self.state_exception:
            raise Exception('Error, Expected a call to pop')
        
        self.conf['translation_stack'] = []
        self.conf_backup = {}

    def background(self, color='black'):
        self.clear()
        self.clearStates()
        self.canvas.create_rectangle(0, 0,
            self.width,
            self.height,
            fill=color)
        self.conf['bg'] = color

    def stroke(self, stroke: str):
        self.conf['stroke'] = stroke
    
    def noStroke(self):
        self.conf['stroke_weight'] = 0

    def strokeWeight(self, weight: int):
        self.conf['stroke_weight'] = weight

    def noFill(self):
        self.conf['filling'] = False

    def fill(self, color):
        self.conf['fill'] = color
        self.conf['filling'] = True

    # special ------------------
    def beginShape(self):
        state_:List = self.conf.get('poly_state')
        state_.append({
            'vertices': []
        })

    def vertex(self, x, y):
        state_:List = self.conf.get('poly_state')
        state_[0].get('vertices').append((x, y))

    def endShape(self):
        state_:List = self.conf.get('poly_state')
        L_ = state_[0]
        state_.remove(L_) # remove the first object
        vertices_:List = L_.get('vertices')
        x_ = vertices_[0][0]
        y_ = vertices_[0][1]
        vertices_.remove(vertices_[0]) # remove first point, sent manually...
        # create the shape now...
        coords = Coord ( x_, y_, 0, 0, poly=vertices_, transformation=TransformationType.POLYGON)
        current_ = self.conf.get('shape_id_count')
        self.conf['shape_id_count'] = self.conf['shape_id_count'] + 1
        GShape(self.canvas, coords, self.conf, current_).create(ShapeType.POLYGON)

    # special end --------------
    '''
        time step to reach T = 10
        use setT(t: float) to change T
    '''
    def dT(self, t: float):
        self.dT_ = t

    def setT(self, t: float):
        self.T_ = t

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    # shapes --- lines...
    def line(self, x1, y1, x2, y2):
        if self.canvas is not None:
            self.canvas.create_line(
                x1 + self.conf.get('translation_')[0],
                y1 + self.conf.get('translation_')[1],
                x2 + self.conf.get('translation_')[0],
                y2 + self.conf.get('translation_')[1],
                fill=self.conf.get('stroke'),
                width=self.conf.get('stroke_weight'))
                
    def ellipse(self, x, y, r1, r2):
        coords = Coord ( x, y, r1, r2)
        current_ = self.conf.get('shape_id_count')
        self.conf['shape_id_count'] = self.conf['shape_id_count'] + 1
        GShape(self.canvas, coords, self.conf, current_).create(ShapeType.ELLIPSE)

    def circle(self, x, y, radius):
        coords = Coord ( x, y, radius, radius)
        current_ = self.conf.get('shape_id_count')
        self.conf['shape_id_count'] = self.conf['shape_id_count'] + 1
        GShape(self.canvas, coords, self.conf, current_).create(ShapeType.ELLIPSE)

    def rect(self, x, y, w, h):
        coords = Coord ( x, y, w, h, transformation=TransformationType.ROTATIONAL)
        current_ = self.conf.get('shape_id_count')
        self.conf['shape_id_count'] = self.conf['shape_id_count'] + 1
        GShape(self.canvas, coords, self.conf, current_).create(ShapeType.RECTANGLE)
    
    def square(self, x, y, size):
        coords = Coord ( x, y, size, size)
        current_ = self.conf.get('shape_id_count')
        self.conf['shape_id_count'] = self.conf['shape_id_count'] + 1
        GShape(self.canvas, coords, self.conf, current_).create(ShapeType.RECTANGLE)

    def triangle(self, x, y, width, height):
        coords = Coord ( x, y, width, height, transformation=TransformationType.TRIANGLE)
        current_ = self.conf.get('shape_id_count')
        self.conf['shape_id_count'] = self.conf['shape_id_count'] + 1
        GShape(self.canvas, coords, self.conf, current_).create(ShapeType.TRIANGLE)

    def text(self, text: str, x: float, y: float, name: str = '"Victor Mono Thin"', size: float = 15):
        font_ = f'{name} {size}'
        coords = Coord( x, y, 0, 0, transformation=TransformationType.NONE )
        coords.apply_translation(self.conf.get('translation_'))
        self.canvas.create_text(coords.x0, coords.y0,
            fill = self.conf.get('fill'), text = text,
            font=font_)

    def image(self, img:PyImage, x:float, y: float):
        coords = Coord(x, y, 0, 0, transformation=TransformationType.NONE)
        coords.apply_translation(self.conf.get('translation_'))
        self.canvas.create_image( coords.x0, coords.y0, anchor=NW,
            image = img.get_tk() )

    def grid(self, spacing: float = 50, labels: bool = True, center: bool = True):
        Grid(spacing, labels, center).show()

    # main --- setup
    def size(self, w, h):
        self.width = w
        self.height = h
        self.root = Tk()
        self.root.title(sys.argv[0].split('.')[0].capitalize())
        self.root.geometry(f'{self.width}x{self.height}')
        self.canvas = Canvas(master=self.root,
            width=self.width,
            height=self.height,
            bg=self.conf.get('bg'))

        self.canvas.pack()
        self.root.bind('<Motion>', self.M)
        self.root.bind('<Key>', self.K)

    def update(self):
        self.canvas.update()

    def clear(self):
        self.canvas.delete('all')
        
    def loop(self):
        self.root.mainloop()

    # Event Handling ...
    def M(self, e):
        self.event['mouseX'] = e.x
        self.event['mouseY'] = e.y

    def K(self, k):
        self.event['key'] = k

    def mX(self):
        return self.event.get('mouseX')

    def mY(self):
        return self.event.get('mouseY')

    def key(self):
        return self.event.get('key')

# --------------------------------
def keyPressed_(f):
    this.root.bind('<Key>', lambda e: f(e))

this = SimpleCanvas()

def setup_(param):
    # param(this)
    param()

def draw_(param):
    t = 0
    while t < this.T_ or this.Inf:
        try:
            this.update()
            # param(this)
            param()
            t += this.dT_
            # time.sleep(0.1)
        except Exception as e:
            print(e)
            exit(0)

    this.loop()


# For Audio ...
class PyAudio:
    def __init__(self, name: str) -> None:
        from pygame import mixer
        mixer.init()
        mixer.music.load(name)
        self.mixer = mixer
        self.finished = False

    def play(self):
        if not self.finished:
            self.mixer.music.play()
            self.finished = True
        # ...
#

from PIL import Image, ImageDraw

img_w = 675
img_h = 225

image = Image.new('RGBA', (img_w, img_h), color='black')
draw = ImageDraw.Draw(image)



#accesses underlying pixels
def access_square_center(x, y):
    return_x = 25*x + 13
    return_y = 25*y + 13

    return return_x, return_y


#input the high level grid of letters, get the underlying pixel coords
def access_square(x, y):
    processedx = (x*2) - 1
    processedy = (y*2) - 1
    return access_square_center(processedx, processedy)


for x in range(1, 14):
    for y in range(1, 5):
        imgx, imgy = access_square(x, y)
        draw.ellipse([imgx, imgy, imgx+10, imgy+10], fill='red')
  



coordinates = {
    '1': (1, 1),
    '2': (2, 1),
    '3': (3, 1),
    '4': (4, 1),
    '5': (5, 1),
    '6': (6, 1),
    '7': (7, 1),
    '8': (8, 1),
    '9': (9, 1),
    '0': (10, 1),
    '-': (11, 1),
    '=': (12, 1),
    'delete': (13, 1),
    'a': (1, 2),
    'b': (2, 2),
    'c': (3, 2),
    'd': (4, 2),
    'e': (5, 2),
    'f': (6, 2),
    'g': (7, 2),
    'h': (8, 2),
    'i': (9, 2),
    'j': (10, 2),
    'k': (11, 2),
    'l': (12, 2),
    'm': (13, 2),
    'n': (1, 3),
    'o': (2, 3),
    'p': (3, 3),
    'q': (4, 3),
    'r': (5, 3),
    's': (6, 3),
    't': (7, 3),
    'u': (8, 3),
    'v': (9, 3),
    'w': (10, 3),
    'x': (11, 3),
    'y': (12, 3),
    'z': (13, 3),
    '[': (1, 4),
    ']': (2, 4),
    '\\': (3, 4),
    ';': (4, 4),
    '\'': (5, 4),
    ',': (6, 4),
    '.': (7, 4),
    '/': (8, 4),
    'shift': (9, 4),
    # 'shift': (10, 4),
    'enter': (11, 4),
    'space': (12, 4),
    'caps lock': (13, 4)
}

image.show()
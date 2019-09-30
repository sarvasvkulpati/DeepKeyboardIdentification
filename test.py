
import keyboard
from PIL import Image, ImageDraw
from test3 import coordinates
import json
import math
import colour
from colour import Color

square_size = 70

img_w = square_size*(13+14)
img_h = square_size*(4+5)

image = Image.new('RGBA', (img_w, img_h), color='black')
draw = ImageDraw.Draw(image)

#accesses underlying pixels
def access_square_center(x, y):
    return_x = square_size*x + math.ceil(square_size/2)
    return_y = square_size*y + math.ceil(square_size/2)

    return return_x, return_y


#input the high level grid of letters, get the underlying pixel coords
def access_square(x, y):
    processedx = (x*2) - 1
    processedy = (y*2) - 1
    return access_square_center(processedx, processedy)

recorded = keyboard.record()

def overlay_circle(image, x, y, size, color = 'red'):
    overlay = Image.new('RGBA', (image.size))
    overlay_draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
    overlay_draw.ellipse([x, y, x+size, y+size], fill=color)
    return Image.alpha_composite(image, overlay)

def overlay_line(image, startx, starty, endx, endy, width, color='red'):
    overlay = Image.new('RGBA', (image.size))
    overlay_draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
    overlay_draw.line((startx, starty, endx, endy), fill=color, width=width)
    return Image.alpha_composite(image, overlay)


#TODO: fix range function, right now it produces a number outside the range and returns an indexerror when trying to access val 
def duration_to_color(max_duration, min_duration, duration, color_range, transparency):

    # print(max_duration, min_duration, duration, color_range)
    OldRange = (max_duration - min_duration)  
    color_index = int(((duration - min_duration) * color_range) / OldRange)
    # print("color index = " + "(" + str(duration) + "-" + str(min_duration) + ")" + "*" + str(color_range) + "/" + str(OldRange))
    # print(color_index)

    red = Color("red")
    blue = Color("blue")
    colors = list(blue.range_to(red, color_range+1))
    # print([color.rgb for color in colors])
    return_color = colors[color_index].rgb
    return_color = tuple([int(x* 255) for x in return_color])
    return (*return_color, transparency)


def duration_to_size(max_duration, min_duration, duration, size_range):
    OldRange = (max_duration - min_duration)  
    print(OldRange)
    size = int((duration - min_duration) * size_range / OldRange) +5 
    return size



# print(recorded)

cache = []
# print(recorded)
for currentEvent in recorded:
    if currentEvent.name == 'esc':
        break

    # if the current letter doesn't exist in the cache, add it to the cache
    if not any(event['name'] == currentEvent.name for event in cache):
        cache.append({'name': currentEvent.name, 'num' : 1, 'start' : currentEvent.time, 'end':None})

    # if it does exist in the cache
    else:
        relevantEvents = [event for event in cache if event['name'] is currentEvent.name]
        try:
            if relevantEvents[len(relevantEvents) - 1]['num'] is 2:
                #if the last one was a complete press, add new event to cache
                cache.append({'name': currentEvent.name, 'num' : 1, 'start' : currentEvent.time, 'end':None})
            else:
                #if the existing one has not been released yet, complete it with the release time
                relevantEvents[len(relevantEvents) - 1].update({'num' : 2, 'end': currentEvent.time})
        except IndexError:
            print('indexerror')
            cache.append({'name': currentEvent.name, 'num' : 1, 'start' : currentEvent.time, 'end':None})

cacheWithLines = []

lastKeyPress = None
for idx, keyPress in enumerate(cache):
    if lastKeyPress:
        # print(lastKeyPress, keyPress)
        down_down_time = keyPress['start'] - lastKeyPress['start']
        cacheWithLines.append(lastKeyPress)
        cacheWithLines.append({'name': 'line', 'time': down_down_time})
        cacheWithLines.append(keyPress)
    lastKeyPress = keyPress

# print(cacheWithLines)

line_timings = [x['time'] for x in cacheWithLines if x['name'] == 'line']

circle_timings = [x['end'] - x['start'] for x in cacheWithLines if x['name'] != 'line' and x['end'] != None]



max_duration_lines = max(line_timings)
min_duration_lines = min(line_timings)

max_duration_circles = max(circle_timings)
min_duration_circles = min(circle_timings)

shapes = []






for idx, event in enumerate(cacheWithLines):
    if event['name'] == 'line':
        try:
            startx, starty = access_square(coordinates[cacheWithLines[idx - 1]['name']][0], coordinates[cacheWithLines[idx - 1]['name']][1])

            endx, endy = access_square(coordinates[cacheWithLines[idx + 1]['name']][0], coordinates[cacheWithLines[idx + 1]['name']][1])

            # print(startx, starty, endx, endy)
            # image = draw.line((startx, starty, endx, endy), fill='red', width=1)
            color = duration_to_color(max_duration_lines, min_duration_lines, event['time'], color_range=50, transparency=50)
            # print(color)
            size = duration_to_size(max_duration_lines, min_duration_lines, event['time'], 20)
            image = overlay_line(image, startx, starty, endx, endy, size, color=color)
        except KeyError:
            continue
    else:
        try:
            imgx, imgy = access_square(coordinates[event['name']][0], coordinates[event['name']][1])
        
            # print(imgx, imgy)
            # draw.ellipse([imgx, imgy, imgx+10, imgy+10], fill=(255,0,0,128))
            if event['end'] != None:
                color = duration_to_color(max_duration_circles, min_duration_circles, event['end']- event['start'], color_range=50, transparency=50)
                # print(color)
                size = duration_to_size(max_duration_circles, min_duration_circles, event['end']- event['start'], 50)
                print(size)
                image = overlay_circle(image, imgx, imgy, size, color=color)
        except KeyError:
            continue

image.save('img.png')
    
keyboard.wait()   





'''
Type: 

the quick brown fox jumped over the lazy dog

12345 + 67890 = 80,235

It's raining very heavily!




'''

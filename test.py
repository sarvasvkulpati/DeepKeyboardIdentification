
import keyboard
from PIL import Image, ImageDraw
from test3 import coordinates
import json

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

recorded = keyboard.record()




print(recorded)

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

print(cacheWithLines)

shapes = []






for idx, event in enumerate(cacheWithLines):
    if event['name'] == 'line':
        try:
            startx, starty = access_square(coordinates[cacheWithLines[idx - 1]['name']][0], coordinates[cacheWithLines[idx - 1]['name']][1])

            endx, endy = access_square(coordinates[cacheWithLines[idx + 1]['name']][0], coordinates[cacheWithLines[idx + 1]['name']][1])

            print(startx, starty, endx, endy)
            draw.line((startx, starty, endx, endy), fill='red', width=1)
        except KeyError:
            continue
    else:
        try:
            imgx, imgy = access_square(coordinates[event['name']][0], coordinates[event['name']][1])
        
            print(imgx, imgy)
            draw.ellipse([imgx, imgy, imgx+10, imgy+10], fill=(255,0,0,128))
        except KeyError:
            continue

image.save('img.png')
    
keyboard.wait()   





# print(recorded)

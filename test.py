
import keyboard
from PIL import Image, ImageDraw

import json

im = Image.open("keyboard.png")
draw = ImageDraw.Draw(im)
key_location = {"Escape": (13, 10, 0), "F1": (78, 10, 0), "F2": (116, 10, 0), "F3": (154, 10, 0), "F4": (193, 10, 0), "F5": (253, 10, 0), "F6": (291, 10, 0), "F7": (329, 10, 0), "F8": (367, 10, 0), "F9": (428, 10, 0), "F10": (466, 10, 0), "F11": (504, 10, 0), "F12": (542, 10, 0), "Snapshot": (601, 10, 0), "Scroll`": (639, 10, 0), "Pause": (677, 10, 0), "Oem_3": (13, 82, 0), "1": (52, 83, 0), "2": (89, 82, 0), "3": (127, 82, 0), "4": (165, 82, 0), "5": (203, 82, 0), "6": (242, 82, 0), "7": (280, 82, 0), "8": (318, 82, 0), "9": (356, 82, 0), "0": (394, 82, 0), "Oem_Minus": (432, 82, 0), "Oem_Plus": (470, 82, 0), "Back": (508, 82, 1), "Insert": (603, 82, 0), "Home": (641, 82, 0), "Prior": (679, 82, 0), "NumLock": (738, 82, 0), "Divide-": (776, 82, 0), "Multiply*": (814, 82, 0), "Subtract": (852, 82, 0), "Tab": (13, 122, 2), "q": (69, 122, 0), "w": (107, 122, 0), "e": (146, 122, 0), "r": (184, 122, 0), "t": (222, 122, 0), "y": (260, 122, 0), "u": (297, 122, 0), "i": (336, 122, 0), "o": (374, 122, 0), "p": (412, 122, 0), "Oem_4": (449, 122, 0), "Oem_6": (487, 122, 0), "Oem_5": (526, 122, 3), "delete": (602, 122, 0), "End": (640, 122, 0), "Next": (678, 122, 0), "Numpad7": (737, 122, 0), "Numpad8": (775, 122, 0), "Numpad9": (813, 122, 0), "Add": (852, 122, 4), "Capital": (13, 161, 5), "a": (79, 161, 0), "s": (117, 161, 0), "d": (156, 161, 0), "f": (194, 161, 0), "g": (232, 161, 0), "h": (270, 161, 0), "j": (308, 161, 0), "k": (346, 161, 0), "l": (384, 161, 0), "Oem_1": (422, 161, 0), "Oem_7": (461, 161, 0), "Return": (499, 161, 6), "Numpad4": (737, 161, 0), "Numpad5": (776, 161, 0), "Numpad6": (814, 161, 0), "Lshift": (13, 200, 7), "z": (106, 200, 0), "x": (145, 200, 0), "c": (183, 200, 0), "v": (222, 200, 0), "b": (260, 200, 0), "n": (298, 200, 0), "m": (336, 200, 0), "Oem_Comma": (374, 200, 0), "Oem_Period": (413, 200, 0), "Oem_2": (451, 200, 0), "Rshift": (489, 200, 8), "Up": (641, 200, 0), "Numpad1": (738, 201, 0), "Numpad2": (775, 201, 0), "Numpad3": (814, 201, 0), "NumpadReturn": (851, 201, 9), "Lcontrol": (13, 240, 10), "Lwin": (69, 240, 11), "Lmenu": (119, 240, 11), "space": (169, 240, 12), "Rmenu": (377, 240, 11), "Rwin": (427, 240, 11), "Apps": (476, 240, 11), "Rcontrol": (525, 240, 10), "Left": (603, 240, 0), "Down": (641, 240, 0), "Right": (679, 240, 0), "Numpad0": (738, 240, 13), "Decimal": (814, 240, 0)}



recorded = keyboard.record()






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
        pass
        startx = key_location[cacheWithLines[idx - 1]['name']][0]
        starty = key_location[cacheWithLines[idx - 1]['name']][1]
        endx = key_location[cacheWithLines[idx + 1]['name']][0]
        endy = key_location[cacheWithLines[idx + 1]['name']][1]
        draw.line((startx, starty, endx, endy), fill='black', width=10)
    else:
        if len(event['name']) == 1:
            imgx = key_location[event['name']][0]
            imgy = key_location[event['name']][1]
            draw.ellipse([imgx, imgy, imgx+10, imgy+10], fill='red')
        elif event['name'] == 'delete':
            imgx = key_location['Back'][0]
            imgy = key_location['Back'][1]
            draw.ellipse([imgx, imgy, imgx+10, imgy+10], fill='red')

    

       


im.save('img.png')


# print(recorded)
keyboard.wait()
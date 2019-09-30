from colour import Color

def duration_to_color(max_duration, min_duration, duration, color_range, transparency):

    OldRange = (max_duration - min_duration)  
    color_index = abs(int(((duration - min_duration) * color_range) / OldRange) )
    print(color_index)

    red = Color("red")
    blue = Color("blue")
    colors = list(blue.range_to(red, color_range))

    return_color = colors[color_index].rgb
    return_color = tuple([int(x) for x in return_color])
    return (*return_color, transparency)



print(duration_to_color(100, 0, 2, 5, 50))
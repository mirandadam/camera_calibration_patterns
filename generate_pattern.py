# -*- coding: utf-8 -*-


def square_template(identifier, centerx, centery, size, direction):
    s = '<rect id="rect{0}" y="{1}" x="{2}" height="{3}" width="{3}" />'
    return s.format(identifier, centery - size / 2, centerx - size / 2, size, size)


def circle_template(identifier, centerx, centery, size, direction):
    # r=size/4. #clearance equals one full circle
    r = size / 3.
    # r=size/2.
    # r=size*(2**0.5 - 1) #equal distance between one circle, the next level and the limit boundary
    # r=size*(2**0.5)/2. #circles touching
    s = '<circle id="circle{0}" r="{1}" cy="{2}" cx="{3}" />'  # filled circle
    return s.format(identifier, r, centery, centerx)


def hollow_circle_template(identifier, centerx, centery, size, direction):
    # r=size/4. #clearance equals one full circle
    # r=size/3.
    r = size / 2.
    # r=size*(2**0.5 - 1) #equal distance between one circle, the next level and the limit boundary
    # r=size*(2**0.5)/2. #circles touching
    s = '<circle style="fill:none;stroke:#000000;stroke-opacity:1;stroke-width:{4}" id="circle{0}" r="{1}" cy="{2}" cx="{3}" />'  # circle outline
    return s.format(identifier, r, centery, centerx, r / 10.)


def color_circle_template(identifier, centerx, centery, size, direction):
    # r=size/4. #clearance equals one full circle
    # r=size/3.
    r = size / 2.
    # r=size*(2**0.5 - 1) #equal distance between one circle, the next level and the limit boundary
    # r=size*(2**0.5)/2. #circles touching
    colors = {-1: '008888', 0: '880000', 1: '008800', 2: '000088', 3: '888800'}
    # Fill the missing color! Uncomment the following for "puzzle mode"
    # if identifier % 4 == 0:
    #    colors = {}
    s = '<circle style="fill:#{4};stroke:#000000;stroke-opacity:1;stroke-width:{5}" id="circle{0}" r="{1}" cy="{2}" cx="{3}" />'  # circle outline
    return s.format(identifier, r, centery, centerx, colors.get(direction, 'FFFFFF'), r / 40)


# input parameters:
#'''
input_pattern = 'templates/a4_template.svg'
output_file = 'small_circles.svg'
placeholder_text = '<rect id="placeholder" width="100" height="100" x="0" y="0" />'
page_height_mm = 210
page_width_mm = 297
pattern_columns = 12
pattern_rows = 8
margins_mm = 5
detail_level = 3  # 0 is just the center marker. Try to keep it at 5 or lower.
marker_template = circle_template
#'''

'''
input_pattern = 'templates/a4_template.svg'
output_file = 'large_circles.svg'
placeholder_text = '<rect id="placeholder" width="100" height="100" x="0" y="0" />'
page_height_mm = 210
page_width_mm = 297
pattern_columns = 3
pattern_rows = 2
margins_mm = 5
detail_level = 5  # 0 is just the center marker. Try to keep it at 5 or lower.
marker_template = circle_template
#'''

'''
input_pattern = 'templates/a4_template.svg'
output_file = 'hollow_circles.svg'
placeholder_text = '<rect id="placeholder" width="100" height="100" x="0" y="0" />'
page_height_mm = 210
page_width_mm = 297
pattern_columns = 3
pattern_rows = 2
margins_mm = 5
detail_level = 4  # 0 is just the center marker. Try to keep it at 5 or lower.
marker_template = hollow_circle_template
#'''

'''
input_pattern = 'templates/a4_template.svg'
output_file = 'color_circles.svg'
placeholder_text = '<rect id="placeholder" width="100" height="100" x="0" y="0" />'
page_height_mm = 210
page_width_mm = 297
pattern_columns = 3
pattern_rows = 2
margins_mm = 5
detail_level = 4  # 0 is just the center marker. Try to keep it at 5 or lower.
marker_template = color_circle_template
#'''

'''
input_pattern = 'templates/a4_template.svg'
output_file = 'deep_squares.svg'
placeholder_text = '<rect id="placeholder" width="100" height="100" x="0" y="0" />'
page_height_mm = 210
page_width_mm = 297
pattern_columns = 3
pattern_rows = 2
margins_mm = 5
detail_level = 6  # 0 is just the center marker. Try to keep it at 5 or lower.
marker_template = square_template
#'''


# calculating internal parameters (mind the default of 90dpi that inkscape uses):
page_height_pix = page_height_mm * 90 / 25.4
page_width_pix = page_width_mm * 90 / 25.4
margins_pix = margins_mm * 90 / 25.4
pattern_size = min((page_height_pix - 2 * margins_pix) / pattern_rows, (page_width_pix - 2 * margins_pix) / pattern_columns)
cell_base_size = pattern_size / 3.  # the pattern linear size converges to 3 times the cell linear size
# x coordinate of the CENTER of the upper left pattern:
offsetx = pattern_size / 2. + (page_width_pix - 2 * margins_pix - pattern_columns * pattern_size) / 2. + margins_pix
# y coordinate of the CENTER of the upper left pattern:
offsety = pattern_size / 2. + (page_height_pix - 2 * margins_pix - pattern_rows * pattern_size) / 2. + margins_pix


backlog = [[offsetx, offsety, 0, -1]]  # x,y,level,direction is 0 to 3, -1 is the initial point
markers = []
while backlog:
    x, y, level, direction = backlog.pop()
    r = cell_base_size / (2.**level)
    markers.append([x, y, r, direction])
    if level <= detail_level:
        d = r * 3 / 4.
        level = level + 1
        if direction != 0:
            backlog.append([x - d, y - d, level, 2])
        if direction != 1:
            backlog.append([x + d, y - d, level, 3])
        if direction != 2:
            backlog.append([x + d, y + d, level, 0])
        if direction != 3:
            backlog.append([x - d, y + d, level, 1])
        del d
    del x, y, level, direction, r
del backlog

f = open(input_pattern, 'r', encoding='utf8')
a, b = f.read().split(placeholder_text)
f.close()

f = open(output_file, 'w', encoding='utf8')
f.write(a)
count = 1

for i in range(pattern_rows):
    dy = i * pattern_size
    for j in range(pattern_columns):
        dx = j * pattern_size
        for x, y, r, direction in markers:
            f.write(marker_template(count, x + dx, y + dy, r, direction) + '\n')
            count = count + 1

x0 = offsetx - pattern_size / 2.
y0 = offsety - pattern_size / 2.
f.write('<rect style="fill:none;stroke:#000000;stroke-opacity:0" y="{0}" x="{1}" height="{2}" width="{3}" />'.format(y0, x0, pattern_rows * pattern_size, pattern_columns * pattern_size) + '\n')

f.write(b)
f.close()

s = 0
for i in range(detail_level + 1):
    s = s + (3**i)
s = (s * 4 + 1) * pattern_columns * pattern_rows


#'''
import subprocess
output_png = output_file[:-4] + '.png'
comando = [
    'C:\\Program Files\\Inkscape\\inkscape.exe',
    '-D',  # '-a','{0}:{1}:{2}:{3}'.format(x0,y0,x1,y1),#'x0:y0:x1:y1',
    '--export-dpi=600',
    '-f', output_file,
    '--export-png=' + output_png]
subprocess.check_output(comando)
output_pdf = output_file[:-4] + '.pdf'
comando = [
    'C:\\Program Files\\Inkscape\\inkscape.exe',
    '-C',  # '-a','{0}:{1}:{2}:{3}'.format(x0,y0,x1,y1),#'x0:y0:x1:y1',
    '-f', output_file,
    '--export-pdf=' + output_pdf]
subprocess.check_output(comando)
#'''

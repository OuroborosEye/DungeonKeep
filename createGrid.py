from PIL import Image

# Each grid cell is 10x10
black = (0,0,0)
green = (51, 204, 51)

cell_template = [green if (0 not in (x,y) and 9 not in (x,y)) else black for x in range(10) for y in range(10)]
print(cell_template)


im = Image.new('RGB', (10,10))
im.putdata(cell_template)
im.save('test.png')
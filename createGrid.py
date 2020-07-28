from PIL import Image


class Grid:
    def __init__(self,row,col,color):
        self.data = []
        self.rows = row
        self.cols = col

        for r in range(row):
            self.data.append([])
            for _ in range(col):
                self.data[r].append(PlainCell(color))

    def replaceCell(self,cell,row,col):
        self.data[row][col] = cell

    def toImageData(self):
        data = []
        for grid_row in self.data:
            for cel_row in range(20):
                for cel in grid_row:
                    data.extend(cel.data[cel_row])
        return data
    
    def saveToFile(self):
        im = Image.new('RGB', (self.rows * cel_size,self.cols * cel_size))
        im.putdata(self.toImageData())
        im.save('test.png')

isBorder = lambda x,y,length: 0 in (x,y) or length-1 in (x,y)
isDiagonal = lambda x,y,length:  x == y or x+y == length
flatten = lambda l: [item for sublist in l for item in sublist]

class PlainCell:
    def __init__(self,color):
        self.data = [[color if not isBorder(x,y,cel_size) else black for x in range(cel_size)] for y in range(cel_size)]

class BlockedCell:
    def __init__(self,color):
        self.data = [[color if not isBorder(x,y,cel_size) and not isDiagonal(x,y,cel_size) else black for x in range(cel_size)] for y in range(cel_size)]


cel_size = 20

# Each grid cell is 10x10
black = (0,0,0)
green = (51, 204, 51)
red = (255, 0, 102)

grid = Grid(5,5,green)
grid.replaceCell(BlockedCell(red),2,3)
grid.saveToFile()

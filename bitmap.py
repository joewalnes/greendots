from sys import stdout


class Bitmap:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[0] * width for i in range(height)]

    def apply(self, bitmap, op=lambda a, b: b, x=0, y=0):
        for py, row in enumerate(bitmap.data):
            for px, pixel in enumerate(row):
                old = self.data[y + py][x + px]
                if y + py >= 0 and y + py < self.height and x + px >= 0 and x + px < self.width:
                    self.data[y + py][x + px] = op(old, pixel)

    def dump(self):
        """Dump this to stdout, for debugging."""
        for row in self.data:
            for pixel in row:
                stdout.write('#' if pixel else ' ')
            stdout.write('\n')
        stdout.flush()




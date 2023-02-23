class Point:
    x: int
    y: int

    def __int__(self, x: int, y: int):
        self.x = x
        self.y = y


class Rectangle:
    x: int
    y: int
    x2: int
    y2: int

    def __init__(self, x: int, y: int, x2: int, y2: int):
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2

    @classmethod
    def from_points(cls, p1: Point, p2: Point):
        return Rectangle(p1.x, p1.y, p2.x, p2.y)

    def to_tuple(self):
        return self.x, self.y, self.x2, self.y2

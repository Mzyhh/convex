from deq import Deq
from r2point import R2Point
from math import sqrt


class Line:
    """ Прямая """

    def __init__(self, p: R2Point, q: R2Point):
        """creating a line using 2 points"""

        self._a = q.y - p.y
        self._b = p.x - q.x
        self._c = -(self._a * p.x + self._b * p.y)

    def delta(self, m):
        """delta is a distance from a point to a line\n
        delta = (a*x + b*y + c) * sgn(c) / sqrt(a**2 + b**2)\n
        a, b, c - coefficients in the equation of a line"""

        sgn_c = 1 if self._c >= 0 else -1
        return (self._a * m.x + self._b * m.y + self._c) * (-sgn_c) /\
            sqrt(self._a**2 + self._b**2)

    def is_close_p(self, p, dist=1):
        """the distance between a point (p) and a line is less than dist"""

        return abs(self.delta(p)) < dist

    def is_close_seg(self, p, q, dist=1):
        """the distance between a segment(p, q) and a line is less than dist"""

        return self.is_close_p(p) and self.is_close_p(q)


class Figure:
    """ Абстрактная фигура """

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def close_edges(self):
        return 0

    def bind_line(self, p, q):
        self.fl = Line(p, q)


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        super().__init__()
        self.p = p

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        super().__init__()
        self.p, self.q = p, q

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def close_edges(self):
        return 2 if self.fl.is_close_seg(self.p, self.q) else 0

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r)
        elif self.q.is_inside(self.p, r):
            return Segment(self.p, r)
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return self


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c, p=None, q=None):
        super().__init__()
        self.points = Deq()
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        if q is None:
            self._close_edges = None
        else:
            self.bind_line(p, q)
            close_points = self.fl.is_close_p(a) + self.fl.is_close_p(b)\
                + self.fl.is_close_p(c)
            self._close_edges = 0 if close_points < 2 else\
                1 if close_points == 2 else 3

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    def close_edges(self):
        return self._close_edges

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))
            if self._close_edges is not None:
                self._close_edges -= self.fl.is_close_seg(self.points.first(),
                                                          self.points.last())

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                if self._close_edges is not None:
                    self._close_edges -= self.fl.\
                        is_close_seg(self.points.first(), p)
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                if self._close_edges is not None:
                    self._close_edges -= self.fl.\
                        is_close_seg(self.points.last(), p)
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())
            if self._close_edges is not None:
                self._close_edges += self.fl.\
                    is_close_seg(t, self.points.first()) + self.fl.\
                    is_close_seg(t, self.points.last())
            self.points.push_first(t)

        return self


if __name__ == "__main__":
    f = Void()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
    f.bind_line(R2Point(2, 2), R2Point(3, 4))

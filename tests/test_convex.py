from pytest import approx
from math import sqrt
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon, Line


class TestLine:

    # Вычисление коэффициентов прямой, заданной двумя различными точками
    #   Прямая-нормис
    def test_bind1(self):
        a = Line(R2Point(-2, 3), R2Point(3, 1))
        assert a._a == -2 and a._b == -5 and a._c == 11

    #   Вертикальная
    def test_bind2(self):
        a = Line(R2Point(-5.0, 4.0), R2Point(-5.0, 0.0))
        assert a._a == -4.0 and a._b == 0.0 and a._c == -20.0

    #   Горизонтальная
    def test_bind3(self):
        a = Line(R2Point(1, 3), R2Point(10, 3))
        assert a._a == 0 and a._b == -9 and a._c == 27

    # Вычисление отклонения
    def test_delta1(self):
        a = Line(R2Point(-2, 3), R2Point(3, 1))
        assert a.delta(R2Point(0.0, 2.2)) == approx(0.0)

    def test_delta2(self):
        a = Line(R2Point(-5.0, 4.0), R2Point(-5.0, 0.0))
        assert a.delta(R2Point(0.0, 0.0)) == approx(-5.0)

    def test_delta3(self):
        a = Line(R2Point(1, 3), R2Point(10, 3))
        assert a.delta(R2Point(0.0, 4.5)) == approx(1.5)


class TestFigure:

    def setup_method(self):
        self.f = Figure()

    # Вычисление коэффициентов прямой, заданной двумя различными точками
    #   Прямая-нормис
    def test_bind1(self):
        self.f.bind_line(R2Point(-2, 3), R2Point(3, 1))
        assert self.f.fl._a == -2 and self.f.fl._b == -5 and self.f.fl._c == 11

    #   Вертикальная
    def test_bind2(self):
        self.f.bind_line(R2Point(-5.0, 4.0), R2Point(-5.0, 0.0))
        assert self.f.fl._a == -4.0 and self.f.fl._b == 0.0 and\
            self.f.fl._c == -20.0

    #   Горизонтальная
    def test_bind3(self):
        self.f.bind_line(R2Point(1, 3), R2Point(10, 3))
        assert self.f.fl._a == 0 and self.f.fl._b == -9 and self.f.fl._c == 27

    # Вычисление отклонения
    def test_delta1(self):
        self.f.bind_line(R2Point(-2, 3), R2Point(3, 1))
        assert self.f.fl.delta(R2Point(0.0, 2.2)) == approx(0.0)

    def test_delta2(self):
        self.f.bind_line(R2Point(-5.0, 4.0), R2Point(-5.0, 0.0))
        assert self.f.fl.delta(R2Point(0.0, 0.0)) == approx(-5.0)

    def test_delta3(self):
        self.f.bind_line(R2Point(1, 3), R2Point(10, 3))
        assert self.f.fl.delta(R2Point(0.0, 4.5)) == approx(1.5)


class TestVoid:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Void()

    # Нульугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Void (нульугольник)
    def test_void(self):
        assert isinstance(self.f, Void)

    # Периметр нульугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь нульугольника нулевая
    def test_area(self):
        assert self.f.area() == 0.0

    # При добавлении точки нульугольник превращается в одноугольник
    def test_add(self):
        assert isinstance(self.f.add(R2Point(0.0, 0.0)), Point)

    # Количество особых ребёр
    def test_edge(self):
        assert self.f.close_edges() == 0


class TestPoint:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Point(R2Point(0.0, 0.0))

    # Одноугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Point (одноугольник)
    def test_point(self):
        assert isinstance(self.f, Point)

    # Периметр одноугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь одноугольника нулевая
    def test_area(self):
        assert self.f.area() == 0.0

    # При добавлении точки одноугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.0, 0.0)) is self.f

    # При добавлении точки одноугольник может превратиться в двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(1.0, 0.0)), Segment)

    # Количество особых ребёр
    def test_edge(self):
        assert self.f.close_edges() == 0


class TestSegment:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Segment(R2Point(0.0, 0.0), R2Point(1.0, 0.0))

    # Двуугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Segment (двуугольник)
    def test_segment(self):
        assert isinstance(self.f, Segment)

    # Периметр двуугольника равен удвоенной длине отрезка
    def test_perimeter(self):
        assert self.f.perimeter() == approx(2.0)

    # Площадь двуугольника нулевая
    def test_area(self):
        assert self.f.area() == 0.0

    # При добавлении точки двуугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.5, 0.0)) is self.f

    # При добавлении точки правее двуугольник может превратиться в другой
    # двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(2.0, 0.0)), Segment)

    # При добавлении точки левее двуугольник может превратиться в другой
    # двуугольник
    def test_add3(self):
        assert isinstance(self.f.add(R2Point(-1.0, 0.0)), Segment)

    # При добавлении точки двуугольник может превратиться в треугольник
    def test_add4(self):
        assert isinstance(self.f.add(R2Point(0.0, 1.0)), Polygon)

    # Проверка на принадлежность 1-окрестности открытой прямой
    def test_edge1(self):
        self.f.bind_line(R2Point(0.0, 0.5), R2Point(1.0, 0.5))
        assert self.f.close_edges() == 2

    def test_edge2(self):
        self.f.bind_line(R2Point(0.5, 0.0), R2Point(0.5, 5.0))
        assert self.f.close_edges() == 2

    def test_edge3(self):
        self.f.bind_line(R2Point(0.0, 0.0), R2Point(0.0, 5.0))
        assert self.f.close_edges() == 0

    def test_edge4(self):
        self.f.bind_line(R2Point(0.0, 1.0), R2Point(3.0, 1.0))
        assert self.f.close_edges() == 0

    def test_edge5(self):
        self.f.bind_line(R2Point(0.0, 1.1), R2Point(3.0, 1.0))
        assert self.f.close_edges() == 0

    def test_edge6(self):
        self.f.bind_line(R2Point(0.0, 0.9), R2Point(3.0, 1.0))
        assert self.f.close_edges() == 2


class TestPolygon:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.a = R2Point(0.0, 0.0)
        self.b = R2Point(1.0, 0.0)
        self.c = R2Point(0.0, 1.0)
        self.f = Polygon(self.a, self.b, self.c)

        self.f2 = Polygon(self.a, self.b, self.c, R2Point(0.0, -0.1),
                          R2Point(1.0, -0.1))

        self.f3 = Polygon(self.a, self.b, self.c, R2Point(0.0, 0.3),
                          R2Point(.5, .5))

    # Многоугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Polygon (многоугольник)
    def test_polygon1(self):
        assert isinstance(self.f, Polygon)

    # Изменение порядка точек при создании объекта всё равно порождает Polygon
    def test_polygon2(self):
        self.f = Polygon(self.b, self.a, self.c)
        assert isinstance(self.f, Polygon)

    # Изменение количества вершин многоугольника
    #   изначально их три
    def test_vertexes1(self):
        assert self.f.points.size() == 3

    #   добавление точки внутрь многоугольника не меняет их количества
    def test_vertexes2(self):
        assert self.f.add(R2Point(0.1, 0.1)).points.size() == 3

    #   добавление другой точки может изменить их количество
    def test_vertexes3(self):
        assert self.f.add(R2Point(1.0, 1.0)).points.size() == 4

    #   изменения выпуклой оболочки могут и уменьшать их количество
    def test_vertexes4(self):
        assert self.f.add(
            R2Point(
                0.4,
                1.0)).add(
            R2Point(
                1.0,
                0.4)).add(
                    R2Point(
                        0.8,
                        0.9)).add(
                            R2Point(
                                0.9,
                                0.8)).points.size() == 7
        assert self.f.add(R2Point(2.0, 2.0)).points.size() == 4

    # Изменение периметра многоугольника
    #   изначально он равен сумме длин сторон
    def test_perimeter1(self):
        assert self.f.perimeter() == approx(2.0 + sqrt(2.0))

    #   добавление точки может его изменить
    def test_perimeter2(self):
        assert self.f.add(R2Point(1.0, 1.0)).perimeter() == approx(4.0)

    # Изменение площади многоугольника
    #   изначально она равна (неориентированной) площади треугольника
    def test_area1(self):
        assert self.f.area() == approx(0.5)

    #   добавление точки может увеличить площадь
    def test_area2(self):
        assert self.f.add(R2Point(1.0, 1.0)).area() == approx(1.0)

    # Тесты на функцию, вычисляющую кол-во ребер, лежащих в 1-окрестность
    # заданной прямой
    #   При инициализации
    def test_edge_init1(self):
        assert self.f.close_edges() is None

    def test_edge_init2(self):
        ff = Polygon(self.a, self.b, self.c, R2Point(0.0, 0.5),
                     R2Point(0.5, 0.0))
        assert ff.close_edges() == 3

    def test_edge_init2(self):
        ff = Polygon(self.a, self.b, self.c, R2Point(0.0, -0.1),
                     R2Point(1.0, -0.1))
        assert ff.close_edges() == 1

    def test_edge_init3(self):
        ff = Polygon(self.a, self.b, self.c, R2Point(0.0, -1.1),
                     R2Point(1.0, -2))
        assert ff.close_edges() == 0

    #   При добавлении новых точек
    def test_edge_add1(self):
        self.f2 = self.f2.add(R2Point(1.0, 1.0))
        assert self.f2.close_edges() == 1

    def test_edge_add2(self):
        self.f2 = self.f2.add(R2Point(3.0, 0.5))
        assert self.f2.close_edges() == 2

    def test_edge_add3(self):
        self.f2 = self.f2.add(R2Point(.5, -0.5))
        assert self.f2.close_edges() == 2

    def test_edge_add4(self):
        self.f2 = self.f2.add(R2Point(.5, -5.0))
        assert self.f2.close_edges() == 0

    def test_edge_add5(self):
        self.f2 = self.f2.add(R2Point(.5, -0.5))
        self.f2 = self.f2.add(R2Point(.8, -0.3))
        assert self.f2.close_edges() == 3

    def test_edge_add6(self):
        self.f3 = self.f3.add(R2Point(1.1, 0.4))
        assert self.f3.close_edges() == 4

    def test_edge_add7(self):
        self.f3 = self.f3.add(R2Point(1.1, 0.4))
        self.f3 = self.f3.add(R2Point(0.5, 0.5))
        self.f3 = self.f3.add(R2Point(-0.5, 0.5))
        assert self.f3.close_edges() == 5

    def test_edge_add8(self):
        self.f3 = self.f3.add(R2Point(-2, 0.5))
        self.f3 = self.f3.add(R2Point(0.6, 0.8))
        self.f3 = self.f3.add(R2Point(3.0, 4.5))
        assert self.f3.close_edges() == 2

    def test_edge_add9(self):
        f4 = Polygon(R2Point(-1.0, 0.0), R2Point(1.0, 0.0), R2Point(0.0, -0.2),
                     R2Point(-1.0, 0.0), R2Point(1.0, 0.0))
        f4 = f4.add(R2Point(-0.9, 0.2))
        f4 = f4.add(R2Point(0.9, 0.2))
        f4 = f4.add(R2Point(-0.8, 0.3))
        f4 = f4.add(R2Point(0.8, 0.3))
        f4 = f4.add(R2Point(-0.6, 0.4))
        f4 = f4.add(R2Point(0.6, 0.4))
        f4 = f4.add(R2Point(-0.3, 0.5))
        f4 = f4.add(R2Point(0.3, 0.5))
        f4 = f4.add(R2Point(0.0, 3.0))
        assert f4.close_edges() == 2

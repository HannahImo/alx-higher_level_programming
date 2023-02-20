#!/usr/bin/python3
"""Tests for data model base class"""


import importlib
import json
import models.base
import models.rectangle
import models.square
import os
import unittest


Base = models.base.Base
Rectangle = models.rectangle.Rectangle
Square = models.square.Square


class BaseTests (unittest.TestCase):
    """Tests for data model base class"""

    def setUp(self):
        """Reset module being tested between tests"""

        importlib.reload(models.base)
        importlib.reload(models.rectangle)
        importlib.reload(models.square)

    def test_Create(self):
        """Creating new instances with the create class method"""

        with self.subTest():
            o = Rectangle.create()
            self.assertIsInstance(o, Rectangle)
            self.assertEqual(o.x, 0)
            self.assertEqual(o.y, 0)
            self.assertEqual(o.id, 1)
        with self.subTest():
            o = Square.create()
            self.assertIsInstance(o, Square)
            self.assertEqual(o.x, 0)
            self.assertEqual(o.y, 0)
            self.assertEqual(o.id, 2)
        with self.subTest():
            o = Rectangle.create(width=3, height=4)
            self.assertEqual(o.width, 3)
            self.assertEqual(o.height, 4)
            self.assertEqual(o.x, 0)
            self.assertEqual(o.y, 0)
            self.assertEqual(o.id, 3)
        with self.subTest():
            o = Rectangle.create(width=4, height=5, extra='extra')
            self.assertEqual(o.width, 4)
            self.assertEqual(o.height, 5)
            self.assertEqual(o.x, 0)
            self.assertEqual(o.y, 0)
            self.assertEqual(o.id, 4)
        with self.subTest():
            o = Square.create(size=3)
            self.assertEqual(o.size, 3)
            self.assertEqual(o.x, 0)
            self.assertEqual(o.y, 0)
            self.assertEqual(o.id, 5)
        with self.subTest():
            o = Square.create(size=4, extra='extra')
            self.assertEqual(o.size, 4)
            self.assertEqual(o.x, 0)
            self.assertEqual(o.y, 0)
            self.assertEqual(o.id, 6)
        with self.subTest():
            o = Rectangle.create(width=1, height=2, x=3, y=4, id='id')
            d = {'width': 1, 'height': 2, 'x': 3, 'y': 4, 'id': 'id'}
            self.assertEqual(o.to_dictionary(), d)
        with self.subTest():
            o = Square.create(size=1, x=3, y=4, id='id')
            d = {'size': 1, 'x': 3, 'y': 4, 'id': 'id'}
            self.assertEqual(o.to_dictionary(), d)

    def test_Csv(self):
        """Converting to CSV files and back"""

        try:
            os.remove('Rectangle.csv')
        except FileNotFoundError:
            pass
        try:
            os.remove('Square.csv')
        except FileNotFoundError:
            pass
        r1 = Rectangle(1, 2, 3, 4)
        r2 = Rectangle(5, 6, 7, 8)
        with self.subTest():
            Rectangle.save_to_file_csv([r1, r2])
            with open('Rectangle.csv', 'rt') as file:
                self.assertEqual(file.read(), '1,1,2,3,4\n2,5,6,7,8\n')
        with self.subTest():
            Rectangle.save_to_file_csv(None)
            with open('Rectangle.csv', 'rt') as file:
                self.assertEqual(file.read(), '')
        s1 = Square(10, 20, 30)
        s2 = Square(100, 200, 300)
        with self.subTest():
            Square.save_to_file_csv([s1, s2])
            with open('Square.csv', 'rt') as file:
                self.assertEqual(file.read(), '3,10,20,30\n4,100,200,300\n')
        with self.subTest():
            Square.save_to_file_csv([])
            with open('Square.csv', 'rt') as file:
                self.assertEqual(file.read(), '')
        try:
            os.remove('Rectangle.csv')
        except FileNotFoundError:
            pass
        try:
            os.remove('Square.csv')
        except FileNotFoundError:
            pass
        with self.subTest():
            self.assertEqual(Rectangle.load_from_file_csv(), [])
        with self.subTest():
            self.assertEqual(Square.load_from_file_csv(), [])
        with open('Rectangle.csv', 'wt'):
            pass
        with open('Square.csv', 'wt'):
            pass
        with self.subTest():
            self.assertEqual(Rectangle.load_from_file_csv(), [])
        with self.subTest():
            self.assertEqual(Square.load_from_file_csv(), [])
        with open('Rectangle.csv', 'wt') as file:
            file.write('"90",1,2,3,4')
        with open('Square.csv', 'wt') as file:
            file.write('1,1,2,3')
        with self.subTest():
            r = Rectangle(1, 2, 3, 4, 90)
            o = Rectangle.load_from_file_csv()[0]
            self.assertEqual(r.to_dictionary(), o.to_dictionary())
        with self.subTest():
            s = Square(1, 2, 3, 1)
            o = Square.load_from_file_csv()[0]
            self.assertEqual(s.to_dictionary(), o.to_dictionary())
        with open('Rectangle.csv', 'at') as file:
            file.write('\n20,5,6,7,8')
        with open('Square.csv', 'at') as file:
            file.write('\n45,4,5,6')
        with self.subTest():
            r = [
                Rectangle(1, 2, 3, 4, 90),
                Rectangle(5, 6, 7, 8, 20)
            ]
            o = Rectangle.load_from_file_csv()
            for a, b in zip(r, o):
                self.assertEqual(a.to_dictionary(), b.to_dictionary())
        with self.subTest():
            s = [Square(1, 2, 3, 1), Square(4, 5, 6, 45)]
            o = Square.load_from_file_csv()
            for a, b in zip(s, o):
                self.assertEqual(a.to_dictionary(), b.to_dictionary())

    def test_FromJson(self):
        """Turning JSON strings into objects"""

        j = None
        with self.subTest():
            self.assertEqual(Base.from_json_string(j), [])
        j = ''
        with self.subTest():
            self.assertEqual(Base.from_json_string(j), [])
        j = '[]'
        with self.subTest():
            self.assertEqual(Base.from_json_string(j), [])
        j = '[{}]'
        with self.subTest():
            self.assertEqual(Base.from_json_string(j), [{}])
        j = '[{"a": 1, "b": 2}]'
        with self.subTest():
            self.assertEqual(Base.from_json_string(j), [{'a': 1, 'b': 2}])
        j = '[{"a": 1, "b": 2}, {"3": "c", "4": "d"}]'
        o = [{'a': 1, 'b': 2}, {'3': 'c', '4': 'd'}]
        with self.subTest():
            self.assertEqual(Base.from_json_string(j), o)

    def test_InitTooManyArgs(self):
        "Passing too many constructor arguments"""

        message = '__init__() takes from 1 to 2 positional arguments but 3 ' \
                  'were given'
        with self.assertRaises(TypeError, msg=message):
            Base(1, 2)

    def test_InitDefaultId(self):
        """Passing no arguments to the constructor"""

        obj = Base()
        self.assertIsInstance(obj, Base)
        self.assertEqual(obj.id, 1)
        obj2 = Base()
        self.assertEqual(obj2.id, 2)
        self.assertEqual(obj.id, 1)
        obj3 = Base('not none')
        self.assertNotEqual(obj3.id, 3)
        obj4 = Base()
        self.assertEqual(obj4.id, 3)

    def test_InitGivenId(self):
        """Passing a desired ID to the constructor"""

        obj = Base('str')
        self.assertEqual(obj.id, 'str')
        obj = Base(1000)
        self.assertEqual(obj.id, 1000)
        obj = Base([1, 2, 3])
        self.assertEqual(obj.id, [1, 2, 3])
        obj = Base(None)
        self.assertEqual(obj.id, 1)

    def test_Load(self):
        """Loading objects from a JSON file"""

        try:
            os.remove('Rectangle.json')
        except FileNotFoundError:
            pass
        try:
            os.remove('Square.json')
        except FileNotFoundError:
            pass
        with self.subTest():
            self.assertEqual(Rectangle.load_from_file(), [])
        with self.subTest():
            self.assertEqual(Square.load_from_file(), [])
        with open('Rectangle.json', 'wt') as file:
            pass
        with open('Square.json', 'wt') as file:
            pass
        with self.subTest():
            self.assertEqual(Rectangle.load_from_file(), [])
        with self.subTest():
            self.assertEqual(Square.load_from_file(), [])
        with open('Rectangle.json', 'wt') as file:
            file.write('[')
            file.write('{"width": 1, "height": 2, "x": 3, "y": 4, "id": "id"}')
            file.write(']')
        with open('Square.json', 'wt') as file:
            file.write('[{"size": 1, "x": 2, "y": 3, "id": "id"}]')
        with self.subTest():
            r = Rectangle(1, 2, 3, 4, 'id')
            o = Rectangle.load_from_file()[0]
            self.assertEqual(r.to_dictionary(), o.to_dictionary())
        with self.subTest():
            s = Square(1, 2, 3, 'id')
            o = Square.load_from_file()[0]
            self.assertEqual(s.to_dictionary(), o.to_dictionary())
        with open('Rectangle.json', 'r+t') as file:
            file.seek(54)
            file.write(', ')
            file.write('{"width": 5, "height": 6, "x": 7, "y": 8, "id": "ye"}')
            file.write(']')
        with open('Square.json', 'r+t') as file:
            file.seek(40)
            file.write(', {"size": 4, "x": 5, "y": 6, "id": "other"}]')
        with self.subTest():
            r = [Rectangle(1, 2, 3, 4, 'id'), Rectangle(5, 6, 7, 8, 'ye')]
            o = Rectangle.load_from_file()
            for a, b in zip(r, o):
                self.assertEqual(a.to_dictionary(), b.to_dictionary())
        with self.subTest():
            s = [Square(1, 2, 3, 'id'), Square(4, 5, 6, 'other')]
            o = Square.load_from_file()
            for a, b in zip(s, o):
                self.assertEqual(a.to_dictionary(), b.to_dictionary())

    def test_Save(self):
        """Saving JSON to a file"""

        try:
            os.remove('Rectangle.json')
        except FileNotFoundError:
            pass
        try:
            os.remove('Square.json')
        except FileNotFoundError:
            pass
        r1 = Rectangle(1, 2, 3, 4)
        r2 = Rectangle(5, 6, 7, 8)
        j = json.dumps([r1.to_dictionary(), r2.to_dictionary()])
        with self.subTest():
            Rectangle.save_to_file([r1, r2])
            with open('Rectangle.json', 'rt') as file:
                self.assertEqual(file.read(), j)
        with self.subTest():
            Rectangle.save_to_file(None)
            with open('Rectangle.json', 'rt') as file:
                self.assertEqual(file.read(), '[]')
        s1 = Square(10, 20, 30)
        s2 = Square(100, 200, 300)
        j = json.dumps([s1.to_dictionary(), s2.to_dictionary()])
        with self.subTest():
            Square.save_to_file([])
            with open('Square.json', 'rt') as file:
                self.assertEqual(file.read(), '[]')
        with self.subTest():
            Square.save_to_file([s1, s2])
            with open('Square.json', 'rt') as file:
                self.assertEqual(file.read(), j)

    def test_ToJson(self):
        """Converting a list to a JSON representation"""

        with self.subTest():
            self.assertEqual(Base.to_json_string(None), '[]')
        with self.subTest():
            self.assertEqual(Base.to_json_string([]), '[]')
        b = Base()
        j = [{'a': 1, 'b': 2}, {1: 'a', 2: 'b'}]
        with self.subTest():
            self.assertEqual(b.to_json_string(j), json.dumps(j))
        with self.subTest():
            self.assertEqual(Base.to_json_string(j), json.dumps(j))

#!/usr/bin/python3
"""Base class for all data models"""


import csv
import json
import os.path
import random
import turtle


class Base:
    """Methods and ID tracking used by all persistent classes"""

    __nb_objects = 0
    """Number of objects created with automatic ID"""

    def __init__(self, id=None):
        """Set up object ID, although this class isn't instantiated directly
        Args:
            id: used for object ID if not None; else number of objects used
        """

        if id is None:
            Base.__nb_objects += 1
            self.id = Base.__nb_objects
        else:
            self.id = id

    @classmethod
    def create(cls, **dictionary):
        """Return a new instance of a class from an attribute dictionary"""

        if cls.__name__ == 'Rectangle':
            obj = cls(1, 1)
        elif cls.__name__ == 'Square':
            obj = cls(1)
        obj.update(**dictionary)
        return obj

    @staticmethod
    def draw(list_rectangles, list_squares):
        """Draw shapes using graphics"""

        turtle.setheading(0)
        turtle.penup()
        for rect in list_rectangles + list_squares:
            turtle.color(tuple(random.random() for _ in range(3)))
            turtle.setposition(rect.x, rect.y)
            turtle.begin_fill()
            turtle.forward(rect.width)
            turtle.left(90)
            turtle.forward(rect.height)
            turtle.left(90)
            turtle.forward(rect.width)
            turtle.left(90)
            turtle.forward(rect.height)
            turtle.left(90)
            turtle.end_fill()

    @staticmethod
    def from_json_string(json_string):
        """Return a decoded JSON string"""

        if json_string is None or len(json_string) < 1:
            return []
        return json.loads(json_string)

    @classmethod
    def load_from_file(cls):
        """Load a list of instances from a JSON file"""

        if not os.path.exists(cls.__name__ + '.json'):
            return []
        with open(cls.__name__ + '.json', 'rt') as file:
            objects = cls.from_json_string(file.read())
        return [cls.create(**d) for d in objects]

    @classmethod
    def load_from_file_csv(cls):
        """Load a list of instances from a CSV table"""

        if not os.path.exists(cls.__name__ + '.csv'):
            return []
        if cls.__name__ == 'Rectangle':
            attrs = ('id', 'width', 'height', 'x', 'y')
        elif cls.__name__ == 'Square':
            attrs = ('id', 'size', 'x', 'y')
        with open(cls.__name__ + '.csv', 'rt', newline='') as file:
            reader = csv.reader(file)
            objects = list(reader)
        objects = ((int(i) for i in l) for l in objects)
        return [cls.create(**dict(zip(attrs, l))) for l in objects]

    @classmethod
    def save_to_file_csv(cls, list_objs):
        """Save a CSV version of the objects in list_objs for a class"""

        if list_objs is None:
            list_objs = []
        if cls.__name__ == 'Rectangle':
            attrs = ('id', 'width', 'height', 'x', 'y')
        elif cls.__name__ == 'Square':
            attrs = ('id', 'size', 'x', 'y')
        list_objs = ([getattr(o, a) for a in attrs] for o in list_objs)
        with open(cls.__name__ + '.csv', 'wt', newline='') as file:
            writer = csv.writer(file)
            for row in list_objs:
                writer.writerow(row)

    @classmethod
    def save_to_file(cls, list_objs):
        """Save a JSON string version of list_objs for the given class"""

        if list_objs is None:
            list_objs = []
        list_objs = [b.to_dictionary() for b in list_objs]
        list_objs = cls.to_json_string(list_objs)
        with open(cls.__name__ + '.json', 'wt') as file:
            file.write(list_objs)

    @staticmethod
    def to_json_string(list_dictionaries):
        """Return JSON string conversion of list_dictionaries"""

        if list_dictionaries is None or len(list_dictionaries) < 1:
            return '[]'
        return json.dumps(list_dictionaries)

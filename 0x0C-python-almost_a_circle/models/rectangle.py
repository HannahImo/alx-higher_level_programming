#!/usr/bin/python3
"""Rectangle data model"""


from models.base import Base


class Rectangle (Base):
    """A rectangle with position and size attributes"""

    def __init__(self, width, height, x=0, y=0, id=None):
        """Create a new complete rectangle
        Args:
            width (int): width
            height (int): height
            x (int): x coordinate
            y (int): y coordinate
            id: object ID
        """
        super().__init__(id)
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def __str__(self):
        """Return serializer-appropriate representation of this object"""

        return '[Rectangle] ({}) {}/{} - {}/{}'.format(
            self.id,
            self.x,
            self.y,
            self.width,
            self.height
        )

    def area(self):
        """Return the area of the rectangle"""

        return self.__width * self.__height

    def display(self):
        """Print rectangle using hash marks"""

        for _ in range(self.__y):
            print()
        for _ in range(self.__height):
            print(' ' * self.__x + '#' * self.__width)

    @property
    def height(self):
        """Get height
        The setter validates the height to be a positive integer
        """

        return self.__height

    @height.setter
    def height(self, value):
        if not isinstance(value, int):
            raise TypeError('height must be an integer')
        if value <= 0:
            raise ValueError('height must be > 0')
        self.__height = value

    def to_dictionary(self):
        """Return dictionary of this object's public attributes"""

        return {
            'id': self.id, 'width': self.width, 'height': self.height,
            'x': self.x, 'y': self.y
        }

    def update(self, *args, **kwargs):
        """Update this object's attributes
        Args:
            id
            width
            height
            x
            y
        """

        if len(args) > 0:
            attrs = ('id', 'width', 'height', 'x', 'y')
            for name, value in zip(attrs, args):
                setattr(self, name, value)
        else:
            self.id = kwargs.get('id', self.id)
            self.width = kwargs.get('width', self.width)
            self.height = kwargs.get('height', self.height)
            self.x = kwargs.get('x', self.x)
            self.y = kwargs.get('y', self.y)

    @property
    def width(self):
        """Get width
        The setter validates the width to be a positive integer
        """

        return self.__width

    @width.setter
    def width(self, value):
        if not isinstance(value, int):
            raise TypeError('width must be an integer')
        if value <= 0:
            raise ValueError('width must be > 0')
        self.__width = value

    @property
    def x(self):
        """Get x position
        The setter validates this to be an integer and >= 0
        """

        return self.__x

    @x.setter
    def x(self, value):
        if not isinstance(value, int):
            raise TypeError('x must be an integer')
        if value < 0:
            raise ValueError('x must be >= 0')
        self.__x = value

    @property
    def y(self):
        """Get y position
        The setter validates this to be an integer and >= 0
        """

        return self.__y

    @y.setter
    def y(self, value):
        if not isinstance(value, int):
            raise TypeError('y must be an integer')
        if value < 0:
            raise ValueError('y must be >= 0')
        self.__y = value

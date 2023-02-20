#!/usr/bin/python3
"""Class to define a rectangle as a kind of square"""


from models.rectangle import Rectangle


class Square (Rectangle):
    """A Square based on a rectangle"""

    def __init__(self, size, x=0, y=0, id=None):
        """Initialize a square object
        Args:
            size (int): length of the square's sides
            x (int): X coordinate of the square
            y (int): Y coordinate of the square
            id: object's ID
        """

        super().__init__(size, size, x, y, id)

    def __str__(self):
        """Return a representation of this object's attributes"""

        return '[Square] ({}) {}/{} - {}'.format(
            self.id,
            self.x,
            self.y,
            self.size
        )

    @property
    def size(self):
        """Return the length of this square's sides
        The setter does the same validation as Rectangle.width
        """

        return self.width

    @size.setter
    def size(self, value):
        self.width = value
        self.height = value

    def to_dictionary(self):
        """Return this object's public attributes as a dictionary"""

        return {'id': self.id, 'size': self.size, 'x': self.x, 'y': self.y}

    def update(self, *args, **kwargs):
        """Update this object's attributes
        Args:
            id
            size
            x
            y
        """

        if len(args) > 0:
            attrs = ('id', 'size', 'x', 'y')
            for name, value in zip(attrs, args):
                setattr(self, name, value)
        else:
            self.id = kwargs.get('id', self.id)
            self.size = kwargs.get('size', self.size)
            self.x = kwargs.get('x', self.x)
            self.y = kwargs.get('y', self.y)

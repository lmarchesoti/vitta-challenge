# -*- coding: utf-8 -*-

import mongoengine as me

class Square(me.Document):
  """ Defines a point on the map. """

  x = me.IntField(required=True)
  y = me.IntField(required=True)
  painted = me.BooleanField(default=False)

  @staticmethod
  def generate_squares(start, end):

    left  = min(start['x'], end['x'])
    right = max(start['x'], end['x'])
    down  = min(start['y'], end['x'])
    up    = max(start['x'], end['x'])

    squares = []

    for x in range(right):

      for y in range(up):
        s = Square(x=left+x, y=down+y, painted=False)
        s.save()

        squares.append(s)

    return squares

  def serialize(self):

    return {
      'x': self.x,
      'y': self.y,
      'painted': self.painted
    }


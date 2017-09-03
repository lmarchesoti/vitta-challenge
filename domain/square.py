# -*- coding: utf-8 -*-

import datetime

import mongoengine as me

class Square(me.Document):
  """ Defines a point on the map. """

  x = me.IntField(required=True)
  y = me.IntField(required=True)
  painted = me.BooleanField(default=False)
  last_update = me.DateTimeField()

  @staticmethod
  def generate_squares(start, end):
    """ Generates the necessary squares for a territory's boundaries. """

    left  = min(start['x'], end['x'])
    right = max(start['x'], end['x'])
    down  = min(start['y'], end['y'])
    up    = max(start['y'], end['y'])

    squares = []

    for x in range(right-left+1):

      for y in range(up-down+1):
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

  def clean(self):
    """ Sets update time. """

    self.last_update = datetime.datetime.now()

def last_painted_squares(n):
  """ Retrieves the n last painted squares. """

  return Square.objects(painted=True).order_by('-last_update')[0:n]

# -*- coding: utf-8 -*-

import mongoengine as me
from mongoengine.queryset.visitor import Q

class Territory(me.Document):
  """ Implements a territory. """

  id = me.SequenceField(primary_key=True)
  name = me.StringField(required=True)
  start = me.DictField(required=True)
  end = me.DictField(required=True)
  area = me.FloatField(default=0.)
  painted_area = me.IntField(default=0)

  def clean(self):
    """
    Invalidates insert of overlapping territory.
    Calculates derived attributes.
    """

    if self.overlapping_territories():
      raise me.ValidationError('Overlapping territory')

    self.area = self.calculate_area()

    self.painted_area = self.calculate_painted_area()

  def overlapping_territories(self):
    """
    Determines if there is another registered territory overlapping this
    location.
    Two territories do NOT overlap if one is totally to the left/right/
    up/down of the other.
    """

    self_left  = min(self.start['x'], self.end['x'])
    self_right = max(self.start['x'], self.end['x'])
    self_down  = min(self.start['y'], self.end['y'])
    self_up    = max(self.start['y'], self.end['y'])

    for t in Territory.objects:

      t_left  = min(t.start['x'], t.end['x'])
      t_right = max(t.start['x'], t.end['x'])
      t_down  = min(t.start['y'], t.end['y'])
      t_up    = max(t.start['y'], t.end['y'])

      overlap = not ((self_left > t_right) or (self_right < t_left)
		  or (self_up   < t_down ) or (self_down  > t_up  ))

      if overlap:
        return True

    return False

  def calculate_area(self):
    """ Find total area. """

    delta_x = abs(self.start['x'] - self.end['x'])
    delta_y = abs(self.start['y'] - self.end['y'])

    return delta_x * delta_y

  def calculate_painted_area(self):
    """ Find total painted area. """

    return 0

  def serialize(self):

    return {
	    'id': str(self.id),
	    'name': self.name,
	    'start': self.start,
	    'end': self.end,
	    'area': self.area,
	    'painted_area': self.painted_area
	   }

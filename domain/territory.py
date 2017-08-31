# -*- coding: utf-8 -*-

import mongoengine as me

class Territory(me.Document):
  """ Implements a territory. """

  #id = me.SequenceField(primary_key=True)
  name = me.StringField(required=True)
  start = me.DictField(required=True)
  end = me.DictField(required=True)
  #start = me.PointField(required=True)
  #end = me.PointField(required=True)
  area = me.FloatField(default=0.)
  painted_area = me.IntField(default=0)

  def clean(self):
    """
    Invalidates insert of overlapping territory.
    Calculates derived attributes.
    """

    overlapping = self.overlapping_territories()
    if len(overlapping) > 0:
      raise LookupError('Overlapping territory')

    self.area = self.calculate_area()

    self.painted_area = self.calculate_painted_area()

  def overlapping_territories(self):
    """
    Finds overlapping territories in database.
    An overlapping area has at least one of its four corners inside the
    x and y ranges of the territory.
    """

    #lower_left_x = min(self.start['x'], self.end['x'])
    #lower_left_y = min(self.start['y'], self.end['y'])
    #upper_right_x = max(self.start['x'], self.end['x'])
    #upper_right_x = max(self.start['y'], self.end['y'])

    overlap = []

    #for t in Territory.objects:
      #if t.start

    # corner 1
    #c1 = Territory.objects(start__x__gt = lower_left_x,
			   #start__x__

    # corner 2

    # corner 3

    # corner 4

    # remove duplicates
    return overlap

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

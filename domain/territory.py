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
    
    #for t in Territory.objects:
    # overlapping territories

    #overlapping = Territory.objects(start__x__gt = self.
				    
      

    self.area = self.calculate_area()

    self.painted_area = self.calculate_painted_area()

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
	    #'id': self.id,
	    'name': self.name,
	    'start': self.start,
	    'end': self.end,
	    'area': self.area,
	    'painted_area': self.painted_area
	   }

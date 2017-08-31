# -*- coding: utf-8 -*-

import math
import mongoengine as me

class POI(me.Document):
  """ Implements a point of interest. """

  name = me.StringField(required=True)
  point = me.PointField(required=True)

  def __str__(self):

    return ("'" + self.name
      + "' (x=" + str(self.point['coordinates'][0])
      +  ", y=" + str(self.point['coordinates'][1]) + ")")

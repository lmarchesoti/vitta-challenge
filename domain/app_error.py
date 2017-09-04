# -*- coding: utf-8 -*-

import datetime

import mongoengine as me

class AppError(me.Document):

  type = me.StringField(required=True)
  timestamp = me.DateTimeField()

  def clean(self):
    """ Sets occurrence time. """

    self.timestamp = datetime.datetime.now()

  def serialize(self):

    return str(self.type)

def last_errors(n):

  return AppError.objects.order_by('-timestamp')[0:n]

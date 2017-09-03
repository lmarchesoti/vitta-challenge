# -*- coding: utf-8 -*-

from domain import territory, square

def territories_by_painted_area():

  sorted_territories = territory.territories_by_painted_area()

  html = '<ol>'

  for t in sorted_territories:
    html += '<li>' + str(t.serialize()) + '</li>'

  html += '</ol>'

  return html 

def territories_by_proportional_painted_area():

  sorted_territories = territory.territories_by_proportional_painted_area()

  html = '<ol>'

  for t in sorted_territories:
    html += '<li>' + str(t.serialize()) + '</li>'

  html += '</ol>'

  return html 

def last_painted_squares(n):

  squares = square.last_painted_squares(n)

  html = '<ol>'

  for s in squares:
    html += '<li>' + str(s.serialize()) + '</li>'

  html += '</ol>'

  return html

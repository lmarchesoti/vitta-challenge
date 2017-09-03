# -*- coding: utf-8 -*-

from domain import territory

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

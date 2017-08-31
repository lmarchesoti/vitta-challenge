# -*- coding: utf-8 -*-

import json
import unittest

import app

class TestTerritories(unittest.TestCase):

  def setUp(self):
    app.app.testing = True
    self.app = app.app.test_client()

  def test_create_territory(self):

    insert_data = { 
		    "name": "A",
		    "start": { "x":  0, "y":  0},
		    "end"  : { "x": 50, "y": 50}
		  }

    rv = self.app.post('/territories', data=json.dumps(insert_data),
		       content_type='application/json')

    resp =  {
	      "data": {
		"id": 1,
		"name": "A",
		"start": { "x": 0, "y": 0 },
		"end": { "x": 50, "y": 50 },
		"area": 2500,
		"painted_area": 0
	      },
	      "error": False
	    }

    self.assertEquals(json.loads(rv.data), resp)

#  def test_list_pois(self):
#
#    try:
#      p1 = poi.POI(name='lanchonete', point=(0, 2))
#      p1.save()
#
#      p2 = poi.POI(name='lavanderia', point=(7, 3))
#      p2.save()
#
#      ans = b"""'lanchonete' (x=0, y=2)\n'lavanderia' (x=7, y=3)\n"""
#
#      rv = self.app.get('/')
#      self.assertEquals(rv.data, ans)
#
#    finally:
#      self.delete_all_pois()
#
#  def test_create_poi(self):
#
#    try:
#      self.app.post('/', data={'name': 'Posto', 'x': 31, 'y': 18})
#      self.app.post('/', data={'name': 'Joalheria', 'x': 15, 'y': 12})
#
#      pois = poi.POI.objects.order_by('name')
#
#      with self.subTest():
#        self.assertEquals(str(pois[0]), "'Joalheria' (x=15, y=12)")
#      with self.subTest():
#        self.assertEquals(str(pois[1]), "'Posto' (x=31, y=18)")
#
#    finally:
#      self.delete_all_pois()
#
#  def test_filter_pois(self):
#
#    try:
#
#      poi.POI(name='Lanchonete', point=(27, 12)).save()
#      poi.POI(name='Posto', point=(31, 18)).save()
#      poi.POI(name='Joalheria', point=(15, 12)).save()
#      poi.POI(name='Floricultura', point=(19, 21)).save()
#      poi.POI(name='Pub', point=(12, 8)).save()
#      poi.POI(name='Supermercado', point=(23, 6)).save()
#      poi.POI(name='Churrascaria', point=(28, 2)).save()
#
#      rv = self.app.get('/?x=20&y=10&dmax=10')
#
#      ans = b"'Lanchonete' (x=27, y=12)\n'Joalheria' (x=15, y=12)\n'Pub' (x=12, y=8)\n'Supermercado' (x=23, y=6)\n"
#
#      self.assertEquals(rv.data, ans)
#
#    finally:
#      self.delete_all_pois()
#
#  def delete_all_pois(self):
#    for p in poi.POI.objects:
#      p.delete()

if __name__ == '__main__':
  unittest.main()

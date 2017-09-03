# -*- coding: utf-8 -*-

import os

import json
import unittest

import app

from domain import territory, square

class TestTerritories(unittest.TestCase):

  def setUp(self):
    app.app.testing = True
    self.app = app.app.test_client()

  def tearDown(self): self.delete_all_territories()

  def delete_all_territories(self):
    for p in territory.Territory.objects:
      p.delete()

  def test_create_territory(self):

    insert_data = { 
		    "name": "A",
		    "start": { "x":  0, "y":  0},
		    "end"  : { "x": 50, "y": 50}
		  }

    rv = self.app.post('/territories', data=json.dumps(insert_data),
		       content_type='application/json')
    item_id = json.loads(rv.data)['data']['id']

    resp =  {
	      "data": {
		"id": item_id,
		"name": "A",
		"start": { "x": 0, "y": 0 },
		"end": { "x": 50, "y": 50 },
		"area": 2500,
		"painted_area": 0
	      },
	      "error": False
	    }

    self.assertEquals(json.loads(rv.data), resp)

  def test_create_territory_incomplete_data(self):

    insert_data = { 
		    #"name": "A",
		    "start": { "x":  0, "y":  0},
		    "end"  : { "x": 50, "y": 50}
		  }

    rv = self.app.post('/territories', data=json.dumps(insert_data),
		       content_type='application/json', follow_redirects=True)

    self.assertEquals(b'Incomplete data\n', rv.data)

  def test_create_territory_overlapping(self):

    insert_data_1 = { 
		    "name": "A",
		    "start": { "x":  0, "y":  0},
		    "end"  : { "x": 50, "y": 50}
		  }

    insert_data_2 = { 
		    "name": "B",
		    "start": { "x":  1, "y": 20},
		    "end"  : { "x": 70, "y": 30}
		  }

    rv = self.app.post('/territories', data=json.dumps(insert_data_1),
		       content_type='application/json')
    rv = self.app.post('/territories', data=json.dumps(insert_data_2),
		       content_type='application/json',
		       follow_redirects=True)

    self.assertTrue(b'Overlapping Territories\n' in rv.data)

  def test_list_territories(self):

    insert_data_1 = { 
		    "name": "A",
		    "start": { "x":  0, "y":  0},
		    "end"  : { "x": 50, "y": 50}
		  }

    insert_data_2 = { 
		    "name": "B",
		    "start": { "x": 70, "y": 70},
		    "end"  : { "x": 90, "y": 90}
		  }
    
    rv = self.app.post('/territories', data=json.dumps(insert_data_1),
		       content_type='application/json')
    item_id_1 = json.loads(rv.data)['data']['id']
    rv = self.app.post('/territories', data=json.dumps(insert_data_2),
		       content_type='application/json')
    item_id_2 = json.loads(rv.data)['data']['id']

    rv = self.app.get('/territories')

    resp = {
	    'count': 2,
	    'data': [
		  {
		    "id": item_id_1,
		    "name": "A",
		    "start": { "x": 0, "y": 0 },
		    "end": { "x": 50, "y": 50 },
		    "area": 2500,
		    "painted_area": 0
		  },
		  {
		    "id": item_id_2,
		    "name": "B",
		    "start": { "x": 70, "y": 70 },
		    "end": { "x": 90, "y": 90 },
		    "area": 400,
		    "painted_area": 0
		  }
		]
	    }

    self.assertEquals(json.loads(rv.data), resp)

  def test_delete_and_not_found(self):

    insert_data = { 
		    "name": "A",
		    "start": { "x":  0, "y":  0},
		    "end"  : { "x": 50, "y": 50}
		  }
    
    rv = self.app.post('/territories', data=json.dumps(insert_data),
		       content_type='application/json')
    item_id = json.loads(rv.data)['data']['id']

    rv_delete = self.app.delete('/territories/%s' % item_id)

    with self.subTest():
      delete_response = { 'error': False }
      self.assertEquals(delete_response, json.loads(rv_delete.data))

    with self.subTest():
      rv = self.app.get('/territories/%s' % item_id, follow_redirects=True)
      self.assertEquals(b'Territory not found\n', rv.data)

  def test_delete_fail(self):

    rv = self.app.delete('/territories/3', follow_redirects=True)

    self.assertEquals(b'Territory not found\n', rv.data)
    

  def test_find_single(self):

    insert_data_1 = { 
		    "name": "A",
		    "start": { "x":  0, "y":  0},
		    "end"  : { "x": 50, "y": 50}
		  }

    insert_data_2 = { 
		    "name": "B",
		    "start": { "x": 70, "y": 70},
		    "end"  : { "x": 90, "y": 90}
		  }
    
    rv = self.app.post('/territories', data=json.dumps(insert_data_1),
		       content_type='application/json')
    item_id = json.loads(rv.data)['data']['id']

    rv = self.app.post('/territories', data=json.dumps(insert_data_2),
		       content_type='application/json')

    rv = self.app.get('/territories/%s' % item_id)

    resp = {
	    'data': 
		  {
		    "id": item_id,
		    "name": "A",
		    "start": { "x": 0, "y": 0 },
		    "end": { "x": 50, "y": 50 },
		    "area": 2500,
		    "painted_area": 0
		  },
	    'error': False
	    }

    self.assertEquals(json.loads(rv.data), resp)

class TestSquares(unittest.TestCase):

  def setUp(self):
    app.app.testing = True
    self.app = app.app.test_client()

  def tearDown(self): self.delete_all_territories()

  def delete_all_territories(self):
    for p in territory.Territory.objects:
      p.delete()

  def test_status_of_square(self):

    t = territory.Territory(name='a', start={'x': 0, 'y': 0}, end={'x': 50, 'y': 50})
    t.save()

    x, y = 1, 2
    rv = self.app.get('/squares/%s/%s' % (x, y))

    ans = {
	"data": {
	  "x": 1,
	  "y": 2,
	  "painted": False  
	},
	"error": False
      }

    self.assertEquals(json.loads(rv.data), ans)

  def test_square_not_found_on_find(self):

    t = territory.Territory(name='a', start={'x': 0, 'y': 0}, end={'x': 50, 'y': 50})
    t.save()

    x, y = 70, 2
    rv = self.app.get('/squares/%s/%s' % (x, y), follow_redirects=True)

    self.assertEquals(b'Square not found\n', rv.data)

  def test_paint_square(self):

    t = territory.Territory(name='a', start={'x': 0, 'y': 0}, end={'x': 50, 'y': 50})
    t.save()

    x, y = 1, 2
    rv = self.app.patch('/squares/%s/%s/paint' % (x, y))

    ans = {
	"data": {
	  "x": 1,
	  "y": 2,
	  "painted": True
	},
	"error": False
      }

    self.assertEquals(json.loads(rv.data), ans)

  def test_square_not_found_on_paint(self):

    t = territory.Territory(name='a', start={'x': 0, 'y': 0}, end={'x': 50, 'y': 50})
    t.save()

    x, y = 70, 2
    rv = self.app.patch('/squares/%s/%s/paint' % (x, y), follow_redirects=True)

    self.assertEquals(b'Square not found\n', rv.data)

  def test_list_painted_squares(self):

    insert_data = { 
		    "name": "A",
		    "start": { "x":  0, "y":  0},
		    "end"  : { "x": 50, "y": 50}
		  }

    rv = self.app.post('/territories', data=json.dumps(insert_data),
		       content_type='application/json')
    item_id = json.loads(rv.data)['data']['id']


    x, y = 1, 2
    self.app.patch('/squares/%s/%s/paint' % (x, y))
    x, y = 2, 3
    self.app.patch('/squares/%s/%s/paint' % (x, y))

    rv = self.app.get('/territories/%s?withpainted=true' % item_id)

    ans ={
	"data": {
	  "id": item_id,
	  "name": "A",
	  "start": { "x": 0, "y": 0 },
	  "end": { "x": 50, "y": 50 },
	  "area": 2500,
	  "painted_area": 2,
	  "painted_squares": [
	    { "x": 1, "y": 2 },
	    { "x": 2, "y": 3 }
	  ]
	},
	"error": False
      }

    self.assertEquals(json.loads(rv.data), ans)

  def test_square_not_found_with_painted(self):

    rv = self.app.get('/territories/%s?withpainted=true' % 13, follow_redirects=True)

    self.assertEquals(b'Territory not found\n', rv.data)

class TestDashboard(unittest.TestCase):

  def setUp(self):
    app.app.testing = True
    self.app = app.app.test_client()

  def tearDown(self): self.delete_all_territories()

  def delete_all_territories(self):
    for p in territory.Territory.objects:
      p.delete()

  def test_main_dashboard(self):

    # issue commands
    insert_data = { 
		    "name": "A",
		    "start": { "x": 0, "y": 0},
		    "end"  : { "x": 4, "y": 4}
		  }
    self.app.post('/territories', data=json.dumps(insert_data),
		       content_type='application/json')
    insert_data = { 
		    "name": "B",
		    "start": { "x": 0, "y": 5},
		    "end"  : { "x": 4, "y": 9}
		  }
    self.app.post('/territories', data=json.dumps(insert_data),
		       content_type='application/json')
    insert_data = { 
		    "name": "C",
		    "start": { "x": 5, "y": 0},
		    "end"  : { "x": 9, "y": 9}
		  }
    self.app.post('/territories', data=json.dumps(insert_data),
		       content_type='application/json')

    x, y = 3, 1
    self.app.patch('/squares/%s/%s/paint' % (x, y))
    x, y = 5, 0
    self.app.patch('/squares/%s/%s/paint' % (x, y))
    x, y = 6, 0
    self.app.patch('/squares/%s/%s/paint' % (x, y))
    x, y = 7, 0
    self.app.patch('/squares/%s/%s/paint' % (x, y))
    x, y = 8, 0
    self.app.patch('/squares/%s/%s/paint' % (x, y))
    x, y = 9, 0
    self.app.patch('/squares/%s/%s/paint' % (x, y))
    x, y = 5, 1
    self.app.patch('/squares/%s/%s/paint' % (x, y))
    x, y = 10, 10
    self.app.patch('/squares/%s/%s/paint' % (x, y))
    x, y = 0, 9
    self.app.patch('/squares/%s/%s/paint' % (x, y))
    x, y = 1, 9
    self.app.patch('/squares/%s/%s/paint' % (x, y))
    x, y = 2, 9
    self.app.patch('/squares/%s/%s/paint' % (x, y))
    x, y = 3, 9
    self.app.patch('/squares/%s/%s/paint' % (x, y))
    x, y = 4, 9
    self.app.patch('/squares/%s/%s/paint' % (x, y))

    self.app.get('/territories/999')

    x, y = 11, 11
    self.app.patch('/squares/%s/%s/paint' % (x, y))

    insert_data = { 
		    "name": "D",
		    "start": { "x": 7, "y": 0},
		    "end"  : { "x": 9, "y": 6}
		  }
    self.app.post('/territories', data=json.dumps(insert_data),
		       content_type='application/json')

    insert_data = { 
		    "name": "D",
		    "end"  : { "x": 9, "y": 6}
		  }
    self.app.post('/territories', data=json.dumps(insert_data),
		       content_type='application/json')

    # access dashboard
    rv = self.app.get('/dashboard')

    # compare answer
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_app', 'dashboard.html'), 'r') as f:
      ans = f.read()

    print(rv.data)

    with self.subTest(): # painted area

      ordered_territories = [
	{ 'id': '3',
	  'name': 'C',
	  'start': {'x': 5, 'y': 0},
	  'end': {'x': 9, 'y': 9},
	  'area': 50.0,
	  'painted_area': 6
	},
	{ 'id': '2',
	  'name': 'B',
	  'start': {'x': 0, 'y': 5},
	  'end': {'x': 4, 'y': 9},
	  'area': 25.0,
	  'painted_area': 5
	},
	{ 'id': '1',
	  'name': 'A',
	  'start': {'x': 0, 'y': 0},
	  'end': {'x': 4, 'y': 4},
	  'area': 25.0,
	  'painted_area': 1
	},
      ]
      ret = [t.serialize() for t in territory.territories_by_painted_area()]
      self.assertEquals(ordered_territories, ret)

    with self.subTest(): # proportional painted area

      ordered_territories = [
	{ 'id': '2',
	  'name': 'B',
	  'start': {'x': 0, 'y': 5},
	  'end': {'x': 4, 'y': 9},
	  'area': 25.0,
	  'painted_area': 5
	},
	{ 'id': '3',
	  'name': 'C',
	  'start': {'x': 5, 'y': 0},
	  'end': {'x': 9, 'y': 9},
	  'area': 50.0,
	  'painted_area': 6
	},
	{ 'id': '1',
	  'name': 'A',
	  'start': {'x': 0, 'y': 0},
	  'end': {'x': 4, 'y': 4},
	  'area': 25.0,
	  'painted_area': 1
	},
      ]

      ret = [t.serialize() for t in territory.territories_by_proportional_painted_area()]
      self.assertEquals(ordered_territories, ret)

    with self.subTest(): # total painted / area

      ans = .12
      ret = territory.total_proportional_painted_area()

      self.assertEquals(ans, ret)

    with self.subTest(): # last 5 painted squares

      painted_squares = [
	{'x': 4, 'y': 9, 'painted': True},
	{'x': 3, 'y': 9, 'painted': True},
	{'x': 2, 'y': 9, 'painted': True},
	{'x': 1, 'y': 9, 'painted': True},
	{'x': 0, 'y': 9, 'painted': True},
      ]

      ret = [s.serialize() for s in square.last_painted_squares(5)]
      self.assertEquals(painted_squares, ret)

    with self.subTest(): # last 5 errors

      pass

if __name__ == '__main__':
  unittest.main()

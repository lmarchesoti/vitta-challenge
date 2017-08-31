# -*- coding: utf-8 -*-

import unittest

from xyinc import poi

class TestPOI(unittest.TestCase):

  def test_poi_repr(self):

    p = poi.POI(name='lanchonete',
	        point={'type': 'Point', 'coordinates': [1, 4]})

    ans = "'lanchonete' (x=1, y=4)"

    self.assertEquals(str(p), ans)


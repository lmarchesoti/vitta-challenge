from flask import Flask, request
import mongoengine as me

from xyinc import poi

app = Flask(__name__)

me.connect('xyinc', host='mongodb://mongo', port=27017)

@app.route('/', methods=['GET'])
def list():
  """ 
  Lista todos os POIs dentro do limite especificado.
  Se não houver parâmetros, lista todos os POIs.
  """

  x = request.args.get('x', type=int)
  y = request.args.get('y', type=int)
  dmax = request.args.get('dmax', type=int)

  # Distance-based search
  if (x is not None) and (y is not None) and (dmax is not None):
    pois = poi.POI.objects(point__geo_within_center=[(x, y), dmax])

  else: # List all POIs
    pois = poi.POI.objects

  # Imprime POIs na resposta
  resp = ''
  for p in pois:
    resp += str(p)
    resp += '\n'

  return resp

@app.route('/', methods=['POST'])
def create():
  """ Cria um POI. """

  p = poi.POI(name=request.form['name'],
	      point={'type': 'Point',
		     'coordinates': [int(request.form['x']), int(request.form['y'])]})
  p.save()
  return str(p)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)

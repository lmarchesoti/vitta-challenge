from flask import Flask, request, jsonify, redirect, url_for
import mongoengine as me

#from xyinc import poi
from domain import territory, square
import view_helper as vh

app = Flask(__name__)

me.connect('vitta-challenge', host='mongodb://mongo', port=27017)

@app.route('/', methods=['GET'])
def root_get(): pass

# territories
@app.route('/territories', methods=['POST'])
def create_territory():
  """ Creates a new territory and its related squares. """

  try:
    data = request.get_json()

    name = data['name']
    start = data['start']
    end = data['end']

    t = territory.Territory(name=name, start=start, end=end)
    t.save()

    return jsonify(data=t.serialize(), error=False)

  except KeyError:
    return redirect(url_for('static', filename='territories/incomplete-data.html'))

  except me.ValidationError:
    return redirect(url_for('static', filename='territories/territory-overlay.html'))
  
@app.route('/territories', methods=['GET'])
def list():

  tlist = territory.Territory.objects 

  return jsonify(count=len(tlist), data=[t.serialize() for t in tlist])

@app.route('/territories/<_id>', methods=['DELETE'])
def delete(_id):

  try:
    obj = territory.Territory.objects(id=_id)[0]
    obj.delete()

    return jsonify(error=False)

  except IndexError:
    return redirect(url_for('static', filename='territories/not-found.html'))

@app.route('/territories/<_id>', methods=['GET'])
def find(_id):

  try:

    withpainted = request.args.get('withpainted')
    if withpainted == 'true':
      include_squares = True

    else:
      include_squares = False

    obj = territory.Territory.objects(id=_id)[0].serialize(include_squares=include_squares)

    return jsonify(data=obj, error=False)

  except IndexError:
    return redirect(url_for('static', filename='territories/not-found.html'))

# squares
@app.route('/squares/<x>/<y>', methods=['GET'])
def find_square(x, y):

  try:
    obj = square.Square.objects(x=x, y=y)[0].serialize()

    return jsonify(data=obj, error=False)

  except IndexError:
    return redirect(url_for('static', filename='squares/not-found.html'))

@app.route('/squares/<x>/<y>/paint', methods=['PATCH'])
def paint_square(x, y):

  try:
    obj = square.Square.objects(x=x, y=y)[0]

    obj.painted = True
    obj.save()

    return jsonify(data=obj.serialize(), error=False)

  except IndexError:
    return redirect(url_for('static', filename='squares/not-found.html'))

@app.route('/dashboard', methods=['GET'])
def dashboard():

  html = '<html><head></head><body>'

  html += '<p> Territories by most painted area: <br/>'
  html += vh.territories_by_painted_area()
  html += '</p>'

  html += '<p> Territories by most proportional painted area: <br/>'
  html += vh.territories_by_proportional_painted_area()
  html += '</p>'

  # last 5 painted

  # last 5 errors

  html += '<p> Painted area / total area of all territories: '
  html += str(territory.total_proportional_painted_area())
  html += '</p>'

  html += '</body></html>'

  return html

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)

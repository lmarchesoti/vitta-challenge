from flask import Flask, request, jsonify, redirect, url_for
import mongoengine as me

#from xyinc import poi
from domain import territory, square, app_error
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
    e = app_error.AppError(type='territories/incomplete-data')
    e.save()
    return redirect(url_for('static', filename='territories/incomplete-data.html'))

  except me.ValidationError:
    e = app_error.AppError(type='territories/territory-overlay')
    e.save()
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
    e = app_error.AppError(type='territories/not-found')
    e.save()
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
    e = app_error.AppError(type='territories/not-found')
    e.save()
    return redirect(url_for('static', filename='territories/not-found.html'))

# squares
@app.route('/squares/<x>/<y>', methods=['GET'])
def find_square(x, y):

  try:
    obj = square.Square.objects(x=x, y=y)[0].serialize()

    return jsonify(data=obj, error=False)

  except IndexError:
    e = app_error.AppError(type='squares/not-found')
    e.save()
    return redirect(url_for('static', filename='squares/not-found.html'))

@app.route('/squares/<x>/<y>/paint', methods=['PATCH'])
def paint_square(x, y):

  try:
    obj = square.Square.objects(x=x, y=y)[0]

    obj.painted = True
    obj.save()

    return jsonify(data=obj.serialize(), error=False)

  except IndexError:
    e = app_error.AppError(type='squares/not-found')
    e.save()
    return redirect(url_for('static', filename='squares/not-found.html'))

@app.route('/dashboard', methods=['GET'])
def dashboard():

  html = '<html><head></head><body>'

  # Territories by most painted area
  html += '<p> Territories by most painted area: '
  html += vh.territories_by_painted_area()
  html += '</p>'

  # Territories by proportional painted area
  html += '<p> Territories by most proportional painted area: '
  html += vh.territories_by_proportional_painted_area()
  html += '</p>'

  # last 5 painted
  html += '<p> Last 5 painted squares: '
  html += vh.last_painted_squares(5)
  html += '</p>'

  # last 5 errors
  html += '<p> Last 5 errors: '
  html += vh.last_errors(5)
  html += '</p>'

  # Painted area / total area of all territories
  html += '<p> Painted area / total area of all territories: '
  html += '%.2f' % (territory.total_proportional_painted_area())
  html += '</p>'

  html += '</body></html>'

  return html

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)

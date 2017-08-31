from flask import Flask, request, jsonify, redirect, url_for
import mongoengine as me

#from xyinc import poi
from domain import territory

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

  except LookupError:
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
    obj = territory.Territory.objects(id=_id)[0].serialize()

    return jsonify(data=obj, error=False)

  except IndexError:
    return redirect(url_for('static', filename='territories/not-found.html'))

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)

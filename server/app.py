# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    try:
        quake = db.session.get(Earthquake, id)
        if quake:

            return jsonify({
                "id": quake.id,
                "location": quake.location,
                "magnitude": quake.magnitude,
                "year": quake.year
            })
        else:
            return jsonify({ "message": f"Earthquake {id} not found."}), 404
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_magnitude(magnitude):
    # get all earthquakes having a magnitude greater than or equal to the parameter value,
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    quake_data = [
        {
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }
        for quake in quakes
    ]
    return jsonify({
        "count": len(quake_data),
        "quakes": quake_data
    })

if __name__ == '__main__':
    app.run(port=5555, debug=True)

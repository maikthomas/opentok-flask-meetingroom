from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

from opentok import MediaModes, OpenTok

import config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
CORS(app)
opentok = OpenTok(config.OPENTOK_API_KEY, config.OPENTOK_SECRET)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    session_id = db.Column(db.String(72), unique=True)
    expiry_date = db.Column(db.DateTime)

    def __init__(self, name):
        self.name = name
        session = opentok.create_session(media_mode=MediaModes.routed)
        self.session_id = session.session_id
        self.expiry_date = datetime.now() + timedelta(days=1)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/room/<room_name>", methods=['GET', 'OPTIONS'])
def room(room_name):
    import pdb; pdb.set_trace()
    room = Room.query.filter_by(name=room_name).first()
    if not room:
        room = Room(name=room_name)
        db.session.add(room)
        db.session.commit()

    session_id = room.session_id
    token = opentok.generate_token(session_id)
    return render_template("room.html", apikey=config.OPENTOK_API_KEY,
                    sessionid=session_id, token=token)




if __name__ == "__main__":
    app.run()

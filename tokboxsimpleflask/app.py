import config
from flask import Flask, g, json, jsonify
from flask_cors import CORS
from opentok import MediaModes, OpenTok

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/session", methods=['GET', 'OPTIONS'])
def session():
    opentok = OpenTok(config.OPENTOK_API_KEY, config.OPENTOK_SECRET)
    session = g.get('session')
    if not session:
            session = opentok.create_session(media_mode=MediaModes.routed)
            g.session = session

    token = session.generate_token()

    session_data = {
        "sessionId": session.session_id,
        "apiKey": config.OPENTOK_API_KEY,
        "token": token
    }

    return jsonify(**session_data)


if __name__ == "__main__":
    app.run()

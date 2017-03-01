from flask import Flask, jsonify
from flask_cors import CORS

from opentok import MediaModes, OpenTok

import config

app = Flask(__name__)
CORS(app)
opentok = OpenTok(config.OPENTOK_API_KEY, config.OPENTOK_SECRET)
opensession = opentok.create_session(media_mode=MediaModes.routed)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/session", methods=['GET', 'OPTIONS'])
def session():
    token = opensession.generate_token()

    session_data = {
        "sessionId": opensession.session_id,
        "apiKey": config.OPENTOK_API_KEY,
        "token": token
    }

    return jsonify(**session_data)


if __name__ == "__main__":
    app.run()

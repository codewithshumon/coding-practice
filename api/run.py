"""Development server entry point.

Usage:
    python run.py           # manual
    flask run               # uses .flaskenv
"""

from app import create_app, socketio

app = create_app()

if __name__ == "__main__":
    # Use socketio.run so WebSockets work in dev (flask run doesn't support them)
    socketio.run(app, host="0.0.0.0", port=app.config["PORT"], debug=True)
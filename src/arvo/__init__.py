from .app import app

def main() -> None:
    app.run(host="127.0.0.1", port=5000)

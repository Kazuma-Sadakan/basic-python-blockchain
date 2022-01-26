import os 
from src import create_app

if __name__ == "__main__":
    config = os.environ.get("development")

    app = create_app(config = config)
    app.run(debug = True)

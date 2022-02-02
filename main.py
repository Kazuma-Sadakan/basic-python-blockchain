import os 
from argparse import ArgumentParser

from src import create_app

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000)
    args = parser.parse_args()
    host = "0.0.0.0"
    port = args.port
    
    os.environ["host"] = host
    os.environ["port"] = port

    app = create_app() 
    app.run(debug = True, host=host, port=port)

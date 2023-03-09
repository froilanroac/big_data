from src.graphs import app
from src.graphs import server

if __name__ == '__main__':
    try:
        app.run_server(debug=True)       
    except:
        print('Unexpected error')

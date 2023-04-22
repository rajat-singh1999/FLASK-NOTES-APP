# entry point for our app
from website import create_app

app = create_app()

# the line below makes sure that the main.py, which is the web server
# runs only when it is manually runs, hopefully it makes sense
# to my future self
if __name__ == '__main__':
    app.run(debug=True)

# debug = true means that everytime we make changes to the 
# python files, the server reruns
# for obvious reasons this is set to false during production

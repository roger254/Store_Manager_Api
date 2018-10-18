import os
from app import create_app

# set the config
config_name = os.getenv('FLASK_ENV')
# create app
app = create_app(config_name)

if __name__ == '__main__':
    app.run()

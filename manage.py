import os
# keeps track of the commands and how they are called
from flask_script import Manager
# MigrateCommand sets of migration commands
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
# get the models to be migrated


# create app with FLASK_ENV setting
app = create_app(config_name=os.getenv('FLASK_ENV'))
migrate = Migrate(app, db)
manager = Manager(app)

# add migration commands and start with db
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

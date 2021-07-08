# cli.py
import click
from app import db
#from app import Model #db.model is used



@click.group()
def main():
    return
    #Run the Granola Explosion CLI.

def create_db():
    """Creates database"""
    db.create_all()

def drop_db():
    """Cleans database"""
    db.drop_all()

#def create_model_table():
#    """ Create table model in the database """
#    Model.__table__.create(db.engine)

def init_app(app):
    # add multiple commands in a bulk
    for command in [create_db, drop_db]:
        app.cli.add_command(app.cli.command()(command))

@click.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=5000, type=int)
def web(host: str, port: int):
    from wsgi import app
    app.run(host=host, port=port)



if __name__ == '__main__':
    main()
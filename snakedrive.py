import click

from app import create_app, db
from app.models import User, File


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'File': File
    }


@app.cli.command('create-user')
@click.argument('email')
@click.argument('username')
@click.argument('password')
def create_admin(email, username, password):
    user_data = {
        'email': email,
        'username': username,
        'verified': True,
    }
    user = User()
    user.from_dict(user_data)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    print(user.to_dict())

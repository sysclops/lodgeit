from lodgeit.application import make_app
from lodgeit.utils import ctx
from lodgeit.database import db
from werkzeug import script
from werkzeug.debug import DebuggedApplication
from werkzeug.serving import run_simple
from werkzeug.utils import create_environ, run_wsgi_app

dburi = 'sqlite:////tmp/lodgeit.db'

def run_app(app, path='/'):
    env = create_environ(path)
    return run_wsgi_app(app, env)

action_runserver = script.make_runserver(
    lambda: make_app(dburi),
    use_reloader=True)

action_rundserver = script.make_runserver(
    lambda: DebuggedApplication(make_app(dburi, True), evalex=True),
    use_reloader=True)

action_shell = script.make_shell(
    lambda: {
        'app': make_app(dburi, False, True),
        'ctx': ctx,
        'db': db,
        'run_app': run_app
    },
    ('\nWelcome to the interactive shell environment of LodgeIt!\n'
     '\n'
     'You can use the following predefined objects: app, ctx, db.\n'
     'To run the application (creates a request) use *run_app*.')
)

if __name__ == '__main__':
    script.run()

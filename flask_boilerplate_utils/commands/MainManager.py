from .InstallFramework import InstallFramework
from .Run import Run
from .Host import Host

from flask.ext.script import Manager

# Manager Factory.
def MainManager(app, **kwargs):
	manager = Manager(app,**kwargs)
	manager.add_command('server', Run(app))
	manager.add_command('meinheld', Host(app))
	manager.add_command('install', InstallFramework(app))
	return manager
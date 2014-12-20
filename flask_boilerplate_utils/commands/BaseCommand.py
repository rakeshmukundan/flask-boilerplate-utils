from flask.ext.script import Command

class BaseCommand(Command):
	def __init__(self, app):
		super(Command, self).__init__()
		self.app = app
